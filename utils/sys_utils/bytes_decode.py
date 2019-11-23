def decode(string):

    return(string.decode() if (isinstance(string, bytes)) else str(string))
