import logging
import mimetypes
import os
import re
import tarfile
import zipfile

from shutil import move


logger = logging.getLogger(__name__)


def unarchive(filename, directory, environment_name_list):
    """extract archive to given directory and return package content"""

    logger.info('Extracting {} to {}'.format(filename, directory))
    filetype = mimetypes.guess_type(filename)[0]
    logger.debug('Detected filetype: {}'.format(filetype))

    if 'zip' in filetype:
        with zipfile.ZipFile(filename, 'r') as z:
            z.extractall(directory)
            result = [f for f in z.namelist() if not f.endswith('/')]
    elif filetype == 'application/x-tar':
        with tarfile.open(filename, 'r') as t:
            t.extractall(directory)
            result = [f.name for f in t.getmembers() if not f.isdir()]
    else:
        raise Exception('Unsupported filetype for {}: {}'.format(filename, filetype))

    for environment_name in environment_name_list:
        logger.debug('Searching for files matching {}'.format(environment_name))
        regex = re.compile('(.*)\.{}'.format(environment_name)) 
        result2 = set()
        for filename in result:
            m = regex.match(filename)
            if m:
                filename2 = m.group(1)
                logger.info('Adjusting environment configuration using ' + filename)
                move(os.path.join(directory, filename), os.path.join(directory, filename2))
                result2.add(filename2)
            else:
                result2.add(filename)

    #for filename in result:
    #    logger.debug(' + {}'.format(filename))

    return sorted(list(result2))

