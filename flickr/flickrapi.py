import re
import urllib
from xml.dom import minidom


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





def getNSID(apiKey, username):
	if not re.match("([0-9]+@N[0-9]+)", username):
		lookupUrl = "http://api.flickr.com/services/rest/?method=flickr.urls.lookupUser&api_key={0}&url=www.flickr.com/photos/{1}".format(apiKey, username)
		dom = minidom.parse(urllib.urlopen(lookupUrl))
		userNode = dom.getElementsByTagName("user")[0]
		nsid = userNode.getAttribute("id")
	else:
		nsid = username
					
	return nsid



def getPhotoPageUrl(selectedPhoto, nsid):
	return "http://www.flickr.com/photos/{0}/{1}".format(nsid, selectedPhoto.id)
	



def getImageUrl(selectedPhoto, size):

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


class FlickrPhoto:
	id = ''
	server = ''
	farm = ''
	secret = ''
