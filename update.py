import requests
import subprocess
from os.path import isfile

url = 'https://raw.githubusercontent.com/DtxdF/Syndicate/master/version.txt'
file_version = 'version.txt'

def get_current_version():

    if not (isfile(file_version)):

        raise FileNotFoundError('El archivo de la versión de Syndicate Project no existe, por favor verifique nuevamente o contacte al administrador del proyecto.')

    with open(file_version, 'rt') as file_object:

        current_version = file_object.read().strip()

    return(current_version)

def check_update():

    version = requests.get(url).content
    version = version.decode() if (isinstance(version, bytes)) else str(version)
    version = version.strip()

    if (version != get_current_version()):

        return(True)

    else:

        return(False)

def main():

    try:

        current_version = get_current_version()

        if (check_update() == True):

            subprocess.call(['git', 'pull', 'origin', 'master'])

            print('Syndicate Project se ha actualizado a la versión: {}'.format())

        else:

            print('Ya tienes la versión actual: {}'.format(current_version))

    except Exception as Except:

        print('Oops..., Ocurrio un mal entendido, intentelo más tarde o verifique que no es un error grave. Excepción: {}'.format(Except))

if __name__ == '__main__':

    main()
