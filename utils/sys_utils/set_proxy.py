from conf import global_conf
from modules.Connections import convex

def autoconf():

    if (global_conf.connector.get('use_proxy') == True):

        convex.transfor(
                
                proxy_type=global_conf.connector.get('proxy_type'),
                proxy_addr='{}:{}'.format(global_conf.connector.get('proxy_addr'), global_conf.connector.get('proxy_port')),
                rdns=global_conf.connector.get('proxy_rds'),
                username=global_conf.connector.get('proxy_username'),
                password=global_conf.connector.get('proxy_password')
                
                )
