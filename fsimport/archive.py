import logging
import mimetypes
import os
import re
import tarfile
import zipfile

from shutil import move


logger = logging.getLogger(__name__)


def unarchive(config, directory, pfilename):
    """extract archive to given directory and return package content"""

    logger.info('Extracting {} to {}'.format(pfilename, directory))
    filetype = mimetypes.guess_type(pfilename)[0]
    logger.debug('Detected filetype: {}'.format(filetype))

    if 'zip' in filetype:
        with zipfile.ZipFile(pfilename, 'r') as z:
            z.extractall(directory)
            result = [f for f in z.namelist() if not f.endswith('/')]
    elif filetype == 'application/x-tar':
        with tarfile.open(pfilename, 'r') as t:
            def is_within_directory(directory, target):
                
                abs_directory = os.path.abspath(directory)
                abs_target = os.path.abspath(target)
            
                prefix = os.path.commonprefix([abs_directory, abs_target])
                
                return prefix == abs_directory
            
            def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
            
                for member in tar.getmembers():
                    member_path = os.path.join(path, member.name)
                    if not is_within_directory(path, member_path):
                        raise Exception("Attempted Path Traversal in Tar File")
            
                tar.extractall(path, members, numeric_owner=numeric_owner) 
                
            
            safe_extract(t, directory)
            result = [f.name for f in t.getmembers() if not f.isdir()]
    else:
        raise Exception('Unsupported filetype for {}: {}'.format(pfilename, filetype))

    environments_matching = []
    environments_ignoring = []
    if 'environment' in config and 'match' in config['environment']:
        environments_matching = config['environment']['match']
    if 'environment' in config and 'ignore' in config['environment']:
        environments_ignore = config['environment']['ignore']

    logger.info('Analyzing environment-specific files')
    result2 = set()
    for filename in result:
        processed = False
        for environment_name in environments_matching:
            if filename.endswith('.' + environment_name):
                logger.info(' A ' + filename)
                filename2 = filename[:len(filename)-len(environment_name)-1]
                move(os.path.join(directory, filename), os.path.join(directory, filename2))
                result2.add(filename2)
                processed = True
        for environment_name in environments_ignore:
            if filename.endswith('.' + environment_name):
                logger.info(' I ' + filename)
                processed = True
        if not processed:
            result2.add(filename)

    #for filename in result:
    #    logger.debug(' + {}'.format(filename))

    return sorted(list(result2))

