from django.db import models


class CuestionarioGobernanza(models.Model):
    RESPUESTA_CHOICES = [
        (1, "Nunca"),
        (2, "Casi nunca"),
        (3, "A veces"),
        (4, "Casi siempre"),
        (5, "Siempre"),
    ]

    TIPO_ENTIDAD_CHOICES = [
        ("GAD", "Gobierno Autónomo Departamental - GAD"),
        ("GAM", "Gobierno Autónomo Municipal - GAM"),
        ("GAR", "Gobierno Autónomo Regional - GAR"),
        ("GAIOC", "Gobierno Autónomo Indígena Originario Campesino - GAIOC"),
        ("OTRO", "Otro"),
    ]

    TIPO_ACTOR_CHOICES = [
        ("Organización social", "Organización social"),
        ("Control social", "Control social"),
        ("Institución pública", "Institución pública"),
        ("Institución privada", "Institución privada"),
        ("Ciudadanía", "Ciudadanía"),
        ("Servidor público", "Servidor público"),
        ("Otro", "Otro"),
    ]

    fecha_registro = models.DateTimeField(auto_now_add=True)

    tipo_entidad = models.CharField(
        "Tipo de entidad",
        max_length=20,
        choices=TIPO_ENTIDAD_CHOICES,
        default="GAM",
    )
    entidad_evaluada = models.CharField(
        "Entidad evaluada",
        max_length=180,
        default="Gobierno Autónomo Municipal de Sacaba",
    )
    distrito = models.CharField("Distrito / ámbito territorial", max_length=120, blank=True)
    tipo_actor = models.CharField("Tipo de actor que responde", max_length=80, choices=TIPO_ACTOR_CHOICES)
    nombre_actor = models.CharField("Organización / institución / persona", max_length=180, blank=True)
    cargo_referencial = models.CharField("Cargo o representación", max_length=160, blank=True)

    # Transparencia
    q01_acceso_informacion = models.PositiveSmallIntegerField(
        "¿Las instituciones ponen a disposición del público información sobre su presupuesto y actividades?",
        choices=RESPUESTA_CHOICES,
    )
    q02_disponibilidad_informacion = models.PositiveSmallIntegerField(
        "¿Los ciudadanos pueden acceder fácilmente a información sobre programas y proyectos institucionales?",
        choices=RESPUESTA_CHOICES,
    )

    # Rendición de cuentas
    q03_informes = models.PositiveSmallIntegerField(
        "¿Las instituciones presentan informes públicos sobre su gestión en el sistema de rendición pública de cuentas SITPRECO?",
        choices=RESPUESTA_CHOICES,
    )
    q04_explicacion_decisiones = models.PositiveSmallIntegerField(
        "¿Las autoridades explican públicamente las decisiones que toman?",
        choices=RESPUESTA_CHOICES,
    )
    q05_cumplimiento_compromisos = models.PositiveSmallIntegerField(
        "¿Las instituciones cumplen los compromisos anunciados o asumidos?",
        choices=RESPUESTA_CHOICES,
    )

    # Participación ciudadana
    q06_espacios_participacion = models.PositiveSmallIntegerField(
        "¿Las instituciones generan espacios para que los ciudadanos participen en decisiones públicas?",
        choices=RESPUESTA_CHOICES,
    )
    q07_participacion_social = models.PositiveSmallIntegerField(
        "¿Los ciudadanos participan en reuniones o consultas institucionales?",
        choices=RESPUESTA_CHOICES,
    )
    q08_influencia_ciudadana = models.PositiveSmallIntegerField(
        "¿El Control Social participa activamente y apoya la gestión, fomentando la transparencia y la rendición pública de cuentas?",
        choices=RESPUESTA_CHOICES,
    )

    # Planificación
    q09_cumplimiento_objetivos_metas = models.PositiveSmallIntegerField(
        "¿Se cumplen los objetivos y las metas establecidas en los planes territoriales?",
        choices=RESPUESTA_CHOICES,
    )
    q10_organizacion_programas_proyectos = models.PositiveSmallIntegerField(
        "¿Los programas y proyectos institucionales se implementan de acuerdo a los procesos de planificación?",
        choices=RESPUESTA_CHOICES,
    )
    q11_seguimiento_evaluacion = models.PositiveSmallIntegerField(
        "¿Se realiza seguimiento y evaluación a los proyectos o programas con participación de los actores?",
        choices=RESPUESTA_CHOICES,
    )

    observaciones = models.TextField("Observaciones", blank=True)

    class Meta:
        verbose_name = "Cuestionario de gobernanza"
        verbose_name_plural = "Cuestionarios de gobernanza"
        ordering = ["-fecha_registro"]

    def __str__(self):
        return f"{self.entidad_evaluada} - {self.fecha_registro:%d/%m/%Y %H:%M}"

    @property
    def puntaje_total(self):
        campos = [
            self.q01_acceso_informacion,
            self.q02_disponibilidad_informacion,
            self.q04_explicacion_decisiones,
            self.q05_cumplimiento_compromisos,
            self.q06_espacios_participacion,
            self.q07_participacion_social,
            self.q08_influencia_ciudadana,
            self.q09_cumplimiento_objetivos_metas,
            self.q10_organizacion_programas_proyectos,
            self.q11_seguimiento_evaluacion,
        ]
        return sum(v for v in campos if v is not None)

    @property
    def promedio(self):
        return round(self.puntaje_total / 10, 2)

    @property
    def nivel_gobernanza(self):
        total = self.puntaje_total
        if total <= 18:
            return "Muy bajo"
        if total <= 26:
            return "Bajo"
        if total <= 34:
            return "Medio"
        if total <= 42:
            return "Alto"
        return "Muy alto"
