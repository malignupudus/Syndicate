from utils.UI import debug

def main(result, log):

    if (isinstance(result, list)):

        for _ in result:

            log.logger('{}'.format(_), debug.WAR)

    else:

        log.logger('El tipo de dato ', debug.WAR)
