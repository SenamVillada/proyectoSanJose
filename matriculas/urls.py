from django.conf.urls import patterns, include, url
from config import settings

urlpatterns = patterns('',

    url(r'^$', 'config.views.home', name='home'),
    url(r'^login/$', 'config.views.login', name='login'),
    url(r'^logout/$', 'config.views.logout', name='logout'),
    url(r'^alumnos/$', 'config.views.alumnos', name='alumnos'),
    url(r'^profesores/$', 'config.views.profesores', name='profesores'),
    url(r'^profesores/(?P<id_profesor>\d+)/$', 'config.views.profesores', name='profesores'),
    url(r'^materias/$', 'config.views.materias', name='materias'),
    url(r'^profes/$', 'config.views.profes', name='profes'),
    url(r'^profes/materias$', 'config.views.profes', name='profes'),
)
