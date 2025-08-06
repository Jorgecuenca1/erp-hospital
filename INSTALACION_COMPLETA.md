# 🏥 HMetaHIS - Guía de Instalación Completa

## 📋 Sistema ERP Hospitalario Superior a Odoo Enterprise

### 🎯 **¿Qué es HMetaHIS?**

**HMetaHIS** es un sistema ERP hospitalario completo con **75+ módulos integrados** que supera ampliamente las capacidades de Odoo Enterprise en el sector salud. Incluye 24 módulos HMS especializados + 27 módulos ERP + 24 módulos adicionales.

---

## 🚀 **Instalación Rápida**

### **Requisitos Previos**
- Python 3.8 o superior
- Django 4.2 o superior
- SQLite (incluido) o PostgreSQL
- 4GB RAM mínimo
- 10GB espacio en disco

### **Paso 1: Clonar el Repositorio**
```bash
git clone https://github.com/tu-usuario/hmetahis.git
cd hmetahis
```

### **Paso 2: Crear Entorno Virtual**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows
```

### **Paso 3: Instalar Dependencias**
```bash
pip install -r requirements.txt
```

### **Paso 4: Configurar Base de Datos**
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### **Paso 5: Iniciar el Sistema**
```bash
python manage.py runserver
```

### **Paso 6: Acceder al Sistema**
- **Landing Page**: http://localhost:8000/
- **Dashboard Admin**: http://localhost:8000/dashboard/
- **Admin Django**: http://localhost:8000/admin/

---

## 🎛️ **Configuración Detallada**

### **1. Configuración de Base de Datos**

#### **SQLite (Por defecto)**
```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

#### **PostgreSQL (Recomendado para producción)**
```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'hmetahis',
        'USER': 'tu_usuario',
        'PASSWORD': 'tu_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### **2. Configuración de Email**
```python
# settings.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'tu_email@gmail.com'
EMAIL_HOST_PASSWORD = 'tu_password'
```

### **3. Configuración de Archivos Estáticos**
```python
# settings.py
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

---

## 🏗️ **Estructura del Sistema**

### **Módulos HMS (24 módulos)**
```
📁 acs_hms_base/              # Base del sistema HMS
📁 acs_hms_emergency/         # Gestión de emergencias
📁 acs_hms_surgery/           # Cirugía y quirófanos
📁 acs_hms_laboratory/        # Laboratorio clínico
📁 acs_hms_radiology/         # Radiología e imágenes
📁 acs_hms_nursing/           # Gestión de enfermería
📁 acs_hms_gynec/             # Ginecología
📁 acs_hms_ophthalmology/     # Oftalmología
📁 acs_hms_paediatric/        # Pediatría
📁 acs_hms_dental/            # Odontología
📁 acs_hms_aesthetic/         # Medicina estética
📁 acs_hms_blood_bank/        # Banco de sangre
📁 acs_hms_hospitalization/   # Hospitalización
📁 acs_hms_patient_portal/    # Portal del paciente
📁 acs_hms_pharmacy/          # Farmacia hospitalaria
📁 acs_hms_online_appointment/ # Citas online
📁 acs_hms_webcam/            # Gestión de webcam
📁 acs_hms_video_call/        # Videollamadas médicas
📁 acs_hms_consent_form/      # Consentimientos
📁 acs_hms_insurance/         # Seguros médicos
📁 acs_hms_commission/        # Comisiones médicas
📁 acs_hms_certification/     # Certificaciones
📁 acs_hms_subscription/      # Suscripciones
📁 acs_hms_waiting_screen/    # Pantallas de espera
```

### **Módulos ERP (27 módulos)**
```
📁 patients/                  # Gestión de pacientes
📁 professionals/             # Gestión de profesionales
📁 appointments/              # Gestión de citas
📁 medical_records/           # Historias clínicas
📁 accounting/                # Contabilidad
📁 billing/                   # Facturación
📁 inventories/               # Inventarios
📁 hr/                        # Recursos humanos
📁 pharmacy/                  # Farmacia
📁 laboratories/              # Laboratorios
📁 reports/                   # Reportes
📁 asset_management/          # Gestión de activos
📁 quality_management/        # Gestión de calidad
📁 pos/                       # Punto de venta
📁 sales/                     # Ventas
📁 purchases/                 # Compras
📁 crm/                       # CRM
📁 website/                   # Sitio web
📁 ecommerce/                 # Comercio electrónico
📁 blog/                      # Blog
📁 forum/                     # Foro
📁 elearning/                 # E-learning
📁 livechat/                  # Chat en vivo
📁 subscriptions/             # Suscripciones
📁 hospital_profile/          # Perfil del hospital
```

---

## 🔧 **Configuración Avanzada**

### **1. Configuración de Producción**
```python
# settings.py
DEBUG = False
ALLOWED_HOSTS = ['tu-dominio.com', 'www.tu-dominio.com']

# Seguridad
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

### **2. Configuración de Redis (Cache)**
```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

