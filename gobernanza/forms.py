from django import forms
from .models import CuestionarioGobernanza


class CuestionarioGobernanzaForm(forms.ModelForm):
    class Meta:
        model = CuestionarioGobernanza
        fields = [
            "tipo_actor",
            "nombre_actor",
            "q01_acceso_informacion",
            "q02_disponibilidad_informacion",
            "q04_explicacion_decisiones",
            "q05_cumplimiento_compromisos",
            "q06_espacios_participacion",
            "q07_participacion_social",
            "q08_influencia_ciudadana",
            "q09_cumplimiento_objetivos_metas",
            "q10_organizacion_programas_proyectos",
            "q11_seguimiento_evaluacion",
            "observaciones",
        ]

        widgets = {
            "tipo_actor": forms.Select(attrs={"class": "form-control"}),
            "nombre_actor": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ej. OTB, junta vecinal, institución, organización social"
            }),
            "observaciones": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if name.startswith("q"):
                field.widget = forms.RadioSelect(
                    choices=CuestionarioGobernanza.RESPUESTA_CHOICES,
                    attrs={"class": "radio-gobernanza"}
                )
