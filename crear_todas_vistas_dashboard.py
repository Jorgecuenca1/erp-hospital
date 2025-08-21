#!/usr/bin/env python3
"""
Script para crear automáticamente todas las vistas de dashboard que faltan
"""

import os

# Definir las vistas que necesitamos crear
VISTAS_NECESARIAS = {
    'ecommerce': {
        'vista': 'EcommerceDashboardView',
        'modelo': 'Producto',
        'campo': 'productos_total'
    },
    'blog': {
        'vista': 'BlogDashboardView', 
        'modelo': 'Articulo',
        'campo': 'articulos_total'
    },
    'livechat': {
        'vista': 'LiveChatDashboardView',
        'modelo': 'Conversacion',
        'campo': 'conversaciones_total'
    },
    'subscriptions': {
        'vista': 'SubscriptionsDashboardView',
        'modelo': 'Suscripcion',
        'campo': 'suscripciones_total'
    }
}

# Template base para vistas
VISTA_TEMPLATE = '''
class {vista_nombre}(LoginRequiredMixin, TemplateView):
    """Dashboard principal de {modulo}"""
    template_name = '{modulo}/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = '{nombre_modulo}'
        context['{campo}'] = 0  # Placeholder
        return context
'''

def crear_vista_en_modulo(modulo, info):
    """Crear vista dashboard en un módulo específico"""
    archivo_views = f'/home/jorge/erp-hospital/{modulo}/views.py'
    
    if not os.path.exists(archivo_views):
        print(f"❌ Archivo {archivo_views} no existe")
        return False
    
    # Leer archivo actual
    with open(archivo_views, 'r') as f:
        contenido = f.read()
    
    # Verificar si ya tiene la vista
    if info['vista'] in contenido:
        print(f"✅ {modulo}: Vista {info['vista']} ya existe")
        return True
    
    # Verificar si tiene TemplateView y LoginRequiredMixin en imports
    if 'TemplateView' not in contenido:
        # Agregar imports necesarios
        lineas = contenido.split('\n')
        for i, linea in enumerate(lineas):
            if 'from django.views.generic import' in linea:
                if 'TemplateView' not in linea:
                    lineas[i] = linea.replace(')', ', TemplateView)')
                break
        
        # Agregar LoginRequiredMixin import si no está
        for i, linea in enumerate(lineas):
            if 'from django.contrib.auth.mixins import' not in contenido:
                if 'from django.urls import' in linea:
                    lineas.insert(i+1, 'from django.contrib.auth.mixins import LoginRequiredMixin')
                    break
        
        contenido = '\n'.join(lineas)
    
    # Crear la vista
    vista_codigo = VISTA_TEMPLATE.format(
        vista_nombre=info['vista'],
        modulo=modulo,
        nombre_modulo=modulo.title(),
        campo=info['campo']
    )
    
    # Insertar después de los imports
    lineas = contenido.split('\n')
    insert_pos = 0
    for i, linea in enumerate(lineas):
        if '# Create your views here.' in linea or 'class ' in linea:
            insert_pos = i
            break
    
    lineas.insert(insert_pos, vista_codigo)
    contenido_nuevo = '\n'.join(lineas)
    
    # Escribir archivo actualizado
    with open(archivo_views, 'w') as f:
        f.write(contenido_nuevo)
    
    print(f"✅ {modulo}: Vista {info['vista']} creada")
    return True

def main():
    print("🏗️ CREANDO VISTAS DASHBOARD AUTOMÁTICAMENTE")
    print("=" * 60)
    
    for modulo, info in VISTAS_NECESARIAS.items():
        crear_vista_en_modulo(modulo, info)
    
    print(f"\n✅ Proceso completado para {len(VISTAS_NECESARIAS)} módulos")
    print("🚀 Intenta iniciar el servidor ahora")

if __name__ == '__main__':
    main()
