#!/usr/bin/env python
"""
Script para crear datos de prueba para el módulo de Admisión - Recepción
"""

import os
import sys
import django
from datetime import date, timedelta
from decimal import Decimal

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HMetaHIS.settings')
django.setup()

from django.contrib.auth.models import User
from admision_recepcion.models import (
    Municipio, Empresa, Convenio, Servicio, Prestador, 
    OrdenServicio, DetalleOrdenServicio
)


def crear_datos_basicos():
    """Crear datos básicos necesarios"""
    print("📊 Creando datos básicos...")
    
    # Crear municipios
    municipios_data = [
        {'codigo': '13001', 'nombre': 'Cartagena', 'departamento': 'Bolívar'},
        {'codigo': '13006', 'nombre': 'Arjona', 'departamento': 'Bolívar'},
        {'codigo': '13030', 'nombre': 'El Banco', 'departamento': 'Magdalena'},
        {'codigo': '11001', 'nombre': 'Bogotá', 'departamento': 'Cundinamarca'},
        {'codigo': '05001', 'nombre': 'Medellín', 'departamento': 'Antioquia'},
    ]
    
    for data in municipios_data:
        municipio, created = Municipio.objects.get_or_create(
            codigo=data['codigo'],
            defaults=data
        )
        if created:
            print(f"  ✅ Municipio: {municipio.nombre}")
    
    # Crear empresas
    empresas_data = [
        {
            'nit': '800123456-1',
            'razon_social': 'Empresa Petrolera Nacional S.A.',
            'tipo_empresa': 'EMPRESA',
            'direccion': 'Calle 72 # 10-07',
            'telefono': '(1) 555-0001',
            'email': 'contacto@petrolera.com'
        },
        {
            'nit': '900234567-2',
            'razon_social': 'EPS Salud Total',
            'tipo_empresa': 'EPS',
            'direccion': 'Carrera 15 # 93-07',
            'telefono': '(1) 555-0002',
            'email': 'info@saludtotal.com'
        },
        {
            'nit': '800345678-3',
            'razon_social': 'ARL Prevención',
            'tipo_empresa': 'ARL',
            'direccion': 'Avenida 68 # 40-35',
            'telefono': '(1) 555-0003',
            'email': 'info@arlprevencion.com'
        },
        {
            'nit': '700456789-4',
            'razon_social': 'Constructora Magdalena',
            'tipo_empresa': 'EMPRESA',
            'direccion': 'Calle Principal # 45-67',
            'telefono': '(5) 555-0004',
            'email': 'construcciones@magdalena.com'
        }
    ]
    
    for data in empresas_data:
        empresa, created = Empresa.objects.get_or_create(
            nit=data['nit'],
            defaults=data
        )
        if created:
            print(f"  ✅ Empresa: {empresa.razon_social}")
    
    # Crear convenios
    convenios_data = [
        {
            'codigo': 'CNV001',
            'nombre': 'Convenio Salud Ocupacional - Petrolera',
            'empresa': Empresa.objects.get(nit='800123456-1'),
            'fecha_inicio': date.today() - timedelta(days=365),
            'fecha_fin': date.today() + timedelta(days=365),
            'valor_contrato': Decimal('50000000'),
            'descripcion': 'Servicios de salud ocupacional para trabajadores de la petrolera'
        },
        {
            'codigo': 'CNV002',
            'nombre': 'Convenio EPS - Consultas',
            'empresa': Empresa.objects.get(nit='900234567-2'),
            'fecha_inicio': date.today() - timedelta(days=180),
            'fecha_fin': date.today() + timedelta(days=545),
            'valor_contrato': Decimal('25000000'),
            'descripcion': 'Servicios de consulta médica para afiliados'
        },
        {
            'codigo': 'CNV003',
            'nombre': 'Convenio ARL - Exámenes',
            'empresa': Empresa.objects.get(nit='800345678-3'),
            'fecha_inicio': date.today() - timedelta(days=90),
            'fecha_fin': date.today() + timedelta(days=275),
            'valor_contrato': Decimal('15000000'),
            'descripcion': 'Exámenes médicos ocupacionales'
        }
    ]
    
    for data in convenios_data:
        convenio, created = Convenio.objects.get_or_create(
            codigo=data['codigo'],
            defaults=data
        )
        if created:
            print(f"  ✅ Convenio: {convenio.nombre}")
    
    # Crear servicios
    servicios_data = [
        {
            'codigo': 'SRV001',
            'nombre': 'Consulta Médica General',
            'tipo': 'CONSULTA',
            'valor_base': Decimal('45000'),
            'descripcion': 'Consulta médica de medicina general'
        },
        {
            'codigo': 'SRV002',
            'nombre': 'Examen Médico Ocupacional',
            'tipo': 'EXAMEN',
            'valor_base': Decimal('75000'),
            'descripcion': 'Examen médico para ingreso laboral',
            'requiere_autorizacion': True
        },
        {
            'codigo': 'SRV003',
            'nombre': 'Laboratorio Clínico Completo',
            'tipo': 'EXAMEN',
            'valor_base': Decimal('85000'),
            'descripcion': 'Cuadro hemático, química sanguínea, parcial de orina'
        },
        {
            'codigo': 'SRV004',
            'nombre': 'Radiografía de Tórax',
            'tipo': 'EXAMEN',
            'valor_base': Decimal('55000'),
            'descripcion': 'Radiografía PA de tórax'
        },
        {
            'codigo': 'SRV005',
            'nombre': 'Electrocardiograma',
            'tipo': 'EXAMEN',
            'valor_base': Decimal('35000'),
            'descripcion': 'EKG de 12 derivaciones'
        },
        {
            'codigo': 'SRV006',
            'nombre': 'Audiometría',
            'tipo': 'EXAMEN',
            'valor_base': Decimal('40000'),
            'descripcion': 'Examen audiométrico ocupacional'
        },
        {
            'codigo': 'SRV007',
            'nombre': 'Visiometría',
            'tipo': 'EXAMEN',
            'valor_base': Decimal('25000'),
            'descripcion': 'Examen de agudeza visual'
        }
    ]
    
    for data in servicios_data:
        servicio, created = Servicio.objects.get_or_create(
            codigo=data['codigo'],
            defaults=data
        )
        if created:
            print(f"  ✅ Servicio: {servicio.nombre}")
    
    # Crear prestadores
    prestadores_data = [
        {
            'codigo': 'PREST001',
            'nombre': 'Dr. Carlos Mendoza',
            'tipo': 'MEDICO',
            'especialidad': 'Medicina General',
            'telefono': '300-555-0001',
            'email': 'cmendoza@hospital.com'
        },
        {
            'codigo': 'PREST002',
            'nombre': 'Dra. Ana Rodríguez',
            'tipo': 'MEDICO',
            'especialidad': 'Medicina del Trabajo',
            'telefono': '300-555-0002',
            'email': 'arodriguez@hospital.com'
        },
        {
            'codigo': 'LAB001',
            'nombre': 'Laboratorio Central',
            'tipo': 'LABORATORIO',
            'especialidad': 'Análisis Clínicos',
            'telefono': '300-555-0101',
            'email': 'laboratorio@hospital.com'
        },
        {
            'codigo': 'RAD001',
            'nombre': 'Servicio de Radiología',
            'tipo': 'RADIOLOGIA',
            'especialidad': 'Imágenes Diagnósticas',
            'telefono': '300-555-0201',
            'email': 'radiologia@hospital.com'
        },
        {
            'codigo': 'CARD001',
            'nombre': 'Servicio de Cardiología',
            'tipo': 'CARDIOLOGIA',
            'especialidad': 'Electrocardiografía',
            'telefono': '300-555-0301',
            'email': 'cardiologia@hospital.com'
        }
    ]
    
    for data in prestadores_data:
        prestador, created = Prestador.objects.get_or_create(
            codigo=data['codigo'],
            defaults=data
        )
        if created:
            print(f"  ✅ Prestador: {prestador.nombre}")


