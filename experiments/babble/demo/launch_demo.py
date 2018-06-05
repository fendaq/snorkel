from flask import Blueprint, Flask, flash, redirect, render_template, request, session, abort, current_app
import os
import sys
sys.path.append('/Users/Stephaniewang/Documents/snorkel')
from snorkel import SnorkelSession
from snorkel.contrib.pipelines import merge_configs
from snorkel.models import candidate_subclass
from snorkel.contrib.babble import ExplanationIO
from experiments.babble.spouse import SpousePipeline
from snorkel.viewer import SentenceNgramViewer
from snorkel.contrib.babble import Explanation
from snorkel.contrib.babble import Babbler

from flask_bootstrap import Bootstrap
from snorkel.contrib.babble import BabbleStream
from snorkel.lf_helpers import *
from experiments.babble.spouse.spouse_examples import get_explanations, get_user_lists
from main_page import main_page
# dependencies:
# flask
# Flask-WTF
# wtforms
# flask_bootstrap
 
def create_app(bs, c, session, pipe):
	app = Flask(__name__)
	app.secret_key = 'myverylongsecretkey'
	bootstrap = Bootstrap(app)
	app.config['babble_stream_object'] = bs
	app.config['candidate'] = c
	app.config['session'] = session
	app.config['pipe'] = pipe
	app.config['metrics'] = {'lf_stats': '', 'coverage': 0, 'num_labels': 0, 'num_examples': 0, 'num_labels_equiv': 0, 'f1': 0}
	app.config['priority_ids'] = {
                # T EXAMPLE 1: 
                    # Because "husband" is right before Y
                    # Because 'with' and 'husband' are within 5 words to the left of Y
                '48355563-37ab-4fb8-9525-4762d6be7fc8::span:7317:7320~~48355563-37ab-4fb8-9525-4762d6be7fc8::span:7378:7383':
                ['Because "husband" is right before Y' , 'Because "with" and "husband" are within 5 words to the left of Y'],
                # F EXAMPLE __3__: 
                    # Because X and Y are the same person.
                    # Because X starts with Y.
                '24a08559-a824-4331-9028-fbeac1f3ca5a::span:1637:1640~~24a08559-a824-4331-9028-fbeac1f3ca5a::span:1706:1709':
                ['Because X and Y are the same person.', 'Because X starts with Y.'],
                # T EXAMPLE 6: 
                    # Because "married to" is between X and Y and there are no people are between them
                    # Because "got married" is between X and Y
                'a587afeb-715c-44ee-bdef-75f61cb7c6e8::span:1108:1117~~a587afeb-715c-44ee-bdef-75f61cb7c6e8::span:1179:1193':
                ['Because "married to" is between X and Y and there are no people are between them','Because "got married" is between X and Y'],
                # F EXAMPLE 5: 
                    # Because none of the words "wife", "husband", "spouse", or "married" are in the sentence.
                    # Because the last word of X is different than the last word of Y
                '6807fb8a-333f-41fd-bf8b-4b47681a5a08::span:711:726~~6807fb8a-333f-41fd-bf8b-4b47681a5a08::span:770:779':
                ['Because none of the words "wife", "husband", "spouse", or "married" are in the sentence.',
                  'Because the last word of X is different than the last word of Y'],
                # T EXAMPLE __2__: 
                    # Because "husband" or "wife" is within five words of X and Y
                    # Because "his wife" is within five words of X and Y
                '40cb15fa-0186-4868-a5b7-eb2fc6a317cf::span:115:123~~40cb15fa-0186-4868-a5b7-eb2fc6a317cf::span:138:153':
                ['Because "husband" or "wife" is within five words of X and Y', 'Because "his wife" is within five words of X and Y'],
                # F EXAMPLE 7: 
                    # Because either "son" or "daughter" is immediately to the left of X or Y
                    # Because "son" is between X and Y
                '7fc3e510-c4e6-44c2-a24b-f9a39bfcfb07::span:4942:4950~~7fc3e510-c4e6-44c2-a24b-f9a39bfcfb07::span:4973:4978':
                ['Because either "son" or "daughter" is immediately to the left of X or Y', 'Because "son" is between X and Y'],
                # F: "X or Y is in all caps"
                '9ee7265a-b7e3-4ebe-a60e-ef145884b80a::span:204:208~~9ee7265a-b7e3-4ebe-a60e-ef145884b80a::span:239:243':
                ['X or Y is in all caps'],
            }
	app.register_blueprint(main_page)
	return app

