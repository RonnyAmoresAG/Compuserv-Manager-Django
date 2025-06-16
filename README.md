
# 🖥️ COMPUSERV - Sistema de Gestión Técnica

Este sistema está desarrollado con Django 5 y PostgreSQL, orquestado con Docker Compose. Permite gestionar servicios técnicos, ventas, facturación, inventario, mensajes y clientes de forma centralizada.

---

## 📦 Requisitos para ejecutar

- Tener **Docker** y **Docker Compose** instalados.
- Tener un archivo `.env` bien configurado.
- Clonar este repositorio o copiar el proyecto completo a otra computadora.

---

## 📄 Variables necesarias (.env)

Debes crear un archivo `.env` en la raíz del proyecto con el siguiente contenido base:

```env
DJANGO_SECRET_KEY=clave_super_secreta_123
DJANGO_DEBUG=True

POSTGRES_DB=sistemadb
POSTGRES_USER=sistemadbuser
POSTGRES_PASSWORD=sistemadbpass
POSTGRES_HOST=db
```

---

## 🚀 Cómo levantar el proyecto desde cero

Sigue estos pasos en orden desde una terminal abierta en la carpeta del proyecto:

```bash
# 1️⃣ Apagar cualquier versión anterior y eliminar volúmenes de base de datos
docker compose down -v

# 2️⃣ Reconstruir los contenedores desde cero sin usar caché
docker compose build --no-cache

# 3️⃣ Levantar los servicios en segundo plano
docker compose up -d

# 4️⃣ Recolectar archivos estáticos (CSS, JS, etc.)
docker compose exec web python manage.py collectstatic --noinput

# 5️⃣ Aplicar migraciones de la base de datos
docker compose exec web python manage.py migrate

# 6️⃣ Crear un usuario administrador
docker compose exec web python manage.py createsuperuser

# 7️⃣ Crear el cliente por defecto "CONSUMIDOR FINAL"
docker compose exec web python manage.py shell -c "from clientes.models import Cliente; Cliente.objects.get_or_create(cedula='9999999999', defaults={'nombre': 'CONSUMIDOR FINAL', 'correo': 'consumidor@final.com', 'telefono': '0000000000', 'direccion': 'NO ESPECIFICADA'})"
```

---

## 🧪 Verificar que DEBUG=True esté activo

Este valor se toma desde el archivo `.env`. Si está correctamente escrito:

```env
DJANGO_DEBUG=True
```

Entonces el entorno funcionará como desarrollo y se mostrará la consola de errores detallada.

---

## 📂 Servir archivos MEDIA solo en desarrollo

Para que los archivos PDF, imágenes y otros subidos funcionen correctamente, añade esto al final del archivo `sistema/urls.py`:

```python
from django.conf import settings
from django.conf.urls.static import static

# 🔁 Servir archivos MEDIA solo en modo desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

Esto permite que los archivos MEDIA (como comprobantes y facturas en PDF) puedan verse correctamente en el navegador cuando `DEBUG=True`.

---

## 🧾 Directorios importantes

- `/media/`: Carpeta donde se guardan los archivos subidos por el sistema.
- `/static/`: Carpeta para archivos estáticos como estilos CSS y JavaScript.

---

## 🛠️ En producción

Para usar este sistema en producción:

- Cambia `DJANGO_DEBUG=False` en el `.env`.
- Configura un servidor como Nginx para servir archivos estáticos y MEDIA.
- Asegura el acceso mediante HTTPS.

---

## 📌 Notas finales

- Asegúrate de ejecutar los pasos en orden si restauras el sistema en una nueva máquina.
- Guarda una copia de seguridad de la carpeta `/media` y del volumen de la base de datos si deseas conservar los datos originales.
