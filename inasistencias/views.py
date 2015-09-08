from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, render, redirect
from django.template import RequestContext
from django.template.defaulttags import NowNode
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.decorators import login_required
from django import forms


from .models import Document
from .forms import DocumentForm

from inasistencias.templatetags.faltas import formatear_fecha
from inasistencias.models import Curso, Preceptor, Alumno, Curso, Inasistencia, Observacion, Amonestacion

import os

def archivo(request):
    return descargar_archivo('lala.ods', 'application/ods')

@login_required(login_url="/loguearse")
def home(request):
    context = RequestContext(request)

    if request.method == 'POST':
	print request.POST

    # Si es Administrador
    if request.user.is_staff:

	if request.method == 'POST':
	    print request.POST
	    
	    if 'infoCurso' in request.POST:
		curso = request.POST['cursos']
		print Curso.objects.filter(id=curso)
		
		return HttpResponseRedirect(reverse('inasistencias:info', args=(int(curso), ) ))
	      
	    elif 'nuevoCurso' in request.POST:
		return HttpResponseRedirect('admin/inasistencias/curso/add/')
		
	    elif 'verPreceptor' in request.POST:
		preceptor = request.POST['preceptores']
		return HttpResponseRedirect('admin/inasistencias/preceptor/' + preceptor + '/')
		
	    elif 'nuevoPreceptor' in request.POST:
		return HttpResponseRedirect('admin/inasistencias/preceptor/add/')
	      
	return render_to_response('admin/administrador.html', {'usuario': request.user, 'cursos': Curso.objects.all(), 'preceptores': Preceptor.objects.all()}, context)
	
    
    # Si es Preceptor
    elif es_preceptor(request.user):
	
	if request.method == 'POST':
	    form = DocumentForm(request.POST, request.FILES)
	    
	    if form.is_valid():
		newdoc = Document(docfile = request.FILES['docfile'])
		newdoc.save()
		
		# Redirect to the document list after POST
		return HttpResponseRedirect('/admin')
	else:
	    form = DocumentForm() # A empty, unbound form
	
	# Load documents for the list page
	documents = Document.objects.all()
	print documents
	
	return render_to_response('preceptor/preceptor.html', {'usuario': request.user, 'cursos': Curso.objects.all().filter(preceptor=request.user), 'dcuments': documents, 'form': form}, context)
    
    # Si es Alumno
    elif es_alumno(request.user):
	return render_to_response('alumno/alumno.html', {'usuario': request.user, 'alumno': Alumno.objects.get(pk=request.user.pk) }, context)
    
    # Sino
    else:
	return HttpResponse('ERROR')

def loguearse(request):
    context = RequestContext(request)
	
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
	# Usuario y contrasena
	username = request.POST['username']
	password = request.POST['password']

	user = authenticate(username=username, password=password)

	if user:
	    # Is the account active? It could have been disabled.
	    if user.is_active:
		# If the account is valid and active, we can log the user in.
		# We'll send the user back to the homepage.
		login(request, user)

		return redirect('/')

	    else:
		# An inactive account was used - no logging in!
		return HttpResponse("ERROR: cuenta inactiva.")
	else:
	    # Bad login details were provided. So we can't log the user in.
	    print "Invalid login details: {0}, {1}".format(username, password)
	    return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
	# No context variables to pass to the template system, hence the
	# blank dictionary object...
	
	return render_to_response('login.html', context)

def desloguearse(request):
    logout(request)
    
    return redirect('/loguearse')

@login_required(login_url="/loguearse")
def curso(request, id_curso):
    fecha = NowNode("SHORT_DATE_FORMAT").render(None)
    alumnos = Alumno.objects.all().filter(curso_id=id_curso)
    cambios = False
    
    if request.method == 'POST':
	
	if request.POST.get('cargar'):
	    fecha = request.POST['fecha']
	
	if request.POST.get('guardar'):
	    fecha = request.POST['fecha']
	    preceptor = request.POST['preceptor']
	    
	    registrar_faltas(fecha, alumnos, request.POST, preceptor)
	    cambios = True
		
    
    # Si es preceptor
    if es_preceptor(request.user):
	return render_to_response('preceptor/curso.html', {'usuario': request.user, 'cambios':cambios, 'alumnos': alumnos, 'curso': Curso.objects.get(id=id_curso), 'dia': fecha}, RequestContext(request))

    # Sino
    else:
	return HttpResponse('Necesitas estar logueado como preceptor para ver esto...')

