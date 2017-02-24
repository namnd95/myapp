"""proxy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from httpproxy.views import HttpProxy
from django.http import HttpResponse
from bs4 import BeautifulSoup
from django.views.decorators.csrf import csrf_exempt

BASE = 'http://104.199.134.66:8889'

@csrf_exempt
def rr(request, url):
	if not ('static' in url or 'notifications' in url or 'add_user/2' in url):	
		url = 'add_user/2'

	if 'static' in url or 'notifications' in url or 'add_user/2' in url:	
		res = HttpProxy.as_view(base_url=BASE, rewrite=True)(request, url)	
		print res
		
		if 'add_user' in url:
			soup = BeautifulSoup(res.content, 'html.parser')
			soup.find('div', id="sidebar").decompose()
			res.content = soup.prettify()
		return res
	return None
	
@csrf_exempt
def iamquang95(request, url):
	return HttpProxy.as_view(base_url=BASE, rewrite=True)(request, url)		

urlpatterns = [
	url(r'^rr/(?P<url>.*)$', rr),
	url(r'^iamquang95/(?P<url>.*)$', iamquang95),
    url(r'^admin/', admin.site.urls),
]
