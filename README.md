# Backend - Catálogo Makyp

Backend del catálogo de `makyp_creations`.

Este proyecto se encarga de la autenticación administrativa, la gestión de productos, adicionales, categorías e imágenes del catálogo.

## Tecnologías

- Django
- Django REST Framework
- PostgreSQL

## Qué incluye

- login para administrador
- CRUD de productos
- CRUD de adicionales
- categorías para el catálogo
- manejo de imágenes
- API para el catálogo público y el panel admin

## Ejecutarlo en local

```bash
python -m venv venv
venv\\Scripts\\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Nota

La conexión a base de datos se maneja por variables de entorno. En producción está preparado para desplegarse en Railway.
