import json
import requests
import re
import unicodedata
from collections import Counter

from django.conf import settings
from django.contrib import messages
from django.contrib.gis.geos import Point
from django.core.serializers.json import DjangoJSONEncoder
from django.db import transaction
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET

from .forms import RegistroEncuestaForm
from .models import RegistroEncuesta, RegistroEvidencia
from .utils import get_client_ip, sha256_text, verify_turnstile


SACABA_CENTER = {
    "lat": -17.4038897,
    "lon": -66.0402024,
    "zoom": 17,
}


STOPWORDS = {
    "para", "como", "este", "esta", "estos", "estas", "desde", "donde",
    "sobre", "entre", "hacia", "hasta", "tambien", "también", "porque",
    "municipio", "ciudad", "sacaba", "quiero", "queremos", "debe", "deben",
    "tener", "hacer", "mejor", "mejorar", "mas", "más", "con", "sin",
    "una", "uno", "unos", "unas", "los", "las", "del", "que", "por",
    "hay", "sea", "ser", "son", "sus", "eso", "esa", "ese", "muy",
    "todo", "toda", "todos", "todas", "anos", "años", "proximos", "próximos",
}


def inicio(request):
    publicados = RegistroEncuesta.objects.filter(estado="publicado").count()
    total = RegistroEncuesta.objects.count()
    revision = RegistroEncuesta.objects.filter(estado="revision").count()
    distritos_participacion = (
        RegistroEncuesta.objects
        .exclude(distrito="")
        .values("distrito")
        .distinct()
        .count()
    )

    return render(request, "encuestas/inicio.html", {
        "total": total,
        "publicados": publicados,
        "revision": revision,
        "distritos_participacion": distritos_participacion,
    })


def _turnstile_ok(request, ip):
    """
    En desarrollo local no bloquea el guardado.
    En producción, cuando DEBUG=False, valida Turnstile normalmente.
    """
    if settings.DEBUG:
        return True, "Verificación omitida en desarrollo local."

    site_key = getattr(settings, "TURNSTILE_SITE_KEY", "")
    secret_key = getattr(settings, "TURNSTILE_SECRET_KEY", "")
    token = request.POST.get("cf-turnstile-response", "")

    if not site_key or not secret_key:
        return True, "Turnstile no configurado."

    if not token:
        return False, "No se recibió el token de verificación humana."

    try:
        return verify_turnstile(token, ip)
    except Exception:
        return False, "No se pudo verificar que la participación sea realizada por una persona."


def encuesta_create(request):
    if request.method == "POST":
        post_data = request.POST.copy()
        post_data["consentimiento_datos"] = "on"
        post_data["acepta_publicacion_anonima"] = "on"
        form = RegistroEncuestaForm(post_data, request.FILES)
        ip = get_client_ip(request)
        evidencias = request.FILES.getlist("evidencias")

        archivos_validos = True
        errores_extra = []

        is_human, turnstile_message = _turnstile_ok(request, ip)

        if not is_human:
            errores_extra.append(turnstile_message)

        if len(evidencias) > 3:
            archivos_validos = False
            errores_extra.append("Solo puedes subir hasta 3 fotografías.")

        for archivo in evidencias:
            if archivo.size > 5 * 1024 * 1024:
                archivos_validos = False
                errores_extra.append("Cada fotografía debe pesar como máximo 5 MB.")

            if not archivo.content_type.startswith("image/"):
                archivos_validos = False
                errores_extra.append("Solo se permiten archivos de imagen.")

        form_valido = form.is_valid()

        for error in errores_extra:
            form.add_error(None, error)

        if form_valido and archivos_validos and is_human:
            with transaction.atomic():
                registro = form.save(commit=False)

                registro.tipo_registro = "problema_propuesta"
                registro.ip_hash = sha256_text(ip)
                registro.user_agent_hash = sha256_text(
                    request.META.get("HTTP_USER_AGENT", "")
                )
                registro.turnstile_verified = is_human
                registro.estado = "revision"

                if registro.lat is not None and registro.lon is not None:
                    registro.geom = Point(
                        float(registro.lon),
                        float(registro.lat),
                        srid=4326
                    )

                registro.save()

                for index, archivo in enumerate(evidencias[:3], start=1):
                    RegistroEvidencia.objects.create(
                        registro=registro,
                        imagen=archivo,
                        orden=index
                    )

            return redirect(
                "encuestas:gracias",
                codigo_publico=registro.codigo_publico
            )

        print("ERRORES DEL FORMULARIO:")
        print(form.errors.as_json())
        print("ERRORES NO ASOCIADOS A CAMPOS:")
        print(form.non_field_errors())

        messages.error(
            request,
            "No se pudo guardar la participación. Revisa los campos observados."
        )

    else:
        form = RegistroEncuestaForm(initial={
            "tipo_registro": "problema_propuesta"
        })

    return render(request, "encuestas/encuesta_form.html", {
        "form": form, "turnstile_site_key": getattr(settings, "TURNSTILE_SITE_KEY", ""),
        "map_center": SACABA_CENTER,
    })


