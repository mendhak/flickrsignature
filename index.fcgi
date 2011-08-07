#!/usr/bin/python
import sys, os


sys.path.insert(0, "/home/mendhak/Code/Easy-Flickr-URL")

# Switch to the directory of your project.
os.chdir("/home/mendhak/Code/Easy-Flickr-URL")

# Set the DJANGO_SETTINGS_MODULE environment variable.
os.environ['DJANGO_SETTINGS_MODULE'] = "settings"

from django.core.servers.fastcgi import runfastcgi
runfastcgi(method="threaded", daemonize="false")
