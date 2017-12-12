import filecmp
import jinja2
import logging
import os

from formic import FileSet
from shutil import copyfile


logger = logging.getLogger(__name__)


def process_rules(config, basedir, files, **kwargs):

    rules = config.get('mappings', [])
    verbose = config.get('verbose', False)
    dry_run = config.get('dry_run', False)

    # reset state for each file and rule as false/not used
    file_used_state = {}
    for filename in files:
        file_used_state[os.path.join(basedir, filename)] = False
    rule_used_state = []

    # reset all counters
    files_added = 0
    files_skipped = 0
    files_updated = 0
    files_ignored = 0

    # setup jinja2 environment
    loader = jinja2.loaders.FileSystemLoader(basedir)
    env = jinja2.Environment(loader=loader)

    # wall through all rules
    for idx, rule in enumerate(rules):
        logger.info('Processing rule {}/{}'.format(idx+1, len(rules)))
        logger.debug(rule)

        # search files matching rule pattern
        rule_used_state.append(False)
        fileset = FileSet(directory=os.path.join(basedir, rule['directory']), include=rule.get('include', '*'), exclude=rule.get('exclude', None))

        # walk through all matches
        for filename in fileset:
            logger.debug('source: {}'.format(filename))
            target = rule.get('target', None)

            # as we found a match, mark file and rule as used
            file_used_state[filename] = True
            rule_used_state[idx] = True

            # filename is absolute, sub_path contains only the part relative to basedir
            sub_path = filename[len(basedir)+1:]
            #logger.debug('subpath: {}'.format(sub_path))

            # skip further processing if rule sets ignore=True
            ignore = rule.get('ignore', False)
            if ignore:
                files_ignored += 1
                if verbose: logger.info(' I {}'.format(sub_path))
                continue

            # render source file if template
            is_template = rule.get('template', False)
            if is_template:
                tpl = env.get_template(sub_path)
                rendered = tpl.render(config)
                filename_rendered = filename + '.rendered'
                with open(filename_rendered, 'wb') as f:
                    f.write(rendered)
                filename = filename_rendered

            # identify target path including filename
            if target is None: target = os.path.join(os.getcwd(), sub_path)
            if isinstance(target, str) or isinstance(target, unicode):
                target = [ target ]
            logger.debug(target)

            # walk through all targets (more than one destination is allowed)
            for t in target:

                # make sure target is a file
                if t.endswith('/') or os.path.isdir(t):
                    t = os.path.join(t, os.path.basename(sub_path))

                # case 1: target already exists
                if os.path.exists(t):
                    if filecmp.cmp(filename, t):
                        if verbose:
                            logger.info(' S {}'.format(t))
                        files_skipped += 1
                    else:
                        logger.info(' U {}'.format(t))
                        files_updated += 1
                        if not dry_run:
                            copyfile(filename, t)

                # case 2: target is missing and will be added
                else:
                    logger.info(' A {}'.format(t))
                    files_added += 1
                    target_path = os.path.dirname(t)
                    if not os.path.isdir(target_path):
                        os.makedirs(target_path)
                    if not dry_run:
                        copyfile(filename, t)

        # print warning if rule was not used
        if rule_used_state[idx] == 0:
            logger.warn('No files found matching rule')
            logger.warn(' + {}'.format(rule))

    # end of loop over rules

    # print files summary
    extra_text = 'WOULD BE ' if dry_run else ''
    logger.info('{} file(s) {}added, {} updated, {} skipped and {} ignored'.format(files_added, extra_text, files_updated, files_skipped, files_ignored))

    # print rules summary
    rules_not_used = len(rules) - sum(rule_used_state)
    files_untouched = len(file_used_state) - sum(file_used_state.values())
    level = logging.INFO if rules_not_used == 0 and files_untouched == 0 else logging.WARN
    logger.log(level, '{} rule(s) found, {} not used, {} file(s) did not match any rule'.format(len(rules), rules_not_used, files_untouched))

    # show details if we are in verbose mode
    if verbose:
        for filename in sorted(file_used_state.keys()):
            if not file_used_state[filename]:
                logger.warn(' + {}'.format(filename))

    return 