if __name__ == "__main__":
	config = {
	'b': 0.5,
	'babbler_candidate_split': 0,
	'babbler_label_split': 0,
	'beam_width': 10,
	'candidate_entities': ['person1', 'person2'],
	'candidate_name': 'Spouse',
	'db_name': 'babble_spouse_demo',
	'debug': False,
	'deps_thresh': 0.01,
	'disc_eval_batch_size': 256,
	'disc_init_params': {'n_threads': 16, 'seed': 123},
	'disc_model_class': 'lstm',
	'disc_model_search_space': 10,
	'disc_params_default': {'batch_size': 128,
	'dim': 50,
	'dropout': 0.5,
	'lr': 0.01,
	'max_sentence_length': 100,
	'n_epochs': 20,
	'print_freq': 1,
	'rebalance': 0.25},
	'disc_params_range': {'dim': [50, 100],
	'dropout': [0.1, 0.25, 0.5],
	'lr': [0.01, 0.001, 0.0001],
	'rebalance': [0.1, 0.25]},
	'display_accuracies': True,
	'display_correlation': False,
	'display_learned_accuracies': False,
	'display_marginals': True,
	'do_filter_consistency': True,
	'do_filter_duplicate_semantics': True,
	'do_filter_duplicate_signatures': True,
	'do_filter_uniform_signatures': True,
	'domain': 'spouse',
	'end_at': 10,
	'gen_f_beta': 1,
	'gen_init_params': {'class_prior': False,
	'lf_class_propensity': False,
	'lf_prior': False,
	'lf_propensity': True,
	'seed': 123},
	'gen_model_search_space': 10,
	'gen_params_default': {'decay': 0.99,
	'epochs': 50,
	'init_class_prior': -1.15,
	'reg_param': 0.5,
	'step_size': 0.0001},
	'gen_params_range': {'LF_acc_prior_weight_default': [0.5, 1.0, 1.5],
	'decay': [0.9, 0.95, 0.99],
	'reg_param': [0.0, 0.01, 0.1, 0.25, 0.5],
	'step_size': [0.01, 0.001, 0.0001, 1e-05]},
	'learn_deps': False,
	'log_dir': 'logs',
	'max_docs': None,
	'max_train': None,
	'no_plots': False,
	'parallelism': 1,
	'postgres': False,
	'reports_dir': 'reports',
	'seed': 0,
	'splits': [0, 1, 2],
	'start_at': 0,
	'supervision': 'generative',
	'top_k': -1,
	'verbose': True
	}
	# Get DB connection string and add to globals
	# default_db_name = 'babble_' + config['domain'] + ('_debug' if config.get('debug', False) else '')
	# DB_NAME = config.get('db_name', default_db_name)
	# if 'postgres' in config and config['postgres']:
	#     DB_TYPE = 'postgres'
	# else:
	#     DB_TYPE = 'sqlite'
	#     DB_NAME += '.db'
	# DB_ADDR = "localhost:{0}".format(config['db_port']) if 'db_port' in config else ""
	# os.environ['SNORKELDB'] = '{0}://{1}/{2}'.format(DB_TYPE, DB_ADDR, DB_NAME)
	# print("$SNORKELDB = {0}".format(os.environ['SNORKELDB']))

	session = SnorkelSession()

	# config = merge_configs(config)

	# if config['debug']:
	#     print("NOTE: --debug=True: modifying parameters...")
	#     config['max_docs'] = 100
	#     config['gen_model_search_space'] = 2
	#     config['disc_model_search_space'] = 2
	#     config['gen_params_default']['epochs'] = 25
	#     config['disc_params_default']['n_epochs'] = 5

	Spouse = candidate_subclass('Spouse', ['person1', 'person2'])
	candidate_class = Spouse
	pipe = SpousePipeline(session, Spouse, config)
	# pipe.parse()
	# pipe.extract()
	# pipe.load_gold()

	bs = BabbleStream(session, candidate_class=Spouse, balanced=True, seed=123, soft_start=True)
	candidates = session.query(Spouse).filter(Spouse.split == 0).all()
	# spouse_explanations = get_explanations()
	# spouse_user_lists = get_user_lists()
	# bs.preload(explanations=spouse_explanations, user_lists=spouse_user_lists)
	c = bs.next()
	app = create_app(bs, c, session, pipe)
	app.run()