def gracias(request, codigo_publico):
    return render(request, "encuestas/gracias.html", {
        "codigo_publico": codigo_publico,
    })


def resultados(request):
    return render(request, "encuestas/resultados.html", {
        "map_center": SACABA_CENTER,
    })


def modelo_ciudad(request):
    return render(request, "encuestas/modelo_ciudad.html")


def ayuda(request):
    return render(request, "encuestas/ayuda.html")


@require_GET
def registros_geojson(request):
    registros = (
        RegistroEncuesta.objects
        .select_related("categoria")
        .filter(estado="publicado")[:5000]
    )

    features = []

    for r in registros:
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [r.lon, r.lat],
            },
            "properties": {
                "codigo": str(r.codigo_publico),
                "fecha": r.fecha_registro.strftime("%Y-%m-%d"),
                "tipo": r.get_tipo_registro_display(),
                "categoria": r.categoria.nombre,
                "color": r.categoria.color_hex,
                "prioridad": r.get_prioridad_display(),
                "distrito": r.distrito,
                "otb_junta_vecinal": r.otb_junta_vecinal,
                "referencia": r.direccion_referencia,
                "problema": r.descripcion_problema[:500],
                "propuesta": r.propuesta_mejora[:500],
                "modelo_ciudad": r.modelo_ciudad_deseada[:500],
            }
        })

    return JsonResponse(
        {
            "type": "FeatureCollection",
            "features": features,
        },
        encoder=DjangoJSONEncoder
    )


def normalize_text(text):
    text = text.lower()
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    return text


def generar_nube_palabras():
    textos = (
        RegistroEncuesta.objects
        .filter(estado="publicado")
        .exclude(modelo_ciudad_deseada="")
        .values_list("modelo_ciudad_deseada", flat=True)
    )

    contador = Counter()

    for texto in textos:
        limpio = normalize_text(texto)
        palabras = re.findall(
            r"\b[a-záéíóúñü]{4,}\b",
            limpio,
            flags=re.IGNORECASE
        )

        for palabra in palabras:
            if palabra not in STOPWORDS:
                contador[palabra] += 1

    top = contador.most_common(50)

    if not top:
        return []

    max_count = top[0][1]

    nube = []

    for palabra, total in top:
        size = 16 + int((total / max_count) * 34)

        nube.append({
            "text": palabra,
            "count": total,
            "size": size,
        })

    return nube


