from urlparse import urlparse
from mod_python import Cookie, util
import re
import time
import urllib
from xml.dom import minidom



def index(req):

	apiKey = "a39dfdf51784c76fa3234f88bec38b0e"
	qs = urlparse(req.subprocess_env['QUERY_STRING'])
	destinationUrl = ""
	
	nsid = ''
	num = 1
	size = 'm'
	item = 'img'

	if len(qs.geturl()) > 0:
		params = dict([part.split('=') for part in qs.geturl().split('&')])
		if len(params) > 0:
			user = params['user']
			if params.has_key('num') and len(params['num']) > 0 and params['num'].isdigit():
				num = int(params['num'])
				if num <= 0:
					num = 1

			if params.has_key('size') and len(params['size']) > 0:
				size = params['size'].lower()

			if params.has_key('item') and len(params['item']) > 0:
				item = params['item'].lower()

			nsid = getNSID(req, apiKey, params['user'])
			
			photo = getPhoto(apiKey, nsid, num)

			if photo:
				if item == 'img':
					req.headers_out.add("Cache-Control", "private, max-age=3600")
					destinationUrl = getImageUrl(photo, size, req)

				else:
					destinationUrl = getPhotoPageUrl(photo, nsid, req)

			util.redirect(req, location=destinationUrl, permanent=False)
					
			
	return 'No parameters supplied'


def getImageUrl(selectedPhoto, size, req):

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

	return "http://farm{0}.static.flickr.com/{1}/{2}_{3}_{4}.jpg".format(selectedPhoto.farm, selectedPhoto.server, selectedPhoto.id, selectedPhoto.secret, size)


def getPhotoPageUrl(selectedPhoto, nsid, req):
	photoPage = "http://www.flickr.com/photos/{0}/{1}".format(nsid, selectedPhoto.id)
	util.redirect(req, location=photoPage, permanent=False) 


def getPhoto(apiKey, nsid, photoNumber):

	photoSearchUrl = "http://api.flickr.com/services/rest/?method=flickr.photos.search&api_key={0}&user_id={1}&per_page=1&page={2}".format(apiKey, nsid, photoNumber)
	dom = minidom.parse(urllib.urlopen(photoSearchUrl))

	photoNode = dom.getElementsByTagName("photo")[0] 
	photo = FlickrPhoto()
	photo.id = photoNode.getAttribute("id")
	photo.server = photoNode.getAttribute("server")
	photo.farm = photoNode.getAttribute("farm")
	photo.secret = photoNode.getAttribute("secret")
	return photo

def getNSID(req, apiKey, username):
	cookies = Cookie.get_cookies(req)
	cookieKey = 'nsid_' + username

	if cookies.has_key(cookieKey):
		nsid = cookies[cookieKey].value
	elif not re.match("([0-9]+@N[0-9]+)", username) and not cookieKey in cookies:
		lookupUrl = "http://api.flickr.com/services/rest/?method=flickr.urls.lookupUser&api_key={0}&url=www.flickr.com/photos/{1}".format(apiKey, username)
		dom = minidom.parse(urllib.urlopen(lookupUrl))
		userNode = dom.getElementsByTagName("user")[0]
		nsid = userNode.getAttribute("id")
		c = Cookie.Cookie(cookieKey, nsid)
		c.expires = time.time() + 30 * 24 * 60 * 60
		Cookie.add_cookie(req, c)
	else:
		nsid = username
					
	return nsid



class FlickrPhoto:
	id = ''
	server = ''
	farm = ''
	secret = ''


