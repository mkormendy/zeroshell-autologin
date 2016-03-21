#!/usr/bin/python

# load python library

from urllib import urlencode
from urllib2 import urlopen
from HTMLParser import HTMLParser
from time import sleep

# login conf

USERNAME = 'admin'
PASSWORD = 'zeroshell'
REALM = 'ZEROSHELL.NET'
SERVER = '192.168.0.75'

# default params

PROTOCOL = 'https'
PORT = '12081'
SCRIPT = 'zscp'
ZSCPRedirect = '_:::_' 

URL = PROTOCOL + '://' + SERVER + ':' + PORT + '/cgi-bin/' + SCRIPT
RENEW_INTERVAL = 40

# class to parse Captive Portal HTML

class ZSParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.params = {}
		params = { 'U' : USERNAME , 'P' : PASSWORD , 'Realm' : REALM , 'Section' : 'CPAuth' , 'Action' : 'Authenticate' , 'ZSCPRedirect' : '_:::_' }
		http_req = urlopen(URL, urlencode(params))
		html_content = http_req.read()
		self.feed(html_content)
	
	def get_authkey(self):
			return self.params['Authenticator'] # after parse HTML return the authenticator string

	def handle_starttag(self, tag, attrs):
		if tag == 'input' and attrs[0][1] == 'hidden': # parse only de html input and hidden tags 
			self.params[attrs[1][1]] = attrs[2][1] 

parser = ZSParser() # instantiate the class
authkey = parser.get_authkey() # get authenticator string

# http_request 1 - Section = CPGW

params = { 'U' : USERNAME , 'P' : PASSWORD , 'Realm' : REALM , 'Authenticator' : authkey, 'Section' : 'CPGW' , 'Action' : 'Connect' , 'ZSCPRedirect' : '_:::_' }
urlopen(URL, urlencode(params))

# http_request 2 - Section = ClientCTRL

params = { 'U' : USERNAME , 'P' : PASSWORD , 'Realm' : REALM , 'Authenticator' : authkey, 'Section' : 'ClientCTRL' , 'Action' : 'Connect' , 'ZSCPRedirect' : '_:::_' }
urlopen(URL, urlencode(params))


while True:
	sleep(RENEW_INTERVAL) # wait a time in seconds to renew the connection
	params = { 'Authenticator' : authkey, 'Section' : 'CPGW' , 'Action' : 'Renew' , 'ZSCPRedirect' : '_:::_' }
	urlopen(URL, urlencode(params))

