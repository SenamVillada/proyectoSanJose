from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Alumno(User):
    # Atributos de la clase
    dni = models.IntegerField("Dni", max_length=100)
    domicilio = models.CharField(max_length=none)
    estado_opciones = (
            ('casado', 'Casado/a'),
            ('soltero', 'Soltero/a'),
            ('viudo', 'Viudo/a'),
            ('divorciado', 'Divorciado/a'),
            ('conyuge', 'Conyuge'),
        )
    estadoCivil = models.CharField(max_length=16,
                                choices=estado_opciones,
                                default='soltero')
    fechaNac = models.DateField()
    legajo = models.AutoField(primary_key=True)
    lugar_de_nacimiento = models.CharField("Lugar de Nacimiento", max_length=50)
    lugar_de_trabajo = models.CharField("Lugar de Trabajo", max_length=50)
    hora_de_trabajo = models.CharField("Horario de Trabajo", max_length=200)
    paternidad = models.BooleanField()
    telefonoF = models.IntegerField("Telefono Fijo", max_length=20)
    telefonoC = models.IntegerField("Telefono Celular", max_length=20)
    trabaja = models.BooleanField()
    
    def __str__(self):
	    return "{}, {}".format(self.nombre , self.apellido)

class Profesor(User):
    cargo_opciones = (
            ('profesor', 'Profesor'),
            ('directorDeTaller', 'Director de taller'),
            ('director', 'Director'),
        )
    cargo = models.CharField(max_length=16,
                                choices=cargo_opciones,
                                default='profesor')
    cuil = models.IntegerField("CUIL", max_length=20)
    curriculum = models.FileField("Curriculum",upload_to='curriculums/%Y/%m')
    dni = models.IntegerField("Dni", max_length=100, primary_key=True)
    domicilio = models.Charfield(max_length=none)
    estado_opciones = (
            ('casado', 'Casado/a'),
            ('soltero', 'Soltero/a'),
            ('viudo', 'Viudo/a'),
            ('divorciado', 'Divorciado/a'),
            ('conyuge', 'Conyuge'),
        )
    estadoCivil = models.CharField(max_length=16,
                                choices=estado_opciones,
                                default='soltero')
    fecha_de_escalafon = models.DateField("Fecha de Escalafon")
    fecha_del_apto_psicofisico = models.DateField("Fecha del Apto Psicofisico")
    fechaNac = models.DateField()
    legajo = models.AutoField(primary_key=True)
    licencias = models.BooleanField()
    lugar_de_nacimiento = models.CharField("Lugar de Nacimiento", max_length=50)
    numeroRegistro = models.IntegerField("Numero de Registro", max_length=100)
    telefonoF = models.IntegerField("Telefono Fijo", max_length=20)
    telefonoC = models.IntegerField("Telefono Celular", max_length=20)
    titulo = models.Charfield("Titulo",max_length=200)
    
    def __str__(self):
	    return "{}, {}".format(self.nombre , self.apellido)

class Materia(models.Model):
    nombre = models.CharField("Nombre",max_length=100)
    relatividad = models.ManyToManyField('Materia',null=True)    
    tipo_opciones = (
        	('asignatura', 'Asignatura'),
        	('seminario', 'Seminario'),
            ('taller', 'Taller'),
    	)
    tipo = models.CharField(max_length=80,
                                      choices=tipo_opciones,
                                      default='asignatura')

    def __unicode__(self):
	    return self.nombre

class Materia(models.Model):
    nombre = models.CharField("Nombre de la Materia", max_lenght=30)
    correlativas_de_cursado = models.ManyToManyField("Correlativas de Cursado")
    correlativas_de_rendir = models.ManyToManyField("Correlativas de Rendir")

    def __unicode__(self):
	    return self.nombre

class Matricula(models.Model):
    anio = models.DateField(auto_now=True)
    condicion_opciones = (
            ('regular','Regular'),
            ('libre','Libre'),
            ('promocionado','Promocionado'),
        )
    condicion = models.Charfield("Condición del alumno",
                                 max_length=12,
                                 choices=condicion_opciones,
                                 default='regular')
    alumno = models.ForeignKey(Alumno)
    profsor = models.ForeignKey(Profesor)
    alumno = models.ForeignKey(Alumno)

