-- Ejecutar como usuario postgres desde pgAdmin o psql.
CREATE DATABASE planifico_municipio;

-- Luego conectarse a la base planifico_municipio y ejecutar:
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS postgis_topology;