@require_GET
def estadisticas_json(request):
    publicados = RegistroEncuesta.objects.filter(estado="publicado")
    total_publicados = publicados.count()
    total_registrados = RegistroEncuesta.objects.count()
    total_revision = RegistroEncuesta.objects.filter(estado="revision").count()

    por_categoria = list(
        publicados
        .values("categoria__nombre", "categoria__color_hex")
        .annotate(total=Count("id"))
        .order_by("-total")
    )

    por_tipo_raw = list(
        publicados
        .values("tipo_registro")
        .annotate(total=Count("id"))
        .order_by("-total")
    )

    tipo_labels = dict(RegistroEncuesta.TIPO_CHOICES)

    por_tipo = [
        {
            "nombre": tipo_labels.get(item["tipo_registro"], item["tipo_registro"]),
            "total": item["total"],
        }
        for item in por_tipo_raw
    ]

    por_prioridad_raw = list(
        publicados
        .values("prioridad")
        .annotate(total=Count("id"))
        .order_by("prioridad")
    )

    prioridad_labels = dict(RegistroEncuesta.PRIORIDAD_CHOICES)

    por_prioridad = [
        {
            "nombre": prioridad_labels.get(item["prioridad"], str(item["prioridad"])),
            "total": item["total"],
        }
        for item in por_prioridad_raw
    ]

    por_distrito = list(
        publicados
        .exclude(distrito="")
        .values("distrito")
        .annotate(total=Count("id"))
        .order_by("-total")[:20]
    )

    modelo_total = (
        publicados
        .exclude(modelo_ciudad_deseada="")
        .count()
    )

    nube = generar_nube_palabras()

    return JsonResponse({
        "total_registrados": total_registrados,
        "total_publicados": total_publicados,
        "total_revision": total_revision,
        "modelo_total": modelo_total,
        "por_categoria": por_categoria,
        "por_tipo": por_tipo,
        "por_prioridad": por_prioridad,
        "por_distrito": por_distrito,
        "nube_palabras": nube,
    })
def cronograma_pad(request):
    """
    Página interactiva del cronograma de actividades para la elaboración del PAD.
    Incluye calendario de fechas de socialización.
    """
    from .models import FechaSocializacionPAD

    socializaciones = []

    try:
        socializaciones_qs = FechaSocializacionPAD.objects.filter(activo=True).order_by(
            "fecha", "hora_inicio", "distrito"
        )

        for item in socializaciones_qs:
            socializaciones.append({
                "id": item.id,
                "fecha": item.fecha.isoformat(),
                "hora_inicio": item.hora_inicio.strftime("%H:%M") if item.hora_inicio else "",
                "hora_fin": item.hora_fin.strftime("%H:%M") if item.hora_fin else "",
                "distrito": item.distrito,
                "tipo_actor": item.tipo_actor,
                "nombre_actor": item.nombre_actor,
                "motivo": item.motivo,
                "lugar": item.lugar,
                "responsable": item.responsable,
                "observaciones": item.observaciones,
            })
    except Exception:
        socializaciones = []

    return render(request, "encuestas/cronograma_pad.html", {
        "socializaciones_json": json.dumps(socializaciones, cls=DjangoJSONEncoder),
        "es_superuser": request.user.is_authenticated and request.user.is_superuser,
    })



def socializaciones_pad_json(request):
    """
    API pública de consulta para el calendario de socializaciones PAD.
    La edición se realiza únicamente desde Django Admin.
    """
    from .models import FechaSocializacionPAD

    items = []

    try:
        qs = FechaSocializacionPAD.objects.filter(activo=True).order_by(
            "fecha", "hora_inicio", "distrito"
        )

        for item in qs:
            items.append({
                "id": item.id,
                "fecha": item.fecha.isoformat(),
                "hora_inicio": item.hora_inicio.strftime("%H:%M") if item.hora_inicio else "",
                "hora_fin": item.hora_fin.strftime("%H:%M") if item.hora_fin else "",
                "distrito": item.distrito,
                "tipo_actor": item.tipo_actor,
                "nombre_actor": item.nombre_actor,
                "motivo": item.motivo,
                "lugar": item.lugar,
                "responsable": item.responsable,
                "observaciones": item.observaciones,
            })

        return JsonResponse({
            "ok": True,
            "count": len(items),
            "items": items,
        })

    except Exception as e:
        return JsonResponse({
            "ok": False,
            "count": 0,
            "items": [],
            "error": str(e),
        })


