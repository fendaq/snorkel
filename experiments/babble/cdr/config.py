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
    'gen_params_range': {
        # 'step_size'     : [1e-2, 1e-3, 1e-4, 1e-5],
        # 'decay'         : [0.9, 0.95, 0.99],
        # 'reg_param'     : [0.0, 0.01, 0.1, 0.25, 0.5, 0.75],
        # 'epochs'        : [10, 25, 50, 100],
    },
    'gen_params_default': {
        'step_size' : 0.01,
        'reg_param' : 0.5,
        'epochs': 0,
        # 'decay'     : 0.95,
        # Used iff lf_prior = True
        # 'LF_acc_prior_weight_default' : 0.5, # [0, 0.5, 1.0, 1.5] = (50%, 62%, 73%, 82%)
        # Used iff class_prior = True
        # 'init_class_prior' : -1.39, # (20%, based on dev balance)
        # logit = ln(p/(1-p)), p = exp(logit)/(1 + exp(logit))
    },
    'tune_b': False,

    # classify
    'disc_model_class': 'logreg',
    'disc_model_search_space': 10,
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