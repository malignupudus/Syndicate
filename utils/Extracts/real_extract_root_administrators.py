from utils.Extracts import extract_root_administrators
from utils.sys_utils import enum_bots
from utils.Wrappers import wrap

def extract():

    root_administrators = []

    for _ in extract_root_administrators.extract():

        max_bot = wrap.read(_, 'max_bot', agent=wrap.USE_ADMIN, separate=True)

        if not (str(max_bot) == 'False'):

            if (max_bot > 0):

                enums = enum_bots.enum(_)

                if not (enums == -1):

                    if not (enums >= max_bot):

                        root_administrators.append(_)

            else:

                root_administrators.append(_)

    return(root_administrators)
