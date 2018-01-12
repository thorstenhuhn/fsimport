from . import __version__

import click
import datetime
import logging
import os
import shutil
import tempfile
import traceback

from fsimport.archive import unarchive
from fsimport.config import load_config
from fsimport.rules import process_rules
from fsimport.source import get_source


logger = logging.getLogger(__name__)
tmp_directory = tempfile.mkdtemp()


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo('fsimport version {}'.format(__version__))
    ctx.exit()


# Ideas for extra-options:
#  - configure tmp_directory
#  - flag to create backup when updating files
# 

@click.command()
@click.option('--config', '-c', type=click.File(), help='configuration file')
@click.option('--dry-run', is_flag=True, help='predict changes without performing them')
@click.option('--extra-vars', '-e', multiple=True)
@click.option('--verbose', '-v', is_flag=True, default=False, help='be more verbose')
@click.option('--version', is_flag=True, callback=print_version, expose_value=False, is_eager=True)
@click.argument('src')
def cli(config, dry_run, extra_vars, verbose, src):
    """fsimport - import files into directory using filesets"""
    logger.debug('config: {}'.format(config))
    logger.debug('dry-run: {}'.format(dry_run))
    logger.debug('verbose: {}'.format(verbose))
    logger.debug('extra-vars: {}'.format(extra_vars))

    # check source
    logger.info('Checking source')
    src = get_source(src)

    # load configuration
    logger.info('Loading configuration')
    config = load_config(config, extra_vars)

    # add options to config
    config['dry_run'] = dry_run
    config['verbose'] = verbose

    try:
        # unarchiving package
        package_files = unarchive(config, tmp_directory, src.name)

        # process rules
        process_rules(config, tmp_directory, package_files)

    except Exception as e:
        if verbose:
            logger.info(traceback.format_exc())
        logger.fatal(str(e))

    finally:    
        shutil.rmtree(tmp_directory)
        # TODO remove file if and only if downloaded
        #os.remove(src.name)

        # write summary unless dry_run mode
        if not dry_run:
            version_info = config.get('version_info', 'fsimport.info')
            if isinstance(version_info, (str, unicode)):
                version_info = [ version_info ]
            for target in version_info:
                logger.info('Writing info file {}'.format(target))
                timestamp = datetime.datetime.now().strftime('%d.%m.%y %H:%M:%S')
                with open(target, 'w') as info:
                    info.write('Package: {}\n'.format(src.name))
                    info.write('Installation date: {}\n'.format(timestamp))


def main():
    cli()


if __name__ == '__main__':
    cli()

