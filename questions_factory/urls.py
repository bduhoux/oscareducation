from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    url(r'^generator/(?P<lesson_id>\d+)/(?P<skill_id>\d+)/(?P<test_id>\d+)/$', views.generator, name='generator'),
    url(r'^generator/(?P<lesson_id>\d+)/(?P<skill_id>\d+)/(?P<test_id>\d+)/submit/$', views.generator_submit, name='generator_submit')
]
