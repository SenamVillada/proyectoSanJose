from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from matriculas.models import *

class AlumnoForm(UserChangeForm):
    class Meta:
	model = Alumno
	fields = ('username', 'dni', 'first_name', 'last_name', 'email','lugarDeTrabajo','horaDeTrabajo','paternidad','anioEgreso', 'situacionExepcional')
    
class AlumnoAddForm(UserCreationForm):
    class Meta:
	model = Alumno
	fields = ('username', 'dni', 'first_name', 'last_name', 'email','lugarDeTrabajo','horaDeTrabajo','paternidad','anioEgreso', 'situacionExepcional')
    
class AlumnoAdmin(admin.ModelAdmin):
    form = AlumnoForm
    add_form = AlumnoAddForm
    
    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            return AlumnoAddForm
        else:
            return super(AlumnoAdmin, self).get_form(request, obj, **kwargs)

class ProfesorForm(UserChangeForm):
    class Meta:
	model = Profesor
	fields = ('username', 'dni', 'first_name', 'last_name', 'domicilio', 'email','cuil','curriculum','fechaEscalafon','fechaAptoPsicofisico','numeroRegistro','titulo')
    
class ProfesorAddForm(UserCreationForm):
    class Meta:
	model = Profesor
	fields = ('username', 'dni', 'first_name', 'last_name','domicilio', 'email','cuil','curriculum','fechaEscalafon','fechaAptoPsicofisico','numeroRegistro','titulo')
    
class ProfesorAdmin(admin.ModelAdmin):
    form = ProfesorForm
    add_form = ProfesorAddForm
    
    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            return ProfesorAddForm
        else:
            return super(ProfesorAdmin, self).get_form(request, obj, **kwargs)

admin.site.register(Alumno, AlumnoAdmin)
admin.site.register(Profesor, ProfesorAdmin)
admin.site.register(Cargo)
admin.site.register(Licencia)
admin.site.register(Materia)
admin.site.register(Matricula)
admin.site.register(Asistencia)
admin.site.register(Nota)
admin.site.register(Horario)
admin.site.register(Cursado)
admin.site.register(Log)