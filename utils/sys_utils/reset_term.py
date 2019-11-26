import sys
from subprocess import call

def reset(code=0):

    call(['reset', '-w'])
    sys.exit(code)
