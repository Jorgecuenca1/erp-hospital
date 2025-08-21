#!/usr/bin/env python3
"""
Script para crear evaluaciones osteomusculares de prueba
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
    FichaClinica, EvaluacionOsteomuscular, Empresa, Prestador, Municipio, RecomendacionOsteomuscular
)


def crear_evaluaciones_osteomusculares():
    """Crear evaluaciones osteomusculares de prueba"""
    
    # Obtener datos necesarios
    empresas = list(Empresa.objects.filter(activo=True))
    prestadores = list(Prestador.objects.filter(activo=True))
    municipios = list(Municipio.objects.filter(activo=True))
    admin_user = User.objects.filter(is_superuser=True).first()
    
    if not empresas or not prestadores:
        print("❌ Faltan datos básicos. Ejecute primero crear_datos_admision.py")
        return
    
    # Datos de trabajadores para evaluación osteomuscular
    trabajadores_data = [
        {
            'numero_identificacion': '43.123.456.789',
            'nombre_trabajador': 'MARIA ELENA RODRIGUEZ CASTRO',
            'genero': 'F',
            'edad': 32,
            'peso_kg': 62.0,
            'talla_cm': 165.0,
            'cargo': 'Secretaria Ejecutiva',
            'funciones_cargo': 'Trabajo prolongado en computador, digitación, atención telefónica',
            'tipo_evaluacion': 'OCUPACIONAL',
            'alteraciones_posturales': ['cervical', 'hombros', 'lumbar'],
            'pruebas_positivas': ['thomas_der', 'ober_izq'],
            'flexibilidad_alterada': ['flexibilidad_columna', 'isquiotibiales_izq']
        },
        {
            'numero_identificacion': '17.234.567.890',
            'nombre_trabajador': 'CARLOS ANDRES MARTINEZ LOPEZ',
            'genero': 'M',
            'edad': 38,
            'peso_kg': 78.5,
            'talla_cm': 175.0,
            'cargo': 'Operario de Construcción',
            'funciones_cargo': 'Carga manual, trabajo en alturas, posiciones forzadas',
            'tipo_evaluacion': 'PREOCUPACIONAL',
            'alteraciones_posturales': ['escapulas', 'pelvis'],
            'pruebas_positivas': ['lasegue_izq', 'cajon_anterior_der'],
            'flexibilidad_alterada': ['aductores_der', 'gastrocnemios_izq', 'gastrocnemios_der']
        },
        {
            'numero_identificacion': '52.345.678.901',
            'nombre_trabajador': 'ANA PATRICIA SUAREZ VILLA',
            'genero': 'F',
            'edad': 45,
            'peso_kg': 68.0,
            'talla_cm': 160.0,
            'cargo': 'Auxiliar de Enfermería',
            'funciones_cargo': 'Movilización de pacientes, bipedestación prolongada, flexiones',
            'tipo_evaluacion': 'OCUPACIONAL',
            'alteraciones_posturales': ['escoliosis', 'pelvis', 'dorsal'],
            'pruebas_positivas': ['thomas_izq', 'thomas_der', 'ely_der'],
            'flexibilidad_alterada': ['flexibilidad_columna', 'extensibilidad', 'isquiotibiales_der']
        },
        {
            'numero_identificacion': '24.456.789.012',
            'nombre_trabajador': 'JORGE LUIS HENAO GARCIA',
            'genero': 'M',
            'edad': 28,
            'peso_kg': 72.0,
            'talla_cm': 178.0,
            'cargo': 'Conductor Profesional',
            'funciones_cargo': 'Conducción prolongada, sedestación, vibraciones',
            'tipo_evaluacion': 'PREOCUPACIONAL',
            'alteraciones_posturales': ['cervical', 'lumbar'],
            'pruebas_positivas': ['lasegue_der', 'ober_der'],
            'flexibilidad_alterada': ['flexibilidad_hombros_der', 'isquiotibiales_izq', 'isquiotibiales_der']
        },
        {
            'numero_identificacion': '36.567.890.123',
            'nombre_trabajador': 'SANDRA MILENA TORRES RUIZ',
            'genero': 'F',
            'edad': 41,
            'peso_kg': 64.5,
            'talla_cm': 162.0,
            'cargo': 'Operaria Textil',
            'funciones_cargo': 'Trabajo repetitivo de manos, bipedestación, flexiones',
            'tipo_evaluacion': 'OCUPACIONAL',
            'alteraciones_posturales': ['hombros', 'torax'],
            'pruebas_positivas': ['bostezo_medial_izq', 'ely_izq'],
            'flexibilidad_alterada': ['flexibilidad_hombros_izq', 'aductores_izq']
        }
    ]
    
    evaluaciones_creadas = 0
    
    for trabajador_data in trabajadores_data:
        # Verificar si ya existe
        if not FichaClinica.objects.filter(
            numero_identificacion=trabajador_data['numero_identificacion'],
            tipo_ficha='OSTEOMUSCULAR'
        ).exists():
            
            # Crear ficha clínica
            ficha = FichaClinica.objects.create(
                tipo_ficha='OSTEOMUSCULAR',
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
            
            # Calcular IMC
            peso = trabajador_data['peso_kg']
            talla = trabajador_data['talla_cm']
            imc = peso / ((talla / 100) ** 2)
            
            # Crear evaluación osteomuscular
            evaluacion = EvaluacionOsteomuscular.objects.create(
                ficha_clinica=ficha,
                producto='Evaluación Osteomuscular Ocupacional',
                peso_kg=trabajador_data['peso_kg'],
                talla_cm=trabajador_data['talla_cm'],
                imc=round(imc, 2),
                funciones_cargo=trabajador_data['funciones_cargo'],
                
                # Evaluación postural basada en el trabajo
                evaluacion_postural_observaciones=f"Evaluación postural para {trabajador_data['cargo']} con alteraciones típicas de la ocupación",
                postura_anterior={'cabeza_anterior': 'cervical' in trabajador_data['alteraciones_posturales'], 
                                'hombros_anterior': 'hombros' in trabajador_data['alteraciones_posturales'],
                                'torax_anterior': 'torax' in trabajador_data['alteraciones_posturales']},
                postura_posterior={'escoliosis': 'escoliosis' in trabajador_data['alteraciones_posturales'],
                                 'escapulas': 'escapulas' in trabajador_data['alteraciones_posturales'],
                                 'pelvis_post': 'pelvis' in trabajador_data['alteraciones_posturales']},
                postura_lateral_izq={'cervical_izq': 'cervical' in trabajador_data['alteraciones_posturales'],
                                   'dorsal_izq': 'dorsal' in trabajador_data['alteraciones_posturales'],
                                   'lumbar_izq': 'lumbar' in trabajador_data['alteraciones_posturales']},
                postura_lateral_der={'cervical_der': 'cervical' in trabajador_data['alteraciones_posturales'],
                                   'dorsal_der': 'dorsal' in trabajador_data['alteraciones_posturales'],
                                   'lumbar_der': 'lumbar' in trabajador_data['alteraciones_posturales']},
                
                # Medidas de longitud (simuladas)
                longitud_real=round(talla - random.uniform(0, 2), 1),
                longitud_aparente=round(talla - random.uniform(0, 3), 1),
                
                # Flexibilidad según el cargo
                extensibilidad='MODERADO' if 'extensibilidad' in trabajador_data['flexibilidad_alterada'] else random.choice(['LEVE', '']),
                flexibilidad_columna='SEVERO' if 'flexibilidad_columna' in trabajador_data['flexibilidad_alterada'] else random.choice(['LEVE', 'MODERADO', '']),
                flexibilidad_hombros_izq='MODERADO' if 'flexibilidad_hombros_izq' in trabajador_data['flexibilidad_alterada'] else '',
                flexibilidad_hombros_der='MODERADO' if 'flexibilidad_hombros_der' in trabajador_data['flexibilidad_alterada'] else '',
                aductores_izq='LEVE' if 'aductores_izq' in trabajador_data['flexibilidad_alterada'] else '',
                aductores_der='LEVE' if 'aductores_der' in trabajador_data['flexibilidad_alterada'] else '',
                gastrocnemios_izq='MODERADO' if 'gastrocnemios_izq' in trabajador_data['flexibilidad_alterada'] else '',
                gastrocnemios_der='MODERADO' if 'gastrocnemios_der' in trabajador_data['flexibilidad_alterada'] else '',
                isquiotibiales_izq='SEVERO' if 'isquiotibiales_izq' in trabajador_data['flexibilidad_alterada'] else '',
                isquiotibiales_der='SEVERO' if 'isquiotibiales_der' in trabajador_data['flexibilidad_alterada'] else '',
                
                # Pruebas semiológicas específicas
                bostezo_medial_izq='POSITIVO' if 'bostezo_medial_izq' in trabajador_data['pruebas_positivas'] else 'NEGATIVO',
                bostezo_medial_der='POSITIVO' if 'bostezo_medial_der' in trabajador_data['pruebas_positivas'] else 'NEGATIVO',
                bostezo_lateral_izq='POSITIVO' if 'bostezo_lateral_izq' in trabajador_data['pruebas_positivas'] else 'NEGATIVO',
                bostezo_lateral_der='POSITIVO' if 'bostezo_lateral_der' in trabajador_data['pruebas_positivas'] else 'NEGATIVO',
                cajon_anterior_izq='POSITIVO' if 'cajon_anterior_izq' in trabajador_data['pruebas_positivas'] else 'NEGATIVO',
                cajon_anterior_der='POSITIVO' if 'cajon_anterior_der' in trabajador_data['pruebas_positivas'] else 'NEGATIVO',
                cajon_posterior_izq='POSITIVO' if 'cajon_posterior_izq' in trabajador_data['pruebas_positivas'] else 'NEGATIVO',
                cajon_posterior_der='POSITIVO' if 'cajon_posterior_der' in trabajador_data['pruebas_positivas'] else 'NEGATIVO',
                thomas_izq='POSITIVO' if 'thomas_izq' in trabajador_data['pruebas_positivas'] else 'NEGATIVO',
                thomas_der='POSITIVO' if 'thomas_der' in trabajador_data['pruebas_positivas'] else 'NEGATIVO',
                ober_izq='POSITIVO' if 'ober_izq' in trabajador_data['pruebas_positivas'] else 'NEGATIVO',
                ober_der='POSITIVO' if 'ober_der' in trabajador_data['pruebas_positivas'] else 'NEGATIVO',
                ely_izq='POSITIVO' if 'ely_izq' in trabajador_data['pruebas_positivas'] else 'NEGATIVO',
                ely_der='POSITIVO' if 'ely_der' in trabajador_data['pruebas_positivas'] else 'NEGATIVO',
                lasegue_izq='POSITIVO' if 'lasegue_izq' in trabajador_data['pruebas_positivas'] else 'NEGATIVO',
                lasegue_der='POSITIVO' if 'lasegue_der' in trabajador_data['pruebas_positivas'] else 'NEGATIVO',
                
                # Análisis de marcha (generalmente normal en evaluaciones ocupacionales)
                choque_talon_izq=random.choice(['NORMAL', 'ALTERADA']) if random.random() < 0.2 else 'NORMAL',
                choque_talon_der=random.choice(['NORMAL', 'ALTERADA']) if random.random() < 0.2 else 'NORMAL',
                apoyo_plantar_izq=random.choice(['NORMAL', 'ALTERADA']) if random.random() < 0.15 else 'NORMAL',
                apoyo_plantar_der=random.choice(['NORMAL', 'ALTERADA']) if random.random() < 0.15 else 'NORMAL',
                apoyo_medio_izq='NORMAL',
                apoyo_medio_der='NORMAL',
                empuje_izq='NORMAL',
                empuje_der='NORMAL',
                aceleracion_izq='NORMAL',
                aceleracion_der='NORMAL',
                balanceo_medio_izq='NORMAL',
                balanceo_medio_der='NORMAL',
                desaceleracion_izq='NORMAL',
                desaceleracion_der='NORMAL',
                
                observaciones=f"Evaluación osteomuscular para {trabajador_data['cargo']}. "
                            f"Se evidencian alteraciones posturales compatibles con las actividades laborales. "
                            f"Se recomienda programa de pausas activas y fortalecimiento muscular específico."
            )
            
            # Crear recomendaciones según los hallazgos
            recomendaciones = []
            
            # Recomendaciones basadas en alteraciones posturales
            if len(trabajador_data['alteraciones_posturales']) > 2:
                recomendaciones.append(('Programa de higiene postural y ergonomía laboral', 'ERGONOMIA'))
                recomendaciones.append(('Fisioterapia para corrección postural', 'FISIOTERAPIA'))
            
            # Recomendaciones basadas en pruebas positivas
            if len(trabajador_data['pruebas_positivas']) > 1:
                recomendaciones.append(('Valoración por medicina física y rehabilitación', 'REMISION'))
                recomendaciones.append(('Ejercicios de fortalecimiento y estiramiento específicos', 'EJERCICIO'))
            
            # Recomendaciones basadas en flexibilidad alterada
            if len(trabajador_data['flexibilidad_alterada']) > 1:
                recomendaciones.append(('Programa de pausas activas cada 2 horas', 'ERGONOMIA'))
                recomendaciones.append(('Ejercicios de flexibilidad y movilidad articular', 'EJERCICIO'))
            
            # Recomendaciones específicas por cargo
            if 'Secretaria' in trabajador_data['cargo']:
                recomendaciones.append(('Ajuste ergonómico de puesto de trabajo (silla, monitor, teclado)', 'ERGONOMIA'))
                recomendaciones.append(('Ejercicios para síndrome del túnel del carpo', 'FISIOTERAPIA'))
            elif 'Construcción' in trabajador_data['cargo']:
                recomendaciones.append(('Entrenamiento en técnicas de levantamiento seguro', 'ERGONOMIA'))
                recomendaciones.append(('Uso obligatorio de faja lumbar para cargas >15kg', 'ERGONOMIA'))
            elif 'Enfermería' in trabajador_data['cargo']:
                recomendaciones.append(('Técnicas de movilización y transferencia de pacientes', 'ERGONOMIA'))
                recomendaciones.append(('Fortalecimiento del core y musculatura paravertebral', 'EJERCICIO'))
            elif 'Conductor' in trabajador_data['cargo']:
                recomendaciones.append(('Ajuste ergonómico del asiento y volante', 'ERGONOMIA'))
                recomendaciones.append(('Paradas obligatorias para estiramiento cada hora', 'ERGONOMIA'))
            elif 'Textil' in trabajador_data['cargo']:
                recomendaciones.append(('Rotación de tareas para evitar movimientos repetitivos', 'ERGONOMIA'))
                recomendaciones.append(('Ejercicios para manos y muñecas', 'FISIOTERAPIA'))
            
            # Siempre agregar control
            recomendaciones.append(('Control osteomuscular según periodicidad ocupacional', 'CONTROL_MEDICO'))
            
            # Crear recomendaciones en la base de datos
            for recomendacion_texto, tipo in recomendaciones:
                RecomendacionOsteomuscular.objects.create(
                    evaluacion_osteomuscular=evaluacion,
                    recomendacion=recomendacion_texto,
                    tipo=tipo
                )
            
            evaluaciones_creadas += 1
            print(f"✅ Evaluación Osteomuscular creada: {ficha.numero_ficha} - {ficha.nombre_trabajador}")
            print(f"   🦴 IMC: {evaluacion.imc}, Alteraciones posturales: {len(trabajador_data['alteraciones_posturales'])}")
            print(f"   🔍 Pruebas positivas: {len(trabajador_data['pruebas_positivas'])}, Flexibilidad alterada: {len(trabajador_data['flexibilidad_alterada'])}")
    
    print(f"\n🎉 Total de evaluaciones osteomusculares creadas: {evaluaciones_creadas}")
    
    # Mostrar estadísticas
    total_evaluaciones = EvaluacionOsteomuscular.objects.count()
    
    print(f"\n📊 Estadísticas de evaluaciones osteomusculares:")
    print(f"   - Total evaluaciones: {total_evaluaciones}")
    
    # Estadísticas por flexibilidad
    from django.db.models import Count
    
    # Contar alteraciones posturales
    evaluaciones_con_alteraciones = 0
    for eval_obj in EvaluacionOsteomuscular.objects.all():
        if eval_obj.get_alteraciones_posturales_total() > 0:
            evaluaciones_con_alteraciones += 1
    
    print(f"\n🦴 Evaluación Postural:")
    print(f"   - Con alteraciones posturales: {evaluaciones_con_alteraciones}")
    print(f"   - Sin alteraciones posturales: {total_evaluaciones - evaluaciones_con_alteraciones}")
    
    # Contar pruebas positivas
    evaluaciones_con_pruebas_positivas = 0
    for eval_obj in EvaluacionOsteomuscular.objects.all():
        if len(eval_obj.get_pruebas_positivas()) > 0:
            evaluaciones_con_pruebas_positivas += 1
    
    print(f"\n🔍 Pruebas Semiológicas:")
    print(f"   - Con pruebas positivas: {evaluaciones_con_pruebas_positivas}")
    print(f"   - Todas negativas: {total_evaluaciones - evaluaciones_con_pruebas_positivas}")
    
    # Estadísticas por empresa
    print(f"\n🏢 Por empresa:")
    empresas_stats = FichaClinica.objects.filter(
        tipo_ficha='OSTEOMUSCULAR',
        empresa__isnull=False
    ).values('empresa__razon_social').annotate(
        total=Count('id')
    ).order_by('-total')
    
    for empresa in empresas_stats:
        print(f"   - {empresa['empresa__razon_social']}: {empresa['total']} evaluaciones")
    
    # Estadísticas por tipo de cargo
    print(f"\n💼 Por tipo de cargo:")
    cargos_stats = FichaClinica.objects.filter(
        tipo_ficha='OSTEOMUSCULAR'
    ).values('cargo').annotate(
        total=Count('id')
    ).order_by('-total')
    
    for cargo in cargos_stats:
        print(f"   - {cargo['cargo']}: {cargo['total']} evaluaciones")
    
    # Estadísticas por flexibilidad alterada
    flexibilidad_stats = {
        'Extensibilidad': EvaluacionOsteomuscular.objects.exclude(extensibilidad__in=['', 'NO_APLICA']).count(),
        'Flexibilidad Columna': EvaluacionOsteomuscular.objects.exclude(flexibilidad_columna__in=['', 'NO_APLICA']).count(),
        'Aductores': EvaluacionOsteomuscular.objects.exclude(aductores_izq__in=['', 'NO_APLICA']).count() + 
                    EvaluacionOsteomuscular.objects.exclude(aductores_der__in=['', 'NO_APLICA']).count(),
        'Gastrocnemios': EvaluacionOsteomuscular.objects.exclude(gastrocnemios_izq__in=['', 'NO_APLICA']).count() + 
                        EvaluacionOsteomuscular.objects.exclude(gastrocnemios_der__in=['', 'NO_APLICA']).count(),
        'Isquiotibiales': EvaluacionOsteomuscular.objects.exclude(isquiotibiales_izq__in=['', 'NO_APLICA']).count() + 
                         EvaluacionOsteomuscular.objects.exclude(isquiotibiales_der__in=['', 'NO_APLICA']).count(),
    }
    
    print(f"\n🤸‍♀️ Alteraciones de flexibilidad:")
    for tipo, count in flexibilidad_stats.items():
        print(f"   - {tipo}: {count} alteraciones")


if __name__ == '__main__':
    print("🦴 Creando evaluaciones osteomusculares de prueba...")
    crear_evaluaciones_osteomusculares()
    print("\n✅ Proceso completado!")
