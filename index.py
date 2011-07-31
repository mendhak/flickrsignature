from urlparse import urlparse
from mod_python import Session
import re
import flickr

def index(req):


	session = Session.Session(req)

	req.content_type="text/html"
	qs = urlparse(req.subprocess_env['QUERY_STRING'])
	
	user = ''
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

			FFF = 0

			if not re.match("([0-9]+@N[0-9]+)", params['user']) and not 'nsid' in session > 0:
				user = flickr.getUserNSID('mendhak')
				session['nsid'] = user
				session.save()
			elif len(session['nsid']) > 0:
				user = session['nsid']
			else:
				user = params['user']
							
			return user
	return 'No parameters supplied'



