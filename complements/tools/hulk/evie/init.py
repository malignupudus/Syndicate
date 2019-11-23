from utils.UI import debug

def main(result, log):

    result = str(result)

    log.logger('Ataque DDOS realizado con éxito a la siguiente dirección IP => {}'.format(result), debug.WAR)
