import logging
import os
import re
import requests
import tempfile


logger = logging.getLogger(__name__)


def get_source(src):

    regex = re.compile('(.*)://(.*)')
    m = regex.match(src)
    if m:
        protocol = m.group(1)
        if protocol.startswith('http'):
            filename = os.path.basename(src)
            logger.info('Downloading {}'.format(filename))
            response = requests.get(src)
            with open(filename, 'wb') as f:
                f.write(response.content)
            return open(filename, 'r')
        elif protocol == 'file':
            logger.debug('Detected file protocol')
            src = m.group(2)
        else:
            raise Exception('Unsupported protocol: {}'.format(protocol))

    # handle src as file
    logger.debug('Opening {}'.format(src))
    return open(src, 'rb')

