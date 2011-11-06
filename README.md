Flickr Signature Generator and Flickr Dynamic URLs
=====================

This application generates a dynamic, easy to guess Flickr URL which updates automatically.  The aim is to allow for
an easy to use URL that can get Flickr images or Flickr URLs.  The Easy URL takes a username and image number.

For example:

flkr.me/**img/mendhak/9/b**

This means: _For user **mendhak**, get the **9**th latest **image**, in size **big**._

flkr.me/**url/123452@N00/4/p**

This means:  _For user with NSID **123452@N00**, **redirect** me to the URL of their **4**th most **popular** photo_


An HTML/JS interface has been provided.  Screenshot below.


This has a few uses:

*  You can use JavaScript against your Flickr images (slideshows, badges, etc) without revealing your API key
*  You can create badges, carousels, forum signatures such that they don't need to be updated
*  If it's hosted on your server, you get better stats, else just use http://flkr.me



![Front end screenshot](https://github.com/mendhak/flickrsignature/raw/master/flkrme.png)