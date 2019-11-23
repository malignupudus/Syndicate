from hashlib import sha256, sha512
from base64 import b64encode

_chars = 'abcdefghijklmnopqrstuvwxyz1234567890'
_n = 30
_decrement_num = 18

def hash(string, limits=0, special_char=_chars, n=_n, decrement_num=_decrement_num):

    limits = int(limits)
    a = string[::2]
    b = string[1::2][::-1]

    string = ''.join((a+b)[::-1])

    if (limits == 0):

        return(sha256(sha512(string.encode()).digest()).hexdigest())

    else:
        
        special_char = str(special_char)
        n = int(n)
        decrement_num = int(decrement_num)
        result = hash(string, 0)
        decrement = False

        for _ in range(limits):

            special_char = b64encode(special_char.encode()).decode()

            if (decrement == False):

                decrement = True

                n -= decrement_num

                if (n == 0):

                    n += 1

            else:

                decrement = False

                n *= n

            a = special_char[::n]
            b = special_char[1::n][::-1]

            result = hash(b+result+a)

        return(result)

def compare(s, h, l=1, sc=_chars, n=_n, dn=_decrement_num):

    salt = 0
    result = hash(s, 0)

    if (result == h):

        return(True)

    while (True):

        salt += 1
        result = hash(s, salt, sc, n, dn)

        if (int(l) == salt):

            break

        elif (result == h):

            return(True)

    if (result == h):

        return(True)

    else:

        return(False)
