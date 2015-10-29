# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from matriculas.models import *
from datetime import datetime
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
                if user.is_staff:
                    return HttpResponseRedirect('/')
                else:
                    return HttpResponseRedirect('/Profesor/inicio')
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
    if request.user.is_staff:
        alumnos = Alumno.objects.all()
        cambios = False
        if request.method == 'POST':
            if 'EgresarAlumnoId' in request.POST:
                idAlumno = request.POST['EgresarAlumnoId']
                alumno = Alumno.objects.get(id = idAlumno)
                cambios = egresar(alumno)
                return render_to_response("alumnos.html",{'alumnos':alumnos, 'cambios':cambios}, RequestContext(request))
            idAlumno = request.POST['buscarAlumnoId']
            alumno = Alumno.objects.get(id = idAlumno)
            if 'btnMatricular' in request.POST:
                idMatricularId = request.POST['idMatricularId']
                cursadoId = Cursado.objects.get(id = idMatricularId)                
                cambios = matricular(alumno, cursadoId)
            materias = alumno.matricula_set.all()
            matriculaSeleccionada = False
            cursadosPosibles = matriculasPosibles(alumno)                
            if 'buscarMatriculaId' in request.POST:
                matriculaSeleccionada = Matricula.objects.get(id = request.POST['buscarMatriculaId'])
            return render_to_response("alumnos.html",{'alumno':alumno, 'alumnos':alumnos, 'materias':materias, 'matriculaSeleccionada': matriculaSeleccionada, 'cursadosPosibles': cursadosPosibles, 'cambios':cambios}, RequestContext(request))
        return render_to_response("alumnos.html",{'alumnos':alumnos}, RequestContext(request))

@login_required(login_url='/login')
def egresados(request):
    if request.user.is_staff:
        alumnos = Alumno.objects.all()
        if request.method == 'POST':
            idAlumno = request.POST['buscarAlumnoId']
            alumno = Alumno.objects.get(id = idAlumno)
            return render_to_response("egresados.html",{'alumno':alumno, 'alumnos':alumnos, 'materias':materias}, RequestContext(request))
        return render_to_response("egresados.html",{'alumnos':alumnos}, RequestContext(request))


@login_required(login_url='/login')
def materias(request):
    if request.user.is_staff:
        anio = int(time.strftime('%Y'))
        materiasTotal = Cursado.objects.all().filter(anio=anio)
        if request.method == 'POST':
            idmateria = request.POST['buscarProfesorId']
            materia = Materia.objects.get(id = idmateria)
            cursado = Cursado.objects.get(materia = materia)
            horarios = cursado.horario_set.all()
            matriculasAsistentes = cursado.matricula_set.all()
            return render_to_response('materias.html', {"materias":materiasTotal, "materiaBuscada":cursado, "horarios":horarios, "alumnosAsistentes":matriculasAsistentes},RequestContext(request))
        return render_to_response('materias.html', {"materias":materiasTotal},RequestContext(request))

@login_required(login_url='/login')
def profesores(request):
    if request.user.is_staff:
        profesores = Profesor.objects.all()
        if request.method == 'POST':
            idProf = request.POST['buscarProfesorId']
            profesor = Profesor.objects.get(id = int(idProf))
            cursados = profesor.cursado_set.all()
            horarios = []
            for i in range(cursados.count()):
                materiasEnI = cursados[i].horario_set.all()
                for j in range(materiasEnI.count()):
                    horarios.append(materiasEnI[j])
            licencias = profesor.licencia_set.all()
            cargos = profesor.cargo_set.all()
            return render_to_response("profesores.html",{"profesor":profesor,"profesores":profesores, "horarios":horarios, "licencias":licencias, 'cargos':cargos}, RequestContext(request))
        return render_to_response('profesores.html', {"profesores":profesores},RequestContext(request))

@login_required(login_url='/login')
def turnos_de_examen(request):
    if request.user.is_staff:
        turnos = TurnoDeExamen.objects.all()
        fechaHoy = time.strftime('%y-%m-%d')
        fechaHoy = datetime.strptime(fechaHoy, '%y-%m-%d')
        fechaHoy = datetime.date(fechaHoy)
        turnosNoPasaron = []
        for i in range(turnos.count()):
            if (turnos[i].fecha > fechaHoy):
                turnosNoPasaron.append(turnos[i])
        return render_to_response("turnos_examen.html", {"turnos":turnosNoPasaron} , RequestContext(request))

@login_required(login_url='/login')
def p_inicio(request):
    if not request.user.is_staff:
        profesor = Profesor.objects.get(username = request.user)
        return render_to_response("Profesor/inicio.html", {"profesor":profesor} , RequestContext(request))

@login_required(login_url='/login')
def p_asistencia(request):
    if not request.user.is_staff:
        return render_to_response("Profesor/asistencia.html", RequestContext(request))

@login_required(login_url='/login')
def p_materias(request):
    if not request.user.is_staff:
        return render_to_response("Profesor/materias.html", RequestContext(request))

def sePuedeMatricular(alumno, cursado):
    correlativas = cursado.materia.correlativasCursado.all()
    matriculas = alumno.matricula_set.all()
    materiasAprobadas = []
    materia = cursado.materia
    anio = int(time.strftime('%Y'))
    cursadosDelAlumno = []
    for k in range(matriculas.count()):
        cursadosDelAlumno.append(matriculas[k].cursado)
    for m in range(cursadosDelAlumno.count()):
        if (cursado.id == cursadosDelAlumno[m].id):
            return False
    for i in range(matriculas.count()):
        if (matriculas[i].cursado.materia == materia):
            if matriculas[i].estaAprobada():
                return False
            elif (matriculas[i].cursado.anio < anio):
                return False
        for j in range(matriculas.count()):
            if matriculas[j].estaAprobada():
                materiasAprobadas.append(matriculas[j].cursado.materia)
        for h in range(correlativas.count()):
            if not correlativas[h] in materiasAprobadas:
                return False
        return True

def matriculasPosibles(alumno):
    cursados = Cursado.objects.filter(finalizada = False)
    cursadosPosibles = []
    for i in range(cursados.count()):
        if (sePuedeMatricular(alumno, cursados[i])):
            cursadosPosibles.append(cursados[i])
    return cursadosPosibles

def matricular(alumno, cursado):
    try:
        crearCursado = Matricula.objects.create(alumno = alumno, cursado = cursadoId)
        return True
    except:
        return False

def egresar(alumno):
    try:
        anio = int(time.strftime('%Y'))
        alumno.anioEgreso = anio
        alumno.save()
        return True
    except:
        return False