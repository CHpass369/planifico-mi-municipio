import uuid
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.core.validators import MaxValueValidator, MinValueValidator, FileExtensionValidator


class CategoriaProblema(models.Model):
    nombre = models.CharField(max_length=120, unique=True)
    descripcion = models.TextField(blank=True)
    color_hex = models.CharField(max_length=7, default='#2E7D32')
    icono = models.CharField(max_length=60, blank=True, help_text='Ej.: salud, educación, seguridad, movilidad')
    activo = models.BooleanField(default=True)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['orden', 'nombre']
        verbose_name = 'Categoría de problema/propuesta'
        verbose_name_plural = 'Categorías de problemas/propuestas'

    def __str__(self):
        return self.nombre


class RegistroEncuesta(models.Model):
    TIPO_CHOICES = [
        ('problema', 'Problema'),
        ('propuesta', 'Propuesta'),
        ('problema_propuesta', 'Problema y propuesta'),
    ]

    ESTADO_CHOICES = [
        ('revision', 'En revisión'),
        ('publicado', 'Publicado'),
        ('descartado', 'Descartado'),
    ]

    PRIORIDAD_CHOICES = [
        (1, 'Baja'),
        (2, 'Media'),
        (3, 'Alta'),
        (4, 'Muy alta'),
    ]

    EDAD_CHOICES = [
        ('menor_15', 'Menor de 15 años'),
        ('15_18', '15 a 18 años'),
        ('19_28', '19 a 28 años'),
        ('29_39', '29 a 39 años'),
        ('40_59', '40 a 59 años'),
        ('60_mas', '60 años o más'),
        ('prefiere_no_decir', 'Prefiere no decir'),
    ]

    RELACION_CHOICES = [
        ('vive', 'Vivo en el municipio'),
        ('trabaja', 'Trabajo en el municipio'),
        ('estudia', 'Estudio en el municipio'),
        ('visita', 'Visito frecuentemente el municipio'),
        ('otro', 'Otra relación'),
    ]

    ACTOR_CHOICES = [
        ('vecino', 'Vecino/a'),
        ('dirigente', 'Dirigente OTB/Junta vecinal'),
        ('comerciante', 'Comerciante'),
        ('transportista', 'Transportista'),
        ('estudiante', 'Estudiante'),
        ('servidor_publico', 'Servidor/a público'),
        ('organizacion_social', 'Organización social'),
        ('otro', 'Otro'),
    ]

    ACCION_CHOICES = [
        ('obra', 'Obra o infraestructura'),
        ('mantenimiento', 'Mantenimiento'),
        ('gestion_servicio', 'Gestión o mejora de servicio'),
        ('normativa_control', 'Normativa, control o fiscalización'),
        ('programa_social', 'Programa social/comunitario'),
        ('educacion_sensibilizacion', 'Educación o sensibilización'),
        ('otro', 'Otro'),
    ]

    PLAZO_CHOICES = [
        ('corto', 'Corto plazo: 0 a 1 año'),
        ('mediano', 'Mediano plazo: 1 a 3 años'),
        ('largo', 'Largo plazo: 3 a 5 años'),
        ('permanente', 'Acción permanente'),
    ]

    FRECUENCIA_CHOICES = [
        ('diario', 'Todos los días'),
        ('semanal', 'Varias veces por semana'),
        ('mensual', 'Algunas veces al mes'),
        ('ocasional', 'Ocasionalmente'),
        ('permanente', 'Es un problema permanente'),
    ]

    MODELO_CIUDAD_CHOICES = [
        ('compacta', 'Compacta'),
        ('proximidad_15min', 'De 15 minutos'),
        ('verde', 'Verde'),
        ('resiliente', 'Resiliente'),
        ('segura', 'Segura'),
        ('inclusiva', 'Inclusiva'),
        ('productiva', 'Productiva'),
        ('educadora', 'Educadora'),
        ('inteligente', 'Inteligente'),
        ('conectada', 'Conectada'),
        ('transparente', 'Transparente'),
        ('cultural', 'Cultural'),
    ]

    codigo_publico = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    tipo_registro = models.CharField(max_length=20, choices=TIPO_CHOICES, default='problema_propuesta')
    categoria = models.ForeignKey(CategoriaProblema, on_delete=models.PROTECT, related_name='registros')

    relacion_municipio = models.CharField(max_length=40, choices=RELACION_CHOICES, blank=True)
    tipo_actor = models.CharField(max_length=40, choices=ACTOR_CHOICES, blank=True)

    descripcion_problema = models.TextField(blank=True, verbose_name='Descripción del problema')
    titulo_problema = models.CharField(max_length=160, blank=True, verbose_name='Título breve del problema')
    propuesta_mejora = models.TextField(blank=True, verbose_name='Propuesta de solución')

    accion_tipo = models.CharField(max_length=40, choices=ACCION_CHOICES, blank=True)
    plazo_ejecucion = models.CharField(max_length=40, choices=PLAZO_CHOICES, blank=True)
    responsable_sugerido = models.CharField(max_length=160, blank=True)

    prioridad = models.PositiveSmallIntegerField(choices=PRIORIDAD_CHOICES, default=2)
    personas_afectadas = models.PositiveIntegerField(blank=True, null=True)
    frecuencia_ocurre = models.CharField(max_length=40, choices=FRECUENCIA_CHOICES, blank=True)

    modelo_ciudad_prioridad_1 = models.CharField(max_length=40, choices=MODELO_CIUDAD_CHOICES, blank=True)
    modelo_ciudad_prioridad_2 = models.CharField(max_length=40, choices=MODELO_CIUDAD_CHOICES, blank=True)
    modelo_ciudad_prioridad_3 = models.CharField(max_length=40, choices=MODELO_CIUDAD_CHOICES, blank=True)

    modelo_ciudad_deseada = models.TextField(
        blank=True,
        verbose_name='Visión al 2030',
        help_text='Describe cómo imaginas el municipio que deseas construir hacia el año 2030.'
    )

    distrito = models.CharField(max_length=80, blank=True)
    otb_junta_vecinal = models.CharField(max_length=150, blank=True)
    direccion_referencia = models.CharField(max_length=200, blank=True)

    edad_rango = models.CharField(max_length=30, choices=EDAD_CHOICES, blank=True)
    genero = models.CharField(max_length=40, blank=True)

    lon = models.FloatField(validators=[MinValueValidator(-180), MaxValueValidator(180)])
    lat = models.FloatField(validators=[MinValueValidator(-90), MaxValueValidator(90)])
    geom = models.PointField(srid=4326, spatial_index=True, blank=True, null=True)

    consentimiento_datos = models.BooleanField(default=False)
    acepta_publicacion_anonima = models.BooleanField(default=False)

    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='revision')
    observacion_moderacion = models.TextField(blank=True)

    ip_hash = models.CharField(max_length=128, blank=True)
    user_agent_hash = models.CharField(max_length=128, blank=True)
    turnstile_verified = models.BooleanField(default=False)

    class Meta:
        ordering = ['-fecha_registro']
        indexes = [
            models.Index(fields=['estado', 'tipo_registro']),
            models.Index(fields=['fecha_registro']),
        ]
        verbose_name = 'Registro de encuesta'
        verbose_name_plural = 'Registros de encuesta'

    def save(self, *args, **kwargs):
        if self.lon is not None and self.lat is not None:
            self.geom = Point(self.lon, self.lat, srid=4326)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.get_tipo_registro_display()} - {self.categoria} - {self.fecha_registro:%Y-%m-%d}'


