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
    if request.user.is_staff:
        return render_to_response("inicio.html", RequestContext(request))
    else:
        profesor = Profesor.objects.get(username = request.user)
        return render_to_response("Profesor/inicio.html", {"profesor":profesor} , RequestContext(request))
        

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
        error = False
        if request.method == 'POST':
            if 'EgresarAlumnoId' in request.POST:
                idAlumno = request.POST['EgresarAlumnoId']
                alumno = Alumno.objects.get(id = idAlumno)
                cambios = egresar(alumno)
                return render_to_response("alumnos.html",{'alumnos':alumnos, 'cambios':cambios}, RequestContext(request))
            idAlumno = request.POST['buscarAlumnoId']
            alumno = Alumno.objects.get(id = idAlumno)
            if 'btnMatricular' in request.POST:
                try:
                    idMatricularId = request.POST['idMatricularId']
                    cursadoId = Cursado.objects.get(id = idMatricularId)
                    print "aca si"
                    cambios = matricular(alumno, cursadoId)
                except:
                    error = True
            materias = alumno.matricula_set.all()
            matriculaSeleccionada = False
            cursadosPosibles = matriculasPosibles(alumno)                
            if 'buscarMatriculaId' in request.POST:
                matriculaSeleccionada = Matricula.objects.get(id = request.POST['buscarMatriculaId'])
            return render_to_response("alumnos.html",{'alumno':alumno, 'alumnos':alumnos, 'materias':materias, 'matriculaSeleccionada': matriculaSeleccionada, 'cursadosPosibles': cursadosPosibles, 'cambios':cambios, 'error':error}, RequestContext(request))
        return render_to_response("alumnos.html",{'alumnos':alumnos}, RequestContext(request))
    else:
        profesor = Profesor.objects.get(username = request.user)
        return render_to_response("Profesor/inicio.html", {"profesor":profesor} , RequestContext(request))

@login_required(login_url='/login')
def egresados(request):
    if request.user.is_staff:
        alumnos = Alumno.objects.all()
        if request.method == 'POST':
            idAlumno = request.POST['buscarAlumnoId']
            alumno = Alumno.objects.get(id = idAlumno)
            return render_to_response("egresados.html",{'alumno':alumno, 'alumnos':alumnos, 'materias':materias}, RequestContext(request))
        return render_to_response("egresados.html",{'alumnos':alumnos}, RequestContext(request))
    else:
        profesor = Profesor.objects.get(username = request.user)
        return render_to_response("Profesor/inicio.html", {"profesor":profesor} , RequestContext(request))


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
    else:
        profesor = Profesor.objects.get(username = request.user)
        return render_to_response("Profesor/inicio.html", {"profesor":profesor} , RequestContext(request))

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
    else:
        profesor = Profesor.objects.get(username = request.user)
        return render_to_response("Profesor/inicio.html", {"profesor":profesor} , RequestContext(request))

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
    else:
        profesor = Profesor.objects.get(username = request.user)
        return render_to_response("Profesor/inicio.html", {"profesor":profesor} , RequestContext(request))

@login_required(login_url='/login')
def p_inicio(request):
    if not request.user.is_staff:
        profesor = Profesor.objects.get(username = request.user)
        return render_to_response("Profesor/inicio.html", {"profesor":profesor} , RequestContext(request))
    else:
        return render_to_response("inicio.html", RequestContext(request))

@login_required(login_url='/login')
def p_asistencia(request):
    if not request.user.is_staff:
        cursados = Cursado.objects.all().filter(profesor = request.user).filter(finalizada = False)
        if request.method == 'POST':
            print request.POST
            idCursado = request.POST.get('idCursado', False)
            fecha = request.POST.get('date', False)
            cursado = Cursado.objects.get(id = idCursado)
            matriculas = cursado.matricula_set.all()
            if not matriculas.count() == 0:
                if 'guardar' in request.POST:
                    for matricula in matriculas:
                        idMatricula = matricula.id
                        if idMatricula in request.POST:
                            print request.POST["idMatricula"]
            return render_to_response("Profesor/asistencia.html", {"cursados":cursados, "matriculas":matriculas} , RequestContext(request))
        return render_to_response("Profesor/asistencia.html", {"cursados":cursados} , RequestContext(request))
    else:
        return render_to_response("inicio.html", RequestContext(request))

