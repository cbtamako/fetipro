from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', 'fetipro.views.index', name='index'),
    url(r'^mypage/$', 'fetipro.views.feties', name='feties'),
    url(r'^users/(?P<username>[^/]+)/$', 'fetipro.views.feties', name='user_feties'),
    url(r'^edit/$', 'fetipro.views.edit_feties', name='edit_feties'),


    url(r'^feties/add/$', 'fetipro.views.add_feti', name='add_feti'),
    url(r'^feties/authorize/$', 'fetipro.views.authorize_feti', name='authorize_feti'),

    url(r'^logout/$', 'fetipro.views.logout', name='logout'),

    url(r'^admin/', include(admin.site.urls)),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url('', include('django.contrib.auth.urls', namespace='auth')),
]

from django.conf import settings
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
