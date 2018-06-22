from snorkel.contrib.pipelines.utils import STAGES

global_config = {
    ### SETUP ###
    'domain': None,
    'project': 'babble',

    'log_dir': 'logs',
    'reports_dir': 'reports', # nested under $SNORKELHOME/
    'postgres': False,
    'parallelism': 1,
    'splits': [0, 1, 2],
    'verbose': True,
    'debug': False,
    'codalab': False,
    'no_plots': True,
    'seed': 0,
    'start_at': STAGES.SETUP, # Stage of pipeline to start at
    'end_at': STAGES.ALL, # Stage of pipeline to end at (inclusive)

    ### PARSE ###
    'max_docs': None,
    'max_extra_docs': None,
    'train_fraction': 1,

    ### EXTRACT ###

    ### LOAD_GOLD ###

    ### COLLECT ###

    ## Babbler
    'babbler_candidate_split': 1, # Look for explanation candidates in this split
    'babbler_label_split': 1, # Check label signatures based on this split
    'beam_width': 10,
    'top_k': -1,
    'max_explanations': None,
    'gold_explanations': False,

    ## FilterBank
    'apply_filters': True,

    ### LABEL ###
    'max_lfs': None,

    ### SUPERVISE ###
    'supervision': 'dp', # ['traditional', 'majority', 'generative', 'dp'],

    ## traditional
    'max_train': None,  # Number of ground truthed training candidates
    'max_dev': None,
    'traditional_split': 0, # Which split has the candidates/labels to use for trad. sup.
    
    ## generative
    'gen_model_search_space': 1,
    'gen_f_beta': 1.0,
    'gen_init_params': {
		'class_prior'           : False,
        'lf_prior'              : False, 
        'lf_propensity'         : True,
        'lf_class_propensity'   : False,
        'seed'                  : None,
    },
    'gen_params_range': {
        'step_size'     : [0.01, 0.05, 0.1, 0.25],
        'reg_param'     : [0.0, 0.1, 0.25, 0.5, 1.0],
        # 'decay'         : [0.9, 0.95, 0.99],
    },
    'gen_params_default': {
        'step_size': 0.01,
        'reg_param': 0.25,
        'epochs'   : 500,
    	'decay'    : 0.95,
        # used iff class_prior = True
        'init_class_prior' : 0, # logit = ln(p/(1-p)), p = exp(logit)/(1 + exp(logit))
        # Used iff lf_prior = True
        'LF_acc_prior_weight_default' : 1.0, # [0, 0.5, 1.0, 1.5] = (50%, 62%, 73%, 82%)
        # 'LF_acc_prior_weights'        : [None], # Used iff lf_prior = True
    },
    'tune_b': True, # default to True for text, False for image

    # dependencies
    'learn_deps': False,
    'deps_thresh': None,

    ## display
    'display_accuracies': True,
    'display_learned_accuracies': False,
    'display_correlation': False,
    'display_marginals': True,

    ### CLASSIFY ###
    'disc_model_class': 'lstm',
    'disc_model_search_space': 1,
	'disc_init_params': {
        'n_threads': 16,
        'seed'     : 123,
    },
    'disc_params_range': {
        'rebalance' : [False, 0.25, 0.5],
        'lr'        : [1e-2, 1e-3, 1e-4],
        'batch_size': [32, 64, 128],
        # 'l1_penalty': [1e2, 1e1, 1e0, 1e-1, 1e-2, 1e-3, 0],
        'l2_penalty': [1e2, 1e1, 1e0, 1e-1, 1e-2, 1e-3, 0],
        # 'dropout'   : [0, 0.25, 0.5],
        # 'dim'       : [32, 64, 128],
        # 'n_epochs'  : [10, 20, 50],
    },
    'disc_params_default': {
        'l1_penalty': 1.0,
        'l2_penalty': 1.0,
        'lr':         0.01,
        'batch_size': 32,
        'rebalance':  0.25,
        'dropout':    0.5,
        'n_epochs':   25,
        'dim':        50,
        'max_sentence_length': 100,
        'print_freq': 1,
    },
    'disc_eval_batch_size': 256,
    
    ## Non-GridSearch parameters
    'b': 0.5,
}


