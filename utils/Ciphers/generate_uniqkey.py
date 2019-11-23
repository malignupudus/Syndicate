from secrets import token_hex

from conf import global_conf

def generate(length=global_conf.token['uniqkey_max_length']):

    return(token_hex(int(length)))
