config = {
    'candidate_name' : 'ChemicalDisease',
    'candidate_entities' : ['chemical', 'disease'],

    # collect
    'babbler_label_split': 1,
    'babbler_candidate_split': [0,1,2],

    # supervise
    'gen_init_params': {
        'lf_propensity'         : True,
        'lf_prior'              : False, 
		'class_prior'           : False,
        'lf_class_propensity'   : False,
        'seed'                  : 123,
    },
    'gen_params_default': {
        'step_size' : 0.01,
        'reg_param' : 0.5,
        'epochs': 0,
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
        'lr':         0.01,
        'batch_size': 32,
        'l1_penalty': 0,
        'l2_penalty': 10,
        'dropout':    0.5,
        'dim':        50,
        'n_epochs':   0,
        'print_freq': 5,
    },
    'disc_eval_batch_size': None,
}