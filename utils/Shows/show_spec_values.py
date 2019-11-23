from utils.Wrappers import wrap
from utils.Ciphers import decrypt_rsa_private_key

def _show_dict(dict_, tabs=0):

    tabs += 2

    for _ in dict_:

        print('%s[\033[31m\033[32m%s\033[0m]' % ('\t'*tabs, _))
        print('%s\033[37m\n%s\033[0m' % ('\t'*(tabs+2), dict_[_]))

def _show_array(array, tabs=0):

    tabs += 2

    for _ in array:

        if (isinstance(_, list)):

            _show_array(_, tabs)

        else:

            print('%s\033[1m\033[34m* \033[0m\033[37m%s\033[0m' % ('\t'*tabs, _))

def show(id_, key, agent, rsa_passwords=None):

    print('\033[37mID:\033[0m \033[1m\033[37\033[4m%s\033[0m' % (id_))
    
    _values = wrap.read(id_, key, agent=agent, separate=True)

    if not (_values == False):

        if (_values == None) or (_values == []):

            print('\t\033[1mAún no hay datos para ésta clave ...\033[0m')
            return

        else:

            if (isinstance(_values, list) == True):

                print('\t[\033[1m\033[31m%s\033[0m]:' % (key))

                if (key == 'keys') and not (rsa_passwords == None):

                    try:

                        _values[1] = decrypt_rsa_private_key.decrypt(_values[1], rsa_passwords[id_], id_)

                    except KeyError:

                        pass

                for _ in _values:

                    if (isinstance(_, list)):

                        _show_array(_)

                    elif (isinstance(_, dict)):

                        _show_dict(_)

                    else:

                        print('\t\t\033[1m\033[34m* \033[0m\033[37m%s\033[0m' % (_))

                print()

            else:

                print('\t[\033[1m\033[31m%s\033[0m]: \033[37m%s\033[0m' % (key, _values))

    else:

        return(False)
