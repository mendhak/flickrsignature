from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
import flickrapi
import time
import datetime
import re

#https://docs.djangoproject.com/en/dev/faq/general/#django-appears-to-be-a-mvc-framework-but-you-call-the-controller-the-view-and-the-view-the-template-how-come-you-don-t-use-the-standard-names
#This 'view' corresponds to the MVC 'controller'.  


apiKey = "a39dfdf51784c76fa3234f88bec38b0e"


def image(request, nsid, num=1, size='b'):

	if not num or not num.isdigit() or int(num) <= 0:
		num = 1
	if not size:
		size = 'b'

	resp = HttpResponse(status=302)
	nsid = getUserNSID(request, resp, apiKey, nsid)
	photo = flickrapi.getPhoto(apiKey, nsid, num)
	destinationUrl = flickrapi.getImageUrl(photo, size)
	resp['Cache-Control'] = "private, max-age=3600"	
	resp['Location'] = destinationUrl
	return resp

def redirect(request, nsid, num):
	if not num or not num.isdigit() or int(num) <= 0:
		num = 1
	resp = HttpResponse(status=302)
	nsid = getUserNSID(request, resp, apiKey, nsid)
	photo = flickrapi.getPhoto(apiKey, nsid, num)
	destinationUrl = flickrapi.getPhotoPageUrl(photo, nsid)
	resp['Location'] = destinationUrl
	return resp

def nsid(request, username):
	resp = HttpResponse()
	nsid = getUserNSID(request, resp, apiKey, username)
	resp.write(nsid)
	return resp

def getUserNSID(request, response, apiKey, username):
	cookies = request.COOKIES
	cookieKey = str('nsid_' + username)

	if cookies.has_key(cookieKey):
		nsid = cookies[cookieKey]
	elif not re.match("([0-9]+@N[0-9]+)", username) and not cookieKey in cookies:
		nsid = flickrapi.getNSID(apiKey, username)
		setCookie(response, cookieKey, nsid)
	else:
		nsid = username
	
	return nsid


def main(request):
	return render_to_response('index.html', {'domain': "localhost:8000"})


def setCookie(response, cookieKey, nsid, expire=None):

	if expire is None:
		max_age = 365*24*60*60  
	else:
		max_age = expire
	expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
	response.set_cookie(key=str(cookieKey), value=nsid, max_age=max_age, expires=expires, domain=None, secure=False)

