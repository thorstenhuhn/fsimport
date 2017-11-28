import jinja2
import logging
import os
import yaml
import hiyapyco


logger = logging.getLogger(__name__)
config_locations = [ '/etc/fsimport.yaml', os.path.expanduser('~/.fsimport.yaml'), './fsimport.yaml' ]


def load_config(config_file=None, extra_vars=[]):
    if config_file is not None:
        config_locations.append(config_file.name)

    # transform extra_vars to yaml and append at the end (highest prio)
    extra_vars_dict = dict(stmt.split('=', 2) for stmt in extra_vars)
    config_locations.append(yaml.safe_dump(extra_vars_dict))
    config = hiyapyco.load(config_locations, method=hiyapyco.METHOD_MERGE, interpolate=True, failonmissingfiles=False)

    # add default rule if mappings are missing
    if config.get('mappings', None) is None:
        config['mappings'] = { 'directory': '.', 'include': '**' }

    logger.debug(config)
    return config

