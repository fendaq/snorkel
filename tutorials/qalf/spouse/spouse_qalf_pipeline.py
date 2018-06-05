import os

from experiments.babble.spouse import SpousePipeline
from tutorials.qalf import QalfPipeline
from tutorials.qalf.qalf_converter_legacy import LegacyQalfConverter

class SpouseQalfPipeline(QalfPipeline, SpousePipeline):
    
    def label(self):
        qc = LegacyQalfConverter(self.session, self.candidate_class)
        matrix_path = (os.environ['SNORKELHOME'] + 
            '/tutorials/qalf/spouse/data/qalf_matrix_hp.tsv')
        stats_path = (os.environ['SNORKELHOME'] + 
            '/tutorials/qalf/spouse/data/qalf_stats_hp.tsv')
        L_train, L_dev, L_test = qc.convert(matrix_path, stats_path)

        self.L_train = L_train
        self.L_dev = L_dev
        self.L_test = L_test