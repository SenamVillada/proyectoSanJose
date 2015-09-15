# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

from fractions import Fraction
from decimal import Decimal

class Curso(models.Model):
    # Atributos de la clase
    numero = models.IntegerField("Curso",max_length=1)
    division = models.CharField("Division", max_length=1)
    anio = models.IntegerField("Ciclo lectivo",max_length=4)
    
    class Meta:
        ordering = ('-anio', 'numero', 'division')
    
    # Metodos de la clase
    def __unicode__(self):
        curso = str(self.numero)+" \""+str(self.division)+"\" - "+str(self.anio)
        return curso
    
    def diasDeClase(self, m=''):
	if m == 'mensual':
	    dias = self.alumno_set.all()[0].inasistencia_set.filter(fecha__month=datetime.now().month, fecha__year=datetime.now().year)
	elif m == 'anual':
	    dias = self.alumno_set.all()[0].inasistencia_set.filter(fecha__year=datetime.now().year)
	else:
	    return 0
	
	return len(dias)
    
    def color(self):
        if self.numero == 1:
            return 'blue'
        elif self.numero == 2:
            return 'green'
        elif self.numero == 3:
            return 'yellow'
        elif self.numero == 4:
            return 'red'
        elif self.numero == 5:
            return 'violet'
        elif self.numero == 6:
            return 'prueba'
        elif self.numero == 7:
            return 'gray'
    
    def getVacio(self):
	if self.alumno_set.all():
	    faltas = self.alumno_set.all()[0].inasistencia_set.all()
	    
	    if faltas: return False
	  
	    else: return True
	    
	else: return True
    
    def getTotalAlumnos(self):
        # Este metodo devuelve el total de alumnos del curso
        cantidad = self.alumno_set.count()
        return cantidad
    
    def getInasistencias(self, m='anual'):
        # Este metodo obtiene el total de inasistencias del curso
        alumnos = self.alumno_set.all()
        inasistencias = 0.0
        
        for i in alumnos:
            inasistencias += i.faltas(True, m=m)
        return inasistencias
    
    def getTotalAsistencias(self, m='anual'):
        # Este metodo calcula la cantidad total de asistencias
        # multiplicando el total de alumnos del curso por los dias de clase
        # y restando a ese resultado el total de inasistencias
        inasistencias = self.getInasistencias(m)
        totalAlumnos = self.getTotalAlumnos()
        dias = self.diasDeClase(m=m)
        print inasistencias, totalAlumnos, dias
        totalAsistencias = ((totalAlumnos * dias) - inasistencias)
        return totalAsistencias
    
    def getAsistenciaMedia(self, m='anual'):
        # Este metodo calcula la asistencia media (total de asistencias sobre los dias de clase)
        asistencias = self.getTotalAsistencias(m)
        dias = self.diasDeClase(m=m)
        asistenciaMedia = (asistencias/dias)
        return round(asistenciaMedia, 2)
    
    def getPorcentajeAsistencia(self, m='anual'):
        # Este metodo devuelve el porcentaje de asistencias
        # dividiendo el numero de asistencias multiplicado por 100
        # en a cantidad de alumnos multiplicado por los dias de clase
        asistencias = (self.getTotalAsistencias(m) * 100)
        alumnos = self.getTotalAlumnos()
        diasDeClase = self.diasDeClase(m=m)
        porcentajeDeAsistencia = (asistencias / (alumnos * diasDeClase))
        return round(porcentajeDeAsistencia, 2)
      
      
      
    def getInasistenciasMensual(self, m='mensual'):
        # Este metodo obtiene el total de inasistencias del curso
        alumnos = self.alumno_set.all()
        inasistencias = 0.0
        
        for i in alumnos:
            inasistencias += i.faltas(True, m=m)
        return inasistencias
    
    def getTotalAsistenciasMensual(self, m='mensual'):
        # Este metodo calcula la cantidad total de asistencias
        # multiplicando el total de alumnos del curso por los dias de clase
        # y restando a ese resultado el total de inasistencias
        inasistencias = self.getInasistenciasMensual()
        print 'INASISTENCIAS: ' + str(inasistencias)
        totalAlumnos = self.getTotalAlumnos()
        print 'TOT ALUMNOS: '+str(totalAlumnos)
        dias = self.diasDeClase(m=m)
        print 'DIAS: '+str(dias)
        totalAsistencias = ((totalAlumnos * dias) - inasistencias)
        return totalAsistencias
    
    def getAsistenciaMediaMensual(self, m='mensual'):
        # Este metodo calcula la asistencia media (total de asistencias sobre los dias de clase)
        asistencias = self.getTotalAsistenciasMensual()
        dias = self.diasDeClase(m=m)
        
        if dias == 0: return '-'
      
        else: 
	    asistenciaMedia = (asistencias/dias)
	    return round(asistenciaMedia, 2)
    
    def getPorcentajeAsistenciaMensual(self, m='mensual'):
        # Este metodo devuelve el porcentaje de asistencias
        # dividiendo el numero de asistencias multiplicado por 100
        # en a cantidad de alumnos multiplicado por los dias de clase
        asistencias = (self.getTotalAsistenciasMensual() * 100)
        alumnos = self.getTotalAlumnos()
        diasDeClase = self.diasDeClase(m=m)
        try:
	    porcentajeDeAsistencia = (asistencias / (alumnos * diasDeClase))
	    return round(porcentajeDeAsistencia, 2)
	except:
	    return '- '
        
        
