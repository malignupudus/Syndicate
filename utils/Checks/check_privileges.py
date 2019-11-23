from utils.Wrappers import wrap

def check(admin, privilege):

    data = wrap.read(admin, 'privileges', agent=wrap.USE_ADMIN, separate=True)

    if (data == False): return(False)

    if ('ALL' in data): return(True)

    if (privilege in data): return(True)

    return(False)
