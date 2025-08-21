#!/usr/bin/env python3
"""
Script para crear fichas clínicas de evaluación ocupacional de prueba
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
    FichaClinica, EvaluacionOcupacional, Empresa, Prestador, Municipio,
    AntecedenteFamiliar, AntecedentePersonal, AntecedenteSistema
)


def crear_fichas_clinicas():
    """Crear fichas clínicas de prueba"""
    
    # Obtener datos necesarios
    empresas = list(Empresa.objects.filter(activo=True))
    prestadores = list(Prestador.objects.filter(activo=True))
    municipios = list(Municipio.objects.filter(activo=True))
    admin_user = User.objects.filter(is_superuser=True).first()
    
    if not empresas or not prestadores:
        print("❌ Faltan datos básicos. Ejecute primero crear_datos_admision.py")
        return
    
    # Datos de trabajadores de ejemplo
    trabajadores_data = [
        {
            'numero_identificacion': '1.123.456.789',
            'nombre_trabajador': 'CARLOS ALBERTO MARTINEZ LOPEZ',
            'genero': 'M',
            'edad': 35,
            'tipo_evaluacion': 'INGRESO',
            'actividad_economica': 'Construcción de edificaciones residenciales',
            'cargo': 'Ingeniero Civil',
            'eps': 'SURA EPS',
            'arl': 'SURA ARL'
        },
        {
            'numero_identificacion': '43.567.890.123',
            'nombre_trabajador': 'MARIA FERNANDA GARCIA RODRIGUEZ',
            'genero': 'F',
            'edad': 28,
            'tipo_evaluacion': 'PERIODICA',
            'actividad_economica': 'Servicios administrativos y de apoyo',
            'cargo': 'Secretaria Ejecutiva',
            'eps': 'COMPENSAR EPS',
            'arl': 'POSITIVA ARL'
        },
        {
            'numero_identificacion': '8.234.567.890',
            'nombre_trabajador': 'JOSE FERNANDO RODRIGUEZ PEREZ',
            'genero': 'M',
            'edad': 42,
            'tipo_evaluacion': 'TRABAJO_ALTURAS',
            'actividad_economica': 'Mantenimiento industrial',
            'cargo': 'Técnico en Mantenimiento',
            'eps': 'NUEVA EPS',
            'arl': 'LIBERTY ARL'
        },
        {
            'numero_identificacion': '52.345.678.901',
            'nombre_trabajador': 'ANA CRISTINA LOPEZ MORALES',
            'genero': 'F',
            'edad': 31,
            'tipo_evaluacion': 'RETIRO',
            'actividad_economica': 'Educación superior',
            'cargo': 'Docente Universitaria',
            'eps': 'SANITAS EPS',
            'arl': 'SURA ARL'
        },
        {
            'numero_identificacion': '15.678.901.234',
            'nombre_trabajador': 'LUIS EDUARDO HERRERA SILVA',
            'genero': 'M',
            'edad': 39,
            'tipo_evaluacion': 'ESPACIOS_CONFINADOS',
            'actividad_economica': 'Industria petroquímica',
            'cargo': 'Supervisor de Seguridad',
            'eps': 'MEDIMAS EPS',
            'arl': 'MAPFRE ARL'
        }
    ]
    
    fichas_creadas = 0
    
    for trabajador_data in trabajadores_data:
        # Verificar si ya existe
        if not FichaClinica.objects.filter(
            numero_identificacion=trabajador_data['numero_identificacion']
        ).exists():
            
            # Crear ficha clínica
            ficha = FichaClinica.objects.create(
                tipo_ficha='EVALUACION_OCUPACIONAL',
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
            
            # Crear evaluación ocupacional
            evaluacion = EvaluacionOcupacional.objects.create(
                ficha_clinica=ficha,
                tipo_evaluacion=trabajador_data['tipo_evaluacion'],
                actividad_economica=trabajador_data['actividad_economica'],
                estado_civil=random.choice(['SOLTERO', 'CASADO', 'UNION_LIBRE']),
                nivel_educativo=random.choice(['UNIVERSITARIO', 'TECNICO', 'SECUNDARIA_COMPLETA']),
                eps=trabajador_data['eps'],
                arl=trabajador_data['arl'],
                afp='PROTECCION',
                tipo_sangre=random.choice(['O+', 'A+', 'B+', 'AB+']),
                numero_hijos=random.randint(0, 3),
                jornada_laboral=random.choice(['DIURNA', 'MIXTA']),
                area_cargo=random.choice(['OPERATIVA', 'ADMINISTRATIVA', 'TECNICA']),
                profesion_cargo=trabajador_data['cargo'],
                motivo_consulta=f"Evaluación médica ocupacional {trabajador_data['tipo_evaluacion'].lower()}",
                # EPP comunes
                epp_casco=True,
                epp_botas=True,
                epp_guantes=True,
                epp_tapabocas=True,
                epp_gafas=random.choice([True, False]),
                epp_auditivos=random.choice([True, False])
            )
            
            # Crear antecedentes familiares por defecto
            patologias_familiares = [
                'ASMA', 'CANCER', 'DIABETES', 'ENFERMEDAD_CORONARIA',
                'ACCIDENTE_CEREBRO_VASCULAR', 'HIPERTENSION_ARTERIAL',
                'COLAGENOSIS', 'PATOLOGIAS_TIROIDEAS'
            ]
            
            for patologia in patologias_familiares:
                AntecedenteFamiliar.objects.create(
                    evaluacion_ocupacional=evaluacion,
                    patologia=patologia,
                    parentesco='NO_REFIERE'
                )
            
            # Crear antecedentes personales por defecto
            tipos_antecedentes = [
                'PATOLOGICOS', 'QUIRURGICOS', 'TRAUMATICOS', 'FARMACOLOGICOS',
                'ALERGICOS', 'PSIQUIATRICOS', 'FOBIAS'
            ]
            
            for tipo in tipos_antecedentes:
                AntecedentePersonal.objects.create(
                    evaluacion_ocupacional=evaluacion,
                    tipo_antecedente=tipo,
                    diagnostico_observaciones='NO REFIERE'
                )
            
            # Crear antecedentes por sistemas por defecto
            sistemas = [
                'CABEZA', 'OJOS', 'OIDOS', 'NARIZ', 'BOCA', 'GARGANTA', 'CUELLO',
                'SISTEMA_ENDOCRINO', 'SISTEMA_CIRCULATORIO', 'SISTEMA_RESPIRATORIO',
                'SISTEMA_GASTROINTESTINAL', 'SISTEMA_GENITOURINARIO',
                'SISTEMA_OSTEOMUSCULAR', 'SISTEMA_NERVIOSO', 'PSIQUIATRICO', 'PIEL_ANEXOS'
            ]
            
            for sistema in sistemas:
                AntecedenteSistema.objects.create(
                    evaluacion_ocupacional=evaluacion,
                    nombre_sistema=sistema,
                    patologicos='NIEGA',
                    quirurgicos='NIEGA',
                    traumaticos='NIEGA'
                )
            
            fichas_creadas += 1
            print(f"✅ Ficha creada: {ficha.numero_ficha} - {ficha.nombre_trabajador}")
    
    print(f"\n🎉 Total de fichas clínicas creadas: {fichas_creadas}")
    
    # Mostrar estadísticas
    total_fichas = FichaClinica.objects.count()
    evaluaciones = FichaClinica.objects.filter(tipo_ficha='EVALUACION_OCUPACIONAL').count()
    pendientes = FichaClinica.objects.filter(estado='PENDIENTE').count()
    
    print(f"\n📊 Estadísticas de fichas clínicas:")
    print(f"   - Total fichas: {total_fichas}")
    print(f"   - Evaluaciones ocupacionales: {evaluaciones}")
    print(f"   - Estado pendiente: {pendientes}")
    
    # Estadísticas por tipo de evaluación
    print(f"\n🏥 Por tipo de evaluación:")
    from django.db.models import Count
    tipos = EvaluacionOcupacional.objects.values('tipo_evaluacion').annotate(
        total=Count('id')
    ).order_by('-total')
    
    for tipo in tipos:
        nombre_tipo = dict(EvaluacionOcupacional.TIPO_EVALUACION_CHOICES).get(
            tipo['tipo_evaluacion'], tipo['tipo_evaluacion']
        )
        print(f"   - {nombre_tipo}: {tipo['total']} evaluaciones")
    
    # Estadísticas por empresa
    print(f"\n🏢 Por empresa:")
    empresas_stats = FichaClinica.objects.filter(
        empresa__isnull=False
    ).values('empresa__razon_social').annotate(
        total=Count('id')
    ).order_by('-total')
    
    for empresa in empresas_stats:
        print(f"   - {empresa['empresa__razon_social']}: {empresa['total']} fichas")


if __name__ == '__main__':
    print("🚀 Creando fichas clínicas de evaluación ocupacional...")
    crear_fichas_clinicas()
    print("\n✅ Proceso completado!")
