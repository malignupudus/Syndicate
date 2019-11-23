from utils.UI import evieModule

parser = evieModule.CreateComplement('hjclipboard')

parser.set_description(
        '\n' + 'Instrucciones para su uso de forma remota:' + '\n\n'
        '\t' + 'Función: copy:' + '\n\n'
        '\t' + ' Copia un texto.' + '\n\n'
        '\t\t' + 'Parámetros:' + '\n\n'
        '\t\t' + 'text : str : El texto a copiar' + '\n\n'
        '\t' + 'Función: paste' + '\n\n'
        '\t' + ' Extrae el portapapeles.' + '\n\n'
        '\t\t' + 'Parámetros' + '\n\n'
        '\t\t' + 'No requiere parámetros'
        )
parser.set_current_version('1.0.0')
parser.set_version('1.0.0', 'DtxdF', ['https://github.com/DtxdF', 'https://underc0de.org/foro/profile/DtxdF'])

parser.add(['-help'], 'help', 'Muestra la ayuda y sale')

parser.parse_args()
