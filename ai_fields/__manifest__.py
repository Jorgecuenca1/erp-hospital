# -*- coding: utf-8 -*-
{
    'name': 'AI Fields',
    'version': '1.0.0',
    'category': 'Productivity/AI',
    'summary': 'AI-powered intelligent form fields',
    'description': """
AI Fields Module
================

This module provides intelligent form fields that can:
* Auto-complete medical diagnoses
* Suggest treatment plans
* Fill patient information automatically
* Predict medical codes
* Validate data using AI
* Provide smart suggestions

Perfect for medical forms, patient records, and clinical documentation.
    """,
    'author': 'HMS ERP Team',
    'website': 'https://hms-erp.com',
    'depends': ['base', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'views/ai_field_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'ai_fields/static/src/js/ai_fields.js',
            'ai_fields/static/src/css/ai_fields.css',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
} 