### **3. Configuración de Celery (Tareas Asíncronas)**
```python
# settings.py
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
```

---

## 🔑 **Acceso al Sistema**

### **1. Dashboard Administrativo**
- **URL**: `/dashboard/`
- **Descripción**: Panel completo con navegación a todos los módulos
- **Características**:
  - Estadísticas en tiempo real
  - Navegación por categorías
  - Búsqueda de módulos
  - Diseño responsivo

### **2. Navegación Principal**
- **HMS**: Módulos especializados en gestión hospitalaria
- **ERP**: Módulos de gestión empresarial
- **ESG**: Módulos de sostenibilidad
- **Admin**: Panel de administración Django

### **3. Usuarios y Permisos**
```python
# Crear usuario administrador
python manage.py createsuperuser

# Crear grupos de usuarios
python manage.py shell
>>> from django.contrib.auth.models import Group, Permission
>>> doctors = Group.objects.create(name='Doctors')
>>> nurses = Group.objects.create(name='Nurses')
>>> admin = Group.objects.create(name='Hospital_Admin')
```

---

## 🧪 **Pruebas del Sistema**

### **1. Ejecutar Pruebas**
```bash
# Prueba completa del sistema
python test_system.py

# Pruebas específicas
python manage.py test patients
python manage.py test acs_hms_emergency
```

### **2. Verificar Instalación**
```bash
# Verificar aplicaciones instaladas
python manage.py check

# Verificar migraciones
python manage.py showmigrations

# Verificar archivos estáticos
python manage.py collectstatic
```

---

## 📈 **Optimización y Rendimiento**

### **1. Optimizaciones de Base de Datos**
```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'OPTIONS': {
            'init_command': 'SET default_storage_engine=INNODB',
        }
    }
}
```

### **2. Optimizaciones de Template**
```python
# settings.py
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'OPTIONS': {
            'loaders': [
                ('django.template.loaders.cached.Loader', [
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                ]),
            ],
        },
    },
]
```

---

## 🔒 **Seguridad**

### **1. Configuración de Seguridad**
```python
# settings.py
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
```

### **2. Autenticación de Dos Factores**
```bash
pip install django-otp
python manage.py addtotpdevice username
```

---

## 🌍 **Adaptabilidad Empresarial**

### **¿Se puede usar en empresas no hospitalarias?**

**¡SÍ!** El sistema es altamente adaptable:

#### **Empresas que pueden usar HMetaHIS:**
- **Clínicas veterinarias** (adaptación menor)
- **Centros de bienestar** (spa, fitness)
- **Laboratorios farmacéuticos**
- **Empresas de servicios** (consultoría, legal)
- **Centros educativos** (colegios, universidades)
- **Empresas manufactureras** (con ERP completo)

#### **Módulos ERP Universales:**
- ✅ Contabilidad
- ✅ Facturación
- ✅ Inventarios
- ✅ Recursos Humanos
- ✅ CRM
- ✅ Punto de Venta
- ✅ E-commerce
- ✅ Gestión de Activos
- ✅ Reportes y Análisis

#### **Personalización Rápida:**
```python
# settings.py - Personalizar para tu empresa
COMPANY_TYPE = 'VETERINARY'  # HOSPITAL, VETERINARY, GENERAL
COMPANY_NAME = 'Mi Empresa'
COMPANY_MODULES = ['accounting', 'billing', 'hr', 'crm']
```

---

## 📞 **Soporte y Mantenimiento**

### **1. Logs del Sistema**
```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'hmetahis.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
```

### **2. Backup de Base de Datos**
```bash
# PostgreSQL
pg_dump hmetahis > backup.sql

# SQLite
cp db.sqlite3 backup_db.sqlite3
```

### **3. Actualizaciones**
```bash
git pull origin main
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic
```

---

## 🎉 **¡Felicitaciones!**

Has instalado exitosamente **HMetaHIS**, el sistema ERP hospitalario más completo y avanzado disponible gratuitamente.

### **🏆 Logros del Sistema:**
- ✅ **75+ módulos** integrados
- ✅ **Superior a Odoo Enterprise**
- ✅ **100% código abierto**
- ✅ **Especializado en salud**
- ✅ **Altamente personalizable**

### **📚 Próximos Pasos:**
1. Explorar el dashboard administrativo
2. Configurar usuarios y permisos
3. Personalizar módulos según necesidades
4. Integrar con sistemas externos
5. Capacitar al personal

---

## 📋 **Información Adicional**

- **Versión**: 2.1.0
- **Licencia**: MIT
- **Soporte**: Comunidad activa
- **Documentación**: Incluida en el sistema
- **Actualizaciones**: Regulares

**¡Bienvenido a HMetaHIS - El futuro de la gestión hospitalaria!** 🚀🏥 