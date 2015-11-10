from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext, ugettext_lazy as _
from matriculas.models import *


class AlumnoAddForm(UserCreationForm):
    class Meta:
        model = Alumno
        fields = ('first_name', 'last_name', 'username', 'dni', 'email', 'domicilio', 'estadoCivil', 'fechaNacimiento', 'lugarNacimiento', 'telefonoFijo', 'telefonoMovil', 'sexo', 'lugarDeTrabajo', 'horaDeTrabajo', 'paternidad', 'anioEgreso','situacionExepcional')

        def __init__(self, *args, **kwargs):
            return super(AlumnoAddForm,self).__init__( *args, **kwargs)

class AlumnoForm(UserChangeForm):

    class Meta:
        model = Alumno
        fields = ('first_name', 'last_name', 'username', 'dni', 'email', 'domicilio', 'estadoCivil', 'fechaNacimiento', 'lugarNacimiento', 'telefonoFijo', 'telefonoMovil', 'sexo', 'lugarDeTrabajo', 'horaDeTrabajo', 'paternidad', 'anioEgreso','situacionExepcional')

class AlumnoAdmin(admin.ModelAdmin):
    form = AlumnoForm
    add_form = AlumnoAddForm
    
    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            return AlumnoAddForm
        else:
            return super(AlumnoAdmin, self).get_form(request, obj, **kwargs)

class ProfesorAddForm(UserCreationForm):

    class Meta:
        model = Profesor
        fields = ('username', 'dni', 'first_name', 'last_name', 'email', 'domicilio', 'estadoCivil', 'fechaNacimiento', 'lugarNacimiento', 'telefonoFijo', 'telefonoMovil', 'sexo', 'cuil','curriculum','fechaEscalafon','fechaAptoPsicofisico','numeroRegistro','titulo')

    def __init__(self, *args, **kwargs):
        return super(ProfesorAddForm,self).__init__( *args, **kwargs)

class ProfesorForm(UserChangeForm):

    class Meta:
        model = Profesor
        fields = ('username', 'dni', 'first_name', 'last_name', 'email', 'domicilio', 'estadoCivil', 'fechaNacimiento', 'lugarNacimiento', 'telefonoFijo', 'telefonoMovil', 'sexo', 'cuil','curriculum','fechaEscalafon','fechaAptoPsicofisico','numeroRegistro','titulo')

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
admin.site.register(Log)
admin.site.register(ExamenFinal)
admin.site.register(Cursado)
admin.site.register(TurnoDeExamen)