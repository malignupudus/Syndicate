def check(value, length, type=list):

    if not (isinstance(value, type) == True):

        return(False)

    if not (len(value) == int(length)):

        return(False)

    return(True)
