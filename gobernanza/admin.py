from django.contrib import admin
from .models import CuestionarioGobernanza


@admin.register(CuestionarioGobernanza)
class CuestionarioGobernanzaAdmin(admin.ModelAdmin):
    list_display = (
        "fecha_registro",
        "tipo_entidad",
        "entidad_evaluada",
        "distrito",
        "tipo_actor",
        "nombre_actor",
        "puntaje_total_display",
        "promedio_display",
        "nivel_gobernanza_display",
    )
    list_filter = ("tipo_entidad", "tipo_actor", "distrito", "fecha_registro")
    search_fields = ("entidad_evaluada", "distrito", "nombre_actor", "cargo_referencial")
    date_hierarchy = "fecha_registro"
    readonly_fields = ("puntaje_total_display", "promedio_display", "nivel_gobernanza_display")

    fieldsets = (
        ("Datos generales", {
            "fields": (
                "tipo_entidad",
                "entidad_evaluada",
                "distrito",
                "tipo_actor",
                "nombre_actor",
                "cargo_referencial",
            )
        }),
        ("Transparencia", {
            "fields": (
                "q01_acceso_informacion",
                "q02_disponibilidad_informacion",
            )
        }),
        ("Rendición de cuentas", {
            "fields": (
                "q03_informes",
                "q04_explicacion_decisiones",
                "q05_cumplimiento_compromisos",
            )
        }),
        ("Participación ciudadana", {
            "fields": (
                "q06_espacios_participacion",
                "q07_participacion_social",
                "q08_influencia_ciudadana",
            )
        }),
        ("Planificación", {
            "fields": (
                "q09_cumplimiento_objetivos_metas",
                "q10_organizacion_programas_proyectos",
                "q11_seguimiento_evaluacion",
            )
        }),
        ("Resultado", {
            "fields": (
                "puntaje_total_display",
                "promedio_display",
                "nivel_gobernanza_display",
                "observaciones",
            )
        }),
    )

    def puntaje_total_display(self, obj):
        return obj.puntaje_total
    puntaje_total_display.short_description = "Puntaje total"

    def promedio_display(self, obj):
        return obj.promedio
    promedio_display.short_description = "Promedio"

    def nivel_gobernanza_display(self, obj):
        return obj.nivel_gobernanza
    nivel_gobernanza_display.short_description = "Nivel de gobernanza"
