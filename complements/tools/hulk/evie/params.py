from utils.UI import evieModule

parser = evieModule.CreateComplement('hulk')

parser.set_description(
        '\n' + 'Instrucciones para su uso de forma remota:' + '\n\n'
        '\t' + 'Función: main:' + '\n\n'
        '\t' + ' Inicia hulk.' + '\n\n'
        '\t\t' + 'Parámetros:' + '\n\n'
        '\t\t' + 'address     : str        : La dirección IP/Nombre de Host a atacar' + '\n'
        '\t\t' + 'iterations  : int:10     : Las iteraciones para crear un nuevo subproceso' + '\n'
        '\t\t' + 'process     : int:15     : El número de procesos a utilizar' + '\n'
        '\t\t' + 'threads     : int:500    : El número de hilos a utilizar por cada proceso creado' + '\n'
        '\t\t' + 'safe        : bool:False : Para si es necesario' + '\n'
        '\t\t' + 'referers    : list:[]    : La lista de referidos. Ya tiene una lista predeterminada, por lo tanto lo único que harás será agregar más.' + '\n'
        '\t\t' + 'user_agents : list:[]    : La lista de agentes de usuarios. Al igual que "referers", ya tiene una lista predeterminada y se hacen las mismas operacones'
        )
parser.set_current_version('1.0.0')
parser.set_version('1.0.0', 'DtxdF', ['https://github.com/DtxdF', 'https://underc0de.org/foro/profile/DtxdF'])

parser.set_footer('\n' + 'Precaución: Este complemento está modificado para que actue de forma destructiva, por favor si harás pruebas "baja" los niveles de los parámetros deacuerdo a tus recursos.')

parser.add(['-help'], 'help', 'Muestra la ayuda y sale')

parser.parse_args()
