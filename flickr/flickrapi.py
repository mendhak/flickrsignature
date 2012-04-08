import re
import urllib
from xml.dom import minidom


def getPhoto(apiKey, nsid, photoNumber, popular):

	popular = popular.lower()

	if popular == 'p':
		popular = 'interestingness-desc'
	else:
		popular = 'date-posted-desc'

	photoSearchUrl = "http://api.flickr.com/services/rest/?method=flickr.photos.search&api_key={0}&user_id={1}&per_page=1&page={2}&sort={3}".format(apiKey, nsid, photoNumber, popular)
	dom = minidom.parse(urllib.urlopen(photoSearchUrl))

	photoNode = dom.getElementsByTagName("photo")[0] 
	photo = FlickrPhoto()
	photo.id = photoNode.getAttribute("id")
	photo.server = photoNode.getAttribute("server")
	photo.farm = photoNode.getAttribute("farm")
	photo.secret = photoNode.getAttribute("secret")
	return photo


def getPhotoBySearch(apiKey, nsid, searchTag, photoNumber):
	photoSearchUrl = "http://api.flickr.com/services/rest/?method=flickr.photos.search&api_key={0}&user_id={1}&per_page=1&page={2}&tags={3}".format(apiKey, nsid, photoNumber, searchTag)
	
	dom = minidom.parse(urllib.urlopen(photoSearchUrl))

	photoNode = dom.getElementsByTagName("photo")[0]
	photo = FlickrPhoto()
	photo.id = photoNode.getAttribute("id")
	photo.server = photoNode.getAttribute("server")
	photo.farm = photoNode.getAttribute("farm")
	photo.secret = photoNode.getAttribute("secret")
	return photo


def getNSID(apiKey, username):

	if not 'http://' in username:
		username = 'http://www.flickr.com/photos/' + username

	if not re.match("([0-9]+@N[0-9]+)", username):
		lookupUrl = "http://api.flickr.com/services/rest/?method=flickr.urls.lookupUser&api_key={0}&url={1}".format(apiKey, username)
		dom = minidom.parse(urllib.urlopen(lookupUrl))
		userNode = dom.getElementsByTagName("user")[0]
		nsid = userNode.getAttribute("id")
	else:
		nsid = username
					
	return nsid



def getPhotoPageUrl(selectedPhoto, nsid):
	if nsid:
		return "http://www.flickr.com/photos/{0}/{1}".format(nsid, selectedPhoto.id)
	else:
		return "http://www.flickr.com/photo.gne?id=" + selectedPhoto.id




def getImageUrl(selectedPhoto, size):

	size = size.lower()
	sizePrefix = '_'


	'''
	s	small square 75x75 *
	q	large square 150x150 *
	t	thumbnail, 100 on longest side *
	m	small, 240 on longest side *
	n	small, 320 on longest side *
	-	medium, 500 on longest side *
	z	medium 640, 640 on longest side *
	c	medium 800, 800 on longest side *
	b	large, 1024 on longest side *
	'''

	if size == 'small' or size == '240':
		size = 'm'
	if size == 'small320' or size == '320':
		size = 'n'
	elif size == 'square' or size == '75':
		size = 's'
	elif size == 'largesquare' or size == '150':
		size = 'q'
	elif size == 'thumb' or size == 'thumbnail' or size == 'tiny' or size == '100':
		size = 't'
	elif size == 'medium640' or size == '640':
		size = 'z'
	elif size == 'medium800' or size == '800':
		size = 'c'
	elif size == 'large' or size == 'big' or size == '1024':
		size = 'b'
	elif size == '' or size == 'medium' or size == 'med' or size == 'x' or size == '500':
		sizePrefix =  ''
		size = ''

	size = sizePrefix + size

	return "http://farm{0}.static.flickr.com/{1}/{2}_{3}{4}.jpg".format(selectedPhoto.farm, selectedPhoto.server, selectedPhoto.id, selectedPhoto.secret, size)


class FlickrPhoto:
	id = ''
	server = ''
	farm = ''
	secret = ''
