from utils.UI import evieModule

parser = evieModule.CreateComplement('keylogger')

parser.set_description(
        '\n' + 'Instrucciones para su uso de forma remota:' + '\n\n'
        '\t' + 'Función: init:' + '\n\n'
        '\t' + ' Inicia la captura de teclas.' + '\n\n'
        '\t\t' + 'Parámetros:' + '\n\n'
        '\t\t' + 'wait : int:30 : La duración de la captura de las teclas'
        )
parser.set_current_version('1.0.0')
parser.set_version('1.0.0', 'DtxdF', ['https://github.com/DtxdF', 'https://underc0de.org/foro/profile/DtxdF'])

parser.add(['-help'], 'help', 'Muestra la ayuda y sale')

parser.parse_args()
