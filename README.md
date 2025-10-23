# 🐾 Veterinaria Vet Love - Sistema de Gestión Veterinaria

Un sistema completo de gestión veterinaria desarrollado con Django, siguiendo las mejores prácticas de desarrollo web. Incluye gestión de mascotas, citas, tienda en línea y panel de administración.

## ✨ Características Principales

### 🐶 Gestión de Mascotas
- **Registro completo** de información médica y personal
- **Historial médico** detallado con tratamientos y diagnósticos
- **Cartilla de vacunación** con recordatorios automáticos

### 📅 Sistema de Citas
- **Agendamiento en línea** con confirmación automática
- **Gestión de prioridades** (urgente, normal, rutinaria)
- **Recordatorios automáticos** por email
- **Calendario integrado** con FullCalendar

### 🛒 Tienda en Línea
- **Catálogo de productos** veterinarios
- **Carrito de compras** con persistencia de sesión
- **Sistema de órdenes** completo
- **Gestión de inventario** en tiempo real

### 👨‍💼 Panel de Administración
- **Dashboard ejecutivo** con métricas en tiempo real
- **Gestión completa** de usuarios, mascotas y productos
- **Reportes y estadísticas** avanzadas
- **Sistema de logs** y auditoría


## 🏗️ Arquitectura y Mejores Prácticas

### 📁 Estructura del Proyecto
```
veterinaria_app/
├── veterinaria_project/          # Configuración principal
│   ├── settings.py              # Configuración con variables de entorno
│   ├── urls.py                  # URLs principales
│   └── middleware.py            # Middleware personalizado
├── administracion/              # App de administración
├── mascotas/                    # App de gestión de mascotas
├── citas/                       # App de citas veterinarias
├── tienda/                      # App de tienda en línea
├── clientes/                    # App de gestión de clientes
├── media/                       # Archivos multimedia
├── static/                      # Archivos estáticos globales
├── staticfiles/                 # Archivos estáticos recopilados
└── templates/                   # Templates globales
```

### 🔧 Tecnologías Utilizadas

#### Backend
- **Django 5.2.6** - Framework web principal
- **Python 3.13** - Lenguaje de programación
- **SQLite** - Base de datos (desarrollo)
- **PostgreSQL** - Base de datos (producción)

#### Frontend
- **Bootstrap 5** - Framework CSS
- **Font Awesome** - Iconos
- **FullCalendar** - Calendarios interactivos
- **Chart.js** - Gráficos y estadísticas

#### Librerías Python
- **python-decouple** - Gestión de variables de entorno
- **django-crispy-forms** - Formularios mejorados
- **psycopg2-binary** - Conector PostgreSQL
- **dj-database-url** - Configuración de base de datos por URL

### 🛡️ Seguridad Implementada

- **Variables de entorno** para configuración sensible
- **Protección CSRF** en todos los formularios
- **Validación de permisos** en todas las vistas
- **Sanitización de datos** en formularios
- **Protección XSS** con templates seguros
- **Control de acceso** basado en roles

### 🚀 Optimización de Rendimiento

- **select_related()** y **prefetch_related()** para consultas optimizadas
- **Archivos estáticos** separados y minificados
- **Caché de templates** y consultas
- **Lazy loading** de imágenes
- **Compresión Gzip** automática

## 📋 Instalación y Configuración

### Prerrequisitos del Sistema
- **Python 3.8 o superior** (recomendado Python 3.11+)
- **pip** (viene incluido con Python)
- **Git** para clonar el repositorio
- **Virtualenv** o **venv** para entornos virtuales (recomendado)

### 🚀 Instalación Paso a Paso

#### 1. Clonar el Repositorio
```bash
git clone <url-del-repositorio>
cd veterinaria_app
```

#### 2. Crear y Activar Entorno Virtual
```bash
# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual
# En Linux/Mac:
source .venv/bin/activate
# En Windows:
.venv\Scripts\activate
```

#### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

#### 4. Configurar Variables de Entorno
```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar el archivo .env con tu editor preferido
# IMPORTANTE: Configurar SECRET_KEY y otras variables sensibles
```

#### 4.5. Configurar PostgreSQL (Opcional - si usas PostgreSQL)
```bash
# Ejecutar script de configuración automática de PostgreSQL
python setup_postgres.py
```
Este script:
- ✅ Verifica que PostgreSQL esté ejecutándose
- ✅ Crea la base de datos VETERINARIA_APP
- ✅ Configura la contraseña del usuario postgres
- ✅ Prueba la conexión

