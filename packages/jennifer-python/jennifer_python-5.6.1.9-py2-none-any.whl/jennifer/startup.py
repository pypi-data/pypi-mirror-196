import os

import jennifer.network_logger
from jennifer.agent import jennifer_agent


# Not used
# def setup_log(config):
#     logger = logging.getLogger('jennifer')
#     logger.setLevel(logging.INFO)
#     logger.propagate = False
#     handler = logging.FileHandler(config['log_path'])
#     formatter = logging.Formatter('%(asctime)s [JENNIFER Python] %(levelname)s %(message)s')
#     handler.setFormatter(formatter)
#     logger.addHandler(handler)
#     print('setup_log')

# config.address == /tmp/jennifer-...sock
# config.log_dir == /tmp


def init():
    jennifer_agent()


def _debug_log(text):
    if os.getenv('JENNIFER_PY_DBG'):
        log_socket = __import__('jennifer').get_log_socket()
        if log_socket is not None:
            log_socket.log(text)
