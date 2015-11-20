from django.conf.urls import patterns, include, url
from config import settings
from . import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='inicio'),
    url(r'^login/', views.user_login, name='login'),
    url(r'^logoutsito/', views.user_logout, name='logout'),
    url(r'^alumnos/', views.alumnos, name='alumnos'),
    url(r'^egresados/', views.egresados, name='egresados'),
    url(r'^profesores/', views.profesores, name='profesores'),
    url(r'^materias/', views.materias, name='materias'),
    url(r'^error_login/', views.error_login, name='error_login'),
    url(r'^turnos_de_examen/', views.turnos_de_examen, name='turnos_de_examen'),
	url(r'^Profesor/inicio/', views.p_inicio, name='p_inicio'),
	url(r'^Profesor/asistencia/', views.p_asistencia, name='p_asistencia'),
	url(r'^Profesor/materias/', views.p_materias, name='p_materias'),
    url(r'^Profesor/examen/', views.p_examen, name='p_examen'),
)
