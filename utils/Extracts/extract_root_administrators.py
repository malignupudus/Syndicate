from utils.Wrappers import wrap
from utils.Shows import show_user_admins

def extract():

    result = []

    for _ in show_user_admins.show():

        _data = wrap.getall(wrap.USE_ADMIN, username=_, separate=True)

        for _ in _data:

            result.append(_) if (_data[_]['root'] == True) else None

    return(result)
