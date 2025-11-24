# Sistema de Control de Ingreso y Salida de Cargas - ForestLog

Sistema web desarrollado para gestionar el control de ingreso y salida de cargas en empresas del sector forestal/logístico del Biobío. Implementa un backend robusto con Django y Django REST Framework, con frontend web y API REST para integración externa.

## 📋 Descripción del Proyecto

Este sistema permite gestionar de forma integral el control de vehículos y registros de acceso a plantas forestales, incluyendo:

- **Gestión de Vehículos**: Registro y control de camiones, camionetas y maquinaria con validación de patentes chilenas y seguimiento de revisión técnica.
- **Control de Acceso**: Registro de entradas y salidas de cargas con información de chofer (con validación de RUT chileno), tipo de carga, origen y destino.
- **Dashboard**: Visualización en tiempo real de estadísticas operacionales y vehículos en planta.
- **API REST**: Endpoints seguros con autenticación JWT para integración con sistemas externos.

## 🏗️ Arquitectura del Sistema

### Modelos de Datos

**Vehicle (Vehículo)**
- Patente (formato chileno: ABCD12)
- Tipo: Camión, Camioneta o Maquinaria
- Propietario
- Estado: Activo/Inactivo
- Fecha de vencimiento revisión técnica
- Capacidad en kilogramos

**AccessRecord (Registro de Acceso)**
- Vehículo (relación FK)
- Nombre y RUT del chofer
- Tipo de carga: Trozos, Chips, Madera Aserrada, Otros
- Origen y Destino
- Estado: En Ingreso, En Planta, Salida
- Timestamps de entrada y salida
- Usuario que creó el registro

## 🛠️ Tecnologías Utilizadas

- **Backend**: Django 4.2.17
- **API REST**: Django REST Framework 3.16.1
- **Base de Datos**: MySQL 8.0 (MariaDB 10.4.32)
- **Autenticación**: JWT (djangorestframework-simplejwt)
- **Frontend**: Django Templates + Bootstrap 5.3
- **Servidor**: Django Development Server
- **Control de Versiones**: Git

## 📦 Requisitos Previos

- Python 3.13 o superior
- MySQL Server (XAMPP 8.2.12 recomendado)
- pip (gestor de paquetes de Python)
- Git

## 🚀 Instalación y Configuración

### 1. Clonar el Repositorio

```bash
git clone https://github.com/NaikoFLG1/Evaluaci-n-3-BackEnd.git
cd Evaluaci-n-3-BackEnd/ingreso_salida_cargas
```

### 2. Crear Entorno Virtual

**Windows:**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

Las dependencias principales son:
- Django==4.2.17
- djangorestframework==3.16.1
- djangorestframework-simplejwt==5.4.0
- mysqlclient==2.2.7
- python-dotenv==1.2.1

### 4. Configurar Base de Datos

#### Iniciar MySQL (XAMPP)
1. Abrir XAMPP Control Panel
2. Iniciar el servicio **MySQL**
3. Verificar que esté corriendo en puerto 3306

#### Crear Base de Datos
Acceder a MySQL y ejecutar:

```sql
CREATE DATABASE forest_log CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 5. Configurar Variables de Entorno

Crear archivo `.env` en la raíz del proyecto (`ingreso_salida_cargas/.env`):

```env
MY_SQL_HOST=localhost
MY_SQL_PORT=3306
MY_SQL_DB=forest_log
MY_SQL_USER=root
MY_SQL_PASSWORD=

DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
JWT_SECRET=tu_clave_secreta_aqui
```

> **Nota**: Si MySQL tiene contraseña, agregarla en `MY_SQL_PASSWORD`

### 6. Ejecutar Migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

Esto creará las tablas necesarias en la base de datos.

### 7. Crear Superusuario

```bash
python manage.py createsuperuser
```

Ingresar los datos solicitados:
- **Username**: admin (recomendado)
- **Email**: admin@forest.com (opcional)
- **Password**: administrador123. (o la que prefiera)

### 8. Iniciar Servidor de Desarrollo

```bash
python manage.py runserver
```

El servidor estará disponible en: `http://127.0.0.1:8000/`

## 📱 Uso del Sistema

### Acceso Web (Frontend)

#### 1. Login
- **URL**: `http://127.0.0.1:8000/login/`
- Ingresar con las credenciales del superusuario creado
- Usuario: `admin`
- Contraseña: `administrador123.`

#### 2. Dashboard Principal
- **URL**: `http://127.0.0.1:8000/`
- Visualiza estadísticas en tiempo real:
  - Total de vehículos
  - Vehículos activos
  - Vehículos en planta
  - Registros del día
  - Últimos registros de acceso
  - Vehículos con revisión técnica próxima a vencer

#### 3. Gestión de Vehículos
- **URL**: `http://127.0.0.1:8000/vehicles/`
- **Funcionalidades**:
  - Listar todos los vehículos
  - Crear nuevo vehículo (validación de patente chilena)
  - Editar vehículo existente
  - Eliminar vehículo
  - Ver estado de revisión técnica

#### 4. Gestión de Registros de Acceso
- **URL**: `http://127.0.0.1:8000/access/`
- **Funcionalidades**:
  - Listar registros de acceso
  - Crear nuevo registro de ingreso
  - Registrar salida de vehículo
  - Filtrar por estado y fechas

#### 5. Panel de Administración Django
- **URL**: `http://127.0.0.1:8000/admin/`
- Acceso completo a todos los modelos con interfaz administrativa

### API REST (Backend)

#### Autenticación JWT

**Obtener Token:**
```bash
POST http://127.0.0.1:8000/api/auth/login/
Content-Type: application/json

{
  "username": "admin",
  "password": "administrador123."
}
```

