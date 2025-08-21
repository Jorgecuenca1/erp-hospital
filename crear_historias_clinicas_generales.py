#!/usr/bin/env python3
"""
Script para crear historias clínicas generales de prueba
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
    FichaClinica, HistoriaClinicaGeneral, AntecedenteFamiliarGeneral, AntecedentePersonalGeneral,
    DiagnosticoGeneral, OrdenMedicamento, OrdenServicioGeneral, OrdenRemision, 
    EvolucionGeneral, Empresa, Prestador, Municipio
)


def crear_historias_clinicas_generales():
    """Crear historias clínicas generales de prueba"""
    
    # Obtener datos necesarios
    empresas = list(Empresa.objects.filter(activo=True))
    prestadores = list(Prestador.objects.filter(activo=True))
    municipios = list(Municipio.objects.filter(activo=True))
    admin_user = User.objects.filter(is_superuser=True).first()
    
    if not empresas or not prestadores:
        print("❌ Faltan datos básicos. Ejecute primero crear_datos_admision.py")
        return
    
    # Datos de pacientes para historia clínica general
    pacientes_data = [
        {
            'numero_identificacion': '27.123.456.789',
            'nombre_trabajador': 'MARIA FERNANDA GUTIERREZ PEÑA',
            'genero': 'F',
            'edad': 35,
            'peso_kg': 65.0,
            'talla_cm': 162.0,
            'estado_civil': 'CASADO',
            'nivel_educativo': 'UNIVERSITARIO',
            'cargo': 'Contadora Pública',
            'tipo_evaluacion': 'CONSULTA_EXTERNA',
            'motivo_consulta': 'Control médico preventivo anual y certificación médica laboral',
            'enfermedad_actual': 'Paciente refiere encontrarse asintomática, acude para control médico rutinario',
            'tension_sistolica': 118,
            'tension_diastolica': 78,
            'frecuencia_cardiaca': 72,
            'frecuencia_respiratoria': 16,
            'pulsioximetria': 98,
            'temperatura': 36.5,
            'perimetro_abdominal': 82.0,
            'eps': 'Sanitas EPS',
            'afp': 'Porvenir',
            'arl': 'Positiva',
            'antecedentes_familiares': {
                'HIPERTENSION_ARTERIAL': 'Madre hipertensa desde los 45 años',
                'DIABETES': 'NO REFIERE',
                'CANCER': 'Tía materna con cáncer de mama',
                'OTROS': 'NO REFIERE'
            },
            'antecedentes_personales': {
                'HTA': 'NO REFIERE',
                'DIABETES': 'NO REFIERE',
                'ENF_RENAL': 'NO REFIERE',
                'QUIRURGICOS': 'Cesárea hace 5 años',
                'TOXICOS_ALERGICOS': 'Alergia a penicilina'
            },
            'diagnosticos': [
                ('Z00.0', 'Examen médico general', 'PRINCIPAL'),
                ('Z76.3', 'Persona en buena salud que acompaña a persona enferma', 'RELACIONADO_1')
            ]
        },
        {
            'numero_identificacion': '15.234.567.890',
            'nombre_trabajador': 'CARLOS EDUARDO MARTINEZ SILVA',
            'genero': 'M',
            'edad': 42,
            'peso_kg': 78.5,
            'talla_cm': 175.0,
            'estado_civil': 'CASADO',
            'nivel_educativo': 'SECUNDARIA',
            'cargo': 'Supervisor de Obra',
            'tipo_evaluacion': 'OCUPACIONAL',
            'motivo_consulta': 'Evaluación médica ocupacional periódica',
            'enfermedad_actual': 'Paciente refiere dolor lumbar ocasional relacionado con actividades laborales',
            'tension_sistolica': 138,
            'tension_diastolica': 88,
            'frecuencia_cardiaca': 78,
            'frecuencia_respiratoria': 18,
            'pulsioximetria': 97,
            'temperatura': 36.7,
            'perimetro_abdominal': 96.0,
            'eps': 'Nueva EPS',
            'afp': 'Colpensiones',
            'arl': 'ARL SURA',
            'antecedentes_familiares': {
                'HIPERTENSION_ARTERIAL': 'Padre y hermano hipertensos',
                'DIABETES': 'Padre diabético tipo 2',
                'CANCER': 'NO REFIERE',
                'OTROS': 'NO REFIERE'
            },
            'antecedentes_personales': {
                'HTA': 'Prehipertensión en controles previos',
                'DIABETES': 'NO REFIERE',
                'TRAUMATICO': 'Fractura de brazo derecho hace 10 años',
                'QUIRURGICOS': 'Apendicectomía hace 15 años'
            },
            'diagnosticos': [
                ('M54.5', 'Dolor lumbar', 'PRINCIPAL'),
                ('I10', 'Hipertensión esencial', 'RELACIONADO_1')
            ]
        },
        {
            'numero_identificacion': '33.345.678.901',
            'nombre_trabajador': 'ANA LUCIA RODRIGUEZ VARGAS',
            'genero': 'F',
            'edad': 28,
            'peso_kg': 58.0,
            'talla_cm': 165.0,
            'estado_civil': 'SOLTERO',
            'nivel_educativo': 'TECNOLOGICO',
            'cargo': 'Auxiliar de Enfermería',
            'tipo_evaluacion': 'PREOCUPACIONAL',
            'motivo_consulta': 'Evaluación médica preocupacional para ingreso laboral',
            'enfermedad_actual': 'Paciente asintomática, refiere buen estado de salud general',
            'tension_sistolica': 110,
            'tension_diastolica': 70,
            'frecuencia_cardiaca': 68,
            'frecuencia_respiratoria': 16,
            'pulsioximetria': 99,
            'temperatura': 36.3,
            'perimetro_abdominal': 75.0,
            'eps': 'Compensar EPS',
            'afp': 'Colfondos',
            'arl': 'Colmena',
            'antecedentes_familiares': {
                'HIPERTENSION_ARTERIAL': 'NO REFIERE',
                'DIABETES': 'NO REFIERE',
                'CANCER': 'NO REFIERE',
                'OTROS': 'NO REFIERE'
            },
            'antecedentes_personales': {
                'HTA': 'NO REFIERE',
                'DIABETES': 'NO REFIERE',
                'HOSPITALIZACIONES': 'NO REFIERE',
                'QUIRURGICOS': 'NO REFIERE',
                'INMUNOLOGICOS': 'Esquema de vacunación completo'
            },
            'diagnosticos': [
                ('Z02.1', 'Examen médico preocupacional', 'PRINCIPAL')
            ]
        },
        {
            'numero_identificacion': '19.456.789.012',
            'nombre_trabajador': 'JORGE MARIO HERRERA CASTRO',
            'genero': 'M',
            'edad': 55,
            'peso_kg': 85.0,
            'talla_cm': 170.0,
            'estado_civil': 'DIVORCIADO',
            'nivel_educativo': 'UNIVERSITARIO',
            'cargo': 'Gerente Comercial',
            'tipo_evaluacion': 'CONSULTA_EXTERNA',
            'motivo_consulta': 'Control médico y seguimiento de hipertensión arterial',
            'enfermedad_actual': 'Paciente con diagnóstico previo de HTA en tratamiento farmacológico',
            'tension_sistolica': 145,
            'tension_diastolica': 92,
            'frecuencia_cardiaca': 82,
            'frecuencia_respiratoria': 18,
            'pulsioximetria': 96,
            'temperatura': 36.8,
            'perimetro_abdominal': 102.0,
            'eps': 'Famisanar EPS',
            'afp': 'Protección',
            'arl': 'SURA',
            'antecedentes_familiares': {
                'HIPERTENSION_ARTERIAL': 'Ambos padres hipertensos',
                'DIABETES': 'Madre diabética',
                'CANCER': 'Abuelo paterno cáncer de próstata',
                'OTROS': 'NO REFIERE'
            },
            'antecedentes_personales': {
                'HTA': 'Hipertensión arterial diagnosticada hace 5 años',
                'DIABETES': 'NO REFIERE',
                'FARMACOLOGICOS': 'Losartán 50mg/día, Amlodipino 5mg/día',
                'TOXICOS_ALERGICOS': 'Exfumador hace 3 años'
            },
            'diagnosticos': [
                ('I10', 'Hipertensión esencial', 'PRINCIPAL'),
                ('E66.9', 'Obesidad no especificada', 'RELACIONADO_1'),
                ('Z87.891', 'Historia personal de uso de tabaco', 'RELACIONADO_2')
            ]
        },
        {
            'numero_identificacion': '41.567.890.123',
            'nombre_trabajador': 'PATRICIA ELENA MORALES DIAZ',
            'genero': 'F',
            'edad': 48,
            'peso_kg': 72.0,
            'talla_cm': 158.0,
            'estado_civil': 'VIUDO',
            'nivel_educativo': 'PRIMARIA',
            'cargo': 'Operaria de Confección',
            'tipo_evaluacion': 'OCUPACIONAL',
            'motivo_consulta': 'Evaluación médica ocupacional y control de diabetes',
            'enfermedad_actual': 'Paciente diabética tipo 2 en tratamiento, refiere buen control metabólico',
            'tension_sistolica': 125,
            'tension_diastolica': 82,
            'frecuencia_cardiaca': 75,
            'frecuencia_respiratoria': 17,
            'pulsioximetria': 98,
            'temperatura': 36.4,
            'perimetro_abdominal': 88.0,
            'eps': 'Medimás EPS',
            'afp': 'Colpensiones',
            'arl': 'Positiva',
            'antecedentes_familiares': {
                'HIPERTENSION_ARTERIAL': 'Madre hipertensa',
                'DIABETES': 'Padre y hermana diabéticos',
                'CANCER': 'NO REFIERE',
                'OTROS': 'NO REFIERE'
            },
            'antecedentes_personales': {
                'DIABETES': 'Diabetes mellitus tipo 2 hace 8 años',
                'HTA': 'NO REFIERE',
                'FARMACOLOGICOS': 'Metformina 850mg c/12h',
                'OFTALMICOS': 'Retinopatía diabética leve'
            },
            'diagnosticos': [
                ('E11.9', 'Diabetes mellitus tipo 2 sin complicaciones', 'PRINCIPAL'),
                ('H36.0', 'Retinopatía diabética', 'RELACIONADO_1')
            ]
        }
    ]
    
    historias_creadas = 0
    
    for paciente_data in pacientes_data:
        # Verificar si ya existe
        if not FichaClinica.objects.filter(
            numero_identificacion=paciente_data['numero_identificacion'],
            tipo_ficha='HISTORIA_CLINICA_GENERAL'
        ).exists():
            
            # Crear ficha clínica
            ficha = FichaClinica.objects.create(
                tipo_ficha='HISTORIA_CLINICA_GENERAL',
                fecha_evaluacion=date.today(),
                numero_identificacion=paciente_data['numero_identificacion'],
                nombre_trabajador=paciente_data['nombre_trabajador'],
                genero=paciente_data['genero'],
                edad=paciente_data['edad'],
                fecha_nacimiento=date.today() - timedelta(days=paciente_data['edad'] * 365),
                empresa=random.choice(empresas),
                cargo=paciente_data['cargo'],
                profesional_evaluador=random.choice(prestadores),
                municipio=municipios[0] if municipios else None,
                estado='COMPLETADA',
                created_by=admin_user
            )
            
            # Calcular IMC y clasificación TA
            peso = paciente_data['peso_kg']
            talla = paciente_data['talla_cm']
            imc = peso / ((talla / 100) ** 2)
            
            # Crear historia clínica general
            historia = HistoriaClinicaGeneral.objects.create(
                ficha_clinica=ficha,
                tipo_evaluacion_medica=paciente_data['tipo_evaluacion'],
                estado_civil=paciente_data['estado_civil'],
                nivel_educativo=paciente_data['nivel_educativo'],
                eps=paciente_data['eps'],
                afp=paciente_data['afp'],
                arl=paciente_data['arl'],
                funciones_cargo=f"Funciones específicas del cargo de {paciente_data['cargo']}",
                motivo_consulta=paciente_data['motivo_consulta'],
                enfermedad_actual=paciente_data['enfermedad_actual'],
                
                # Signos vitales
                tension_sistolica=paciente_data['tension_sistolica'],
                tension_diastolica=paciente_data['tension_diastolica'],
                frecuencia_cardiaca=paciente_data['frecuencia_cardiaca'],
                frecuencia_respiratoria=paciente_data['frecuencia_respiratoria'],
                pulsioximetria=paciente_data['pulsioximetria'],
                temperatura=paciente_data['temperatura'],
                lateralidad_dominante='DIESTRO',
                
                # Antropometría
                peso_kg=paciente_data['peso_kg'],
                talla_cm=paciente_data['talla_cm'],
                imc=round(imc, 2),
                perimetro_abdominal=paciente_data['perimetro_abdominal'],
                
                # Revisión por sistemas (normal por defecto)
                revision_sistemas={
                    'epilepsia_convulsiones': False,
                    'deformidades_amputaciones': False,
                    'cardiovascular': 'ASINTOMÁTICO',
                    'dermatologico': 'ASINTOMÁTICO',
                    'digestivo': 'ASINTOMÁTICO',
                    'genitourinario': 'ASINTOMÁTICO',
                    'neurologico': 'ASINTOMÁTICO',
                    'ocular': 'ASINTOMÁTICO',
                    'otorrinolaringologico': 'ASINTOMÁTICO',
                    'osteomuscular': 'ASINTOMÁTICO' if 'lumbar' not in paciente_data['motivo_consulta'].lower() else 'Dolor lumbar ocasional',
                    'respiratorio': 'ASINTOMÁTICO',
                    'otros_sistemas': '',
                    'observaciones': 'Revisión por sistemas sin hallazgos patológicos significativos'
                },
                
                # Examen físico (normal por defecto)
                examen_fisico={
                    'tegumentario': {'atrofia': 'NORMAL', 'otro': ''},
                    'cabeza': {'cuero_cabelludo': 'NORMAL', 'otro': ''},
                    'ojos': {
                        'escleras_color': 'ANICTERICAS',
                        'estrabismo': False,
                        'hiperemia_conjuntival': False,
                        'pupilas_normorreactivas': True,
                        'otro': ''
                    },
                    'oidos': {
                        'pabellon': 'NORMAL',
                        'audicion': 'NORMAL',
                        'otoscopia': 'NORMAL',
                        'otro': ''
                    },
                    'cardio_pulmonar': {
                        'ruidos_cardiacos': 'RÍTMICOS, BIEN TIMBRADOS, SIN SOPLOS',
                        'auscultacion_pulmonar': 'RUIDOS RESPIRATORIOS NORMALES SIN AGREGADOS',
                        'otro': ''
                    },
                    'abdomen': {
                        'inspeccion': 'NORMAL',
                        'palpacion': 'BLANDO, NO DOLOROSO, NO MASAS, NO MEGALIAS',
                        'auscultacion': 'RUIDOS INTESTINALES PRESENTES NORMALES',
                        'otro': ''
                    },
                    'neurologico': {
                        'fuerza_muscular': 'NORMAL',
                        'sensibilidad': 'CONSERVADA NORMAL',
                        'otro': ''
                    },
                    'extremidades': {
                        'inspeccion': 'SIMÉTRICAS, EUTRÓFICAS',
                        'deformidad': False,
                        'edemas': False,
                        'otro': ''
                    }
                }
            )
            
            # Crear antecedentes familiares
            for tipo_ant, observacion in paciente_data['antecedentes_familiares'].items():
                AntecedenteFamiliarGeneral.objects.create(
                    historia_clinica=historia,
                    tipo_antecedente=tipo_ant,
                    observacion=observacion
                )
            
            # Crear antecedentes personales
            antecedentes_default = [
                'HTA', 'DIABETES', 'ENF_RENAL', 'ENF_ARTICULAR', 'TBC', 'VENEREAS',
                'SIND_CONVULSIVO', 'INMUNOLOGICOS', 'HOSPITALIZACIONES', 
                'TOXICOS_ALERGICOS', 'TRAUMATICO', 'QUIRURGICOS', 'OTRO'
            ]
            
            for tipo_ant in antecedentes_default:
                observacion = paciente_data['antecedentes_personales'].get(tipo_ant, 'NO REFIERE')
                AntecedentePersonalGeneral.objects.create(
                    historia_clinica=historia,
                    tipo_antecedente=tipo_ant,
                    observacion=observacion
                )
            
            # Crear diagnósticos
            for cie10, nombre, tipo in paciente_data['diagnosticos']:
                DiagnosticoGeneral.objects.create(
                    historia_clinica=historia,
                    tipo_diagnostico=tipo,
                    codigo_cie10=cie10,
                    nombre_diagnostico=nombre,
                    tipo_impresion='CONFIRMADO',
                    profesional=random.choice(prestadores)
                )
            
            # Crear órdenes médicas según el caso
            if 'hipertensión' in paciente_data['enfermedad_actual'].lower() or paciente_data['tension_sistolica'] > 130:
                # Orden de medicamento para hipertensión
                OrdenMedicamento.objects.create(
                    historia_clinica=historia,
                    numero_orden=1,
                    nombre_medicamento='Losartán',
                    cantidad='30 tabletas',
                    posologia='1 tableta de 50mg cada 24 horas',
                    frecuencia='Cada 24 horas',
                    dias=30
                )
                
                # Orden de servicio para control
                OrdenServicioGeneral.objects.create(
                    historia_clinica=historia,
                    numero_orden=1,
                    nombre_servicio='Control de tensión arterial',
                    cantidad=1,
                    observaciones='Control en 1 mes para evaluar respuesta al tratamiento'
                )
            
            if 'diabetes' in paciente_data['enfermedad_actual'].lower():
                # Orden de medicamento para diabetes
                OrdenMedicamento.objects.create(
                    historia_clinica=historia,
                    numero_orden=1,
                    nombre_medicamento='Metformina',
                    cantidad='60 tabletas',
                    posologia='1 tableta de 850mg cada 12 horas',
                    frecuencia='Cada 12 horas',
                    dias=30
                )
                
                # Orden de servicio para laboratorio
                OrdenServicioGeneral.objects.create(
                    historia_clinica=historia,
                    numero_orden=1,
                    nombre_servicio='Hemoglobina glicosilada',
                    cantidad=1,
                    observaciones='Control trimestral de diabetes'
                )
                
                # Remisión a especialista
                OrdenRemision.objects.create(
                    historia_clinica=historia,
                    numero_orden=1,
                    nombre_especialidad='Endocrinología',
                    motivo_remision='Control y seguimiento de diabetes mellitus tipo 2'
                )
            
            if paciente_data['tipo_evaluacion'] == 'PREOCUPACIONAL':
                # Crear evolución de ingreso
                EvolucionGeneral.objects.create(
                    historia_clinica=historia,
                    profesional_asistencial=random.choice(prestadores),
                    evolucion=f"Paciente evaluado para ingreso laboral como {paciente_data['cargo']}. "
                              f"Examen físico y paraclínicos dentro de límites normales. "
                              f"APTO para el cargo solicitado."
                )
            else:
                # Crear evolución general
                EvolucionGeneral.objects.create(
                    historia_clinica=historia,
                    profesional_asistencial=random.choice(prestadores),
                    evolucion=f"Paciente evaluado en consulta de {paciente_data['tipo_evaluacion']}. "
                              f"Se continúa manejo actual y se solicitan controles según protocolo. "
                              f"Paciente orientado sobre su condición y tratamiento."
                )
            
            historias_creadas += 1
            print(f"✅ Historia Clínica General creada: {ficha.numero_ficha} - {ficha.nombre_trabajador}")
            print(f"   📋 Tipo: {historia.tipo_evaluacion_medica}, IMC: {historia.imc}")
            print(f"   🩺 TA: {historia.tension_sistolica}/{historia.tension_diastolica} mmHg")
            print(f"   📊 Diagnósticos: {len(paciente_data['diagnosticos'])}")
    
    print(f"\n🎉 Total de historias clínicas generales creadas: {historias_creadas}")
    
    # Mostrar estadísticas
    total_historias = HistoriaClinicaGeneral.objects.count()
    
    print(f"\n📊 Estadísticas de historias clínicas generales:")
    print(f"   - Total historias: {total_historias}")
    
    # Estadísticas por tipo de evaluación
    from django.db.models import Count
    
    tipos_stats = HistoriaClinicaGeneral.objects.values('tipo_evaluacion_medica').annotate(
        total=Count('id')
    ).order_by('-total')
    
    print(f"\n📋 Por tipo de evaluación:")
    for tipo in tipos_stats:
        print(f"   - {tipo['tipo_evaluacion_medica']}: {tipo['total']} historias")
    
    # Estadísticas por clasificación de TA
    ta_stats = HistoriaClinicaGeneral.objects.values('clasificacion_ta').annotate(
        total=Count('id')
    ).order_by('-total')
    
    print(f"\n🩺 Por clasificación de tensión arterial:")
    for ta in ta_stats:
        if ta['clasificacion_ta']:
            print(f"   - {ta['clasificacion_ta']}: {ta['total']} casos")
    
    # Estadísticas por estado civil
    civil_stats = HistoriaClinicaGeneral.objects.values('estado_civil').annotate(
        total=Count('id')
    ).order_by('-total')
    
    print(f"\n👥 Por estado civil:")
    for civil in civil_stats:
        if civil['estado_civil']:
            print(f"   - {civil['estado_civil']}: {civil['total']} pacientes")
    
    # Estadísticas por empresa
    print(f"\n🏢 Por empresa:")
    empresas_stats = FichaClinica.objects.filter(
        tipo_ficha='HISTORIA_CLINICA_GENERAL',
        empresa__isnull=False
    ).values('empresa__razon_social').annotate(
        total=Count('id')
    ).order_by('-total')
    
    for empresa in empresas_stats:
        print(f"   - {empresa['empresa__razon_social']}: {empresa['total']} historias")
    
    # Conteo de diagnósticos principales
    diagnosticos_stats = DiagnosticoGeneral.objects.filter(
        tipo_diagnostico='PRINCIPAL'
    ).values('codigo_cie10', 'nombre_diagnostico').annotate(
        total=Count('id')
    ).order_by('-total')
    
    print(f"\n🔍 Diagnósticos principales más frecuentes:")
    for diag in diagnosticos_stats:
        print(f"   - {diag['codigo_cie10']} {diag['nombre_diagnostico']}: {diag['total']} casos")
    
    # Conteo de órdenes médicas
    ordenes_medicamentos = OrdenMedicamento.objects.count()
    ordenes_servicios = OrdenServicioGeneral.objects.count()
    ordenes_remisiones = OrdenRemision.objects.count()
    
    print(f"\n💊 Órdenes médicas generadas:")
    print(f"   - Medicamentos: {ordenes_medicamentos}")
    print(f"   - Servicios: {ordenes_servicios}")
    print(f"   - Remisiones: {ordenes_remisiones}")


if __name__ == '__main__':
    print("📋 Creando historias clínicas generales de prueba...")
    crear_historias_clinicas_generales()
    print("\n✅ Proceso completado!")
