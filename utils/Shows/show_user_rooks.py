from os import listdir
from os.path import splitext, isfile

from conf import global_conf

def show():

    folder = '{}/{}'.format(global_conf.databases['database'], global_conf.databases['credentials'])

    return([splitext(x)[0] for x in listdir(folder) if (x.endswith('.db') and (isfile('{}/{}'.format(folder, x))))])
