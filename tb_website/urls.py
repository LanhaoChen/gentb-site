#
# Copyright (C) 2017 Maha Farhat
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
"""
Global anchor for the website's urls
"""

from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView as Tv

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from apps.versioner.views import Version

urlpatterns = [
    url(r'^$', Tv.as_view(template_name='home.html'), name="home"),
    url(r'^about/$', Tv.as_view(template_name='about.html'), name="about"),
    url(r'^data/$', Tv.as_view(template_name='data.html'), name="data"),
    url(r'^data/info/$', Tv.as_view(template_name='info.html'), name="info"),
    url(r'^terms/$', Tv.as_view(template_name='terms.html'), name="terms"),

    url(r'^gentb-admin/', include(admin.site.urls)),
    url(r'^models/', include('django_spaghetti.urls', namespace='spaghetti')),
    url(r'^user/', include('apps.tb_users.urls', namespace='users')),
    url(r'^auth/', include('apps.tb_users.auth_urls')),

    #url(r'.+', Tv.as_view(template_name='offline.html'), name="offline"),

    url(r'^explore/', include('apps.explore.urls', namespace='explore')),
    url(r'^predict/', include('apps.predict.urls', namespace='predict')),
    url(r'^pipeline/', include('apps.pipeline.urls', namespace='pipeline')),
    url(r'^uploads/', include('apps.uploads.urls', namespace='uploads')),
    url(r'^genes/', include('apps.mutations.urls', namespace='genes')),
    url(r'^maps/', include('apps.maps.urls', namespace='maps')),

    url(r'^version/', Version.as_view(), name='version'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    import debug_toolbar
    urlpatterns.append(url(r'^__debug__/', include(debug_toolbar.urls)))


from .views import Error

for e in ('403','404','500'):
    locals()['handler'+e] = Error.as_error(e)
    urlpatterns.append(url('^error/%s/$' % e, Error.as_error(e)))

