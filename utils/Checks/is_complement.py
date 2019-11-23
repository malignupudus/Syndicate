from os import listdir
from os.path import isfile

from conf import global_conf

complements = global_conf.databases['complements']

def check(name):

    for _ in listdir(complements):

        if (name == _):

            folder_name = '{}/{}'.format(complements, _)

            if (isfile('{}/rook/src/init.py'.format(folder_name))) and (isfile('{}/evie/init.py'.format(folder_name))):

                return(True)

    return(False)
