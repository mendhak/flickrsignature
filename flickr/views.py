from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
import flickrapi
import datetime
import re


#https://docs.djangoproject.com/en/dev/faq/general/#django-appears-to-be-a-mvc-framework-but-you-call-the-controller-the-view-and-the-view-the-template-how-come-you-don-t-use-the-standard-names
#This 'view' corresponds to the MVC 'controller'.  


apiKey = "a39dfdf51784c76fa3234f88bec38b0e"


def image(request, nsid, num=1, size='', popular=''):

	if not num or not num.isdigit() or int(num) <= 0:
		num = 1
	if not size:
		size = 's'
	if not popular :
		popular = ''




	resp = HttpResponse(status=302)
	nsid = getUserNSID(request, resp, apiKey, nsid)
	photo = flickrapi.getPhoto(apiKey, nsid, num, popular)
	destinationUrl = flickrapi.getImageUrl(photo, size)
	resp['Cache-Control'] = "private, max-age=3600"	
	resp['Location'] = destinationUrl
	return resp

def searchImage(request, tags='', num=1, size='', nsid='' ):
	if not num or not num.isdigit() or int(num) <= 0:
		num = 1
	if not size:
		size = 's'

	resp = HttpResponse(status=302)
	nsid = getUserNSID(request, resp, apiKey, nsid)
	photo = flickrapi.getPhotoBySearch(apiKey, nsid, tags, num)
	destinationUrl = flickrapi.getImageUrl(photo, size)
	resp['Cache-Control'] = "private, max-age=3600"
	resp['Location'] = destinationUrl
	return resp

def searchRedirect(request, tags='', num=1, nsid=''):
	if not num or not num.isdigit() or int(num) <= 0:
		num = 1
	resp = HttpResponse(status=302)
	nsid = getUserNSID(request, resp, apiKey, nsid)
	photo = flickrapi.getPhotoBySearch(apiKey, nsid, tags, num)
	destinationUrl = flickrapi.getPhotoPageUrl(photo, nsid)
	resp['Location'] = destinationUrl
	return resp


def redirect(request, nsid, num, popular):
	if not num or not num.isdigit() or int(num) <= 0:
		num = 1
	if not popular:
		popular = ''

	resp = HttpResponse(status=302)
	nsid = getUserNSID(request, resp, apiKey, nsid)
	photo = flickrapi.getPhoto(apiKey, nsid, num, popular)
	destinationUrl = flickrapi.getPhotoPageUrl(photo, nsid)
	resp['Location'] = destinationUrl
	return resp

def nsid(request, username):
	resp = HttpResponse()
	nsid = getUserNSID(request, resp, apiKey, username)
	resp.write(nsid)
	return resp

def getUserNSID(request, response, apiKey, username):

	if username is None:
		return ''

	if 'http://' in username or 'www.' in username:
		userRegex = re.compile(r'photos/(?P<username>[^/]+)')
		m = userRegex.search(username)
		username = m.group('username')

	cookies = request.COOKIES
	cookieKey = str('nsid_' + username)
	nsidRegex = re.compile("([0-9]+@N[0-9]+)")

	if cookies.has_key(cookieKey):
		nsid = cookies[cookieKey]
	elif not nsidRegex.match(username) and not cookieKey in cookies:
		nsid = flickrapi.getNSID(apiKey, username)
		setCookie(response, cookieKey, nsid)
	else:
		nsid = username
	
	return nsid


def main(request):
	return render_to_response('sig.html', {'domain': request.get_host()}, context_instance=RequestContext(request))


def setCookie(response, cookieKey, nsid, expire=None):

	if expire is None:
		max_age = 365*24*60*60  
	else:
		max_age = expire
	expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
	response.set_cookie(key=str(cookieKey), value=nsid, max_age=max_age, expires=expires, domain=None, secure=False)

