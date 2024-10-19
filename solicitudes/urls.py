# solicitudes/urls.py
from django.urls import path
from .views import crear_solicitud, gestion_ot, listar_ot
from . import views

urlpatterns = [
    path('crear/', crear_solicitud, name='crear_solicitud'),
    path('gestion_ot/', gestion_ot, name='gestion_ot'),
    path('listar_ot/', listar_ot, name='listar_ot'),

    
]
