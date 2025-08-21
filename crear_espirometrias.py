#!/usr/bin/env python3
"""
Script para crear espirometrías de prueba
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
    FichaClinica, Espirometria, Empresa, Prestador, Municipio, RecomendacionEspirometria
)


def crear_espirometrias():
    """Crear espirometrías de prueba"""
    
    # Obtener datos necesarios
    empresas = list(Empresa.objects.filter(activo=True))
    prestadores = list(Prestador.objects.filter(activo=True))
    municipios = list(Municipio.objects.filter(activo=True))
    admin_user = User.objects.filter(is_superuser=True).first()
    
    if not empresas or not prestadores:
        print("❌ Faltan datos básicos. Ejecute primero crear_datos_admision.py")
        return
    
    # Datos de trabajadores para espirometría
    trabajadores_data = [
        {
            'numero_identificacion': '22.234.567.890',
            'nombre_trabajador': 'CARLOS EDUARDO MORALES SANCHEZ',
            'genero': 'M',
            'edad': 34,
            'peso_kg': 72.5,
            'talla_cm': 175.0,
            'cargo': 'Soldador Industrial',
            'funciones_cargo': 'Soldadura de estructuras metálicas con exposición a humos',
            'fuma_tabaco': True,
            'cigarrillos_dia': 15,
            'anos_fumando': 10
        },
        {
            'numero_identificacion': '41.345.678.901',
            'nombre_trabajador': 'SANDRA PATRICIA LOPEZ TORRES',
            'genero': 'F',
            'edad': 28,
            'peso_kg': 58.0,
            'talla_cm': 162.0,
            'cargo': 'Operaria Textil',
            'funciones_cargo': 'Operación de máquinas textiles con exposición a fibras',
            'fuma_tabaco': False,
            'cigarrillos_dia': 0,
            'anos_fumando': 0
        },
        {
            'numero_identificacion': '19.456.789.012',
            'nombre_trabajador': 'MIGUEL ANGEL RIVERA CASTRO',
            'genero': 'M',
            'edad': 45,
            'peso_kg': 85.0,
            'talla_cm': 180.0,
            'cargo': 'Minero de Carbón',
            'funciones_cargo': 'Extracción de carbón subterráneo con exposición a polvo mineral',
            'fuma_tabaco': False,
            'cigarrillos_dia': 0,
            'anos_fumando': 0,
            'es_exfumador': True,
            'anos_sin_fumar': 5
        },
        {
            'numero_identificacion': '36.567.890.123',
            'nombre_trabajador': 'ELENA MARIA GUTIERREZ PEÑA',
            'genero': 'F',
            'edad': 31,
            'peso_kg': 65.5,
            'talla_cm': 168.0,
            'cargo': 'Química de Laboratorio',
            'funciones_cargo': 'Análisis químico con manejo de solventes y vapores',
            'fuma_tabaco': False,
            'cigarrillos_dia': 0,
            'anos_fumando': 0
        },
        {
            'numero_identificacion': '17.678.901.234',
            'nombre_trabajador': 'JOSE ANTONIO HERRERA VALENCIA',
            'genero': 'M',
            'edad': 52,
            'peso_kg': 78.0,
            'talla_cm': 172.0,
            'cargo': 'Pintor Industrial',
            'funciones_cargo': 'Aplicación de pinturas y recubrimientos industriales',
            'fuma_tabaco': True,
            'cigarrillos_dia': 20,
            'anos_fumando': 25,
            'asma': True
        }
    ]
    
    espirometrias_creadas = 0
    
    for trabajador_data in trabajadores_data:
        # Verificar si ya existe
        if not FichaClinica.objects.filter(
            numero_identificacion=trabajador_data['numero_identificacion'],
            tipo_ficha='ESPIROMETRIA'
        ).exists():
            
            # Crear ficha clínica
            ficha = FichaClinica.objects.create(
                tipo_ficha='ESPIROMETRIA',
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
            
            # Generar valores espirométricos realistas basados en características del trabajador
            def generar_valores_espirometricos(edad, genero, talla_cm, peso_kg, fuma, anos_fumando=0, exposicion_ocupacional=False):
                """Generar valores espirométricos basados en ecuaciones de predicción"""
                
                # Ecuaciones de predicción simplificadas (basadas en Knudson)
                talla_m = talla_cm / 100
                
                if genero == 'M':
                    # Hombres
                    cvf_predicho = (5.76 * talla_m) - (0.026 * edad) - 4.34
                    vef1_predicho = (4.30 * talla_m) - (0.029 * edad) - 2.49
                else:
                    # Mujeres
                    cvf_predicho = (4.43 * talla_m) - (0.026 * edad) - 2.89
                    vef1_predicho = (3.18 * talla_m) - (0.025 * edad) - 1.30
                
                # Ajustar por factores de riesgo
                factor_reduccion = 1.0
                
                # Reducción por tabaquismo
                if fuma:
                    factor_reduccion -= (anos_fumando * 0.01)  # 1% por año
                
                # Reducción por exposición ocupacional
                if exposicion_ocupacional:
                    factor_reduccion -= 0.05  # 5% de reducción
                
                # Aplicar factor de reducción
                cvf_real = cvf_predicho * factor_reduccion
                vef1_real = vef1_predicho * factor_reduccion
                
                # Calcular VEF1/CVF ratio
                vef1_cvf_ratio = (vef1_real / cvf_real) * 100
                
                # FEF 25-75 (aproximadamente 75% del VEF1)
                fef_25_75 = vef1_real * 0.75
                
                # Agregar variabilidad natural
                cvf_real += random.uniform(-0.2, 0.2)
                vef1_real += random.uniform(-0.15, 0.15)
                vef1_cvf_ratio += random.uniform(-3, 3)
                fef_25_75 += random.uniform(-0.3, 0.3)
                
                # Asegurar valores positivos
                cvf_real = max(1.0, cvf_real)
                vef1_real = max(0.8, vef1_real)
                vef1_cvf_ratio = max(40, min(90, vef1_cvf_ratio))
                fef_25_75 = max(0.5, fef_25_75)
                
                return {
                    'cvf_predicho': round(cvf_predicho, 2),
                    'vef1_predicho': round(vef1_predicho, 2),
                    'cvf_real': round(cvf_real, 2),
                    'vef1_real': round(vef1_real, 2),
                    'vef1_cvf_ratio': round(vef1_cvf_ratio, 1),
                    'fef_25_75': round(fef_25_75, 2)
                }
            
            # Determinar exposición ocupacional
            exposicion_ocupacional = trabajador_data['cargo'] in [
                'Soldador Industrial', 'Minero de Carbón', 'Pintor Industrial'
            ]
            
            valores = generar_valores_espirometricos(
                edad=trabajador_data['edad'],
                genero=trabajador_data['genero'],
                talla_cm=trabajador_data['talla_cm'],
                peso_kg=trabajador_data['peso_kg'],
                fuma=trabajador_data['fuma_tabaco'],
                anos_fumando=trabajador_data.get('anos_fumando', 0),
                exposicion_ocupacional=exposicion_ocupacional
            )
            
            # Crear espirometría
            espirometria = Espirometria.objects.create(
                ficha_clinica=ficha,
                producto='Espirometría Ocupacional',
                peso_kg=trabajador_data['peso_kg'],
                talla_cm=trabajador_data['talla_cm'],
                imc=round(imc, 2),
                fecha_ingreso_empresa=date.today() - timedelta(days=random.randint(365, 3650)),
                antiguedad_cargo_anos=random.randint(1, 15),
                antiguedad_cargo_meses=random.randint(0, 11),
                funciones_cargo=trabajador_data['funciones_cargo'],
                eps=random.choice(['EPS Sura', 'Salud Total', 'Nueva EPS', 'Compensar']),
                fecha_ultimo_examen=date.today() - timedelta(days=random.randint(30, 730)),
                resultado_anterior=random.choice(['NO APLICA', 'NORMAL', 'ANORMAL']),
                
                # Características de exposición
                caracteristica_exposicion=f"Exposición a factores de riesgo respiratorio en {trabajador_data['cargo']}",
                riesgos_ocupacionales=f"Riesgos asociados a {trabajador_data['cargo'].lower()}",
                
                # EPP según el cargo
                uso_mascarilla=exposicion_ocupacional,
                uso_respirador=trabajador_data['cargo'] in ['Soldador Industrial', 'Pintor Industrial'],
                uso_otros_epp=True,
                otros_epp_cual='Guantes, gafas de seguridad',
                
                # Factores de riesgo según el cargo
                factor_polvo=trabajador_data['cargo'] == 'Minero de Carbón',
                factor_humos=trabajador_data['cargo'] == 'Soldador Industrial',
                factor_gases=trabajador_data['cargo'] == 'Química de Laboratorio',
                factor_vapores=trabajador_data['cargo'] in ['Pintor Industrial', 'Química de Laboratorio'],
                factor_neblinas=trabajador_data['cargo'] == 'Operaria Textil',
                tiempo_exposicion_anos=random.randint(1, 15),
                tiempo_exposicion_meses=random.randint(0, 11),
                
                # Hábitos personales
                fuma_tabaco=trabajador_data['fuma_tabaco'],
                fuma_cantidad=f"{trabajador_data['cigarrillos_dia']} cigarrillos/día" if trabajador_data['fuma_tabaco'] else '',
                fuma_tiempo=f"{trabajador_data['anos_fumando']} años" if trabajador_data['fuma_tabaco'] else '',
                es_exfumador=trabajador_data.get('es_exfumador', False),
                exfumador_cantidad='15 cigarrillos/día' if trabajador_data.get('es_exfumador') else '',
                ano_dejo_fumar=2019 if trabajador_data.get('es_exfumador') else None,
                practica_deporte=random.choice([True, False]),
                deporte_horas_semana='3 horas/semana' if random.choice([True, False]) else '',
                deporte_cual=random.choice(['Fútbol', 'Natación', 'Ciclismo', 'Trotar']) if random.choice([True, False]) else '',
                cocina_lena=random.choice([True, False]),
                lena_tiempo_exposicion='10 años' if random.choice([True, False]) else '',
                
                # Sintomatología
                dificultad_respirar=trabajador_data['fuma_tabaco'] or trabajador_data.get('asma', False),
                dificultad_esfuerzo_fisico=trabajador_data['fuma_tabaco'],
                tos_frecuente=trabajador_data['fuma_tabaco'] or exposicion_ocupacional,
                tos_con_esputo=trabajador_data['fuma_tabaco'],
                enfermedad_cardiaca=False,
                dolor_respirar=False,
                alergia_respiratoria=trabajador_data['cargo'] == 'Operaria Textil',
                alergia_respiratoria_que='Fibras textiles' if trabajador_data['cargo'] == 'Operaria Textil' else '',
                asma=trabajador_data.get('asma', False),
                asma_edad_ultima_crisis='50 años' if trabajador_data.get('asma') else '',
                otra_enfermedad_respiratoria=False,
                
                # Valores espirométricos
                cvf_pre=round(valores['cvf_real'] * 0.95, 2),  # Pre-broncodilatador ligeramente menor
                cvf_post=valores['cvf_real'],
                cvf_teor=valores['cvf_predicho'],
                
                vef1_pre=round(valores['vef1_real'] * 0.93, 2),  # Pre-broncodilatador ligeramente menor
                vef1_post=valores['vef1_real'],
                vef1_teor=valores['vef1_predicho'],
                
                vef1_cvf_pre=round(valores['vef1_cvf_ratio'] * 0.95, 1),
                vef1_cvf_post=valores['vef1_cvf_ratio'],
                vef1_cvf_teor=80.0,  # Valor normal de referencia
                
                fef_25_75_pre=round(valores['fef_25_75'] * 0.90, 2),
                fef_25_75_post=valores['fef_25_75'],
                fef_25_75_teor=round(valores['fef_25_75'] * 1.2, 2),  # Valor teórico más alto
                
                # Interpretación
                marca_espirometro=random.choice([
                    'Vitalograph Alpha', 'CareFusion MasterScreen', 'nSpire KoKo',
                    'MGC Diagnostics', 'Schiller SP-1'
                ]),
                fecha_ultima_calibracion=date.today() - timedelta(days=random.randint(1, 90)),
                escala_interpretacion='KNUDSON',
                
                observaciones='Espirometría realizada según estándares ATS/ERS. Colaboración adecuada del paciente.'
            )
            
            # La interpretación y severidad se calculan automáticamente en el método save()
            
            # Crear recomendaciones según el resultado
            recomendaciones = []
            
            vef1_percent = (valores['vef1_real'] / valores['vef1_predicho']) * 100
            
            if vef1_percent < 80:
                recomendaciones.append(('Control médico especializado', 'CONTROL'))
                recomendaciones.append(('Valoración por neumología', 'REMISION'))
            
            if trabajador_data['fuma_tabaco']:
                recomendaciones.append(('Cesación del hábito tabáquico', 'PREVENCION'))
                recomendaciones.append(('Programa antitabaquismo', 'TRATAMIENTO'))
            
            if exposicion_ocupacional:
                recomendaciones.append(('Uso permanente de EPP respiratorio', 'PREVENCION'))
                recomendaciones.append(('Control espirométrico anual', 'CONTROL'))
            
            if valores['vef1_cvf_ratio'] < 70:
                recomendaciones.append(('Espirometría post-broncodilatador', 'EXAMEN'))
                recomendaciones.append(('Evaluación función pulmonar completa', 'EXAMEN'))
            
            # Siempre agregar recomendación de control
            recomendaciones.append(('Control espirométrico según periodicidad ocupacional', 'CONTROL'))
            
            for recomendacion_texto, tipo in recomendaciones:
                RecomendacionEspirometria.objects.create(
                    espirometria=espirometria,
                    recomendacion=recomendacion_texto,
                    tipo=tipo
                )
            
            espirometrias_creadas += 1
            print(f"✅ Espirometría creada: {ficha.numero_ficha} - {ficha.nombre_trabajador}")
            print(f"   📊 IMC: {espirometria.imc}, Patrón: {espirometria.patron_funcional}, Severidad: {espirometria.severidad}")
            print(f"   🫁 VEF1: {espirometria.vef1_post}L ({vef1_percent:.1f}%), CVF: {espirometria.cvf_post}L")
    
    print(f"\n🎉 Total de espirometrías creadas: {espirometrias_creadas}")
    
    # Mostrar estadísticas
    total_espirometrias = Espirometria.objects.count()
    
    print(f"\n📊 Estadísticas de espirometrías:")
    print(f"   - Total espirometrías: {total_espirometrias}")
    
    # Estadísticas por patrón funcional
    from django.db.models import Count
    patron_stats = Espirometria.objects.values('patron_funcional').annotate(
        total=Count('id')
    ).order_by('patron_funcional')
    
    print(f"\n🫁 Patrón Funcional:")
    for stat in patron_stats:
        patron_display = dict(Espirometria.PATRON_FUNCIONAL_CHOICES).get(stat['patron_funcional'], stat['patron_funcional'])
        print(f"   - {patron_display}: {stat['total']} casos")
    
    # Estadísticas por severidad
    severidad_stats = Espirometria.objects.values('severidad').annotate(
        total=Count('id')
    ).order_by('severidad')
    
    print(f"\n⚠️ Severidad:")
    for stat in severidad_stats:
        severidad_display = dict(Espirometria.SEVERIDAD_CHOICES).get(stat['severidad'], stat['severidad'])
        print(f"   - {severidad_display}: {stat['total']} casos")
    
    # Estadísticas por empresa
    print(f"\n🏢 Por empresa:")
    empresas_stats = FichaClinica.objects.filter(
        tipo_ficha='ESPIROMETRIA',
        empresa__isnull=False
    ).values('empresa__razon_social').annotate(
        total=Count('id')
    ).order_by('-total')
    
    for empresa in empresas_stats:
        print(f"   - {empresa['empresa__razon_social']}: {empresa['total']} espirometrías")
    
    # Estadísticas por hábito tabáquico
    fumadores = Espirometria.objects.filter(fuma_tabaco=True).count()
    exfumadores = Espirometria.objects.filter(es_exfumador=True).count()
    no_fumadores = Espirometria.objects.filter(fuma_tabaco=False, es_exfumador=False).count()
    
    print(f"\n🚬 Hábito tabáquico:")
    print(f"   - Fumadores activos: {fumadores}")
    print(f"   - Ex-fumadores: {exfumadores}")
    print(f"   - No fumadores: {no_fumadores}")


if __name__ == '__main__':
    print("🫁 Creando espirometrías de prueba...")
    crear_espirometrias()
    print("\n✅ Proceso completado!")
