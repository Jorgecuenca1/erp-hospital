#!/usr/bin/env python
"""
Script para crear seguimientos de ejemplo para el módulo de Seguimiento a Pacientes
"""

import os
import sys
import django
from datetime import date, datetime, timedelta
from random import choice, randint

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HMetaHIS.settings')
django.setup()

from django.contrib.auth.models import User
from admision_recepcion.models import (
    OrdenServicio, DetalleOrdenServicio, SeguimientoPaciente,
    Municipio, Empresa, Convenio, Servicio, Prestador
)
from django.utils import timezone


def crear_ordenes_ejemplo():
    """Crear varias órdenes de ejemplo para seguimiento"""
    print("📋 Creando órdenes adicionales para seguimiento...")
    
    # Obtener datos necesarios
    municipio = Municipio.objects.first()
    convenio = Convenio.objects.first()
    empresa = Empresa.objects.first()
    user = User.objects.filter(username='admin_admision').first()
    
    # Datos de pacientes de ejemplo
    pacientes_data = [
        {
            'numero_identificacion': '23456789',
            'primer_nombre': 'María',
            'primer_apellido': 'Rodríguez',
            'segundo_apellido': 'Vargas',
            'genero': 'F',
            'fecha_nacimiento': date(1990, 8, 22),
            'profesion_cargo': 'Contadora',
            'tipo_evaluacion': 'Examen médico ocupacional periódico'
        },
        {
            'numero_identificacion': '34567890',
            'primer_nombre': 'Carlos',
            'primer_apellido': 'Mendoza',
            'segundo_apellido': 'Silva',
            'genero': 'M',
            'fecha_nacimiento': date(1988, 3, 15),
            'profesion_cargo': 'Operador de Máquina',
            'tipo_evaluacion': 'Examen médico ocupacional de retiro'
        },
        {
            'numero_identificacion': '45678901',
            'primer_nombre': 'Ana',
            'primer_apellido': 'López',
            'segundo_apellido': 'Torres',
            'genero': 'F',
            'fecha_nacimiento': date(1985, 12, 8),
            'profesion_cargo': 'Supervisora de Producción',
            'tipo_evaluacion': 'Examen médico ocupacional de ingreso'
        },
        {
            'numero_identificacion': '56789012',
            'primer_nombre': 'Pedro',
            'primer_apellido': 'Sánchez',
            'segundo_apellido': 'Morales',
            'genero': 'M',
            'fecha_nacimiento': date(1982, 7, 30),
            'profesion_cargo': 'Técnico de Mantenimiento',
            'tipo_evaluacion': 'Examen médico ocupacional por cambio de cargo'
        },
        {
            'numero_identificacion': '67890123',
            'primer_nombre': 'Laura',
            'primer_apellido': 'González',
            'segundo_apellido': 'Herrera',
            'genero': 'F',
            'fecha_nacimiento': date(1992, 11, 18),
            'profesion_cargo': 'Analista de Sistemas',
            'tipo_evaluacion': 'Examen médico ocupacional de ingreso'
        }
    ]
    
    ordenes_creadas = []
    
    for i, data in enumerate(pacientes_data):
        orden_data = {
            'tipo_documento': 'CC',
            'ciudad_nacimiento': 'El Banco',
            'estado_civil': choice(['SOLTERO', 'CASADO', 'UNION_LIBRE']),
            'nivel_educativo': choice(['TECNICO', 'TECNOLOGO', 'PROFESIONAL']),
            'correo_electronico': f"{data['primer_nombre'].lower()}.{data['primer_apellido'].lower()}@example.com",
            'zona': 'URBANA',
            'direccion': f"Calle {randint(10, 90)} # {randint(10, 50)}-{randint(10, 90)}",
            'barrio': choice(['Centro', 'Norte', 'Sur', 'Oriental', 'Popular']),
            'localidad': f'Comuna {randint(1, 5)}',
            'sede': choice(['PRINCIPAL', 'SUCURSAL_1']),
            'estrato': choice(['2', '3', '4']),
            'municipio': municipio,
            'celulares': f"30{randint(0, 9)}-{randint(100, 999)}-{randint(1000, 9999)}",
            'telefonos': f"{randint(100, 999)}-{randint(1000, 9999)}",
            'funciones_cargo': f"Funciones específicas de {data['profesion_cargo'].lower()}",
            'convenio': convenio,
            'empresa_mision': empresa,
            'eps': choice(['EPS Salud Total', 'Nueva EPS', 'Sanitas']),
            'afp': choice(['AFP Protección', 'AFP Porvenir', 'Colfondos']),
            'arl': 'ARL Prevención',
            'observaciones': f"Examen programado para {data['primer_nombre']} {data['primer_apellido']}",
            'fecha_solicitud': date.today(),
            'fecha_orden': date.today(),
            'created_by': user
        }
        
        # Combinar datos
        orden_data.update(data)
        
        orden, created = OrdenServicio.objects.get_or_create(
            numero_identificacion=data['numero_identificacion'],
            defaults=orden_data
        )
        
        if created:
            print(f"  ✅ Orden creada: {orden.numero_orden} - {orden.nombre_completo}")
            ordenes_creadas.append(orden)
            
            # Agregar servicios aleatorios
            servicios_posibles = list(Servicio.objects.all())
            num_servicios = randint(2, 4)
            servicios_seleccionados = []
            
            for _ in range(num_servicios):
                servicio = choice(servicios_posibles)
                if servicio not in servicios_seleccionados:
                    servicios_seleccionados.append(servicio)
            
            for servicio in servicios_seleccionados:
                prestador = Prestador.objects.filter(
                    tipo__in=['MEDICO', 'LABORATORIO', 'RADIOLOGIA', 'CARDIOLOGIA']
                ).order_by('?').first()
                
                DetalleOrdenServicio.objects.create(
                    orden=orden,
                    cantidad=1,
                    servicio=servicio,
                    prestador=prestador,
                    valor_unitario=servicio.valor_base,
                    forma_pago='CONVENIO',
                    valor_pagar=servicio.valor_base
                )
            
            # Calcular totales
            orden.calcular_totales()
        else:
            print(f"  ⚠️  Orden ya existe: {orden.numero_orden}")
            ordenes_creadas.append(orden)
    
    return ordenes_creadas


