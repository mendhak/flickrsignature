from urlparse import urlparse
from mod_python import Cookie, util
import re
import flickr
import time
import urllib
from xml.dom import minidom


def index(req):

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
				if num <= 0:
					num = 1
	
			if 'size' in params and len(params['size']) > 0:
				size = params['size']

			if 'item' in params and len(params['item']) > 0:
				item = params['item']

			nsid = getNSID(req, params)
			
			#Now get the photos
			photos = getPhoto(nsid, num)

			if len(photos) > 0:
				selectedPhoto = photos.pop(0)
				
				if item == 'img':
					redirectToImage(selectedPhoto, size, req)
				else:
					redirectToPhotoPage(selectedPhoto, nsid, req)
					
			
	return 'No parameters supplied'


def getPhoto(nsid, photoNumber):
	return flickr.photos_search(user_id=nsid, per_page=1, page=photoNumber)
	


def redirectToImage(selectedPhoto, size, req):
	size = size.lower()

	if size == 'm' or size == 'medium' or size == 'med':
		size = 'm'
	elif size == 's' or size == 'small':
		size = 's'
	elif size == 't' or size == 'thumb' or size == 'thumbnail' or size == 'tiny':
		size = 't'
	elif size == 'z' or size == 'medium640' or size == 'medium 640':
		size = 'z'
	elif size == 'b' or size == 'large' or size == 'big':
		size = 'b'

	photoUrl = "http://farm{0}.static.flickr.com/{1}/{2}_{3}_{4}.jpg".format(selectedPhoto.farm, selectedPhoto.server, selectedPhoto.id, selectedPhoto.secret, size)
	util.redirect(req, location=photoUrl, permanent=False)

def redirectToPhotoPage(selectedPhoto, nsid, req):
	photoPage = "http://www.flickr.com/photos/{0}/{1}".format(nsid, selectedPhoto.id)
	util.redirect(req, location=photoPage, permanent=False) 


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
		nsid = params['user']
					
	return nsid

