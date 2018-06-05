import csv
import os
import random

import numpy as np
from six.moves.cPickle import load

from snorkel.candidates import Ngrams, PretaggedCandidateExtractor
from snorkel.matchers import PersonMatcher
from snorkel.models import Document, Sentence, StableLabel
from snorkel.parser import CorpusParser, TSVDocPreprocessor

from snorkel.contrib.pipelines import TRAIN, DEV, TEST

from snorkel.contrib.babble import Babbler
from snorkel.contrib.babble import BabblePipeline

from experiments.babble.protein.utils import ProteinKinaseLookupTagger
from experiments.babble.protein.load_external_annotations import load_external_labels
from experiments.babble.protein.protein_examples import get_explanations, get_user_lists

DATA_ROOT = os.environ['SNORKELHOME'] + '/experiments/babble/protein/data/'

class ProteinPipeline(BabblePipeline):
    def parse(self, 
              # file_path=(DATA_ROOT + 'abstracts_subset.txt'), 
              file_path=(DATA_ROOT + 'abstracts_razor_utf8.txt'), 
              clear=True,
              config=None):
        if 'subset' in file_path:
            print("WARNING: you are currently using a subset of the data.")
        doc_preprocessor = TSVDocPreprocessor(file_path, 
                                              max_docs=self.config['max_docs'])
        pk_lookup_tagger = ProteinKinaseLookupTagger()
        corpus_parser = CorpusParser(fn=pk_lookup_tagger.tag)
        corpus_parser.apply(list(doc_preprocessor), 
                            parallelism=self.config['parallelism'], 
                            clear=clear)
        
        if self.config['verbose']:
            print("Documents: {}".format(self.session.query(Document).count()))
            print("Sentences: {}".format(self.session.query(Sentence).count()))

        if self.config['max_extra_docs']:
            print("Beginning to parse {} extra documents.".format(self.config['max_extra_docs']))
            extra_docs = DATA_ROOT + 'extra_10k_abstracts.txt'
            doc_preprocessor2 = TSVDocPreprocessor(extra_docs, 
                                                max_docs=self.config['max_extra_docs'])
            corpus_parser.apply(list(doc_preprocessor2), 
                        parallelism=self.config['parallelism'], 
                        clear=False)
        
        if self.config['verbose']:
            print("Documents: {}".format(self.session.query(Document).count()))
            print("Sentences: {}".format(self.session.query(Sentence).count()))
        
    def extract(self, clear=True, config=None):
                
        with open(DATA_ROOT + 'all_pkr_ids.pkl', 'rb') as f:
        # with open(DATA_ROOT + 'subset_pkr_ids.pkl', 'rb') as f:
            train_ids, dev_ids, test_ids = load(f)
            train_ids, dev_ids, test_ids = set(train_ids), set(dev_ids), set(test_ids)

        train_sents, dev_sents, test_sents = set(), set(), set()
        docs = self.session.query(Document).order_by(Document.name).all()

        num_extra_docs = 0
        for i, doc in enumerate(docs):
            if doc.name not in train_ids:
                num_extra_docs += 1

            for s in doc.sentences:
                if doc.name in dev_ids:
                    dev_sents.add(s)
                elif doc.name in test_ids:
                    test_sents.add(s)
                else:
                    if (self.config['train_fraction'] != 1
                        and random.random() > self.config['train_fraction']):
                        continue
                    train_sents.add(s)

        print("Extracted candidates from {} 'extra' sentences".format(num_extra_docs))

        candidate_extractor = PretaggedCandidateExtractor(self.candidate_class,
                                                          ['protein', 'kinase'])
        
        for split, sents in enumerate([train_sents, dev_sents, test_sents]):
            if len(sents) > 0 and split in self.config['splits']:
                super(ProteinPipeline, self).extract(
                    candidate_extractor, sents, split=split, clear=clear)


    def load_gold(self, config=None):
        load_external_labels(self.session, self.candidate_class, split=0, annotator='gold')
        load_external_labels(self.session, self.candidate_class, split=1, annotator='gold')
        load_external_labels(self.session, self.candidate_class, split=2, annotator='gold')

    def collect(self):
        explanations = get_explanations()
        user_lists = get_user_lists()
        super(ProteinPipeline, self).babble('text', explanations, user_lists, self.config)