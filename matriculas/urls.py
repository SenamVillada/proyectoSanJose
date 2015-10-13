from django.conf.urls import patterns, include, url
from config import settings
from . import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='inicio'),
    url(r'^login/', views.user_login, name='login'),
    url(r'^logoutsito/', views.user_logout, name='logout'),
    url(r'^alumnos/', views.alumnos, name='alumnos'),
    url(r'^profesores/', views.profesores, name='profesores'),
    url(r'^materias/', views.materias, name='materias'),
    url(r'^error_login/', views.error_login, name='error_login'),               
    #url(r'^$', 'config.views.home', name='home'),
    #url(r'^login/$', 'config.views.login', name='login'),
    #url(r'^alumnos/$', 'config.views.alumnos', name='alumnos'),
    #url(r'^profesores/$', 'config.views.profesores', name='profesores'),
    #url(r'^profesores/(?P<id_profesor>\d+)/$', 'config.views.profesores', name='profesores'),
    #url(r'^materias/$', 'config.views.materias', name='materias'),
    #url(r'^profes/$', 'config.views.profes', name='profes'),
    #url(r'^profes/materias$', 'config.views.profes', name='profes'),
)