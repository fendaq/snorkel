from imp import load_source
import os

from config import global_config

def merge_configs(config):
    if 'domain' not in config:
        raise Exception("config must have non-None value for 'domain'.")
    local_config = get_local_config(domain=config['domain'], project=config.get('project', 'babble'))
    config = recursive_merge_dicts(local_config, config)
    config = recursive_merge_dicts(global_config, config)
    return config  


def get_local_config(domain, project='babble'):
    if project not in ['babble', 'qalf']:
        raise ValueError

    local_config_path = os.path.join(os.environ['SNORKELHOME'], 
        'experiments', project, domain, 'config.py')
    if not os.path.exists(local_config_path):
        raise Exception("The config.py for the {} domain was not found at {}.".format(
            domain, local_config_path))
    local_config = load_source('local_config', local_config_path)
    return local_config.config


def get_local_pipeline(domain, project='babble'):
    if project == 'babble':
        pipeline_path = os.path.join(os.environ['SNORKELHOME'],
            'experiments', project, domain, '{}_pipeline.py'.format(domain))
        pipeline_name = '{}Pipeline'.format(domain.capitalize())
    else:
        raise ValueError
    if not os.path.exists(pipeline_path):
        raise Exception("Pipeline for the {} domain ({}) was not found at {}.".format(
            domain, pipeline_name, pipeline_path))
    pipeline_module = load_source('pipeline_module', pipeline_path)
    pipeline = getattr(pipeline_module, pipeline_name)
    print("Using {} object.".format(pipeline_name))
    return pipeline


def recursive_merge_dicts(x, y, verbose=False):
    """
    Merge dictionary y into x, overwriting elements of x when there is a
    conflict, except if the element is a dictionary, in which case recurse.
    """
    for k, v in y.iteritems():
        if k in x and isinstance(x[k], dict):
            x[k] = recursive_merge_dicts(x[k], v, verbose=verbose)
        elif v is not None:
            if k in x and x[k] != v:
                if verbose:
                    print("Overwriting {}={} to {}={}".format(k, x[k], k, v))
            x[k] = v
    return x