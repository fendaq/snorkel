config = {
    'candidate_name' : 'ProteinKinase',
    'candidate_entities' : ['protein', 'kinase'],
    'babbler_candidate_split': [0,1,2],
    'traditional_split': 1,

    'gen_f_beta': 1.0,
    'gen_params_default': {
        'step_size' : 0.25,
        'reg_param' : 0.1,
        # 'decay'     : 0.95,
        # Used iff lf_prior = True
        # 'LF_acc_prior_weight_default' : 0.5, # [0, 0.5, 1.0, 1.5] = (50%, 62%, 73%, 82%)
        # Used iff class_prior = True
        # 'init_class_prior' : -1.39, # (20%, based on dev balance)
        # logit = ln(p/(1-p)), p = exp(logit)/(1 + exp(logit))
    },
    'disc_params_default': { # optimal tradit logreg settings
        'rebalance':  0.5,
        'lr':         0.001,
        'batch_size': 32,
        'l1_penalty': 0,
        'l2_penalty': 0.1,
        'dropout':    0.5,
        'dim':        50,
        'n_epochs':   20,
        'print_freq': 5,
    },    
}