config = {
    'candidate_name' : 'ChemicalDisease',
    'candidate_entities' : ['chemical', 'disease'],

    # collect
    'babbler_label_split': 1,
    'babbler_candidate_split': [0,1,2],

    # supervise
    'supervision': 'generative',
    'gen_init_params': {
        'lf_propensity'         : True,
        'lf_prior'              : False, 
		'class_prior'           : False,
        'lf_class_propensity'   : False,
        'seed'                  : 123,
    },
    'gen_params_default': {
        'step_size' : 0.01,
        'reg_param' : 5,
    },
    'tune_b': False,

    # classify
    'disc_model_class': 'logreg',
    'disc_init_params': {
        'n_threads': 16,
        'seed'     : 123,
    },
    'disc_params_default': { # optimal tradit logreg settings
        'rebalance':  0,
        'lr':         0.001,
        'batch_size': 64,
        'l1_penalty': 0,
        'l2_penalty': 1,
        'dropout':    0.5,
        'dim':        50,
        'n_epochs':   20,
        'print_freq': 20,
    },
    'disc_eval_batch_size': None,
}