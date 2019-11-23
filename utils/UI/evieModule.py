# Esto módulo pretende crear parámetros para los complementos 
# para syndicate con fácilidad Usando argprogrammer.
#
# Recuerde que para usar los parámetros proporcionados, se usa la siguiente sintaxis:
#      ./evie.py -<El nombre de tu compleento>-<Parámetro propuesto> <Valor sí lo necesita>
#
# - Dtxdf

import sys
import shelve
import re
import os
from utils.Wrappers import wrap
from utils.sys_utils import create_folder
from modules.UI import argprogrammer
from collections import namedtuple

from conf import global_conf

default_config_help = argprogrammer.default_config_help
default_config_type = argprogrammer.default_config_type
default_config_action = argprogrammer.default_config_action
default_config_require = argprogrammer.default_config_require
default_config_value = argprogrammer.default_config_value
default_config_uniqval = argprogrammer.default_config_uniqval
default_config_ignorecase = argprogrammer.default_config_ignorecase
default_config_limit = argprogrammer.default_config_limit
default_parameter = argprogrammer.default_parameter

root_folder = '%s/%s' % (global_conf.databases['database'], global_conf.databases['preserved'])

class noModuleNameIsPresent(Exception):

    '''Cuando no se configura el nombre del complemento'''

class CreateDatabase(object):

    def __init__(self, complement_name):

        self.__complement_name = os.path.basename(str(complement_name)).strip()
        
        if (self.__complement_name == '') or (re.search(r'(?=\.+)', self.__complement_name)):

            raise ValueError('El nombre del complemento no es correcto')

        create_folder.create(root_folder)
        self.__db = '%s/%s.evd' % (root_folder, self.__complement_name)

    def getDB(self):

        return(wrap.getDB(wrap.USE_PERSONAL, self.__db))

    def add(self, *args, **kwargs):

        return(wrap.add(*args, **kwargs, agent=wrap.USE_PERSONAL, personal=self.__db))

    def raw(self, *args, **kwargs):

        return(wrap.raw(*args, **kwargs, agent=wrap.USE_PERSONAL, personal=self.__db))

    def delete(self, *args, **kwargs):

        return(wrap.delete(*args, **kwargs, agent=wrap.USE_PERSONAL, personal=self.__db))

    def write(self, *args, **kwargs):

        return(wrap.write(*args, **kwargs, agent=wrap.USE_PERSONAL, personal=self.__db))

    def read(self, *args, **kwargs):

        return(wrap.read(*args, **kwargs, agent=wrap.USE_PERSONAL, personal=self.__db))

    def getall(self, *args, **kwargs):

        return(wrap.getall(agent=wrap.USE_PERSONAL, personal=self.__db))