#### 5. Ejecutar Migraciones de Base de Datos
```bash
python manage.py migrate
```

#### 6. Crear Grupos de Usuarios (Obligatorio)
```bash
python manage.py shell -c "from setup_groups import setup_groups; setup_groups()"
```

#### 7. Crear Superusuario Administrador
```bash
python manage.py createsuperuser
```
Sigue las instrucciones para crear el usuario administrador.

#### 8. Recopilar Archivos Estáticos
```bash
python manage.py collectstatic --noinput
```

#### 9. Ejecutar Servidor de Desarrollo
```bash
python manage.py runserver
```

#### 10. Acceder al Sistema
- **Aplicación principal**: http://localhost:8000
- **Panel de administración**: http://localhost:8000/admin/

### ⚙️ Configuración de Variables de Entorno

Crear un archivo `.env` en la raíz del proyecto con el siguiente contenido:

```env
# Configuración Básica de Django
SECRET_KEY=tu-clave-secreta-muy-segura-de-al-menos-50-caracteres-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Base de Datos PostgreSQL
DATABASE_URL=postgresql://usuario:password@localhost:5432/VETERINARIA_APP

# Configuración de Email (obligatorio para registro de usuarios)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend  # Para desarrollo
# Para producción usar SMTP:
# EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
# EMAIL_HOST=smtp.gmail.com
# EMAIL_PORT=587
# EMAIL_USE_TLS=True
# EMAIL_HOST_USER=tu-email@gmail.com
# EMAIL_HOST_PASSWORD=tu-app-password

# Configuración de Epayco (para tienda en línea)
EPAYCO_PUBLIC_KEY=tu-clave-publica-epayco
EPAYCO_PRIVATE_KEY=tu-clave-privada-epayco
EPAYCO_P_CUST_ID_CLIENTE=tu-id-cliente-epayco
EPAYCO_P_KEY=tu-p-key-epayco
EPAYCO_TEST=True  # Cambiar a False en producción

```

### 🐘 Configuración de PostgreSQL

Si ya tienes PostgreSQL instalado y configurado:

1. **Crear la base de datos** (si no existe):
```sql
CREATE DATABASE VETERINARIA_APP;
```

2. **Crear usuario de base de datos** (opcional pero recomendado):
```sql
CREATE USER veterinaria_user WITH PASSWORD 'tu_password_seguro';
GRANT ALL PRIVILEGES ON DATABASE VETERINARIA_APP TO veterinaria_user;
```

3. **Configurar la conexión** en tu archivo `.env`:
```env
DATABASE_URL=postgresql://veterinaria_user:tu_password_seguro@localhost:5432/VETERINARIA_APP
```

#### Instalación de PostgreSQL (si no lo tienes)

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

**CentOS/RHEL:**
```bash
sudo yum install postgresql-server postgresql-contrib
sudo postgresql-setup initdb
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

**macOS (con Homebrew):**
```bash
brew install postgresql
brew services start postgresql
```

**Windows:**
1. Descargar e instalar desde: https://www.postgresql.org/download/windows/
2. Durante la instalación, configura la contraseña `01032001` para el usuario postgres
3. Asegúrate de que el servicio PostgreSQL esté ejecutándose
4. Verifica la instalación con: `pg_isready -h localhost -p 5432`

#### Verificar Conexión a PostgreSQL
```bash
# Conectar a PostgreSQL desde el directorio de instalación
# Normalmente: C:\Program Files\PostgreSQL\XX\bin\
"C:\Program Files\PostgreSQL\14\bin\psql.exe" -U postgres -d VETERINARIA_APP

