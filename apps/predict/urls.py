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
Predict app's urls
"""

from django.conf.urls import include, url

from .views import Datasets, UploadChoices, UploadView, DatasetView, AddNote

def url_tree(regex, *urls):
    class UrlTwig(object):
        urlpatterns = urls
    return url(regex, include(UrlTwig))

urlpatterns = [
  url(r'^$', Datasets.as_view(), name="view_my_datasets"),
  url_tree(r'^upload/',
    url(r'^$', UploadChoices.as_view(), name="upload"),
    url(r'^(?P<type>[\w-]+)/$', UploadView.as_view(), name="upload"),
  ),
  url_tree(r'^(?P<slug>\w{32})/',
    url(r'^$',          DatasetView.as_view(),   name="view_single_dataset"),
    url(r'^note/$',     AddNote.as_view(),       name="add_note"),
  ),
]

