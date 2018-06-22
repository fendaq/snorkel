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
    },

    'disc_model_class': 'logreg',
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
    'disc_eval_batch_size': None,
}