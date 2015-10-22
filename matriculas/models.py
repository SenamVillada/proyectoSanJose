# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class Cargo(models.Model):
    nombre = models.CharField("Nombre", max_length = 20)
    fechaAlta = models.DateField("Fecha de Alta")
    fechaBaja = models.DateField("Fecha de Baja", blank=True, null=True)

    def __str__(self):
        return self.nombre

class Persona(User):
    dni = models.IntegerField("DNI")
    domicilio = models.CharField("Domicilio", max_length=300, blank=True, null=True)
    estadoOpciones = (
            ('Casado', 'Casado/a'),
            ('Soltero', 'Soltero/a'),
            ('Viudo', 'Viudo/a'),
            ('Divorciado', 'Divorciado/a'))
    estadoCivil = models.CharField("Estado Civil", max_length=16, choices=estadoOpciones, default='Soltero')
    fechaNacimiento = models.DateField("Fecha de Nacimiento")
    lugarNacimiento = models.CharField("Lugar de Nacimiento", max_length=50, blank=True, null=True)
    telefonoFijo = models.IntegerField("Telefono Fijo", blank=True, null=True)
    telefonoMovil = models.IntegerField("Telefono Celular", blank=True, null=True)
    sexoOpciones = (
            ('Masculino', 'Masculino'),
            ('Femenino', 'Femenino'))
    sexo = models.CharField("Sexo", max_length=16, choices=sexoOpciones, default='Masculino')

class Alumno(Persona):
    lugarDeTrabajo = models.CharField("Lugar de Trabajo", max_length=50, blank=True, null=True)
    horaDeTrabajo = models.CharField("Horario de Trabajo", max_length=200, blank=True, null=True)
    paternidad = models.BooleanField("Paternidad")
    anioEgreso = models.IntegerField("Año de Egreso", blank=True, null=True)
    
    class Meta:
        verbose_name = 'Alumno'
        verbose_name_plural = 'Alumnos'
    
    def __unicode__(self):
	    return self.last_name + ", " + self.first_name

    def egreso(self):
        if (self.anioEgreso != None):
            return True
        else:
            return False

class Profesor(Persona):
    cuil = models.IntegerField("CUIL")
    curriculum = models.FileField("Curriculum",upload_to='curriculums/%Y/%m', blank=True)
    fechaEscalafon = models.DateField("Fecha de Escalafon", blank=True, null=True)
    fechaAptoPsicofisico = models.DateField("Fecha del Apto Psicofisico", blank=True, null=True)
    numeroRegistro = models.IntegerField("Numero de Registro", blank=True, null=True)
    titulo = models.CharField("Titulo",max_length=200, blank=True, null=True)
    cargo = models.ForeignKey(Cargo)
    
    class Meta:
        verbose_name = 'Profesor'
        verbose_name_plural = 'Profesores'
    
    def __str__(self):
	    return self.last_name + ", " + self.first_name

class Licencia(models.Model):
    fechaInicio = models.DateField("Fecha de Alta")
    fechaFinal = models.DateField("Fecha de Baja")
    motivo = models.CharField("Motivo", max_length=200)
    profesor = models.ForeignKey(Profesor)

class Materia(models.Model):
    nombre = models.CharField("Nombre de la Materia", max_length=30)
    correlativasCursado = models.ManyToManyField('self', blank=True)
    correlativasRendir = models.ManyToManyField('self', blank=True)
    profesor = models.ForeignKey(Profesor)
    tipoOpciones = (
        	('Asignatura', 'Asignatura'),
        	('Seminario', 'Seminario'),
            ('Taller', 'Taller'),
    	)
    tipo = models.CharField("Tipo de Materia", max_length=80, choices=tipoOpciones, default='Asignatura')

    def __unicode__(self):
	    return self.nombre

    def verMateria(self):
        return "Nombre: "+self.nombre+"\nTipo de materia: "+self.tipo+"\nCorrelativas de cursado: "+self.correlativasCursado+"\nCorrelativas para rendir: "+self.correlativasRendir

class Matricula(models.Model):
    anio = models.IntegerField("Año")
    aprobada = models.BooleanField("Aprobada?", default=False)
    alumno = models.ForeignKey(Alumno)
    materia = models.ForeignKey(Materia)
    finalizada = models.BooleanField("Finalizada?", default=False)

    def __unicode__(self):
        return self.alumno.first_name + ", " + self.alumno.last_name + " - " + self.materia.nombre + " - " + str(self.anio)
    
    def condicion(self):
        if (self.aprobada == True):
            return "Aprobada"
        if (self.esRegular == True):
            return "Regular"
        if (self.finalizada == True):
            return "Desaprobada/Libre"
        else:
            return "Cursando"
    
    def porcentajeAsistencia(self):
        asistencias = self.asistencia_set.all()
        vinoAClase = asistencias.filter(vino=True)
        if (asistencias.count() != 0):
            porcentaje = ((vinoAClase.count()/asistencias.count())*100)
            porcentaje = (porcentaje + 1)
            return porcentaje
        else:
            return False

    def esRegular(self):
        return False
    
    def getPromedio(self):
        arrayNotas = self.nota_set.all()
        notas = 0.0
        if (arrayNotas.count() != 0):
            for i in range(arrayNotas.count()):
                notas = notas + arrayNotas[i].calificacion
            return (notas/arrayNotas.count())
        else:
            return False

    def cantFaltas(self):
        cantidad = self.asistencia_set.all().filter(vino=False).count()
        print cantidad
        return cantidad

class Asistencia(models.Model):
    fecha = models.DateField("Fecha")
    vino = models.BooleanField("Vino?", default=True)
    matricula = models.ForeignKey(Matricula)

class Nota(models.Model):
    fecha = models.DateField("Fecha")
    calificacion = models.IntegerField("Calificacion")
    observacion = models.CharField("Observacion", max_length=100)
    matricula = models.ForeignKey(Matricula)

    def __unicode__(self):
        return str(self.calificacion) + " - " + str(self.matricula.alumno.dni)
    
class Horario(models.Model):
    materia = models.ForeignKey(Materia)
    diaOpciones = (
        	('Lunes', 'Lunes'),
        	('Martes', 'Martes'),
            ('Miercoles', 'Miercoles'),
            ('Jueves', 'Jueves'),
            ('Viernes', 'Viernes'),
            ('Sabado', 'Sabado'),
    	)
    dia = models.CharField("Día", max_length=10, choices=diaOpciones, default='Lunes')
    horaInicio = models.CharField("Hora de Inicio", max_length=20, default="00:00")
    horaFinal = models.CharField("Hora de Final", max_length=20, default="00:00")

    def __unicode__(self):
        return self.materia.nombre

class Log(models.Model):
    fecha = models.DateField("Fecha")
    log = models.CharField("Log", max_length=200)

    def __unicode__(self):
        return str(self.fecha) + self.log