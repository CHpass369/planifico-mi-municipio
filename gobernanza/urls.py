from django.urls import path
from . import views

app_name = "gobernanza"

urlpatterns = [
    path("", views.cuestionario_gobernanza, name="cuestionario"),
    path("gracias/", views.gracias_gobernanza, name="gracias"),
]
