from django.urls import path

from . import views


app_name = "encuestas"


urlpatterns = [
    path("api/socializaciones-pad.json", views.socializaciones_pad_json, name="socializaciones_pad_json"),
    path("cronograma/", views.cronograma_pad, name="cronograma_pad"),
    path("", views.inicio, name="inicio"),
    path("participa/", views.encuesta_create, name="participa"),
    path("gracias/<uuid:codigo_publico>/", views.gracias, name="gracias"),
    path("resultados/", views.resultados, name="resultados"),
    path("modelo-ciudad/", views.modelo_ciudad, name="modelo_ciudad"),
    path("ayuda/", views.ayuda, name="ayuda"),
    path("api/registros.geojson", views.registros_geojson, name="registros_geojson"),
    path("api/estadisticas.json", views.estadisticas_json, name="estadisticas_json"),
]