def crear_seguimientos_ejemplo(ordenes):
    """Crear seguimientos de ejemplo para las órdenes"""
    print("\n👥 Creando seguimientos de ejemplo...")
    
    user = User.objects.filter(username='admin_admision').first()
    estados_posibles = ['EN_ESPERA', 'EN_ATENCION', 'ATENDIDO']
    
    for i, orden in enumerate(ordenes):
        # Limpiar seguimientos existentes
        orden.seguimientos.all().delete()
        
        # Crear seguimiento inicial (INGRESADO)
        seguimiento_inicial = SeguimientoPaciente.objects.create(
            orden=orden,
            estado='INGRESADO',
            fecha_estado=timezone.now() - timedelta(minutes=randint(30, 120)),
            observaciones=f'Paciente {orden.nombre_completo} ingresado al sistema',
            usuario=user
        )
        
        # Crear seguimiento actual basado en el índice para variedad
        if i < len(ordenes):
            estado_actual = estados_posibles[i % len(estados_posibles)]
            
            # Tiempo aleatorio desde el ingreso
            minutos_transcurridos = randint(5, 60)
            
            observaciones_por_estado = {
                'EN_ESPERA': [
                    'Paciente esperando en sala de espera',
                    'Documentos verificados, aguardando llamado',
                    'En espera de disponibilidad de médico',
                    'Paciente registrado, en cola de atención'
                ],
                'EN_ATENCION': [
                    'Paciente en consulta médica',
                    'Realizando exámenes médicos',
                    'En proceso de evaluación',
                    'Atención médica en progreso'
                ],
                'ATENDIDO': [
                    'Consulta médica completada',
                    'Exámenes realizados exitosamente',
                    'Evaluación médica finalizada',
                    'Paciente dado de alta'
                ]
            }
            
            seguimiento_actual = SeguimientoPaciente.objects.create(
                orden=orden,
                estado=estado_actual,
                fecha_estado=timezone.now() - timedelta(minutes=randint(0, minutos_transcurridos)),
                observaciones=choice(observaciones_por_estado[estado_actual]),
                usuario=user
            )
            
            print(f"  📊 {orden.numero_orden} - {orden.nombre_completo}: {estado_actual}")


def mostrar_resumen():
    """Mostrar resumen de órdenes y seguimientos"""
    print("\n" + "=" * 60)
    print("✅ ¡Seguimientos creados exitosamente!")
    print("\n📊 Resumen del Seguimiento:")
    
    # Contar por estados
    from django.db.models import Count
    from collections import Counter
    
    ordenes_hoy = OrdenServicio.objects.filter(fecha_orden=date.today())
    total_ordenes = ordenes_hoy.count()
    
    estados_count = Counter()
    for orden in ordenes_hoy:
        ultimo_seguimiento = orden.seguimientos.first()
        if ultimo_seguimiento:
            estados_count[ultimo_seguimiento.estado] += 1
    
    print(f"  📅 Órdenes de hoy: {total_ordenes}")
    print(f"  ⏳ En Espera: {estados_count.get('EN_ESPERA', 0)}")
    print(f"  🩺 En Atención: {estados_count.get('EN_ATENCION', 0)}")
    print(f"  ✅ Atendidos: {estados_count.get('ATENDIDO', 0)}")
    print(f"  📋 Total Seguimientos: {SeguimientoPaciente.objects.count()}")
    
    print("\n🔗 URLs de Seguimiento:")
    print("  👥 Seguimiento: http://localhost:8000/admision/seguimiento/")
    print("  📊 Dashboard: http://localhost:8000/admision/")
    print("  📋 Órdenes: http://localhost:8000/admision/ordenes/")


if __name__ == '__main__':
    print("🏥 Iniciando creación de seguimientos para pacientes")
    print("=" * 60)
    
    try:
        ordenes = crear_ordenes_ejemplo()
        crear_seguimientos_ejemplo(ordenes)
        mostrar_resumen()
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
