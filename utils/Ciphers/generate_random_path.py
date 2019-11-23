from random import shuffle, randint
from base64 import b64encode

chars = 'abcdefghijklmnopqrstuvwxyz0123456789'

def generate():

    global chars

    array_chars = ' '.join(b64encode(chars.encode()).decode()).split()
    
    for _ in range(randint(1, 1000)):

        shuffle(array_chars)

    return(''.join(array_chars[0:randint(5, 10)]))
