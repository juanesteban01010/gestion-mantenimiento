# solicitudes/forms.py
from django import forms
from .models import Solicitud, GestionOt, OrdenTrabajo

class SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = ['consecutivo','creado_por', 'descripcion_problema', 'numero_activo', 'email_solicitante','PDV','fecha_creacion' ]
        

class GestionOtForm(forms.ModelForm):
    class Meta:
        model = GestionOt
        fields = ['solicitud', 'tecnico']  # Puedes incluir otros campos si lo deseas
 
class OrdenTrabajoForm(forms.ModelForm):
    class Meta:
        model = OrdenTrabajo
        fields = ['numero_solicitud', 'fecha_actividad', 'tecnico_asignado', 'estado']
        widgets = {
            'numero_solicitud': forms.TextInput(attrs={'readonly': 'readonly'}),  # Este campo será solo lectura
            'fecha_actividad': forms.DateInput(attrs={'type': 'date'}),
             }