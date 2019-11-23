from colorama import init # Windows
from time import strftime

init()

# Simple Colors

NORMAL = '\033[0m'
BLUE_simple = '\033[36m'
BLUE_DARK_simple = '\033[34m'
RED_simple = '\033[31m'
YELLOW_simple = '\033[33m'
LIME_simple = '\033[32m'
WHITE_simple = '\033[37m' 

class simpleLoggingLevelNotFound(Exception): """
Excepción generada cuando se coloca como argumento un nivel inexistente
"""

def output_func(string, path):

    open(path, 'ab').write(string.encode())

class logger(object):

    def __init__(self, prompt='Evie', output=False, _format='\033[1m\033[33m[\033[0m%s:%s\033[1m\033[33m]\033[0m\033[1m\033[32:\033[0m\033[1m\033[37m-%s', time_format='%H:%M:%S'): 

        self._format = _format
        self._format_bak = _format
        
        # Attributes

        self.BOLD = '\033[1m'

        # Foreground colors!
        
        self.FG_RED = self.BOLD + '\033[31m%s' + NORMAL
        self.FG_BLUE = self.BOLD + '\033[34m%s'+ NORMAL
        self.FG_GREEN = self.BOLD + '\033[32m%s' + NORMAL
        self.FG_YELLOW = self.BOLD + '\033[33m%s' + NORMAL
        self.FG_WHITE = self.BOLD + '\033[37m%s' + NORMAL
        self.FG_BLACK = self.BOLD + '\033[30m%s' + NORMAL

        # Background colors!

        self.BG_RED = self.BOLD + WHITE_simple + '\033[41m%s' + NORMAL
        self.BG_BLUE = self.BOLD + BLUE_simple + '\033[44m%s'+ NORMAL
        self.BG_GREEN = self.BOLD + WHITE_simple + '\033[42m%s' + NORMAL
        self.BG_YELLOW = self.BOLD + WHITE_simple + '\033[43m%s' + NORMAL
        self.BG_WHITE = self.BOLD + WHITE_simple + '\033[47m%s' + NORMAL

        # Prompt

        self.prompt = self.BOLD + WHITE_simple + prompt + NORMAL
        
        # Time attrs

        self.register_time = True
        
        if (self.register_time == True):
            self.time_for_console = self.FG_YELLOW % ('(') + self.FG_GREEN % ('%s') + NORMAL + self.FG_YELLOW % (')')
            self.time_format = time_format

        if not (isinstance(output, str)):

            self.output = False

        else:

            self.output = output

    def log(self, message, level=1, **kwargs):

        if not (level == 0):

            self._format = self._format_bak

            if (level == 1):

                message = self.BG_BLUE % (message)

                try:

                    message_level = kwargs['info']

                except KeyError:

                    message_level = self.FG_BLUE % ('INFORME')

            elif (level == 2):

                message = self.BG_YELLOW % (message)

                try:

                    message_level = kwargs['warning']

                except KeyError:

                    message_level = self.FG_YELLOW % ('ADVERTENCIA')

            elif (level == 3):

                message = self.BG_GREEN % (message)

                try:

                    message_level = kwargs['personal']

                except KeyError:

                    message_level = self.FG_GREEN % ('PERSONAL')

            elif (level == 4):

                message = self.BG_RED % (message)

                try:

                    message_level = kwargs['com']

                except KeyError:

                    message_level = self.FG_RED % ('COMPROMETIDO')

            else:

                raise simpleLoggingLevelNotFound('El nivel no existe! ...')

        else:

            try:

                self._format = kwargs['nullformat']

            except KeyError:

                self._format = '[%s]:- %s'

        if not (level == 0):

            if (level == 1):

                _extra = self.BOLD + WHITE_simple + '------:' + WHITE_simple + BLUE_DARK_simple + '*' + WHITE_simple + ': ' + NORMAL

            elif (level == 2):

                _extra = self.BOLD + WHITE_simple + '--:' + WHITE_simple + YELLOW_simple + '!' + WHITE_simple + ': ' + NORMAL

            elif (level == 3):

                _extra = self.BOLD + WHITE_simple + '-----:' + WHITE_simple + LIME_simple + '+' + WHITE_simple + ': ' + NORMAL

            elif (level == 4):

                _extra = self.BOLD + WHITE_simple + '-:' + WHITE_simple + RED_simple + 'x' + WHITE_simple + ': ' + NORMAL

            value = self._format % (self.prompt, message_level, '%s%s' % (_extra, message))

        else:

            value = self._format % (self.prompt, message)

        if (self.register_time == True):

            value = self.time_for_console % (strftime(self.time_format)) + value

        print(value)

        if (self.output):
            output_func(value + '\n', self.output)
