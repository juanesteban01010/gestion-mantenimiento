# models.py
from datetime import timezone
from django.db import models

class Solicitud(models.Model):
    consecutivo = models.AutoField(primary_key=True)
    creado_por = models.CharField(max_length=100)  # Nuevo campo para el creador de la solicitud
    descripcion_problema = models.TextField()  # Nuevo campo para la descripción del problema
    numero_activo = models.IntegerField()  # Nuevo campo para el número de activo
    email_solicitante = models.EmailField(max_length=254, null=True)
    fecha_creacion = models.DateTimeField(blank=True, null=True)
    PDV = models.CharField(max_length=100, default='')

    def __str__(self):
        return f"Solicitud {self.consecutivo}"
    
class GestionOt(models.Model):
    solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE)
    tecnico = models.CharField(max_length=100)
    fecha_asignacion = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"GestionOt {self.solicitud}"
    
class OrdenTrabajo(models.Model):
    numero_solicitud = models.IntegerField()
    tecnico_asignado = models.CharField(max_length=100)
    fecha_actividad = models.DateField()
    estado = models.CharField(max_length=50, default="En Proceso")

    def __str__(self):
        return f"OT-{self.numero_solicitud} - {self.tecnico_asignado}"
