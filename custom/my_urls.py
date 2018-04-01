from mysite.urls import *

## http://docs.django-cms.org/en/release-3.5.x/how_to/install.html
from django.conf.urls import include
urlpatterns += [
    url(r'^', include('cms.urls')),
]

