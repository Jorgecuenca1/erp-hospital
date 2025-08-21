#!/usr/bin/env python3
"""
Script para crear exámenes visuales de prueba
"""

import os
import sys
import django
from datetime import datetime, date, timedelta
import random

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HMetaHIS.settings')
django.setup()

from django.contrib.auth.models import User
from django.utils import timezone
from admision_recepcion.models import (
    FichaClinica, ExamenVisual, Empresa, Prestador, Municipio,
    AntecedenteVisual, DiagnosticoVisual, ConductaRecomendacionVisual
)


def crear_examenes_visuales():
    """Crear exámenes visuales de prueba"""
    
    # Obtener datos necesarios
    empresas = list(Empresa.objects.filter(activo=True))
    prestadores = list(Prestador.objects.filter(activo=True))
    municipios = list(Municipio.objects.filter(activo=True))
    admin_user = User.objects.filter(is_superuser=True).first()
    
    if not empresas or not prestadores:
        print("❌ Faltan datos básicos. Ejecute primero crear_datos_admision.py")
        return
    
    # Datos de trabajadores para examen visual
    trabajadores_data = [
        {
            'numero_identificacion': '22.345.678.901',
            'nombre_trabajador': 'CLAUDIA PATRICIA MORENO GARCIA',
            'genero': 'F',
            'edad': 29,
            'cargo': 'Secretaria',
            'motivo_consulta': 'Evaluación visual ocupacional periódica',
            'ultimo_examen': '15/01/2024',
            'lugar_ultimo_examen': 'Clínica Visual Los Andes'
        },
        {
            'numero_identificacion': '17.456.789.012',
            'nombre_trabajador': 'MIGUEL ANGEL RODRIGUEZ TORRES',
            'genero': 'M',
            'edad': 34,
            'cargo': 'Soldador',
            'motivo_consulta': 'Control visual por exposición a radiación',
            'ultimo_examen': '10/03/2024',
            'lugar_ultimo_examen': 'Centro Médico Industrial'
        },
        {
            'numero_identificacion': '40.567.890.123',
            'nombre_trabajador': 'MARIA JOSE VARGAS DELGADO',
            'genero': 'F',
            'edad': 26,
            'cargo': 'Operadora de PC',
            'motivo_consulta': 'Fatiga visual por trabajo con pantallas',
            'ultimo_examen': '05/02/2024',
            'lugar_ultimo_examen': 'Óptica Especializada'
        },
        {
            'numero_identificacion': '9.678.901.234',
            'nombre_trabajador': 'CARLOS EDUARDO SILVA MONTENEGRO',
            'genero': 'M',
            'edad': 41,
            'cargo': 'Supervisor de Calidad',
            'motivo_consulta': 'Examen visual ocupacional de ingreso',
            'ultimo_examen': 'Primer examen',
            'lugar_ultimo_examen': 'N/A'
        },
        {
            'numero_identificacion': '35.789.012.345',
            'nombre_trabajador': 'ANDREA MILENA CASTRO RUIZ',
            'genero': 'F',
            'edad': 32,
            'cargo': 'Diseñadora Gráfica',
            'motivo_consulta': 'Control visual por uso intensivo de monitor',
            'ultimo_examen': '20/01/2024',
            'lugar_ultimo_examen': 'Instituto de la Visión'
        }
    ]
    
    examenes_creados = 0
    
    for trabajador_data in trabajadores_data:
        # Verificar si ya existe
        if not FichaClinica.objects.filter(
            numero_identificacion=trabajador_data['numero_identificacion'],
            tipo_ficha='EXAMEN_VISUAL'
        ).exists():
            
            # Crear ficha clínica
            ficha = FichaClinica.objects.create(
                tipo_ficha='EXAMEN_VISUAL',
                fecha_evaluacion=date.today(),
                numero_identificacion=trabajador_data['numero_identificacion'],
                nombre_trabajador=trabajador_data['nombre_trabajador'],
                genero=trabajador_data['genero'],
                edad=trabajador_data['edad'],
                fecha_nacimiento=date.today() - timedelta(days=trabajador_data['edad'] * 365),
                empresa=random.choice(empresas),
                cargo=trabajador_data['cargo'],
                profesional_evaluador=random.choice(prestadores),
                municipio=municipios[0] if municipios else None,
                estado='PENDIENTE',
                created_by=admin_user
            )
            
            # Crear examen visual
            examen = ExamenVisual.objects.create(
                ficha_clinica=ficha,
                ultimo_examen=trabajador_data['ultimo_examen'],
                lugar_ultimo_examen=trabajador_data['lugar_ultimo_examen'],
                motivo_consulta=trabajador_data['motivo_consulta'],
                sintomatologia='ASINTOMATICO',
                # Agudeza visual sin corrección (valores realistas)
                ojo_derecho_vl_sc='20',
                ojo_derecho_vp_sc='20',
                ojo_derecho_ph_sc='20',
                ojo_izquierdo_vl_sc='20',
                ojo_izquierdo_vp_sc='20',
                ojo_izquierdo_ph_sc='20',
                ambos_ojos_vl_sc='20',
                ambos_ojos_vp_sc='20',
                ambos_ojos_ph_sc='20',
                # Agudeza visual con corrección
                ojo_derecho_vl_cc='20',
                ojo_derecho_vp_cc='20',
                ojo_izquierdo_vl_cc='20',
                ojo_izquierdo_vp_cc='20',
                ambos_ojos_vl_cc='20',
                ambos_ojos_vp_cc='20',
                # Examen externo
                ojo_derecho_externo='Normal, sin alteraciones aparentes',
                ojo_izquierdo_externo='Normal, sin alteraciones aparentes',
                # Otros campos por defecto
                reflejos_observacion='PRESENTES Y NORMALES',
                vision_lejana_cover='NORMAL',
                vision_proxima_cover='NORMAL',
                motilidad_observacion='NORMAL',
                convergencia_observacion='NORMAL',
                ojo_derecho_oftalmoscopia='FONDO DE OJO APARENTEMENTE NORMAL',
                ojo_izquierdo_oftalmoscopia='FONDO DE OJO APARENTEMENTE NORMAL',
                ojo_derecho_vision_color='NORMAL',
                ojo_izquierdo_vision_color='NORMAL',
                estereopsis_observacion='NORMAL',
                diagnostico_recomendaciones='Examen visual dentro de parámetros normales. Se recomienda control anual.'
            )
            
            # Crear antecedentes visuales por defecto
            tipos_antecedentes = [
                ('ANTECEDENTES_PERSONALES', 'NIEGA'),
                ('ANTECEDENTES_FAMILIARES', 'NIEGA'),
                ('ANTECEDENTES_OCUPACIONALES', 'NIEGA'),
                ('EXPOSICION_LABORAL_VISUAL', ''),
                ('USA_ANTEOJOS', 'NO USA'),
                ('MULTIFOCAL', 'NO'),
                ('LENTES_CONTACTO', 'NO USA'),
                ('TRAE_RX', 'NO'),
                ('TIPO_USO', 'NO APLICA'),
                ('ULTIMO_DIAGNOSTICO', '')
            ]
            
            for tipo, observacion in tipos_antecedentes:
                AntecedenteVisual.objects.create(
                    examen_visual=examen,
                    tipo_antecedente=tipo,
                    observacion=observacion
                )
            
            # Crear algunas conductas y recomendaciones por defecto
            conductas_default = [
                ('CONDUCTA', 'CONTROL_1_ANO', 'Control en un año', True),
                ('CONDUCTA', 'PAUSAS_ACTIVAS', 'Realizar pausas activas', True),
                ('CONDUCTA', 'PROTECCION_VISUAL', 'Uso de elementos de protección visual', False),
                ('REMISION', 'OFTALMOLOGIA', 'Valoración por Oftalmología', False),
            ]
            
            for tipo_item, codigo, descripcion, seleccionado in conductas_default:
                ConductaRecomendacionVisual.objects.create(
                    examen_visual=examen,
                    tipo_item=tipo_item,
                    codigo=codigo,
                    descripcion=descripcion,
                    seleccionado=seleccionado
                )
            
            examenes_creados += 1
            print(f"✅ Examen visual creado: {ficha.numero_ficha} - {ficha.nombre_trabajador}")
    
    print(f"\n🎉 Total de exámenes visuales creados: {examenes_creados}")
    
    # Mostrar estadísticas
    total_examenes = ExamenVisual.objects.count()
    examenes_asintomaticos = ExamenVisual.objects.filter(sintomatologia='ASINTOMATICO').count()
    
    print(f"\n📊 Estadísticas de exámenes visuales:")
    print(f"   - Total exámenes: {total_examenes}")
    print(f"   - Asintomáticos: {examenes_asintomaticos}")
    
    # Estadísticas por empresa
    print(f"\n🏢 Por empresa:")
    from django.db.models import Count
    empresas_stats = FichaClinica.objects.filter(
        tipo_ficha='EXAMEN_VISUAL',
        empresa__isnull=False
    ).values('empresa__razon_social').annotate(
        total=Count('id')
    ).order_by('-total')
    
    for empresa in empresas_stats:
        print(f"   - {empresa['empresa__razon_social']}: {empresa['total']} exámenes")
    
    # Estadísticas por profesional
    print(f"\n👨‍⚕️ Por profesional:")
    profesionales_stats = FichaClinica.objects.filter(
        tipo_ficha='EXAMEN_VISUAL',
        profesional_evaluador__isnull=False
    ).values('profesional_evaluador__nombre').annotate(
        total=Count('id')
    ).order_by('-total')
    
    for profesional in profesionales_stats:
        print(f"   - {profesional['profesional_evaluador__nombre']}: {profesional['total']} exámenes")


if __name__ == '__main__':
    print("👁️ Creando exámenes visuales de prueba...")
    crear_examenes_visuales()
    print("\n✅ Proceso completado!")
