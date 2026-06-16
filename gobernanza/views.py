from django.shortcuts import render, redirect
from .forms import CuestionarioGobernanzaForm


def cuestionario_gobernanza(request):
    if request.method == "POST":
        form = CuestionarioGobernanzaForm(request.POST)
        if form.is_valid():
            registro = form.save(commit=False)

            # Campo eliminado de la interfaz; se guarda un valor neutro interno
            registro.q03_informes = 3

            registro.save()
            request.session["ultimo_puntaje_gobernanza"] = registro.puntaje_total
            request.session["ultimo_nivel_gobernanza"] = registro.nivel_gobernanza
            return redirect("gobernanza:gracias")
    else:
        form = CuestionarioGobernanzaForm()

    grupos = [
        {
            "dimension": "Transparencia",
            "descripcion": "Acceso, disponibilidad y claridad de la información pública institucional.",
            "campos": [
                ("Acceso a información", form["q01_acceso_informacion"]),
                ("Disponibilidad de información", form["q02_disponibilidad_informacion"]),
            ],
        },
        {
            "dimension": "Rendición de cuentas",
            "descripcion": "Información pública sobre gestión, decisiones y cumplimiento de compromisos.",
            "campos": [
                ("Explicación de decisiones", form["q04_explicacion_decisiones"]),
                ("Cumplimiento de compromisos", form["q05_cumplimiento_compromisos"]),
            ],
        },
        {
            "dimension": "Participación ciudadana",
            "descripcion": "Espacios, participación social e influencia ciudadana en la gestión pública.",
            "campos": [
                ("Espacios de participación", form["q06_espacios_participacion"]),
                ("Participación social", form["q07_participacion_social"]),
                ("Influencia ciudadana", form["q08_influencia_ciudadana"]),
            ],
        },
        {
            "dimension": "Planificación",
            "descripcion": "Cumplimiento de metas, organización de programas y seguimiento participativo.",
            "campos": [
                ("Cumplimiento de objetivos y metas", form["q09_cumplimiento_objetivos_metas"]),
                ("Organización de programas y proyectos", form["q10_organizacion_programas_proyectos"]),
                ("Seguimiento y evaluación", form["q11_seguimiento_evaluacion"]),
            ],
        },
    ]

    return render(request, "gobernanza/cuestionario.html", {
        "form": form,
        "grupos": grupos,
    })


def gracias_gobernanza(request):
    puntaje = request.session.pop("ultimo_puntaje_gobernanza", None)
    nivel = request.session.pop("ultimo_nivel_gobernanza", None)

    return render(request, "gobernanza/gracias.html", {
        "puntaje": puntaje,
        "nivel": nivel,
    })
