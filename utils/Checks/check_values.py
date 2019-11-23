def check(value, length, type=tuple):

    if not (isinstance(value, type) == True):

        return(False)

    if not (len(value) == int(length)):

        return(False)

    return(True)