@login_required(login_url="/loguearse")
def alumno(request, id_alumno):
    faltas = Inasistencia.objects.all().filter(alumno_id=id_alumno)
    cambios = False
    
    # Si es preceptor
    if es_preceptor(request.user):
      
	# Si se ha recibido una peticion "POST"
        if request.method == 'POST':
	    print request.POST
	    
	    # Si es una peticion de "Guardar faltas"    
            if 'guardarFaltas' in request.POST:
		guardarFaltas(faltas, request.POST)
		cambios = True

            # Si es una peticion de "Crear Observacion"    
            if request.POST.get('motivoObservacion'):
                fecha = request.POST.get('fechaObservacion')
                fecha2 = formatear_fecha(fecha)
                motivo = request.POST['motivoObservacion']
                alumno = Alumno.objects.get(id=id_alumno)
                preceptor = request.POST['preceptor']
                preceptor = Preceptor.objects.get(id=preceptor)
                observar(alumno, fecha2, motivo, preceptor)
                cambios = True

            # Si es una peticion de "Crear Amonestacion"
            if request.POST.get('motivoAmonestacion'):
		print request.POST
                fecha = request.POST.get('fechaAmonestacion')
                fecha2 = formatear_fecha(fecha)
                motivo = request.POST['motivoAmonestacion']
                cantidad = request.POST['cantAmonestacion']
                alumno = Alumno.objects.get(id=id_alumno)
                preceptor = request.POST['preceptor']
                preceptor = Preceptor.objects.get(id=preceptor)
                amonestar(alumno, fecha2, motivo, cantidad, preceptor)
                cambios = True

            # Si es una peticion de "Reincorporar"
            if request.POST.get('alumnoReincorporacion'):
                alumno = Alumno.objects.get(id=id_alumno)
                reincorporar(alumno)
                cambios = True
	
	return render_to_response('preceptor/alumno.html', {'usuario': request.user, 'cambios': cambios, 'alumno': Alumno.objects.get(id=id_alumno)}, RequestContext(request))

    # Sino
    else:
	return HttpResponse('Necesitas estar logueado como preceptor para ver esto...')

@login_required(login_url="/loguearse")
def info(request, id_curso):
    print request.POST
    # Si es preceptor o administrador
    if es_preceptor(request.user) or request.user.is_staff:
	return render_to_response('preceptor/info.html', {'usuario': request.user, 'curso': Curso.objects.get(id=id_curso)}, RequestContext(request))

    # Sino
    else:
	return HttpResponse('Necesitas estar logueado como preceptor para ver esto...')


# Devuelve true si es preceptor
def es_preceptor(usuario):
    try:
	Preceptor.objects.get(pk=usuario.pk)
	return True
    except:
	return False

# Devuelve true si es alumno
def es_alumno(usuario):
    try:
	Alumno.objects.get(pk=usuario.pk)
	return True
    except:
	return False

# Leva a cabo el registro de faltas de una lista de alumnos
def registrar_faltas(fecha, alumnos, post, preceptor):
    fecha = formatear_fecha(fecha)
    dic = {
      'P': 0,
      '1/2': 0.5,
      '1/4': 0.25,
      '3/4': 0.75,
      'A': 1,
    }

    for al in alumnos:
	falta = Inasistencia.objects.filter(alumno=al).filter(fecha=fecha)
	# Tipo de inasistencia
	tipo = post[str(al.id)]
	
	# Si existe una falta de ese alumno en esa fecha
	if falta:
	    # Si no coincide
	    if dic[tipo] != falta[0].tipo:
		falta[0].tipo = dic[tipo]
		falta[0].save()
	
	# Si no existe una falta de ese alumno en esa fecha se crea
	else:
	    fal = Inasistencia(tipo=dic[tipo], alumno=al, preceptor=Preceptor.objects.get(username=preceptor), fecha=fecha)
	    fal.save()

# Guarda la justificacion de las faltas
def guardarFaltas(faltas, post):
    for f in faltas:
	jus = post[str(f.id)]
	
	if jus == 'False':
	    f.justificar(False)
	elif jus == 'True':
	    f.justificar(True)
	    

# Agrega una observacion al alumno
def observar(alumno, fecha, motivo, id_preceptor):
    observacion = Observacion(descripcion=motivo, alumno=alumno, fecha=fecha, preceptor=id_preceptor)
    observacion.save()

# Agrega una amonestacion al alumno
def amonestar(alumno, fecha, motivo, cantidad, id_preceptor):
    amonestacion = Amonestacion(descripcion=motivo, alumno=alumno, fecha=fecha, cantidad=cantidad, preceptor=id_preceptor)
    amonestacion.save()

# Agrega una reincorporacion al alumno
def reincorporar(alumno):
    alumno.reincoporar()

# Funcion para descargar un archivo
def descargar_archivo(url, content_type):
  
    response = HttpResponse(content_type=content_type)
    response['Content-Disposition'] = 'attachment; filename=' + url
    
    fichero = open(url, 'rb')
    contenido = fichero.read()
    fichero.close()

    response.write(contenido)

    return response

def handle_uploaded_file(f):
    with open('some/file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)