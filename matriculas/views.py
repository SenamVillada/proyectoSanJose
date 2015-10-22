# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from matriculas.models import *
import time

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

def error_login(request):
    return render_to_response("errorLogin.html", RequestContext(request))

@login_required(login_url='/login')
def alumnos(request):
    alumnos = Alumno.objects.all()
    if request.method == 'POST':
        print request.POST
        idAlumno = request.POST['buscarAlumnoId']
        alumno = Alumno.objects.get(id = idAlumno)
        materias = alumno.matricula_set.all()
        matriculaSeleccionada = False
        if 'buscarMatriculaId' in request.POST:
            matriculaSeleccionada = Matricula.objects.get(id = request.POST['buscarMatriculaId'])
        return render_to_response("alumnos.html",{'alumno':alumno, 'alumnos':alumnos, 'materias':materias, 'matriculaSeleccionada': matriculaSeleccionada}, RequestContext(request))
    return render_to_response("alumnos.html",{'alumnos':alumnos}, RequestContext(request))

@login_required(login_url='/login')
def egresados(request):
    alumnos = Alumno.objects.all()
    if request.method == 'POST':
        idAlumno = request.POST['buscarAlumnoId']
        alumno = Alumno.objects.get(id = idAlumno)
        return render_to_response("egresados.html",{'alumno':alumno, 'alumnos':alumnos, 'materias':materias}, RequestContext(request))
    return render_to_response("egresados.html",{'alumnos':alumnos}, RequestContext(request))


@login_required(login_url='/login')
def materias(request):
    materiasTotal = Materia.objects.all()
    if request.method == 'POST':
        try:
            idmateria = request.POST['buscarProfesorId']
            materia = Materia.objects.get(id = idmateria)
            horarios = materia.horario_set.all()
            anio = int(time.strftime('%Y'))
            matriculasAsistentes = materia.matricula_set.all().filter(anio=anio)
            return render_to_response('materias.html', {"materias":materiasTotal, "materiaBuscada":materia, "horarios":horarios, "alumnosAsistentes":matriculasAsistentes},RequestContext(request))
        except:
            return render_to_response('materias.html', {"materias":materiasTotal},RequestContext(request))
    return render_to_response('materias.html', {"materias":materiasTotal},RequestContext(request))

@login_required(login_url='/login')
def profesores(request):
    profesores = Profesor.objects.all()
    if request.method == 'POST':
        try:
            idProf = request.POST['buscarProfesorId']
            profesor = Profesor.objects.get(id = int(idProf))
            materias = profesor.materia_set.all()
            horarios = []
            for i in range(materias.__len__()):
                materiasEnI = materias[i].horario_set.all()
                for j in range(materiasEnI.count()):
                    horarios.append(materiasEnI[j])
            licencias = profesor.licencia_set.all()
            return render_to_response("profesores.html",{"profesor":profesor,"profesores":profesores, "horarios":horarios, "licencias":licencias}, RequestContext(request))
        except:
            return render_to_response("profesores.html",{'errorProfesor':True}, RequestContext(request))
    return render_to_response('profesores.html', {"profesores":profesores},RequestContext(request))