class RegistroEvidencia(models.Model):
    registro = models.ForeignKey(
        RegistroEncuesta,
        on_delete=models.CASCADE,
        related_name='evidencias'
    )

    imagen = models.ImageField(
        upload_to='evidencias/%Y/%m/',
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'])]
    )

    orden = models.PositiveSmallIntegerField(default=1)
    fecha_carga = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['orden', 'id']
        verbose_name = 'Evidencia fotográfica'
        verbose_name_plural = 'Evidencias fotográficas'

    def __str__(self):
        return f'Evidencia {self.orden} - {self.registro.codigo_publico}'

class FechaSocializacionPAD(models.Model):
    DISTRITO_CHOICES = [
        ("Distrito 1", "Distrito 1"),
        ("Distrito 2", "Distrito 2"),
        ("Distrito 3", "Distrito 3"),
        ("Distrito 4", "Distrito 4"),
        ("Distrito 5", "Distrito 5"),
        ("Distrito 6", "Distrito 6"),
        ("Distrito 7", "Distrito 7"),
        ("Distrito Lava Lava", "Distrito Lava Lava"),
        ("Distrito Ucuchi", "Distrito Ucuchi"),
        ("Distrito Aguirre", "Distrito Aguirre"),
        ("Distrito Palca", "Distrito Palca"),
        ("Municipal", "Nivel municipal"),
        ("Otro", "Otro"),
    ]

    TIPO_ACTOR_CHOICES = [
        ("Organización social", "Organización social"),
        ("Institución pública", "Institución pública"),
        ("Institución privada", "Institución privada"),
        ("Público general", "Público general"),
        ("Mixto", "Mixto"),
        ("Otro", "Otro"),
    ]

    fecha = models.DateField("Fecha de socialización")
    hora_inicio = models.TimeField("Hora de inicio", blank=True, null=True)
    hora_fin = models.TimeField("Hora de finalización", blank=True, null=True)

    distrito = models.CharField("Distrito", max_length=80, choices=DISTRITO_CHOICES)
    tipo_actor = models.CharField("Tipo de actor", max_length=80, choices=TIPO_ACTOR_CHOICES)

    nombre_actor = models.CharField(
        "Organización social / institución / actor convocado",
        max_length=220
    )

    motivo = models.TextField("Motivo de la reunión / socialización")
    lugar = models.CharField("Lugar de reunión", max_length=220, blank=True)
    responsable = models.CharField("Responsable municipal", max_length=180, blank=True)
    observaciones = models.TextField("Observaciones", blank=True)

    activo = models.BooleanField("Visible en el cronograma", default=True)

    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Fecha de socialización PAD"
        verbose_name_plural = "Fechas de socialización PAD"
        ordering = ["fecha", "hora_inicio", "distrito"]

    def __str__(self):
        hora = self.hora_inicio.strftime("%H:%M") if self.hora_inicio else "Sin hora"
        return f"{self.fecha} - {hora} - {self.distrito} - {self.nombre_actor}"
