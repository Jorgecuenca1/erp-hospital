# -*- coding: utf-8 -*-
{
    'name': 'AI Agents',
    'version': '1.0.0',
    'category': 'Productivity/AI',
    'summary': 'AI Conversational Agents for HMS ERP',
    'description': """
AI Agents Module
================

This module provides intelligent conversational agents that can:
* Assist with medical queries and procedures
* Help with administrative tasks
* Provide customer service support
* Offer technical assistance
* Support sales activities
* Learn from conversations and improve over time

Key Features:
* Multiple AI model providers (OpenAI, Anthropic, Local)
* Customizable agent personalities and knowledge bases
* Conversation history and analytics
* Permission-based access control
* Medical-specific AI agents
* Auto-learning capabilities
* Integration with HMS modules

The AI agents can be configured to work with different departments and use cases,
making them perfect for hospitals, clinics, and medical facilities.
    """,
    'author': 'HMS ERP Team',
    'website': 'https://hms-erp.com',
    'depends': ['base', 'hr', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/ai_agent_views.xml',
        'views/ai_conversation_views.xml',
        'views/ai_knowledge_base_views.xml',
        'views/menus.xml',
        'data/ai_agent_data.xml',
    ],
    'demo': [
        'demo/demo_data.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
    'images': ['static/description/banner.png'],
} 