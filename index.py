from urlparse import urlparse
from mod_python import Cookie
import re
import flickr
import time

def index(req):


	req.content_type="text/html"
	qs = urlparse(req.subprocess_env['QUERY_STRING'])
	
	nsid = ''
	num = 1
	size = 'm'
	item = 'img'

	if len(qs.geturl()) > 0:
		params = dict([part.split('=') for part in qs.geturl().split('&')])
		if len(params) > 0:
			user = params['user']
			if 'num' in params and len(params['num']) > 0:
				num = params['num']
	
			if 'size' in params and len(params['size']) > 0:
				size = params['size']

			if 'item' in params and len(params['item']) > 0:
				item = params['item']

			nsid = getNSID(req, params)
			return nsid
			
	return 'No parameters supplied'


def getNSID(req, params):
	cookies = Cookie.get_cookies(req)
	cookieKey = 'nsid_' + params['user']

	if cookies.has_key(cookieKey):
		nsid = cookies[cookieKey].value
	elif not re.match("([0-9]+@N[0-9]+)", params['user']) and not cookieKey in cookies:
		nsid = flickr.getUserNSID(params['user'])
		c = Cookie.Cookie(cookieKey, nsid)
		c.expires = time.time() + 30 * 24 * 60 * 60
		Cookie.add_cookie(req, c)
	else:
		nsid = params['nsid']
					
	return nsid



