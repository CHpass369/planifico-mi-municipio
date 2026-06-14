from django import forms
from .models import RegistroEncuesta, CategoriaProblema


class RegistroEncuestaForm(forms.ModelForm):
    GENERO_CHOICES = [
        ('', 'Selecciona una opción'),
        ('femenino', 'Femenino'),
        ('masculino', 'Masculino'),
        ('otro', 'Otro'),
    ]

    genero = forms.ChoiceField(
        choices=GENERO_CHOICES,
        required=False,
        widget=forms.Select()
    )

    class Meta:
        model = RegistroEncuesta

        fields = [
            'tipo_registro',
            'relacion_municipio',
            'tipo_actor',
            'edad_rango',
            'genero',
            'distrito',
            'otb_junta_vecinal',
            'categoria',
            'descripcion_problema',
            'propuesta_mejora',
            'accion_tipo',
            'plazo_ejecucion',
            'responsable_sugerido',
            'prioridad',
            'personas_afectadas',
            'frecuencia_ocurre',
            'modelo_ciudad_prioridad_1',
            'modelo_ciudad_prioridad_2',
            'modelo_ciudad_prioridad_3',
            'modelo_ciudad_deseada',
            'lon',
            'lat',
            'consentimiento_datos',
            'acepta_publicacion_anonima',
        ]

        widgets = {
            'tipo_registro': forms.HiddenInput(),
            'prioridad': forms.HiddenInput(),
            'lon': forms.HiddenInput(),
            'lat': forms.HiddenInput(),
            'modelo_ciudad_prioridad_1': forms.HiddenInput(),
            'modelo_ciudad_prioridad_2': forms.HiddenInput(),
            'modelo_ciudad_prioridad_3': forms.HiddenInput(),

            'descripcion_problema': forms.Textarea(attrs={
                'rows': 5,
                'maxlength': 1000,
                'placeholder': 'Cuéntanos con más detalle qué ocurre, dónde ocurre y a quién afecta.'
            }),

            'propuesta_mejora': forms.Textarea(attrs={
                'rows': 5,
                'maxlength': 1000,
                'placeholder': 'Escribe tu propuesta de solución aquí.'
            }),

            'modelo_ciudad_deseada': forms.Textarea(attrs={
                'rows': 6,
                'maxlength': 600,
                'placeholder': 'Ej.: Un Sacaba ordenado, verde y productivo, con oportunidades para todas y todos.'
            }),

            'responsable_sugerido': forms.TextInput(attrs={
                'placeholder': 'Ej.: Gobierno Municipal, OTB, vecinos, empresa de servicios...'
            }),

            'otb_junta_vecinal': forms.TextInput(attrs={
                'placeholder': 'Escribe aquí'
            }),

            'personas_afectadas': forms.NumberInput(attrs={
                'placeholder': 'Ej.: 150',
                'min': 1
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Consentimientos ocultos / no visibles en la encuesta
        if "consentimiento_datos" in self.fields:
            self.fields["consentimiento_datos"].required = False
        if "acepta_publicacion_anonima" in self.fields:
            self.fields["acepta_publicacion_anonima"].required = False

        # Opciones oficiales de distrito para la encuesta PAD
        distrito_choices_pad = [
            ("", "Selecciona tu distrito"),
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
            ("Fuera del Municipio", "Ninguno, fuera del Municipio."),
        ]

        if "distrito" in self.fields:
            self.fields["distrito"].required = True
            self.fields["distrito"].choices = distrito_choices_pad
            self.fields["distrito"].widget = forms.Select(
                choices=distrito_choices_pad,
                attrs={
                    "class": "form-select",
                }
            )

        # Categorías PAD con emojis
        if "categoria" in self.fields:
            campos_categoria = {f.name for f in CategoriaProblema._meta.fields}
            qs_categoria = CategoriaProblema.objects.all()

            if "activo" in campos_categoria:
                qs_categoria = qs_categoria.filter(activo=True)

            if "orden" in campos_categoria:
                qs_categoria = qs_categoria.order_by("orden", "nombre")
            else:
                qs_categoria = qs_categoria.order_by("nombre")

            self.fields["categoria"].queryset = qs_categoria
            self.fields["categoria"].empty_label = "Selecciona el ámbito o problema identificado"
            self.fields["categoria"].label_from_instance = (
                lambda obj: f"{getattr(obj, 'icono', '')} {obj.nombre}".strip()
            )
