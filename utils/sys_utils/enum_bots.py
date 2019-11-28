from utils.Wrappers import wrap
from utils.Shows import show_user_rooks

def enum(admin, count=True):

    bots = []

    for _ in show_user_rooks.show():

        admins = wrap.read(_, 'admins', agent=wrap.USE_BOT, separate=True)

        if (admins == False):

            bot.append(-1)

        if (admin in admins):

            bots.append((_, wrap.read(_, 'username', separate=True)))

    return(bots if (count == False) else len(bots))
