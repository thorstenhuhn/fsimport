import __builtin__
import jinja2
import logging
import os
import yaml

from jinja2 import meta


logger = logging.getLogger(__name__)


def _check_missing_vars(env, tpl_file, config):
    """Check for missing variables in a template string"""
    tpl_str = tpl_file.read()
    ast = env.parse(tpl_str)
    required_properties = meta.find_undeclared_variables(ast)
    missing_properties = required_properties - config.viewkeys() - set(dir(__builtin__))

    if len(missing_properties) > 0:
        print('Required properties not set: {}'.format(','.join(missing_properties)))
        sys.exit(1)


def _new_jinja_env(tpl_path):
    loader = jinja2.loaders.FileSystemLoader(tpl_path)
    env = jinja2.Environment(loader=loader)
    return env


class Mapping(object):

    def __init__(self, tpl_file, config):
        self.config = yaml.load(tpl_file)
        tpl_path, tpl_fname = os.path.split(tpl_file.name)
        env = _new_jinja_env(tpl_path)
        _check_missing_vars(env, tpl_file, config)
        tpl = env.get_template(tpl_fname)
        rendered = tpl.render(config)
        logger.debug(rendered)

