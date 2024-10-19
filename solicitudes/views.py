# solicitudes/views.py
from django.shortcuts import render, redirect
from .forms import SolicitudForm, GestionOtForm, OrdenTrabajoForm
from .models import Solicitud, GestionOt,OrdenTrabajo

# Vista para crear una solicitud
def crear_solicitud(request):
    if request.method == 'POST':
        form = SolicitudForm(request.POST)
        if form.is_valid():
            nueva_solicitud = form.save(commit=False)
            ultimo_numero = Solicitud.objects.count()
            nueva_solicitud.numero_activo = ultimo_numero + 1
            nueva_solicitud.estado = 'Solicitudes'
            nueva_solicitud.save()
            return redirect('crear_solicitud')
        else:
            # Mostrar los errores de validación del formulario en la consola
            print("Errores en el formulario:", form.errors)
    else:
        form = SolicitudForm()

    return render(request, 'solicitudes/crear_solicitud.html', {'form': form})

from django.http import JsonResponse
import json

def gestion_ot(request):
    if request.method == 'POST':
        # Aquí manejamos tanto la creación como la actualización
        if 'actualizar' in request.POST:
            # Manejar actualización de solicitud
            numero_solicitud = request.POST.get('numero_solicitud')
            estado = request.POST.get('estado')
            tecnico = request.POST.get('tecnico_asignado')
            fecha = request.POST.get('fecha_actividad')

            try:
                solicitud = Solicitud.objects.get(numero_activo=numero_solicitud)
                solicitud.estado = estado
                solicitud.tecnico_asignado = tecnico
                solicitud.fecha_actividad = fecha
                solicitud.save()

                return JsonResponse({'status': 'ok'})
            except Solicitud.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Solicitud no encontrada'}, status=404)

        # Manejar creación de nueva orden de trabajo
        form = GestionOtForm(request.POST)
        if form.is_valid():
            form.save()  # Guardar la nueva orden de trabajo
            return redirect('gestion_ot')  # Redirigir a la misma página
    
    form = GestionOtForm()
    ordenes_trabajo = GestionOt.objects.all()
    solicitudes_pendientes = Solicitud.objects.filter(gestionot__isnull=True)

    return render(request, 'solicitudes/gestion_ot.html', {
        'form': form,
        'ordenes_trabajo': ordenes_trabajo,
        'solicitudes': solicitudes_pendientes
    })


def listar_ot(request):
    ots = OrdenTrabajo.objects.all()
    return render(request, 'solicitudes/listar_ot.html', {'ots': ots})
