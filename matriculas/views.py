# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from matriculas.models import *

# Create your views here.
@login_required(login_url='/login')
def index(request):
    return render_to_response("inicio.html", RequestContext(request))

def user_login(request):
    context = RequestContext(request)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponse("Tu cuenta no esta habilitada")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponseRedirect('/error_login')
    else:
        return render_to_response('login.html', {}, context)

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')
#---------------------------------------END LOGOUT---------------------------------------------
#---------------------------------------ERROR LOGIN---------------------------------------------
def error_login(request):
    return render_to_response("errorLogin.html", RequestContext(request))

@login_required(login_url='/login')
def alumnos(request):
    alumnos = Alumno.objects.all()
    if request.method == 'POST':
        try:
            dni = request.POST['buscarAlumnoDni']
            alumno = Alumno.objects.get(dni = dni)
            materias = alumno.matricula_set.all()
            return render_to_response("alumnos.html",{'alumno':alumno, 'alumnos':alumnos, 'materias':materias}, RequestContext(request))
        except:
            print error
            return render_to_response("alumnos.html",{'errorAlumno':True, 'alumnos':alumnos}, RequestContext(request))

    return render_to_response("alumnos.html",{'alumnos':alumnos}, RequestContext(request))
@login_required(login_url='/login')
def materias(request):
    materias = Materia.objects.all()
    return render_to_response('materias.html', {"materias":materias},RequestContext(request))
@login_required(login_url='/login')
def profesores(request):
    profesores = Profesor.objects.all()
    if request.method == 'POST':
        try:
            idProf = request.POST['buscarProfesorId']
            profe = Profesor.objects.get(id = idProf)
            #materias = Materias.objects.get()
            return render_to_response("profesor.html",{'profesor':profesor}, RequestContext(request))
        except:
            print error
            return render_to_response("profesor.html",{'errorProfesor':True, 'profesor':profesor}, RequestContext(request))
    return render_to_response('profesores.html', {"profesores":profesores},RequestContext(request))
#---------------------------------------END PROFESORES-----------------------------------------
def mostrarMaterias(request):
    materias = Materia.objects.all()
    return render_to_response('materias.html', {"materias":materias}, context)
