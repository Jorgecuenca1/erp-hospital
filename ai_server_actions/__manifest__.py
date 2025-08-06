# -*- coding: utf-8 -*-
{
    'name': 'AI Server Actions',
    'version': '1.0.0',
    'category': 'Productivity/AI',
    'summary': 'AI-powered server actions and automation',
    'description': """
AI Server Actions Module
========================

This module provides AI-powered server actions that can:
* Automatically classify medical records
* Route patient cases to appropriate specialists
* Generate automated responses
* Predict patient outcomes
* Automate administrative tasks
* Process medical documents

Perfect for workflow automation and intelligent decision making.
    """,
    'author': 'HMS ERP Team',
    'website': 'https://hms-erp.com',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/ai_server_action_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
} 