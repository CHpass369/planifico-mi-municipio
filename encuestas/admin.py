from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin
from .models import CategoriaProblema, RegistroEncuesta, FechaSocializacionPAD


@admin.register(CategoriaProblema)
class CategoriaProblemaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'color_hex', 'icono', 'activo', 'orden')
    list_filter = ('activo',)
    search_fields = ('nombre', 'descripcion')
    ordering = ('orden', 'nombre')


@admin.register(RegistroEncuesta)
class RegistroEncuestaAdmin(GISModelAdmin):
    list_display = ('fecha_registro', 'tipo_registro', 'categoria', 'prioridad', 'distrito', 'estado', 'turnstile_verified')
    list_filter = ('estado', 'tipo_registro', 'categoria', 'prioridad', 'turnstile_verified', 'fecha_registro')
    search_fields = ('descripcion_problema', 'propuesta_mejora', 'distrito', 'otb_junta_vecinal', 'direccion_referencia')
    readonly_fields = ('codigo_publico', 'fecha_registro', 'ip_hash', 'user_agent_hash', 'turnstile_verified', 'geom')
    actions = ['publicar_registros', 'descartar_registros']

    @admin.action(description='Publicar registros seleccionados')
    def publicar_registros(self, request, queryset):
        queryset.update(estado='publicado')

    @admin.action(description='Descartar registros seleccionados')
    def descartar_registros(self, request, queryset):
        queryset.update(estado='descartado')


@admin.register(FechaSocializacionPAD)
class FechaSocializacionPADAdmin(admin.ModelAdmin):
    list_display = (
        "fecha",
        "hora_inicio",
        "hora_fin",
        "distrito",
        "tipo_actor",
        "nombre_actor",
        "responsable",
        "activo",
    )
    list_filter = ("fecha", "distrito", "tipo_actor", "activo")
    search_fields = ("nombre_actor", "motivo", "lugar", "responsable", "distrito")
    date_hierarchy = "fecha"
    ordering = ("fecha", "hora_inicio", "distrito")

    fieldsets = (
        ("Fecha y lugar", {
            "fields": ("fecha", "hora_inicio", "hora_fin", "lugar")
        }),
        ("Actor convocado", {
            "fields": ("distrito", "tipo_actor", "nombre_actor")
        }),
        ("Contenido de la socialización", {
            "fields": ("motivo", "responsable", "observaciones", "activo")
        }),
    )

    def has_module_permission(self, request):
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
