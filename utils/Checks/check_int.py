def check(n, pos_convert=True):

    try:

        n = int(n)

    except (TypeError, ValueError):

        return(None)

    else:

        if ('-' in str(n)) and (pos_convert == True):

            n = n*-1

        return(n)
