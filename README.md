# Planifico mi Municipio - MVP

Aplicativo base para una encuesta geoespacial participativa orientada al PAD municipal.

## 1. Qué incluye

- Formulario web para registrar problemas y propuestas ciudadanas.
- Mapa interactivo con Leaflet para seleccionar coordenadas.
- Base de datos PostgreSQL/PostGIS mediante GeoDjango.
- Verificación humana con Cloudflare Turnstile.
- Administración interna en Django Admin.
- Mapa público con registros revisados y publicados.
- Publicación anónima: los datos personales no se muestran en el mapa público.

## 2. Requisitos en Windows sin Docker

Instalar:

1. Python 3.12 o superior.
2. PostgreSQL con PostGIS.
3. OSGeo4W para disponer de GDAL/GEOS/PROJ si GeoDjango lo requiere en Windows.
4. Git opcional.

## 3. Crear base de datos

Desde pgAdmin o psql, ejecutar:

```sql
CREATE DATABASE planifico_municipio;
```

Luego conectarse a `planifico_municipio` y ejecutar:

```sql
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS postgis_topology;
```

## 4. Crear entorno de desarrollo

En PowerShell, dentro de la carpeta del proyecto:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env
```

Editar `.env` con los datos reales de PostgreSQL.

## 5. Ejecutar migraciones

```powershell
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata categorias_iniciales
python manage.py createsuperuser
python manage.py runserver
```

Abrir:

- Encuesta: http://127.0.0.1:8000/
- Mapa público: http://127.0.0.1:8000/mapa/
- Administración: http://127.0.0.1:8000/admin/

## 6. Publicar aportes en el mapa

Los registros entran con estado `En revisión`. Para que aparezcan en el mapa público:

1. Entrar al admin.
2. Abrir “Registros de encuesta”.
3. Seleccionar registros válidos.
4. Usar la acción “Publicar registros seleccionados”.

## 7. Activar Cloudflare Turnstile

Crear un sitio en Cloudflare Turnstile y copiar:

- `TURNSTILE_SITE_KEY`
- `TURNSTILE_SECRET_KEY`

Pegar esos valores en `.env`.

En desarrollo, si no se configuran las claves, el sistema permite registrar pruebas. En producción, configurar las claves es obligatorio.

## 8. Recomendaciones para pasar de MVP a producción

- Usar HTTPS.
- Configurar `DEBUG=False`.
- Configurar dominio real en `ALLOWED_HOSTS`.
- Activar Turnstile obligatoriamente.
- Crear backups automáticos de PostgreSQL.
- Implementar límite por IP, barrio o intervalo de tiempo.
- Crear dashboard de análisis: cantidad de aportes por categoría, distrito, prioridad y fecha.
- Agregar exportación GeoJSON, CSV y conexión directa a QGIS.
- Incorporar límites distritales y validación de punto dentro del municipio.
