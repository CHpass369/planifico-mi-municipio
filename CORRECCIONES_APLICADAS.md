# Correcciones aplicadas - Planifico mi Municipio

## Archivos corregidos

1. `encuestas/templates/encuestas/encuesta_form.html`
   - Se reconstruyó la estructura del wizard para evitar elementos fuera de la tarjeta.
   - Se corrigió el paso 7 y el paso 8 para que no aparezcan botones o textos externos.
   - El mapa se inicializa recién al entrar al paso 3.
   - El mapa se centra en `-17.4033374, -66.0390759` con zoom 16.
   - Se usa `data-lat`, `data-lon` y `data-zoom` para evitar errores de renderizado.
   - Se agregó soporte estable para GPS, selección de prioridad, modelos de ciudad y revisión final.

2. `encuestas/views.py`
   - Se actualizó `SACABA_CENTER`.

3. `encuestas/static/encuestas/app.css`
   - Se agregaron reglas finales de limpieza para el wizard.
   - Se amplió la tarjeta de encuesta.
   - Se amplió el mapa.
   - Se ocultó definitivamente el campo `id_prioridad`.
   - Se corrigió la visualización de los botones dentro de cada paso.

4. `encuestas/templates/encuestas/base.html`
   - Se agregó cache-busting al CSS: `?v=20260611_fix2`.

5. `encuestas/models.py`
   - Se limpió la indentación del rango de edad.

## Comandos recomendados

```bash
python manage.py check
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

Luego recargar en el navegador con:

```text
Ctrl + F5
```
