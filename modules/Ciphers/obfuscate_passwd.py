def obfuscate(string):

    a = string[::2]
    b = string[1::2][::-1]

    return(''.join((a+b)[::-1]))
