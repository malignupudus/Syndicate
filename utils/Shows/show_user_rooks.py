from os import listdir
from os.path import splitext

from conf import global_conf

def show():

    return([splitext(x)[0] for x in listdir('%s/%s' % (global_conf.databases['database'], global_conf.databases['credentials']))])
