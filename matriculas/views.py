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

#---------------------------------------LOGIN---------------------------------------------
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
#---------------------------------------END LOGIN------------------------------------------
#---------------------------------------LOGOUT---------------------------------------------
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')
#---------------------------------------END LOGOUT-----------------------------------------
#---------------------------------------ERROR LOGIN---------------------------------------------
def error_login(request):
    return render_to_response("errorLogin.html", RequestContext(request))
#---------------------------------------END ERROR LOGIN-----------------------------------------
#---------------------------------------Alumnos---------------------------------------------
@login_required(login_url='/login')
def alumnos(request):
    return render_to_response("alumnos.html", RequestContext(request))
#---------------------------------------END Alumnos-----------------------------------------
#---------------------------------------MATERIAS---------------------------------------------
@login_required(login_url='/login')
def materias(request):
    return render_to_response("materias.html", RequestContext(request))
#---------------------------------------END MATERIAS-----------------------------------------
#---------------------------------------PROFESORES---------------------------------------------
@login_required(login_url='/login')
def profesores(request):
    return render_to_response("profesores.html", RequestContext(request))
#---------------------------------------END PROFESORES-----------------------------------------
#---------------------------------------MOSTRAR MATERIAS---------------------------------------------
def mostrarMaterias(request):
    materias = Materia.objects.all()
    return render_to_response('materias.html', {"materias":materias}, context)
    
#---------------------------------------END PROFESORES-----------------------------------------