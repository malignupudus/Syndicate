from utils.Wrappers import wrap
from os.path import splitext
from os import listdir

def enum(admin, count=True):

    bots = []

    for _ in [splitext(x)[0] for x in listdir(wrap.getDB(wrap.USE_BOT))]:

        admins = wrap.read(_, 'admins', agent=wrap.USE_BOT, separate=True)

        if (admins == False):

            return(-1)

        if (admin in admins):

            bots.append((_, wrap.read(_, 'username', separate=True)))

    return(bots if (count == False) else len(bots))