# O si creaste un usuario específico
"C:\Program Files\PostgreSQL\14\bin\psql.exe" -U veterinaria_user -d VETERINARIA_APP
```

#### Configuración Manual para Windows
Si el script automático no funciona, configura PostgreSQL manualmente:

1. **Instalar PostgreSQL** desde https://www.postgresql.org/download/windows/

2. **Durante la instalación**:
   - Configura la contraseña `01032001` para el usuario postgres
   - Asegúrate de instalar pgAdmin y Command Line Tools
   - Recuerda la versión instalada (14, 15, etc.)

3. **Agregar PostgreSQL al PATH** (opcional pero recomendado):
   - Busca "Variables de entorno" en el menú Inicio
   - Edita la variable PATH
   - Agrega: `C:\Program Files\PostgreSQL\XX\bin\` (reemplaza XX con tu versión)

4. **Crear la base de datos**:
   ```cmd
   # Abrir Command Prompt como administrador
   # Si PostgreSQL está en PATH:
   psql -U postgres -c "CREATE DATABASE VETERINARIA_APP;"

   # Si no está en PATH, usa la ruta completa:
   "C:\Program Files\PostgreSQL\14\bin\psql.exe" -U postgres -c "CREATE DATABASE VETERINARIA_APP;"
   ```

5. **Verificar la instalación**:
   ```cmd
   # Si está en PATH:
   pg_isready -h localhost -p 5432

   # Si no está en PATH:
   "C:\Program Files\PostgreSQL\14\bin\pg_isready.exe" -h localhost -p 5432
   ```

6. **Usar pgAdmin** (alternativa gráfica):
   - Abre pgAdmin desde el menú Inicio
   - Conecta con usuario: postgres, contraseña: 01032001
   - Crea la base de datos VETERINARIA_APP desde la interfaz gráfica

7. **Configurar el archivo .env**:
   ```env
   DATABASE_URL=postgresql://postgres:01032001@localhost:5432/VETERINARIA_APP
   ```

### 🔧 Comandos Adicionales de Configuración

#### Verificar Instalación
```bash
# Verificar configuración completa del proyecto
python check_setup.py

# Verificar que Django está configurado correctamente
python manage.py check

# Verificar que todas las dependencias están instaladas
pip list
```

#### Ejecutar Tests
```bash
python manage.py test
```

#### Verificar Conexión a Base de Datos
```bash
python manage.py dbshell
# Esto abrirá el cliente de base de datos correspondiente (psql para PostgreSQL, sqlite3 para SQLite)
```


### 🐛 Solución de Problemas Comunes

#### Error: "ModuleNotFoundError: No module named 'decouple'"
```bash
pip install python-decouple
```

#### Error: "SECRET_KEY not found"
- Asegurarse de que el archivo `.env` existe y contiene `SECRET_KEY`
- Generar una nueva SECRET_KEY segura con:
```python
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

#### Error: "No such table" después de migrate
```bash
# Resetear base de datos
python manage.py migrate --run-syncdb
```

#### Error de Permisos en Archivos Estáticos
```bash
# En Linux/Mac, dar permisos
chmod -R 755 static/
chmod -R 755 media/
```

#### Problemas con Grupos de Usuarios
```bash
# Recrear grupos si es necesario
python manage.py shell -c "from setup_groups import setup_groups; setup_groups()"
```

#### Error de Email en Registro
- Para desarrollo, usar `EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'`
- Los emails se mostrarán en la consola en lugar de enviarse

#### Error de Conexión a PostgreSQL
```bash
# Verificar que PostgreSQL esté ejecutándose
sudo systemctl status postgresql

# Verificar credenciales de conexión
psql -U veterinaria_user -d VETERINARIA_APP -h localhost

# Si hay problemas de autenticación, verificar pg_hba.conf
sudo nano /etc/postgresql/XX/main/pg_hba.conf
```

#### Error: "psycopg2.OperationalError: FATAL: database does not exist"
```bash
# Crear la base de datos
sudo -u postgres createdb VETERINARIA_APP

# O desde psql
sudo -u postgres psql -c "CREATE DATABASE VETERINARIA_APP;"
```

### 🌐 Configuración para Producción

Para desplegar en producción, cambiar las siguientes variables en `.env`:

```env
DEBUG=False
SECRET_KEY=tu-clave-produccion-super-segura
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com
DATABASE_URL=postgresql://user:pass@host:5432/dbname
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
# ... configuración SMTP completa
```

### 📱 Verificación de Instalación Exitosa

Después de completar la instalación, verificar que:

1. ✅ El servidor se ejecuta sin errores
2. ✅ Puedes acceder a http://localhost:8000
3. ✅ El panel admin funciona en /admin/
4. ✅ Puedes registrar un nuevo usuario
5. ✅ Los archivos estáticos se cargan correctamente
6. ✅ La base de datos tiene las tablas creadas

## 🎯 Uso del Sistema

### 👤 Para Clientes

1. **Registro**: Crear cuenta en el sistema
2. **Perfil**: Completar información personal
3. **Mascotas**: Registrar mascotas con información médica completa
4. **Citas**: Agendar consultas veterinarias
5. **Tienda**: Comprar productos veterinarios

