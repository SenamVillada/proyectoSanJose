# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

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
    situacionExepcional = models.BooleanField("Situacion Excepcional", default=False)
    
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
    
    class Meta:
        verbose_name = 'Profesor'
        verbose_name_plural = 'Profesores'
    
    def __str__(self):
	    return self.last_name + ", " + self.first_name
    
    def cantHoras(self):
        cursados = self.cursado_set.all()
        cantidadHoras = 0
        for i in range(cursados.count()):
            horarios = cursados[i].horario_set.all()
            for j in range(horarios.count()):
                cantidadHoras = cantidadHoras + horarios[j].cantHoras()
        return cantidadHoras

class Cargo(models.Model):
    nombre = models.CharField("Nombre", max_length = 20)
    fechaAlta = models.DateField("Fecha de Alta")
    fechaBaja = models.DateField("Fecha de Baja", blank=True, null=True)
    profesor = models.ForeignKey(Profesor)

    def __str__(self):
        return self.nombre

class Licencia(models.Model):
    fechaInicio = models.DateField("Fecha de Alta")
    fechaFinal = models.DateField("Fecha de Baja")
    motivo = models.CharField("Motivo", max_length=200)
    profesor = models.ForeignKey(Profesor)

class Materia(models.Model):
    nombre = models.CharField("Nombre de la Materia", max_length=30)
    correlativasCursado = models.ManyToManyField('self', blank=True)
    correlativasRendir = models.ManyToManyField('self', blank=True)
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

class Cursado(models.Model):
    anio = models.IntegerField("Año")
    materia = models.ForeignKey(Materia)
    profesor = models.ForeignKey(Profesor)
    
    def __unicode__(self):
        return self.materia.nombre + " - " + self.profesor.last_name +", " + self.profesor.last_name +" - "+ str(self.anio)

class Matricula(models.Model):
    alumno = models.ForeignKey(Alumno)
    cursado = models.ForeignKey(Cursado)

    def __unicode__(self):
        return self.alumno.first_name + ", " + self.alumno.last_name + " - " + self.materia.nombre + " - " + str(self.anio)

    def condicion(self):
        if (self.estaAprobada() == True):
            return "Aprobada"
        elif (self.esRegular() == True):
            return "Regular"
        elif (self.estaCursando == True):
            return "Cursando"
        else:
            return "Desaprobada/Libre"

    def estaAprobada(self):
        examenes = self.examenfinal_set.all()
        aprobado = False
        for i in range(examenes.count()):
            if (examenes[i].nota.calificacion >= 4):
                aprobado = True
        return aprobado

    def esRegular(self):
        regular = True
        asistencia = (self.porcentajeAsistencia()-1)
        notas = self.nota_set.all()
        porcentaje = 75
        if (self.alumno.situacionExepcional == True):
            porcentaje = 60
        if (asistencia >= porcentaje):
            for i in range(notas.count()):
                if (notas[i].calificacion < 7):
                    regular = False
        else:
            regular = False
        return regular
    
    def estaCursando(self):
        return True

    def porcentajeAsistencia(self):
        asistencias = self.asistencia_set.all()
        vinoAClase = asistencias.filter(vino=True)
        if (asistencias.count() != 0):
            porcentaje = ((vinoAClase.count()/asistencias.count())*100)
            porcentaje = (porcentaje + 1)
            return porcentaje
        else:
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
    cursado = models.ForeignKey(Cursado)
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
        return self.cursado.materia.nombre
    
    def cantHoras(self):
        hora1 = self.horaInicio
        hora2 = self.horaFinal
        horaConvertida1 = datetime.strptime(hora1, '%H:%M')
        horaConvertida2 = datetime.strptime(hora2, '%H:%M')
        cantidad = horaConvertida2 - horaConvertida1
        cantidad = (cantidad.total_seconds()/3600)
        return cantidad

class TurnoDeExamen(models.Model):
    fecha = models.DateField("Fecha")
    cursado = models.ForeignKey(Cursado)

class ExamenFinal(models.Model):
    nota = models.ForeignKey(Nota)
    matricula = models.ForeignKey(Matricula)
    turno = models.ForeignKey(TurnoDeExamen)

class Log(models.Model):
    fecha = models.DateField("Fecha")
    log = models.CharField("Log", max_length=200)

    def __unicode__(self):
        return str(self.fecha) + self.log