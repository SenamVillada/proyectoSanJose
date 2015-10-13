from django.db import models
from django.contrib.auth.models import User

class Cargo(models.Model):
    nombre = models.CharField("Nombre", max_length = 20)
    fechaAlta = models.DateField("Fecha de Alta")
    fechaBaja = models.DateField("Fecha de Baja")

    def __str__(self):
        return self.nombre

class Persona(User):
    dni = models.IntegerField("DNI")
    domicilio = models.CharField("Domicilio", max_length=300)
    estadoOpciones = (
            ('casado', 'Casado/a'),
            ('soltero', 'Soltero/a'),
            ('viudo', 'Viudo/a'),
            ('divorciado', 'Divorciado/a'))
    estadoCivil = models.CharField("Estado Civil", max_length=16, choices=estadoOpciones, default='soltero')
    fechaNacimiento = models.DateField("Fecha de Nacimiento")
    lugarNacimiento = models.CharField("Lugar de Nacimiento", max_length=50)
    telefonoFijo = models.IntegerField("Telefono Fijo")
    telefonoMovil = models.IntegerField("Telefono Celular")
    sexoOpciones = (
            ('masculino', 'Masculino'),
            ('femenino', 'Femenino'))
    sexo = models.CharField("Sexo", max_length=16, choices=sexoOpciones, default='masculino')
    

class Alumno(Persona):
    lugarDeTrabajo = models.CharField("Lugar de Trabajo", max_length=50)
    horaDeTrabajo = models.CharField("Horario de Trabajo", max_length=200)
    paternidad = models.BooleanField("Paternidad")
    
    def __unicode__(self):
	    return self.last_name + ", " + self.first_name

class Profesor(Persona):
    cuil = models.IntegerField("CUIL")
    curriculum = models.FileField("Curriculum",upload_to='curriculums/%Y/%m')
    fechaEscalafon = models.DateField("Fecha de Escalafon")
    fechaAptoPsicofisico = models.DateField("Fecha del Apto Psicofisico")
    numeroRegistro = models.IntegerField("Numero de Registro")
    titulo = models.CharField("Titulo",max_length=200)
    cargo = models.ForeignKey(Cargo)
    
    def __str__(self):
	    return self.last_name + ", " + self.first_name

class Licencia(models.Model):
    fechaInicio = models.DateField("Fecha de Alta")
    fechaFinal = models.DateField("Fecha de Baja")
    motivo = models.CharField("Motivo", max_length=200)
    profesor = models.ForeignKey(Profesor)

class Materia(models.Model):
    nombre = models.CharField("Nombre de la Materia", max_length=30)
    correlativasCursado = models.ManyToManyField('self',blank=True)
    correlativasRendir = models.ManyToManyField('self',blank=True)
    tipoOpciones = (
        	('asignatura', 'Asignatura'),
        	('seminario', 'Seminario'),
            ('taller', 'Taller'),
    	)
    tipo = models.CharField("Tipo de Materia", max_length=80, choices=tipoOpciones, default='asignatura')

    def __unicode__(self):
	    return self.nombre

    def verMateria(self):
        texto = "Nombre: "+self.nombre+"\nTipo de materia: "+self.tipo+"\nCorrelativas de cursado: "+self.correlativasCursado+"\nCorrelativas para rendir: "+self.correlativasRendir
        return texto
class Matricula(models.Model):
    anio = models.DateField(auto_now=True)
    horario = models.CharField("Horario", max_length=200)
    aprobada = models.BooleanField("Aprobada?")
    alumno = models.ForeignKey(Alumno)
    profesor = models.ForeignKey(Profesor)
    materia = models.ForeignKey(Materia)

    def __unicode__(self):
        self.alumno.first_name + ", " + self.alumno.last_name + " - " + self.materia.nombre + " - " + str(self.anio)

class Asistencia(models.Model):
    fecha = models.DateField("Fecha", auto_now=True)
    vino = models.BooleanField("Vino?")
    matricula = models.ForeignKey(Matricula)

class Nota(models.Model):
    fecha = models.DateField("Fecha", auto_now=True)
    calificacion = models.IntegerField("Calificacion")
    observacion = models.CharField("Observacion", max_length=100)
    matricula = models.ForeignKey(Matricula)

    def __unicode__():
        return str(calificacion)

class Log(models.Model):
    fecha = models.DateField("Fecha")
    log = models.CharField("Log", max_length=200)

    def __unicode__(self):
        return str(self.fecha) + self.log
