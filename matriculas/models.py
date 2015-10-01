from django.db import models
from django.contrib.auth.models import User

class Alumno(User):
    dni = models.IntegerField("DNI", max_length=100)
    domicilio = models.CharField("Domicilio", max_length=none)
    estado_opciones = (
            ('casado', 'Casado/a'),
            ('soltero', 'Soltero/a'),
            ('viudo', 'Viudo/a'),
            ('divorciado', 'Divorciado/a'))
    estadoCivil = models.CharField("Estado Civil", max_length=16, choices=estado_opciones, default='soltero')
    fechaNac = models.DateField("Fecha de Nacimiento")
    lugar_de_nacimiento = models.CharField("Lugar de Nacimiento", max_length=50)
    lugar_de_trabajo = models.CharField("Lugar de Trabajo", max_length=50)
    hora_de_trabajo = models.CharField("Horario de Trabajo", max_length=200)
    paternidad = models.BooleanField("Paternidad")
    telefonoF = models.IntegerField("Telefono Fijo", max_length=20)
    telefonoC = models.IntegerField("Telefono Celular", max_length=20)
    
    def __unicode__(self):
	    return self.last_name + ", " + self.first_name

class Cargo(models.Model)
    nombre = models.CharField("Nombre", max_lenght=30)
    fecha_alta = models.DateField("Fecha de Alta")
    fecha_baja = models.DateField("Fecha de Baja")

    def __unicode__():
        return self.nombre

class Profesor(User):
    cargo = models.ForeingKey(Cargo)
    cuil = models.IntegerField("CUIL", max_length=20)
    curriculum = models.FileField("Curriculum",upload_to='curriculums/%Y/%m')
    dni = models.IntegerField("DNI", max_length=100, primary_key=True)
    domicilio = models.Charfield("Domicilio", max_length=none)
    estado_opciones = (
            ('casado', 'Casado/a'),
            ('soltero', 'Soltero/a'),
            ('viudo', 'Viudo/a'),
            ('divorciado', 'Divorciado/a')
        )
    estadoCivil = models.CharField("Estado Civil", max_length=16, choices=estado_opciones, default='soltero')
    fecha_de_escalafon = models.DateField("Fecha de Escalafon")
    fecha_del_apto_psicofisico = models.DateField("Fecha del Apto Psicofisico")
    fechaNacimiento = models.DateField("Fecha de Nacimiento")
    lugar_de_nacimiento = models.CharField("Lugar de Nacimiento", max_length=50)
    numeroRegistro = models.IntegerField("Numero de Registro", max_length=100)
    telefonoF = models.IntegerField("Telefono Fijo", max_length=20)
    telefonoC = models.IntegerField("Telefono Celular", max_length=20)
    titulo = models.Charfield("Titulo",max_length=200)
    
    def __unicode__(self):
	    return self.last_name + ", " + self.first_name

class Licencia(models.Model):
    fecha_inicio = models.DateField("Fecha de Alta")
    fecha_final = models.DateField("Fecha de Baja")
    motivo = models.CharField("Motivo", max_lenght=200)
    profesor = models.ForeingKey(Profesor)

class Materia(models.Model):
    nombre = models.CharField("Nombre de la Materia", max_lenght=30)
    correlativas_de_cursado = models.ManyToManyField("Correlativas de Cursado", null = True)
    correlativas_de_rendir = models.ManyToManyField("Correlativas de Rendir", null = True)
    tipo_opciones = (
        	('asignatura', 'Asignatura'),
        	('seminario', 'Seminario'),
            ('taller', 'Taller'),
    	)
    tipo = models.CharField("Tipo de Materia", max_length=80, choices=tipo_opciones, default='asignatura')

    def __unicode__(self):
	    return self.nombre

class Matricula(models.Model):
    anio = models.DateField(auto_now=True)
    horario = models.CharField("Horario", max_lenght=200)
    aprobada = models.BooleanField("Aprobada?")
    alumno = models.ForeignKey(Alumno)
    profesor = models.ForeignKey(Profesor)
    materia = models.ForeingKey(Materia)

    def __unicode__(self):
        self.alumno.first_name + ", " + self.alumno.last_name + " - " + self.materia.nombre + " - " + str(self.anio)

class Asistencia(models.Model):
    fecha = models.DateField("Fecha", auto_now=True)
    vino = models.BooleanField("Vino?")

class Log(models.Model):
    fecha = models.DateField("Fecha")
    log = models.CharField("Log", max_lenght=200)

    def __unicode__(self):
        return str(self.fecha) + self.log