**Respuesta:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Refrescar Token:**
```bash
POST http://127.0.0.1:8000/api/auth/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### Endpoints de Vehículos

**Listar vehículos:**
```bash
GET http://127.0.0.1:8000/api/vehicles/
Authorization: Bearer {access_token}
```

**Crear vehículo:**
```bash
POST http://127.0.0.1:8000/api/vehicles/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "plate": "ABCD12",
  "type": "truck",
  "owner": "Transportes del Sur",
  "status": "active",
  "tech_review_due": "2026-12-31",
  "capacity_kg": 15000
}
```

**Actualizar vehículo:**
```bash
PUT http://127.0.0.1:8000/api/vehicles/{id}/
Authorization: Bearer {access_token}
```

**Eliminar vehículo:**
```bash
DELETE http://127.0.0.1:8000/api/vehicles/{id}/
Authorization: Bearer {access_token}
```

**Activar/Desactivar vehículo:**
```bash
POST http://127.0.0.1:8000/api/vehicles/{id}/activate/
POST http://127.0.0.1:8000/api/vehicles/{id}/deactivate/
Authorization: Bearer {access_token}
```

#### Endpoints de Registros de Acceso

**Listar registros:**
```bash
GET http://127.0.0.1:8000/api/access-records/
Authorization: Bearer {access_token}
```

**Crear registro de ingreso:**
```bash
POST http://127.0.0.1:8000/api/access-records/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "vehicle": 1,
  "driver_name": "Juan Pérez",
  "driver_rut": "12345678-9",
  "load_type": "logs",
  "origin": "Faena Los Pinos",
  "destination": "Planta Concepción"
}
```

**Registrar salida:**
```bash
POST http://127.0.0.1:8000/api/access-records/{id}/register_exit/
Authorization: Bearer {access_token}
```

**Consultar vehículos en planta:**
```bash
GET http://127.0.0.1:8000/api/access-records/vehicles_in_plant/
Authorization: Bearer {access_token}
```

#### Filtros Disponibles

**Vehículos:**
- `?status=active` - Filtrar por estado
- `?type=truck` - Filtrar por tipo
- `?search=ABCD` - Búsqueda por patente

**Registros:**
- `?state=en_planta` - Filtrar por estado
- `?vehicle=1` - Filtrar por vehículo
- `?date_from=2025-11-01` - Desde fecha
- `?date_to=2025-11-30` - Hasta fecha
- `?search=Juan` - Búsqueda general

## 🔒 Seguridad Implementada

1. **Autenticación JWT**: Tokens con expiración (30 minutos access, 7 días refresh)
2. **Contraseñas con Hash**: Django usa PBKDF2 por defecto
3. **Validación de Datos**: 
   - RUT chileno con dígito verificador
   - Patentes formato chileno (4 letras + 2 números)
   - Validación de fechas de revisión técnica
4. **Permisos Personalizados**: 
   - GET/POST: Usuarios autenticados
   - PUT/DELETE: Solo administradores
5. **Protección CSRF**: Activada en formularios web
6. **Variables de Entorno**: Credenciales en archivo `.env`
7. **Manejo de Errores**: Handler personalizado para respuestas uniformes

## 📁 Estructura del Proyecto

```
ingreso_salida_cargas/
├── app_ingreso_salidas/          # Aplicación principal
│   ├── migrations/                # Migraciones de base de datos
│   ├── templates/                 # Templates HTML
│   │   ├── base.html             # Template base
│   │   ├── login.html            # Página de login
│   │   ├── dashboard.html        # Dashboard principal
│   │   ├── vehicle_list.html     # Lista de vehículos
│   │   ├── vehicle_form.html     # Formulario de vehículo
│   │   ├── access_list.html      # Lista de registros
│   │   └── access_form.html      # Formulario de registro
│   ├── admin.py                  # Configuración admin
│   ├── forms.py                  # Formularios Django
│   ├── models.py                 # Modelos de datos
│   ├── serializers.py            # Serializers DRF
│   ├── validators.py             # Validadores personalizados
│   ├── views.py                  # ViewSets API REST
│   ├── views_web.py              # Vistas web Django
│   ├── views_health.py           # Health check endpoint
│   └── urls.py                   # URLs de la app
├── ingreso_salida_cargas/        # Configuración del proyecto
│   ├── settings.py               # Configuración Django
│   ├── urls.py                   # URLs principales
│   ├── rest_errors.py            # Handler de errores
│   └── wsgi.py                   # Configuración WSGI
├── .env                          # Variables de entorno
├── manage.py                     # Script de gestión Django
└── requirements.txt              # Dependencias Python
```

## 🧪 Testing

### Probar API con Python

```python
import requests

BASE_URL = 'http://127.0.0.1:8000'

# Login
response = requests.post(
    f'{BASE_URL}/api/auth/login/',
    json={'username': 'admin', 'password': 'administrador123.'}
)
token = response.json()['access']

# Listar vehículos
headers = {'Authorization': f'Bearer {token}'}
vehicles = requests.get(f'{BASE_URL}/api/vehicles/', headers=headers)
print(vehicles.json())
```

### Health Check

```bash
GET http://127.0.0.1:8000/api/health/db/
```

Respuesta esperada:
```json
{
  "db": "ok"
}
```

## 🐛 Solución de Problemas

### Error: "No module named 'MySQLdb'"
```bash
pip install mysqlclient
```

### Error: MySQL no conecta
1. Verificar que MySQL esté corriendo en XAMPP
2. Verificar credenciales en `.env`
3. Verificar que la base de datos `forest_log` exista

### Error: "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### Error: Migraciones pendientes
```bash
python manage.py migrate
```

### Puerto 8000 en uso
```bash
python manage.py runserver 8080
```

