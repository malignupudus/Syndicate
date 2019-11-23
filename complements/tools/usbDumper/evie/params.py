from utils.UI import evieModule

parser = evieModule.CreateComplement('usbDumper')

parser.set_description(
        '\n' + 'Instrucciones para su uso de forma remota:' + '\n\n'
        '\t' + 'Función: init:' + '\n\n'
        '\t' + ' Lista todos los archivos posibles con sus permisos necesarios.' + '\n\n'
        '\t\t' + 'Parámetros:' + '\n\n'
        '\t\t' + 'directory : str : La ruta donde se encuentran los archivos a copiar. Sí no se define, se usan los directorios predeterminados según el SO/Distribución. NT[A-Z] (Excepto "C") y POSIX[/media]' + '\n\n'
        '\t' + 'Función: copy:' + '\n\n'
        '\t' + ' Copia un archivo.' + '\n\n'
        '\t\t' + 'Parámetros:' + '\n\n'
        '\t\t' + 'filename  : str : La ruta del archivo a copiar' + '\n\n'
        '\t' + 'Función: copytree:' + '\n\n'
        '\t' + ' Copia todos los archivos posibles.' + '\n\n'
        '\t\t' + 'Parámetros:' + '\n\n'
        '\t\t' + 'directory : str : La ruta donde se encuentran los archivos a copiar. Sí no se define, se usan los directorios predeterminados según el SO/Distribución. NT[A-Z] (Excepto "C") y POSIX[/media]' + '\n\n'
        '\t' + 'Función: detect:' + '\n\n'
        '\t' + ' Queda en espera hasta que detecte un archivo en la ruta especificada.' + '\n\n'
        '\t\t' + 'Parámetros:' + '\n\n'
        '\t\t' + 'directory : str : La ruta donde se encuentran los archivos a copiar. Sí no se define, se usan los directorios predeterminados según el SO/Distribución. NT[A-Z] (Excepto "C") y POSIX[/media]' + '\n\n'
        )
parser.set_current_version('1.0.0')
parser.set_version('1.0.0', 'DtxdF', ['https://github.com/DtxdF', 'https://underc0de.org/foro/profile/DtxdF'])

parser.add(['-help'], 'help', 'Muestra la ayuda y sale')

parser.parse_args()