class Preceptor(User):
    cursos = models.ManyToManyField(Curso)
    
    class Meta:
        verbose_name = 'preceptor'
        verbose_name_plural = 'preceptores'
        
    # Similar a __str__, devuelve una descripcion mas amigable
    def __unicode__(self):
        return self.username
      
    def observar(self, alumno, descripcion):
        self.observacion_set.create(descripcion=descripcion)
        return descripcion

#Clase alumno:
class Alumno(User):
    # Atributos de la clase
    telefono = models.IntegerField("Telefono", max_length=20)
    legajo = models.AutoField(primary_key=True)
    fechaNac = models.DateField()
    paternidad = models.BooleanField()
    trabaja = models.BooleanField()
    dni = models.IntegerField("Dni", max_length=100)
    curso = models.ForeignKey(Curso)
    
    
    class Meta:
        verbose_name = 'alumno'
        verbose_name_plural = 'alumnos'

    # Similar a __str__, devuelve una descripcion mas amigable
    def __unicode__(self):
        return self.username
    
    # Devuelve todas las faltas del alumno
    def totalFaltas(self):
        return self.inasistencia_set.all()

    # Devuelve todas las faltas del alumno
    def faltas(self, b=False, m='anual'):
	if m == 'mensual':
	    fts = self.inasistencia_set.filter(fecha__month=datetime.now().month, fecha__year=datetime.now().year)
	elif m == 'anual':
	    fts = self.inasistencia_set.filter(fecha__year=datetime.now().year)
	else:
	    fts = self.inasistencia_set.all()

	tot = 0
	
	for i in fts:
	    tot += i.tipo
	    
	if b:
	    return tot
	else:
	    return self.a_mixto(tot)

    # Devuelve todas las faltas injustificadas del alumno
    def injustificadas(self):
	fts = self.inasistencia_set.all().filter(justificado=False)
	tot = 0
	
	for i in fts:
	    tot += i.tipo
	
        return self.a_mixto(tot)
    
    # Devuelve todas las faltas justificadas del alumno
    def justificadas(self):
	fts = self.inasistencia_set.all().filter(justificado=True)
	tot = 0
	
	for i in fts:
	    tot += i.tipo
	
        return self.a_mixto(tot)
    
    # Devuelve todas las observaciones del alumno
    def observaciones(self):
        return self.observacion_set.count()

    # Devuelve todas las amonestaciones del alumno
    def amonestaciones(self):
	am = self.amonestacion_set.all()
	tot = 0
	
	for i in am:
	    tot += i.cantidad
	
        return tot

    def a_mixto(self, num):
	# componente entero
	num_t = int(num)
	# componente fraccion
	frac = Fraction( Decimal(num) - num_t ).__str__()
	mixto = ''
	
	if num_t:
	    mixto += str(num_t)
	
	if frac != '0':
	    mixto += ' '+frac
	
	if frac == '0' and not num_t:
	    mixto += '0'
	
	return mixto
    
    # Devuelve el vector con todas las amonestaciones del alumno
    def vectorAmonestaciones(self):
        return self.amonestacion_set.all()

    # Devuelve el vector con todas las observaciones del alumno
    def vectorObservaciones(self):
        return self.observacion_set.all()

    # Devuelve el vector con todas las inasistencias del alumno
    def vectorInasistencias(self):
        return self.inasistencia_set.all()

    # Reincopora al alumno
    def reincoporar(self):
        self.reincorporacion = (self.reincorporacion + 1)
        self.save()

class Profesor(User):
    telefono = models.IntegerField("Telefono", max_length=20)
    domicilio = models.CharField("Direccion", max_length=100)
    cuil = models.IntegerField("CUIL", max_length=20)
    mail = models.EmailField(max_length=254)
#    titulo y numero de registro
    fecha_de_escalafon = models.DateField("Fecha de escalafon")
    fecha_del_apto_psicofisico = models.DateField("Fecha del apto psicofisico")
    cargo_opciones = (
            ('profesor', 'Profesor'),
            ('directorDeTaller', 'Director de taller'),
            ('director', 'Director'),
        )
    cargo = models.CharField(max_length=16,
                                choices=cargo_opciones,
                                default='profesor')
    licencias = models.BooleanField()
    lugar_de_nacimiento = models.CharField("Lugar de nacimiento", max_length=50)
    legajo = models.AutoField(primary_key=True)
    fechaNac = models.DateField()
    dni = models.IntegerField("Dni", max_length=100, primary_key=True)
    curso = models.ForeignKey(Curso)
    curriculum = models.FileField("Curriculum",upload_to='curriculums/%Y/%m')
class Inasistencia (models.Model):
    tipo = models.FloatField()
    justificado = models.BooleanField(default=False)
    fecha = models.DateField()
    preceptor = models.ForeignKey(Preceptor)
    alumno = models.ForeignKey(Alumno)
    
    # Similar a __str__, devuelve una descripcion mas amigable
    def __unicode__(self):
        return self.fecha.__str__()

    def justificar(self, bo):
	self.justificado = bo
	self.save()
	return self.justificado
    
    def cantMixto(self):
        frac = Fraction(self.tipo).__str__()
        mixto = ''

        if frac != '0':
            mixto += ''+frac

        if frac == '0' and not self.tipo:
            mixto += '0'
            
class Materia(models.Model):
    nombre = models.CharField("Nombre",max_length=100)
    tipo_opciones = (
        	('asignatura', 'Asignatura'),
        	('seminario', 'Seminario'),
            ('taller', 'Taller'),
    	)
    tipo = models.CharField(max_length=80,
                                      choices=tipo_opciones,
                                      default='asignatura')
    relatividad = models.ManyToManyField('Materia',null=True)
    
    def __unicode__(self):
	    return self.nombre