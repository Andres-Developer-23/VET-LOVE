# Veterinaria VET LOVE

Sistema de gestión integral para veterinaria desarrollado con Django.

## Descripción

Este proyecto es una aplicación web completa para la gestión de una veterinaria que incluye:

- Gestión de clientes y mascotas
- Sistema de citas médicas
- Tienda en línea con carrito de compras
- Panel de administración
- Sistema de notificaciones
- Reportes y estadísticas

## Características Principales

### 🏥 Gestión Veterinaria
- Registro y administración de clientes
- Gestión completa de mascotas (perros, gatos, aves, reptiles, etc.)
- Sistema de citas médicas con estados y recordatorios
- Historial médico de mascotas
- Vacunas y tratamientos

### 🛒 Tienda en Línea
- Catálogo de productos por categorías
- Carrito de compras
- Sistema de pagos con Epayco
- Gestión de inventario
- Órdenes y entregas

### 👥 Administración
- Dashboard con estadísticas en tiempo real
- Gestión de usuarios y permisos
- Reportes exportables (PDF, Excel)
- Sistema de notificaciones personalizadas
- Plantillas de carnets de vacunación

### 🔐 Seguridad
- Autenticación de usuarios
- Roles y permisos (Admin, Veterinario, Cliente)
- Middleware de seguridad
- Validación de formularios

## Tecnologías Utilizadas

- **Backend**: Django 5.2.7
- **Base de datos**: SQLite (desarrollo) / PostgreSQL (producción)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Librerías adicionales**:
  - django-crispy-forms (formularios)
  - crispy-bootstrap5 (estilos)
  - reportlab (PDF)
  - openpyxl (Excel)
  - pillow (imágenes)
  - psycopg2-binary (PostgreSQL)

## Instalación

### Prerrequisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git

### Pasos de Instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/tu-usuario/veterinaria-vet-love.git
   cd veterinaria-vet-love
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv .venv
   ```

3. **Activar entorno virtual**
   - Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source .venv/bin/activate
     ```

4. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configurar variables de entorno**
   Crear archivo `.env` en la raíz del proyecto:
   ```env
   SECRET_KEY=tu-clave-secreta-aqui
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   DATABASE_URL=sqlite:///db.sqlite3

   # Configuración de Epayco (opcional)
   EPAYCO_PUBLIC_KEY=tu-public-key
   EPAYCO_PRIVATE_KEY=tu-private-key
   EPAYCO_P_CUST_ID_CLIENTE=tu-id-cliente
   EPAYCO_P_KEY=tu-p-key
   EPAYCO_TEST=True
   ```

6. **Ejecutar migraciones**
   ```bash
   python manage.py migrate
   ```

7. **Crear superusuario**
   ```bash
   python manage.py createsuperuser
   ```

8. **Ejecutar servidor de desarrollo**
   ```bash
   python manage.py runserver
   ```

9. **Acceder a la aplicación**
   - Sitio web: http://127.0.0.1:8000/
   - Panel de administración: http://127.0.0.1:8000/admin/

## Estructura del Proyecto

```
veterinaria-vet-love/
├── veterinaria_project/          # Configuración principal de Django
│   ├── settings/
│   │   ├── base.py              # Configuración base
│   │   ├── development.py       # Configuración desarrollo
│   │   └── production.py        # Configuración producción
│   ├── urls.py                  # URLs principales
│   ├── wsgi.py
│   └── asgi.py
├── administracion/               # App de administración
├── clientes/                     # App de gestión de clientes
├── mascotas/                     # App de gestión de mascotas
├── citas/                        # App de gestión de citas
├── tienda/                       # App de tienda en línea
├── notificaciones/               # App de notificaciones
├── templates/                    # Plantillas HTML
├── static/                       # Archivos estáticos
├── media/                        # Archivos multimedia
├── requirements.txt              # Dependencias Python
├── .env                          # Variables de entorno
└── README.md                     # Este archivo
```

## Configuración de Producción

Para desplegar en producción:

1. Configurar variables de entorno para producción
2. Usar configuración de producción en `settings/production.py`
3. Configurar servidor web (Nginx + Gunicorn)
4. Configurar base de datos PostgreSQL
5. Configurar sistema de archivos para archivos estáticos y multimedia

## Uso del Sistema

### Para Administradores
- Acceder al dashboard: `/administracion/dashboard/`
- Gestionar clientes, mascotas y citas
- Ver estadísticas y reportes
- Administrar productos de la tienda

### Para Veterinarios
- Acceder al dashboard veterinario: `/administracion/veterinario/dashboard/`
- Gestionar citas y tratamientos
- Ver historial médico de mascotas

### Para Clientes
- Registrarse y gestionar perfil
- Agregar y gestionar mascotas
- Solicitar citas médicas
- Comprar productos en la tienda

## API y Endpoints

El sistema incluye varios endpoints para integración:

- `/api/estadisticas/` - Estadísticas del sistema
- `/administracion/api/cambiar-estado-cita/` - Cambiar estado de citas
- Endpoints de tienda para carrito y pagos

## Contribución

1. Fork el proyecto
2. Crear rama para nueva funcionalidad (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.

## Soporte

Para soporte técnico o preguntas:
- Email: soporte@vetlove.com
- Documentación: [Link a documentación completa]

## Versiones

- **v1.0.0** - Versión inicial con funcionalidades básicas
- **v1.1.0** - Agregada tienda en línea
- **v1.2.0** - Sistema de notificaciones y reportes

---

**Desarrollado con ❤️ para Veterinaria VET LOVE**
