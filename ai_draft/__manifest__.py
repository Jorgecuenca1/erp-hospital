# -*- coding: utf-8 -*-
{
    'name': 'AI Draft',
    'version': '1.0.0',
    'category': 'Productivity/AI',
    'summary': 'AI-powered document drafting and writing assistance',
    'description': """
AI Draft Module
===============

This module provides AI-powered writing assistance that can:
* Generate medical reports automatically
* Create email drafts
* Write patient summaries
* Generate discharge summaries
* Create prescription notes
* Draft referral letters

Perfect for medical documentation and administrative tasks.
    """,
    'author': 'HMS ERP Team',
    'website': 'https://hms-erp.com',
    'depends': ['base', 'mail', 'medical_records'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/ai_draft_wizard.xml',
        'views/ai_draft_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
} 