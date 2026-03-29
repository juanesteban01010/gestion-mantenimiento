from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from django.db import models
from django.utils import timezone
from datetime import timedelta
import datetime
from dateutil.parser import isoparse
from .models import  OrdenTrabajo, Estado, CierreOt
from .forms import GestionOtForm, OrdenTrabajoForm, CierreOtForm
from solicitudes.models import Solicitud
import logging
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder

class CustomDjangoJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, models.FileField):
            return obj.url if obj else None
        return super().default(obj)


# Configurar el logger
logger = logging.getLogger(__name__)
@login_required
# Vista para gestionar órdenes de trabajo
def gestion_ot(request):
    ordenes_trabajo = OrdenTrabajo.objects.all()
    solicitudes_pendientes = Solicitud.objects.filter(gestionot__isnull=True)
    tecnicos = User.objects.filter(groups__name='Tecnico')  # Filtra los usuarios que pertenecen al grupo 'Tecnico'

    # Filtros
    filtro_fecha_inicio = request.GET.get('fecha_inicio')
    filtro_fecha_fin = request.GET.get('fecha_fin')
    filtro_pdv = request.GET.get('pdv')

    pdvs = Solicitud.objects.values_list('PDV', flat=True).distinct()

    # Si no hay filtros aplicados, mostrar las solicitudes del mes actual
    if not filtro_fecha_inicio and not filtro_fecha_fin:
        now = timezone.now()
        first_day_of_month = now.replace(day=1)
        last_day_of_month = (first_day_of_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        filtro_fecha_inicio = first_day_of_month.date()
        filtro_fecha_fin = last_day_of_month.date()

    if filtro_fecha_inicio and filtro_fecha_fin:
        if isinstance(filtro_fecha_inicio, str):
            filtro_fecha_inicio = timezone.make_aware(datetime.datetime.strptime(filtro_fecha_inicio, '%Y-%m-%d'), timezone.get_current_timezone())
        if isinstance(filtro_fecha_fin, str):
            filtro_fecha_fin = timezone.make_aware(datetime.datetime.strptime(filtro_fecha_fin, '%Y-%m-%d'), timezone.get_current_timezone())
        solicitudes_pendientes = solicitudes_pendientes.filter(fecha_creacion__range=[filtro_fecha_inicio, filtro_fecha_fin])
    if filtro_pdv:
        solicitudes_pendientes = solicitudes_pendientes.filter(PDV=filtro_pdv)

    form = GestionOtForm()
    return render(request, 'Gestion_ot/gestion_ot.html', {
        'form': form,
        'ordenes_trabajo': ordenes_trabajo,
        'solicitudes': solicitudes_pendientes,
        'pdvs': pdvs,
        'filtro_fecha_inicio': filtro_fecha_inicio,
        'filtro_fecha_fin': filtro_fecha_fin,
        'filtro_pdv': filtro_pdv,
        'tecnicos': tecnicos,
    })



# Vista para actualizar el estado de una solicitud
@csrf_exempt
@require_POST
@login_required
def actualizar_estado_solicitud(request):
    try:
        data = json.loads(request.body)
        logger.debug(f"Datos recibidos: {data}")
        
        numero_solicitud = data.get('numero')
        nuevo_estado_nombre = data.get('estado')
        tecnico = data.get('tecnico')
        fecha = data.get('fecha')

        logger.debug(f"Numero de Solicitud: {numero_solicitud}")
        logger.debug(f"Nuevo Estado: {nuevo_estado_nombre}")
        logger.debug(f"Tecnico: {tecnico}")
        logger.debug(f"Fecha: {fecha}")

        if not numero_solicitud or not nuevo_estado_nombre:
            logger.error("Número y estado son requeridos.")
            return JsonResponse({'status': 'error', 'message': 'Número y estado son requeridos.'}, status=400)

        if not fecha:
            logger.error("Fecha de actividad es requerida.")
            return JsonResponse({'status': 'error', 'message': 'Fecha de actividad es requerida.'}, status=400)

        solicitud = Solicitud.objects.get(consecutivo=numero_solicitud)
        logger.debug(f"Solicitud encontrada: {solicitud}")

        nuevo_estado = Estado.objects.get(nombre=nuevo_estado_nombre)
        solicitud.estado = nuevo_estado
        if tecnico:
            solicitud.tecnico_asignado = tecnico
        # Asegurarse de que fecha sea aware datetime
        fecha = isoparse(fecha)
        if timezone.is_naive(fecha):
            fecha = timezone.make_aware(fecha, timezone.get_current_timezone())
        solicitud.fecha_actividad = fecha
        solicitud.save()
        logger.debug(f"Solicitud actualizada: {solicitud}")

        # Crear o actualizar la Orden de Trabajo
        orden_trabajo, created = OrdenTrabajo.objects.update_or_create(
            solicitud=solicitud,
            defaults={
                'tecnico_asignado': tecnico,
                'fecha_actividad': fecha,
                'estado': nuevo_estado
            }
        )
        logger.debug(f"Orden de Trabajo {'creada' if created else 'actualizada'}: {orden_trabajo}")

        return JsonResponse({'status': 'ok', 'message': 'Solicitud y Orden de Trabajo actualizadas correctamente'})

    except Solicitud.DoesNotExist:
        logger.error("Solicitud no encontrada.")
        return JsonResponse({'status': 'error', 'message': 'Solicitud no encontrada'}, status=404)
    except Exception as e:
        logger.exception("Error al actualizar la solicitud.")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)

