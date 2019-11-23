from mss import mss
from mss.tools import to_png

def save():

    screenshots = []

    with mss() as mon:

        monitors = mon.monitors

    monitors = monitors[1:] if (len(monitors) > 1) else monitors

    for _ in monitors:

            with mss() as img:

                content = img.grab(_)

            screenshots.append(to_png(content.rgb, content.size))

    return(screenshots)