### 👨‍⚕️ Para Veterinarios/Administradores

1. **Dashboard**: Ver métricas y estadísticas en tiempo real
2. **Pacientes**: Gestionar información médica de mascotas
3. **Citas**: Administrar agenda y consultas
4. **Inventario**: Controlar productos de la tienda
5. **Reportes**: Generar estadísticas y reportes


## 📊 API Endpoints

### Mascotas
- `GET /mascotas/` - Lista de mascotas del usuario
- `POST /mascotas/agregar/` - Registrar nueva mascota
- `GET /mascotas/{id}/` - Detalle de mascota

### Citas
- `GET /citas/mis-citas/` - Citas del usuario
- `POST /citas/solicitar/` - Solicitar nueva cita
- `GET /citas/{id}/calendario/` - Calendario de vacunación

### Tienda
- `GET /tienda/` - Catálogo de productos
- `POST /carrito/agregar/` - Agregar al carrito
- `GET /ordenes/mis-ordenes/` - Historial de compras

## 🧪 Testing

### Ejecutar Tests
```bash
python manage.py test
```

### Cobertura de Tests
- ✅ Modelos y validaciones
- ✅ Vistas y permisos
- ✅ Formularios
- ✅ API endpoints

### Ejecutar Tests con Cobertura
```bash
pip install coverage
coverage run manage.py test
coverage report
```

### Script de Verificación de Configuración
```bash
python check_setup.py
```
Este script verifica:
- ✅ Instalación de dependencias
- ✅ Configuraciones de Django requeridas
- ✅ Variables de entorno
- ✅ Conexión a base de datos
- ✅ Existencia de tablas

### Script de Configuración de PostgreSQL
```bash
python setup_postgres.py
```
Este script configura automáticamente:
- ✅ Verificación de PostgreSQL ejecutándose
- ✅ Creación de la base de datos VETERINARIA_APP
- ✅ Configuración de credenciales
- ✅ Prueba de conexión

## ✅ Mejores Prácticas Implementadas

### Arquitectura
- ✅ Separación modular de settings por entorno
- ✅ Apps Django bien estructuradas por funcionalidad
- ✅ Uso de variables de entorno para configuración sensible
- ✅ Middleware personalizado para seguridad

### Código
- ✅ Decoradores `@login_required` en todas las vistas protegidas
- ✅ Verificación de permisos en vistas críticas
- ✅ Uso de `get_object_or_404` para manejo seguro de objetos
- ✅ Validaciones en modelos con choices apropiadas
- ✅ Índices en modelos de alto uso

### Seguridad
- ✅ Protección CSRF habilitada
- ✅ Configuración de cookies seguras
- ✅ Autenticación por email con activación
- ✅ Control de acceso basado en roles
- ✅ Sanitización de datos en formularios

### Base de Datos
- ✅ Migraciones correctamente estructuradas
- ✅ Relaciones ForeignKey apropiadas
- ✅ Uso de select_related/prefetch_related para optimización

### Frontend
- ✅ Templates con herencia correcta
- ✅ Archivos estáticos organizados
- ✅ JavaScript modular y funcional

## 🚀 Despliegue en Producción

### Configuración Recomendada

1. **Servidor Web**: Nginx + Gunicorn
2. **Base de Datos**: PostgreSQL
3. **Cache**: Redis
4. **Archivos Estáticos**: AWS S3 o similar
5. **SSL**: Certificado Let's Encrypt

### Variables de Producción
```env
DEBUG=False
SECRET_KEY=tu-clave-produccion-super-segura
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com
DATABASE_URL=postgresql://user:pass@host:5432/dbname
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-app-password
```

### Comandos de Despliegue
```bash
# Recopilar archivos estáticos
python manage.py collectstatic --noinput

# Ejecutar migraciones
python manage.py migrate

# Crear superusuario si es necesario
python manage.py createsuperuser

# Ejecutar con Gunicorn
gunicorn veterinaria_project.wsgi:application --bind 0.0.0.0:8000
```

## 🤝 Contribución

1. Fork el proyecto
2. Crear rama para feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## 📞 Contacto

**Veterinaria Vet Love**
- Email: info@vetlove.com
- Sitio Web: [www.vetlove.com](https://www.vetlove.com)
- Teléfono: +57 310 5956453

---

## 🎉 ¡Gracias por usar Veterinaria Vet Love!