# Vista para listar todas las órdenes de trabajo
@login_required
def listar_ot(request):
    if request.user.groups.filter(name='Admin').exists():
        ots = OrdenTrabajo.objects.all()
    else:
        ots = OrdenTrabajo.objects.filter(tecnico_asignado=request.user.username)
    
    return render(request, 'Gestion_ot/listar_ot.html', {
        'ots': ots,
    })

# Vista para cerrar una OT
@login_required
def cierre_ot(request, ot_id):
    ot = get_object_or_404(OrdenTrabajo, id=ot_id)
    cierre_ot, created = CierreOt.objects.get_or_create(orden_trabajo=ot)
    if request.method == 'POST':
        form = CierreOtForm(request.POST, instance=cierre_ot)
        if form.is_valid():
            estado_revision = Estado.objects.get(nombre="en revision")
            ot.estado = estado_revision
            ot.save()
            cierre_ot.estado = estado_revision
            cierre_ot.save()
            solicitud = ot.solicitud
            solicitud.estado = estado_revision
            solicitud.save()
            return redirect('listar_ot')
    else:
        form = CierreOtForm(instance=cierre_ot)
    return render(request, 'Gestion_ot/cierre_ot.html', {'form': form, 'ot': ot})


# Detalles de la solicitud
@login_required
def detalles_solicitud(request, consecutivo):
    solicitud = get_object_or_404(Solicitud, consecutivo=consecutivo)
    ordenes_trabajo = solicitud.ordenes_trabajo.all()
    data = {
        'consecutivo': solicitud.consecutivo,
        'pdv': solicitud.PDV,
        'descripcion': solicitud.descripcion_problema,
        'fecha_creacion': solicitud.fecha_creacion,
        'estado': solicitud.estado.nombre,
        'ordenes_trabajo': []
    }
    for ot in ordenes_trabajo:
        try:
            cierre_ot = CierreOt.objects.get(orden_trabajo=ot)
            data['ordenes_trabajo'].append({
                'tecnico_asignado': ot.tecnico_asignado,
                'estado__nombre': ot.estado.nombre,
                'fecha_actividad': ot.fecha_actividad,
                'causa_falla': cierre_ot.causa_falla,
                'correo_tecnico': cierre_ot.correo_tecnico,
                'descripcion_falla': cierre_ot.descripcion_falla,
                'documento_tecnico': cierre_ot.documento_tecnico.url if cierre_ot.documento_tecnico else None,
                'fecha_inicio_actividad': cierre_ot.fecha_inicio_actividad,
                'hora_fin': cierre_ot.hora_fin,
                'hora_inicio': cierre_ot.hora_inicio,
                'materiales_utilizados': cierre_ot.materiales_utilizados,
                'nombre_tecnico': cierre_ot.nombre_tecnico,
                'observaciones': cierre_ot.observaciones,
                'tipo_intervencion': cierre_ot.tipo_intervencion,
                'tipo_mantenimiento': cierre_ot.tipo_mantenimiento,
            })
        except CierreOt.DoesNotExist:
            data['ordenes_trabajo'].append({
                'tecnico_asignado': ot.tecnico_asignado,
                'estado__nombre': ot.estado.nombre,
                'fecha_actividad': ot.fecha_actividad,
                # Otros campos de OrdenTrabajo que sean necesarios
            })
    
    return JsonResponse(data, encoder=CustomDjangoJSONEncoder)
