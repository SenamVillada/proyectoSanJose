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
<<<<<<< HEAD
#---------------------------------------END LOGOUT-----------------------------------------
#---------------------------------------ERROR LOGIN---------------------------------------------
def error_login(request):
    return render_to_response("errorLogin.html", RequestContext(request))
#---------------------------------------END ERROR LOGIN-----------------------------------------
#---------------------------------------Alumnos---------------------------------------------
@login_required(login_url='/login')
=======

>>>>>>> 7be1d9859f3f0706025ae292e7b59227d8ed0ee2
def alumnos(request):

    if request.method == 'POST':
        try:
            dni = request.POST['buscarAlumnoDni']
            alumno = Alumno.objects.get(dni = dni)
            return render_to_response("alumnos.html",{'alumno':alumno}, RequestContext(request))

        except:
            print error
            return render_to_response("alumnos.html",{'errorAlumno':True}, RequestContext(request))

    return render_to_response("alumnos.html", RequestContext(request))

def materias(request):
    return render_to_response("materias.html", RequestContext(request))

def profesores(request):
    return render_to_response("profesores.html", RequestContext(request))
<<<<<<< HEAD
#---------------------------------------END PROFESORES-----------------------------------------
#---------------------------------------MOSTRAR MATERIAS---------------------------------------------
def mostrarMaterias(request):
    materias = Materia.objects.all()
    return render_to_response('materias.html', {"materias":materias}, context)
    
#---------------------------------------END PROFESORES-----------------------------------------
=======
>>>>>>> 7be1d9859f3f0706025ae292e7b59227d8ed0ee2
