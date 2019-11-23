from pager import getchars

def iInput(char=None, char_limit=None, indicator='', end_char='\n', datatype=str, all_delete_key='\x04', dinamic_char='*', hide_string=True, hide_key='\x08'):

    _current_char = None
    string = ''
    index = 0
    dinamic_change = False

    print(f'\r{indicator}', end='')

    while(True):

        if not (char_limit == None):

            if (len(string) == char_limit):

                break

        _current_char = ''.join(getchars())

        if (_current_char == end_char):

            break

        elif (_current_char == '\x7f'):

            string = string[:-1]

        elif (_current_char == hide_key):

            if (hide_string == True):

                if (dinamic_change == False) and (char == None):

                    char = dinamic_char
                    dinamic_change = True

                else:

                    char = None
                    dinamic_change = False

                _current_char = ''

            else:

                continue

        elif (_current_char == all_delete_key):

            pass

        elif ('\x1b' in _current_char):

            continue

        else:

            if (datatype == int):

                try:

                    int(_current_char)

                except ValueError:

                    continue

            string += _current_char

        print(f'\r{indicator}%s' % (''.join([' ' for x in range(len(string)+1)])), end='')

        if not (_current_char == all_delete_key):

            if (char == None):

                print(f'\r{indicator}{string}', end='')

            else:

                print('\r%s%s' % (indicator, char*len(string)), end='')

        else:

            string = ''
            print(f'\r{indicator}', end='')

    print()

    result = string.rstrip()

    if (datatype == int):

        return(0 if (result == '') else int(result))

    else:

        return(result)
