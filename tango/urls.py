from django.conf.urls import url
from tango import views

urlpatterns = [
    # url(r'^$',views.index,name='index'),
    url(r'^$',views.IndexView.as_view(),name='index'),
    url(r'^about/',views.about,name='about'),
    url(r'^category/(?P<slug>[\w-]+)/$',views.ShowCategoryView.as_view(),name='show_category'),
    url(r'^register/',views.UserRegisterView.as_view(),name='register'),
]