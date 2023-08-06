'''
all logging-related utilities
'''

import os

def setup_logging(run_name, rootdir, info=None):
    '''
    set up logging for this run
    '''
    os.makedirs(os.path.join(rootdir, 'models'), exist_ok=True)
    os.makedirs(os.path.join(rootdir, 'logs'), exist_ok=True)
    os.makedirs(os.path.join(rootdir, 'models', run_name), exist_ok=True)
    os.makedirs(os.path.join(rootdir, 'logs', run_name), exist_ok=True)

    if info:
        with open(os.path.join(rootdir, 'logs', run_name, 'info.txt'), 'w') as f:
            f.write(info)