@login_required(login_url='/login')
def p_materias(request):
    if not request.user.is_staff:
        cursados = Cursado.objects.filter(profesor = request.user).filter(finalizada = False)
        if request.method == 'POST':
            idCursado = request.POST['idCursado']
            cursado = Cursado.objects.get(id = idCursado)
            matriculas = cursado.matricula_set.all()
            if 'notaCalificacion' in request.POST:
                calificacion = request.POST['notaCalificacion']
                idMatricula = request.POST['idMatricula']
                matricula = Matricula.objects.get(id = idMatricula)
                observacion = request.POST['notaObservacion']
                nota = crearNota(calificacion, matricula, observacion)
            elif 'finalizarCursado' in request.POST:
                cursado.finalizada = True
                cursado.save()
                return render_to_response("Profesor/materias.html", {"cursados":cursados} , RequestContext(request))
            return render_to_response("Profesor/materias.html", {"cursados":cursados, "matriculas":matriculas, "CursadoBuscado":cursado} , RequestContext(request))
        return render_to_response("Profesor/materias.html", {"cursados":cursados} , RequestContext(request))
    else:
        return render_to_response("inicio.html", RequestContext(request))

@login_required(login_url='/login')
def p_examen(request):
    if not request.user.is_staff:
        cursados = Cursado.objects.all().filter(profesor = request.user)
        if request.method == 'POST':
            if 'guardar' in request.POST:
                idCursado = request.POST['idCursado']
                cursado = Cursado.objects.get(id = idCursado)
            else:
                idMatricula = request.POST['matriculaId']
                matricula = Matricula.objects.get(id = idMatricula)
                cursado = matricula.cursado
                turnoId = request.POST['turnoId']
                turno = TurnoDeExamen.objects.get(id = turnoId)
                nota = request.POST['nota']
                crearExamen(nota, matricula, turno)
            matriculas = cursado.matricula_set.all()
            turnos = TurnoDeExamen.objects.filter(cursado = cursado)
            turnosEsMenorAUnMes = []
            for i in range(turnos.count()):
                if (turnos[i].esMenorAUnMes() == True):
                    turnosEsMenorAUnMes.append(turnos[i])
            return render_to_response("Profesor/examen.html", {"cursados":cursados, "matriculas":matriculas, "turnos":turnosEsMenorAUnMes} , RequestContext(request))
        return render_to_response("Profesor/examen.html", {"cursados":cursados} , RequestContext(request))
    else:
        return render_to_response("inicio.html", RequestContext(request))

def sePuedeMatricular(alumno, cursado):
    correlativas = cursado.materia.correlativasCursado.all()
    matriculas = alumno.matricula_set.all()
    materiasAprobadas = []
    materia = cursado.materia
    anio = int(time.strftime('%Y'))
    cursadosDelAlumno = []
    for k in range(matriculas.count()):
        if (matriculas[k].cursado.id == cursado.id):
            return False
        cursadosDelAlumno.append(matriculas[k].cursado)
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
        matriculas = alumno.matricula_set.all()
        cursadosDelAlumno = []
        for i in range(matriculas.count()):
            if (matriculas[i].cursado.id == cursado.id):
                return False
        crearCursado = Matricula.objects.create(alumno = alumno, cursado = cursado)
        crearCursado.save()
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

def tomarAsistencia(matricula, fecha, boolean):
    try:
        asistencia = Asistencia.objects.create(fecha = fecha, vino = boolean, matricula = matricula)
        asistencia.save()
        return True
    except:
        return False

def crearExamen(nota, matricula, turno):
    examen = ExamenFinal.objects.create(nota = nota, matricula = matricula, turno = turno)
    examen.save()

def crearNota(calificacion, matricula, observacion):
    try:
        fecha = time.strftime('%Y-%m-%d')
        nota = Nota.objects.create(calificacion = calificacion, matricula = matricula, observacion = observacion, fecha = fecha)
        nota.save()
        return True
    except:
        return False