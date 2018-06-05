config = {
    'candidate_name' : 'Spouse',
    'candidate_entities' : ['person1', 'person2'],

    'babbler_label_split': 1,
    'babbler_candidate_split': [0,1,2], # Only need all three if using intro_exps
    'lf_source': 'gradturk30',

    'gen_init_params': {
		'class_prior'           : False, # TRUE!?
        'lf_propensity'         : True,
    },
    'gen_params_default': {
        'step_size': 0.01,
        'reg_param': 0.25,
        # 'decay'    : 0.95,
        # used iff class_prior = True
        # 'init_class_prior' : -1.15, # (9%)
        # Used iff lf_prior = True
        # 'LF_acc_prior_weight_default' : 0.5, # [0, 0.5, 1.0, 1.5] = (50%, 62%, 73%, 82%)
        # logit = ln(p/(1-p)), p = exp(logit)/(1 + exp(logit))
    },

    # LSTM
    # 'disc_model_class': 'lstm',
    # 'disc_model_search_space': 10,
    # 'disc_init_params': {
    #     'n_threads': 16,
    #     'seed'     : 123,
    # },
    # 'disc_params_default': {
    #     'lr':         0.01,
    #     'dim':        50,
    #     'n_epochs':   20,
    #     'dropout':    0.5,
    #     'rebalance':  0.25,
    #     'batch_size': 128,
    #     'max_sentence_length': 100,
    #     'print_freq': 1,
    # },    
    # 'disc_params_range': {
    #     'lr'        : [1e-2, 1e-3, 1e-4],
    #     'dim'       : [64, 128],
    #     'dropout'   : [0.1, 0.25, 0.5],
    #     'rebalance' : [0.25, 0.5, False],
    # },
    # 'disc_eval_batch_size': 256,

    'disc_model_class': 'logreg',
    'disc_model_search_space': 10,
    'disc_init_params': {
        'n_threads': 16,
        'seed'     : 123,
    },
    'disc_params_default': { # optimal tradit logreg settings
        'rebalance':  0,
        'lr':         0.001,
        'batch_size': 32,
        'l1_penalty': 0,
        'l2_penalty': 0.001,
        'dropout':    0.5,
        'dim':        50,
        'n_epochs':   20,
        'print_freq': 5,
    },    
    'disc_params_range': {
        # 'lr'        : [1e-2, 1e-3, 1e-4],
        # 'rebalance' : [0.25, 0.5, False],
        # 'n_epochs'  : [25, 50, 100],
        # 'batch_size': [16, 32, 64],
    },
    'disc_eval_batch_size': None,
}