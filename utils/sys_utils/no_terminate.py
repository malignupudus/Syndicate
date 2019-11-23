while (1):

    try:

        import signal
        import sys

    except KeyboardInterrupt:

        continue

    else:

        break

def _no_kill(signum, frame):

    sys.exit(0)

signal.signal(signal.SIGTERM, _no_kill)
signal.signal(signal.SIGINT, _no_kill)
