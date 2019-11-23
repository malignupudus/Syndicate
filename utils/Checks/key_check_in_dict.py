def check(dic, key):

    try:

        dic[key]

    except KeyError:

        return(False)

    else:

        return(True)