class CreateComplement(argprogrammer.Parser):

    def __init__(self, complement_name):

        super().__init__(complement_name)

        self.optionals = 'Opcionales'

        #// INIT VERSION
        self.current_version = None
        self.__start_version = True # Evitar escribir denuebo el parámetro
        #// END VERSION

        #// INIT VERSIONS
        self.versions = {}
        self.__start_versions = True # Evitar escribir denuebo el parámetro
        #// END VERSIONS

        #// INIT REQUIREMENTS
        self.requirements = {}
        self.__start_requirements = True # Evitar escribir denuebo el parámetro
        #// END REQUIREMENTS

        complement_name = str(complement_name)

        try:

            namedtuple(complement_name, '')

        except ValueError:

            raise ValueError('Error con el nombre del complemento, no es correcto')

        else:

            self.complement_name = complement_name

        super().set_head(
                '%sSyndicate Project - Complemento: %s' % (' '*7, self.complement_name) + '\n'
                '%s-----------------   -----------' % (' '*7)
                )

        super().set_error_format('{}: El parámetro "%s" no es válido'.format(self.complement_name))
        super().set_uniq_message('{}: El valor "%s" no está permitido debido a qué no es igual es este/estos valor/es "%s"'.format(self.complement_name))
        super().set_type_message('{}: El tipo de dato del valor "%s" no es igual a "%s"'.format(self.complement_name))

    @staticmethod
    def __check_version(version):

        version = str(version)

        if not (re.match(r'\d\.\d\.\d', version)):

            raise ValueError('La sintaxis de la versión debe ser la siguiente: n.n.n')
    
    def set_requirements(self, pack, version=None, control=None):

        if (version == None) or (control == None):

            self.requirements[pack] = None

        else:

            if (control in ['>', '<', '==', '<=', '>=']):

                self.requirements[pack] = (version, control)

            else:

                raise ValueError('Sólo se permiten las siguientes operaciones: "<, >, <=, >=, =="')

        if (self.__start_requirements == True):

            self.__start_requirements = False
            super().add(['-%s-requirements' % (self.complement_name)], 'requirements', 'Muestra los requerimientos', type=bool, group=self.optionals, action=True)

    def set_current_version(self, version):

        self.current_version = str(version)
        
        self.__check_version(self.current_version)

        if (self.__start_version == True):

            self.__start_version = False
            super().add(['-%s-version' % (self.complement_name)], 'version', 'Muestra la versión actual del complemento', type=bool, group=self.optionals, action=True)

    def set_version(self, version, author, social_networks=None):

        version = str(version)
        author = str(author)

        if not (social_networks == None):

            if not (isinstance(social_networks, list) == True):

                raise TypeError('El tipo de dato para las redes sociales debe ser una lista')

            social_networks = [str(x) for x in social_networks]

        self.__check_version(version)

        if (self.versions.get(version) == None):

            self.versions[version] = []

        self.versions[version].append((author, social_networks))

        if (self.__start_versions == True):

            self.__start_versions = False
            super().add(['-%s-versions' % (self.complement_name)], 'versions', 'Muestra las versiones del complemento', group=self.optionals, type=bool, action=True)

    def set_description(self, description):

        super().set_head(self._Parser__head + '\n' + str(description))

    def add(self, param_name, key, help=default_config_help, type=default_config_type, group=default_parameter, action=default_config_action, default=default_config_value, uniqval=default_config_uniqval, ignorecase=default_config_ignorecase, limit=default_config_limit):

        new_param_name = []

        if not (isinstance(param_name, list) == True):

            raise TypeError('El argumento no está siguiendo el tipo de dato correcto')
        
        if (len(param_name) == 0):

            raise ValueError('La lista no puede estar vacia')

        for _ in param_name:

            if (_[:2] == '--'):

                new_param_name.append('-%s-%s' % (self.complement_name, _[2:]))

            elif (_[0] == '-'):

                new_param_name.append('-%s-%s' % (self.complement_name, _[1:]))

            else:

                new_param_name.append(_)

        super().add(param_name=new_param_name, key=key, help=help, type=type, group=group, action=action, require=False, default=default, uniqval=uniqval, ignorecase=ignorecase, limit=limit)

    def parse_args(self):

        args = super().parse_args(show_error=False)

        if (hasattr(args, 'requirements')):

            if (args.requirements == True):

                if (self.requirements == {}):

                    print('No hay requerimientos actualmente...')

                else:

                    for key, value in self.requirements.items():

                        if (value == None):

                            print(key)

                        else:

                            print('{0}{1}{2}'.format(key, value[1], value[0]))

                sys.exit(0)

        if (hasattr(args, 'version')):

            if (args.version == True):

                if (self.current_version == None):

                    print('No hay una versión actual todavía')

                else:

                    print('La versión actual es: {}'.format(self.current_version))

                sys.exit(1)

        if (hasattr(args, 'versions')):

            if (args.versions == True):

                if (self.versions == {}):

                    print('No hay versiones disponibles....')

                else:

                    print()

                    for key, value in self.versions.items():

                        print('Versión: {}'.format(key), end='\n\n')
                        
                        for _ in value:

                            _social_networks = ', '.join(_[1])

                            print('   * {}{}'.format(_[0], ' ({})'.format(_social_networks) if not (_social_networks == '') else ''))

                        print()

                sys.exit(1)

        return(args)
