from utils.UI import evieModule

parser = evieModule.CreateComplement('inject')

parser.set_description(
        '\n' + 'Instrucciones para su uso de forma remota:' + '\n\n'
        '\t' + 'Función: inject:' + '\n\n'
        '\t' + ' Inyecta un ejecutable portable o un shellcode en un proceso arbitrario.' + '\n\n'
        '\t\t' + 'Parámetros:' + '\n\n'
        '\t\t' + 'pid        : int        : El identificador del proceso a inyectar' + '\n'
        '\t\t' + 'shellcode  : bytes      : El código a inyectar' + '\n'
        '\t\t' + 'exe        : bool:True  : Sí "exe" es True significa que "shellcode" es el código de un ejecutable y no un shellcode ne sí, por lo tanto lo convertira a un shellcode'
        )
parser.set_current_version('1.0.0')
parser.set_version('1.0.0', 'DtxdF', ['https://github.com/DtxdF', 'https://underc0de.org/foro/profile/DtxdF'])
parser.set_version('1.0.0', 'Barry Shteiman')

parser.add(['-help'], 'help', 'Muestra la ayuda y sale')

parser.parse_args()
