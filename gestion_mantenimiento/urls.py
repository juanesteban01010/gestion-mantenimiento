# gestion_mantenimiento/urls.py
from django.contrib import admin
from django.urls import path, include  # Asegúrate de importar include
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('solicitudes/', include('solicitudes.urls')),  # Incluir las URLs de la app solicitudes
]