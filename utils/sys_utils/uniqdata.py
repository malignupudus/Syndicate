from yaml import dump
from hashlib import md5

def uniqdata(data):

        result = {}

        for _ in data:

            result[md5(dump(_).encode()).hexdigest()] = _

        return(list(result.values()))
