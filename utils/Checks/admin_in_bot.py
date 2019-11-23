from utils.Wrappers import wrap

def check(admin, bot):

    data = wrap.read(bot, 'admins', separate=True)

    if (data == False):

        return(False)
    
    return(admin in data)
