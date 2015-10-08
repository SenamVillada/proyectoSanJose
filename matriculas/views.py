from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required

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
            return HttpResponseRedirect('../error')
    else:
        return render_to_response('login.html', {}, context)
#---------------------------------------END LOGIN------------------------------------------
#---------------------------------------LOGOUT---------------------------------------------
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')
#---------------------------------------END LOGOUT-----------------------------------------
#---------------------------------------Alumnos---------------------------------------------
def alumnos(request):
    return render_to_response("alumnos.html", RequestContext(request))
#---------------------------------------END Alumnos-----------------------------------------
#---------------------------------------MATERIAS---------------------------------------------
def materias(request):
    return render_to_response("materias.html", RequestContext(request))
#---------------------------------------END MATERIAS-----------------------------------------
#---------------------------------------PROFESORES---------------------------------------------
def profesores(request):
    return render_to_response("profesores1.html", RequestContext(request))
#---------------------------------------END PROFESORES-----------------------------------------