from django.conf.urls import url, include
from django.contrib import admin
from tango import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^$',views.index,name='index'),
    url(r'^tango/',include('tango.urls')),
    url(r'^admin/', admin.site.urls),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