def crear_orden_ejemplo():
    """Crear una orden de servicio de ejemplo"""
    print("\n📋 Creando orden de servicio de ejemplo...")
    
    # Obtener datos necesarios
    municipio = Municipio.objects.first()
    convenio = Convenio.objects.first()
    empresa = Empresa.objects.first()
    
    # Crear usuario si no existe
    user, created = User.objects.get_or_create(
        username='admin_admision',
        defaults={
            'first_name': 'Admin',
            'last_name': 'Admisión',
            'email': 'admin@hospital.com',
            'is_staff': True
        }
    )
    if created:
        user.set_password('admin123')
        user.save()
        print(f"  ✅ Usuario creado: {user.username}")
    
    # Crear orden de servicio
    orden_data = {
        'tipo_documento': 'CC',
        'numero_identificacion': '12345678',
        'ciudad_nacimiento': 'El Banco',
        'fecha_nacimiento': date(1985, 5, 15),
        'primer_apellido': 'García',
        'segundo_apellido': 'López',
        'primer_nombre': 'Juan',
        'otros_nombres': 'Carlos',
        'genero': 'M',
        'estado_civil': 'CASADO',
        'nivel_educativo': 'PROFESIONAL',
        'correo_electronico': 'juan.garcia@example.com',
        'zona': 'URBANA',
        'direccion': 'Calle 25 # 14-36',
        'barrio': 'Centro',
        'localidad': 'Comuna 1',
        'sede': 'PRINCIPAL',
        'estrato': '3',
        'municipio': municipio,
        'celulares': '300-555-1234',
        'telefonos': '555-4321',
        'profesion_cargo': 'Ingeniero de Sistemas',
        'funciones_cargo': 'Desarrollo de software y administración de sistemas',
        'tipo_evaluacion': 'Examen médico ocupacional de ingreso',
        'convenio': convenio,
        'empresa_mision': empresa,
        'eps': 'EPS Salud Total',
        'afp': 'AFP Protección',
        'arl': 'ARL Prevención',
        'observaciones': 'Examen de ingreso para nuevo empleado',
        'fecha_solicitud': date.today(),
        'created_by': user
    }
    
    orden, created = OrdenServicio.objects.get_or_create(
        numero_identificacion='12345678',
        defaults=orden_data
    )
    
    if created:
        print(f"  ✅ Orden creada: {orden.numero_orden}")
        
        # Agregar detalles de servicios
        servicios = [
            ('SRV002', 'PREST002', 1),  # Examen médico ocupacional
            ('SRV003', 'LAB001', 1),    # Laboratorio
            ('SRV004', 'RAD001', 1),    # Radiografía
            ('SRV005', 'CARD001', 1),   # EKG
            ('SRV006', 'PREST002', 1),  # Audiometría
            ('SRV007', 'PREST002', 1),  # Visiometría
        ]
        
        for srv_codigo, prest_codigo, cantidad in servicios:
            servicio = Servicio.objects.get(codigo=srv_codigo)
            prestador = Prestador.objects.get(codigo=prest_codigo)
            
            detalle = DetalleOrdenServicio.objects.create(
                orden=orden,
                cantidad=cantidad,
                servicio=servicio,
                prestador=prestador,
                valor_unitario=servicio.valor_base,
                forma_pago='CONVENIO',
                valor_pagar=servicio.valor_base * cantidad
            )
            print(f"    ➤ Servicio: {servicio.nombre} - ${servicio.valor_base}")
        
        # Calcular totales
        orden.calcular_totales()
        print(f"    💰 Total: ${orden.total_pagar}")
    else:
        print(f"  ⚠️  Orden ya existe: {orden.numero_orden}")


if __name__ == '__main__':
    print("🏥 Iniciando creación de datos para Admisión - Recepción")
    print("=" * 50)
    
    try:
        crear_datos_basicos()
        crear_orden_ejemplo()
        
        print("\n" + "=" * 50)
        print("✅ ¡Datos creados exitosamente!")
        print("\n📊 Resumen:")
        print(f"  📍 Municipios: {Municipio.objects.count()}")
        print(f"  🏢 Empresas: {Empresa.objects.count()}")
        print(f"  📄 Convenios: {Convenio.objects.count()}")
        print(f"  🩺 Servicios: {Servicio.objects.count()}")
        print(f"  👨‍⚕️ Prestadores: {Prestador.objects.count()}")
        print(f"  📋 Órdenes: {OrdenServicio.objects.count()}")
        print(f"  📝 Detalles: {DetalleOrdenServicio.objects.count()}")
        
        print("\n🔗 URLs disponibles:")
        print("  📊 Dashboard: http://localhost:8000/admision/")
        print("  📋 Órdenes: http://localhost:8000/admision/ordenes/")
        print("  ➕ Nueva Orden: http://localhost:8000/admision/ordenes/crear/")
        print("  👥 Seguimiento: http://localhost:8000/admision/seguimiento/")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)
