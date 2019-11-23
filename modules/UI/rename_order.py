from os.path import splitext, isfile

def rename(filename):

    filename = str(filename)

    if not (isfile(filename)):

        return(False)

    while (isfile(filename)):

        (_name, _ext) = splitext(filename)

        if (_ext == '') or (_ext == '.'):

            filename = _name+'.1'

        else:

            _bak_ext = _ext.replace('.','')

            try:

                _num_ext = int(_bak_ext)
                _num_ext += 1

                filename = _name+'.'+str(_num_ext)

            except ValueError:

                filename = filename+'.1'

    return(filename)
