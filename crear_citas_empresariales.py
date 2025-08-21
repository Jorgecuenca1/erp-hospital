#!/usr/bin/env python3
"""
Script para crear citas empresariales de prueba
"""

import os
import sys
import django
from datetime import datetime, timedelta, time

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HMetaHIS.settings')
django.setup()

from django.contrib.auth.models import User
from django.utils import timezone
from admision_recepcion.models import CitaEmpresarial, Empresa, Servicio, Prestador


def crear_citas_empresariales():
    """Crear citas empresariales de prueba"""
    
    # Obtener o crear empresas
    empresa1, _ = Empresa.objects.get_or_create(
        nit='800123456-7',
        defaults={
            'razon_social': 'Constructora del Norte S.A.S.',
            'nombre_comercial': 'Constructora Norte',
            'telefono': '3101234567',
            'email': 'info@constructoranorte.com',
            'direccion': 'Cra 15 #45-67, Barranquilla',
            'activo': True
        }
    )
    
    empresa2, _ = Empresa.objects.get_or_create(
        nit='900234567-8',
        defaults={
            'razon_social': 'Servicios Industriales del Caribe Ltda.',
            'nombre_comercial': 'SICAR',
            'telefono': '3209876543',
            'email': 'recursos@sicar.com',
            'direccion': 'Zona Industrial Km 8 vía Ciénaga',
            'activo': True
        }
    )
    
    empresa3, _ = Empresa.objects.get_or_create(
        nit='900345678-9',
        defaults={
            'razon_social': 'Transportes Magdalena S.A.',
            'nombre_comercial': 'Transmag',
            'telefono': '3156789012',
            'email': 'talento@transmag.co',
            'direccion': 'Terminal de Transporte Local 45',
            'activo': True
        }
    )
    
    # Obtener servicios y prestadores existentes
    servicios = list(Servicio.objects.filter(activo=True)[:3])
    prestadores = list(Prestador.objects.filter(activo=True)[:4])
    
    # Obtener usuario admin
    admin_user = User.objects.filter(is_superuser=True).first()
    
    # Datos de trabajadores de prueba
    trabajadores_data = [
        {
            'numero_identificacion': '12345678',
            'nombre_trabajador': 'Carlos Alberto Pérez González',
            'telefono_trabajador': '3101234567',
            'email_trabajador': 'carlos.perez@constructoranorte.com',
            'empresa': empresa1,
            'tipo_servicio': 'EXAMEN_INGRESO',
            'estado': 'PROGRAMADA'
        },
        {
            'numero_identificacion': '23456789',
            'nombre_trabajador': 'María Elena Rodríguez Vargas',
            'telefono_trabajador': '3209876543',
            'email_trabajador': 'maria.rodriguez@sicar.com',
            'empresa': empresa2,
            'tipo_servicio': 'EXAMEN_PERIODICO',
            'estado': 'CONFIRMADA'
        },
        {
            'numero_identificacion': '34567890',
            'nombre_trabajador': 'José Manuel García López',
            'telefono_trabajador': '3156789012',
            'email_trabajador': 'jose.garcia@transmag.co',
            'empresa': empresa3,
            'tipo_servicio': 'EXAMEN_ALTURA',
            'estado': 'PROGRAMADA'
        },
        {
            'numero_identificacion': '45678901',
            'nombre_trabajador': 'Ana Patricia Mendoza Silva',
            'telefono_trabajador': '3187654321',
            'email_trabajador': 'ana.mendoza@constructoranorte.com',
            'empresa': empresa1,
            'tipo_servicio': 'AUDIOMETRIA',
            'estado': 'CANCELADA'
        },
        {
            'numero_identificacion': '56789012',
            'nombre_trabajador': 'Roberto Carlos Jiménez Torres',
            'telefono_trabajador': '3001234567',
            'email_trabajador': 'roberto.jimenez@sicar.com',
            'empresa': empresa2,
            'tipo_servicio': 'VISIOMETRIA',
            'estado': 'CONFIRMADA'
        },
        {
            'numero_identificacion': '67890123',
            'nombre_trabajador': 'Sandra Milena Herrera Castro',
            'telefono_trabajador': '3123456789',
            'email_trabajador': 'sandra.herrera@transmag.co',
            'empresa': empresa3,
            'tipo_servicio': 'LABORATORIO',
            'estado': 'PROGRAMADA'
        }
    ]
    
    # Crear citas para hoy y próximos días
    base_date = timezone.now().date()
    base_times = [
        time(8, 0),   # 8:00 AM
        time(9, 30),  # 9:30 AM
        time(11, 0),  # 11:00 AM
        time(14, 0),  # 2:00 PM
        time(15, 30), # 3:30 PM
        time(16, 0),  # 4:00 PM
    ]
    
    citas_creadas = 0
    
    for i, trabajador in enumerate(trabajadores_data):
        # Distribuir citas en diferentes días
        fecha_cita = base_date + timedelta(days=i % 3)  # Hoy, mañana, pasado mañana
        hora_cita = base_times[i % len(base_times)]
        
        # Verificar si ya existe una cita para este trabajador
        if not CitaEmpresarial.objects.filter(
            numero_identificacion=trabajador['numero_identificacion'],
            fecha_cita=fecha_cita
        ).exists():
            
            cita_data = {
                'fecha_cita': fecha_cita,
                'hora_cita': hora_cita,
                'estado': trabajador['estado'],
                'numero_identificacion': trabajador['numero_identificacion'],
                'tipo_documento': 'CC',
                'nombre_trabajador': trabajador['nombre_trabajador'],
                'telefono_trabajador': trabajador['telefono_trabajador'],
                'email_trabajador': trabajador['email_trabajador'],
                'empresa': trabajador['empresa'],
                'contacto_empresa': f"RH {trabajador['empresa'].razon_social.split()[0]}",
                'telefono_empresa': trabajador['empresa'].telefono,
                'email_empresa': trabajador['empresa'].email,
                'tipo_servicio': trabajador['tipo_servicio'],
                'observaciones_servicio': f"Examen solicitado desde portal empresarial para {trabajador['nombre_trabajador']}",
                'sede_cita': 'PRINCIPAL',
                'valor_estimado': 150000,  # $150,000 pesos
                'requiere_autorizacion': False,
                'programada_por_portal': True,
                'ip_origen': '192.168.1.100'
            }
            
            # Asignar prestador si hay disponibles
            if prestadores:
                cita_data['prestador_asignado'] = prestadores[i % len(prestadores)]
            
            cita = CitaEmpresarial.objects.create(**cita_data)
            
            # Agregar servicios adicionales si hay disponibles
            if servicios:
                cita.servicios_adicionales.add(servicios[i % len(servicios)])
            
            # Si la cita está confirmada, agregar fecha de confirmación
            if trabajador['estado'] == 'CONFIRMADA' and admin_user:
                cita.confirmar_cita(admin_user)
            
            # Si la cita está cancelada, agregar información de cancelación
            elif trabajador['estado'] == 'CANCELADA' and admin_user:
                cita.cancelar_cita("Cancelada por solicitud de la empresa", admin_user)
            
            citas_creadas += 1
            print(f"✅ Cita creada: {cita.numero_cita} - {cita.nombre_trabajador} ({cita.empresa.razon_social})")
    
    # Crear algunas citas adicionales para días pasados (vencidas)
    citas_vencidas = [
        {
            'numero_identificacion': '78901234',
            'nombre_trabajador': 'Miguel Ángel Sánchez Ruiz',
            'telefono_trabajador': '3145678901',
            'email_trabajador': 'miguel.sanchez@constructoranorte.com',
            'empresa': empresa1,
            'tipo_servicio': 'EXAMEN_RETIRO',
            'estado': 'PROGRAMADA',
            'dias_atras': 2
        },
        {
            'numero_identificacion': '89012345',
            'nombre_trabajador': 'Claudia Patricia Vargas Díaz',
            'telefono_trabajador': '3176543210',
            'email_trabajador': 'claudia.vargas@sicar.com',
            'empresa': empresa2,
            'tipo_servicio': 'CONSULTA_MEDICINA',
            'estado': 'CONFIRMADA',
            'dias_atras': 1
        }
    ]
    
    for i, trabajador in enumerate(citas_vencidas):
        fecha_cita = base_date - timedelta(days=trabajador['dias_atras'])
        hora_cita = time(10, 0)  # 10:00 AM
        
        if not CitaEmpresarial.objects.filter(
            numero_identificacion=trabajador['numero_identificacion'],
            fecha_cita=fecha_cita
        ).exists():
            
            cita_data = {
                'fecha_cita': fecha_cita,
                'hora_cita': hora_cita,
                'estado': trabajador['estado'],
                'numero_identificacion': trabajador['numero_identificacion'],
                'tipo_documento': 'CC',
                'nombre_trabajador': trabajador['nombre_trabajador'],
                'telefono_trabajador': trabajador['telefono_trabajador'],
                'email_trabajador': trabajador['email_trabajador'],
                'empresa': trabajador['empresa'],
                'contacto_empresa': f"RH {trabajador['empresa'].razon_social.split()[0]}",
                'telefono_empresa': trabajador['empresa'].telefono,
                'email_empresa': trabajador['empresa'].email,
                'tipo_servicio': trabajador['tipo_servicio'],
                'observaciones_servicio': f"Cita vencida - {trabajador['nombre_trabajador']}",
                'sede_cita': 'PRINCIPAL',
                'valor_estimado': 120000,
                'requiere_autorizacion': False,
                'programada_por_portal': True,
                'ip_origen': '192.168.1.100'
            }
            
            if prestadores:
                cita_data['prestador_asignado'] = prestadores[i % len(prestadores)]
            
            cita = CitaEmpresarial.objects.create(**cita_data)
            
            if trabajador['estado'] == 'CONFIRMADA' and admin_user:
                cita.confirmar_cita(admin_user)
            
            citas_creadas += 1
            print(f"⚠️  Cita vencida creada: {cita.numero_cita} - {cita.nombre_trabajador}")
    
    print(f"\n🎉 Total de citas empresariales creadas: {citas_creadas}")
    
    # Mostrar resumen
    total_citas = CitaEmpresarial.objects.count()
    programadas = CitaEmpresarial.objects.filter(estado='PROGRAMADA').count()
    confirmadas = CitaEmpresarial.objects.filter(estado='CONFIRMADA').count()
    canceladas = CitaEmpresarial.objects.filter(estado='CANCELADA').count()
    
    print("\n📊 Resumen de citas empresariales:")
    print(f"   - Total: {total_citas}")
    print(f"   - Programadas: {programadas}")
    print(f"   - Confirmadas: {confirmadas}")
    print(f"   - Canceladas: {canceladas}")
    
    print("\n🏢 Empresas con citas:")
    for empresa in [empresa1, empresa2, empresa3]:
        citas_empresa = CitaEmpresarial.objects.filter(empresa=empresa).count()
        print(f"   - {empresa.razon_social}: {citas_empresa} citas")


if __name__ == '__main__':
    print("🚀 Creando citas empresariales de prueba...")
    crear_citas_empresariales()
    print("\n✅ Proceso completado!")
