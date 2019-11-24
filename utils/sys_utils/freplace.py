def replace(string, replace_list):

    if not (isinstance(string, str)):

        raise TypeError('El tipo de dato del string no es correcto')

    if not (isinstance(replace_list, list)):

        raise TypeError('La lista de remplazos no tiene un tipo de dato correcto')

    for _ in replace_list:

        if not (isinstance(_, tuple)):

            raise TypeError('Hay un remplazo que no tiene un tipo de dato correcto')

        else:

            if (len(_) != 2):

                raise ValueError('Hay un remplazo que no está siguiendo la longitud de los valores correspondidos')

        if (string.find(str(_[0])) != -1):

            string = string.replace(str(_[0]), str(_[1]))

    return(string)
