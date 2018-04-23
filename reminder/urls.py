from django.conf.urls import url, include
from .views import *

urlpatterns = [
    url(r'^$', ChapterListViewView.as_view(), name='chapter_list'),
    url(r'^(?P<slug>\d+)/$', ChapterDetailView.as_view(), name='chapter_detail'),
]
