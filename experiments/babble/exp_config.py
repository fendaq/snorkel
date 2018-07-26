def get_exp_config(args):
    config = {'disc_params_default': {}}

    if args['domain'] == 'spouse':
        if args['supervision'] == 'dp':
            if not args['apply_filters']:        
                config['disc_params_default']['lr'] = 0.001
                config['disc_params_default']['l2_penalty'] = 0
                config['disc_params_default']['rebalance'] = 0.25
                config['disc_params_default']['batch_size'] = 128
            elif args['gold_explanations']:
                config['disc_params_default']['lr'] = 0.001
                config['disc_params_default']['l2_penalty'] = 0.001
                config['disc_params_default']['rebalance'] = 0
                config['disc_params_default']['batch_size'] = 32
        elif args['supervision'] == 'jt':
            config['disc_params_default']['lr'] = 0.1
            config['disc_params_default']['l2_penalty'] = 0.0001
            config['disc_params_default']['rebalance'] = 0.5
            config['disc_params_default']['batch_size'] = 64
    
    elif args['domain'] == 'cdr':
        if args['supervision'] == 'dp':
            if not args['apply_filters']:        
                config['disc_params_default']['lr'] = 0.01
                config['disc_params_default']['l2_penalty'] = 10
                config['disc_params_default']['rebalance'] = 0.5
                config['disc_params_default']['batch_size'] = 128
            elif args['gold_explanations']:
                config['disc_params_default']['lr'] = 0.001
                config['disc_params_default']['l2_penalty'] = 10
                config['disc_params_default']['rebalance'] = 0.5
                config['disc_params_default']['batch_size'] = 64
        elif args['supervision'] == 'traditional':
                config['disc_params_default']['lr'] = 0.001
                config['disc_params_default']['l2_penalty'] = 1
                config['disc_params_default']['rebalance'] = 0.5
                config['disc_params_default']['batch_size'] = 32
        elif args['supervision'] == 'jt':
            if args['gold_explanations']:
                config['disc_params_default']['lr'] = 0.01
                config['disc_params_default']['l2_penalty'] = 0.01
                config['disc_params_default']['rebalance'] = 0.5
                config['disc_params_default']['batch_size'] = 64
            else:
                config['disc_params_default']['lr'] = 0.01
                config['disc_params_default']['l2_penalty'] = 0.01
                config['disc_params_default']['rebalance'] = 0.4
                config['disc_params_default']['batch_size'] = 64

    return config