from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import logout, authenticate, login

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

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
                return HttpResponseRedirect('/inicio/')
            else:
                return HttpResponse("Tu cuenta no esta habilitada")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponseRedirect('../error')
    else:
        return render_to_response('login.html', {}, context)
#---------------------------------------END LOGIN------------------------------------------