def convert(data):

    return(str(data).encode() if not (isinstance(data, bytes)) else data)
