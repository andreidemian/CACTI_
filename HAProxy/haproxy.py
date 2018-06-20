#!/usr/bin/python

import os
import re
import sys
import urllib3

HAPROXY_STATS_URL = '/haproxy'
HAPROXY_PORT = 80
HAPROXY_IP = '192.168.0.1'
HAPROXY_HTTPS = ''
HAPROXY_AUTH = ''
HAPROXY_USER = 'user'
HAPROXY_PASS = 'pass'


def haproxy_stats(pxname, svname):

	http = urllib3.PoolManager()
	headers = urllib3.util.make_headers(basic_auth=HAPROXY_USER + ':' + HAPROXY_PASS)

	url = ''
	if((HAPROXY_HTTPS == 'on') or (HAPROXY_HTTPS == 'ON')):
		url = 'https://{}:{}{};csv'.format(HAPROXY_IP,HAPROXY_PORT,HAPROXY_STATS_URL)
	else:
		url = 'http://{}:{}{};csv'.format(HAPROXY_IP,HAPROXY_PORT,HAPROXY_STATS_URL)

	if((HAPROXY_AUTH == 'on') or (HAPROXY_AUTH == 'ON')):
		r = http.request('GET', url, headers=headers)
	else:
		r = http.request('GET', url)


	if(r.status == 200):
		lines = re.split('\n+', r.data)
		head = re.split(',', lines[0])
		out = ''
		sep = ''
		for i in xrange(1, (len(lines) - 1)):
			m = re.split(',',lines[i])
			for z in xrange(0,1):
				if((m[z] == pxname) and (m[z+1] == svname)):
					for x in xrange(2, (len(m) - 1)):
						cont = m[x]
						if(cont == ''):
							cont = '0'
						out += sep + head[x] + ':' + cont
						sep = ' '
		print out
	else:
		print '	haproxy http error:{}'.format(r.status)


arg = ['','FRONTEND']
if(len(sys.argv) != 1):
	for i in xrange(1, len(sys.argv)):
        	if(sys.argv[i] == '--group'):
                	arg[0] = sys.argv[i+1]

        	if(sys.argv[i] == '--srv'):
                	arg[1] = sys.argv[i+1]

		if(sys.argv[i] == '--port'):
			HAPROXY_PORT = sys.argv[i+1]
	
		if(sys.argv[i] == '--ip'):
			HAPROXY_IP = sys.argv[i+1]

		if(sys.argv[i] == '--auth'):
			HAPROXY_AUTH = sys.argv[i+1]

		if(sys.argv[i] == '--user'):
			HAPROXY_USER = sys.argv[i+1]
	
	        if(sys.argv[i] == '--pass'):
        	        HAPROXY_PASS = sys.argv[i+1]

		if(sys.argv[i] == '--https'):
			HAPROXY_HTTPS = sys.argv[i+1]

		if(sys.argv[i] == '--url'):
			HAPROXY_STATS_URL = sys.argv[i+1]

		if(sys.argv[i] == '--help'):
			print '''
---------------------------------------------------------------------------------------------------------------------------------------------------
	HOW TO:

	example: python haproxy.py --group Servers --srv web1 --ip 192.168.0.1 --port 1936 --auth on --user admin --pass thisismypass --https off --url /haproxy


	Options:

	--group -> frontend name or BACKEND server group
	
	--srv -> specify BACKEND server ( for the FRONTEND default is --srv FRONTEND )

	--port -> haproxy stats webinterface ( default port is 80 )

	--ip -> haproxy stats webinterface IP ( example: 192.168.0.1 )

	--auth -> activate authentication
	
	--user -> haproxy stats username
	
	--pass -> haproxy pass password

	--https -> activate https

	--url -> haproxy stats url ( default is /haproxy )
----------------------------------------------------------------------------------------------------------------------------------------------------
'''

	if((arg[0] != '') and (arg[1]) != ''):
		haproxy_stats(arg[0], arg[1])


else:
	print '''
----------------------------------------------------------------------------------------------------------------------------------------------------

	No arguments are selected, for more info type ./haproxy.py --help or python haproxy.py --help
		
-----------------------------------------------------------------------------------------------------------------------------------------------------
'''
