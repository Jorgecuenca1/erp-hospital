# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime
import json

class AIConversation(models.Model):
    _name = 'ai.conversation'
    _description = 'AI Agent Conversation'
    _order = 'create_date desc'
    
    name = fields.Char(string='Conversation', compute='_compute_name', store=True)
    agent_id = fields.Many2one('ai.agent', string='AI Agent', required=True, ondelete='cascade')
    user_id = fields.Many2one('res.users', string='User', required=True)
    
    # Conversation Content
    user_message = fields.Text(string='User Message', required=True)
    agent_response = fields.Text(string='Agent Response')
    context = fields.Text(string='Context', help='Additional context as JSON')
    
    # Status
    status = fields.Selection([
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('error', 'Error')
    ], string='Status', default='pending')
    
    # Analytics
    response_time = fields.Float(string='Response Time (s)', help='Time taken to generate response')
    satisfaction_rating = fields.Selection([
        ('1', 'Very Poor'),
        ('2', 'Poor'),
        ('3', 'Average'),
        ('4', 'Good'),
        ('5', 'Excellent')
    ], string='Satisfaction Rating')
    
    feedback = fields.Text(string='User Feedback')
    
    # Metadata
    ip_address = fields.Char(string='IP Address')
    user_agent = fields.Char(string='User Agent')
    session_id = fields.Char(string='Session ID')
    
    @api.depends('user_message', 'create_date')
    def _compute_name(self):
        for conversation in self:
            if conversation.user_message:
                # Take first 50 characters of user message
                preview = conversation.user_message[:50]
                if len(conversation.user_message) > 50:
                    preview += '...'
                conversation.name = f"{preview} ({conversation.create_date.strftime('%Y-%m-%d %H:%M')})"
            else:
                conversation.name = f"Conversation {conversation.create_date.strftime('%Y-%m-%d %H:%M')}"
    
    def rate_conversation(self, rating, feedback=None):
        """Rate the conversation"""
        self.write({
            'satisfaction_rating': str(rating),
            'feedback': feedback or ''
        })
    
    def get_context_data(self):
        """Get parsed context data"""
        if self.context:
            try:
                return json.loads(self.context)
            except json.JSONDecodeError:
                return {}
        return {}
    
    def set_context_data(self, data):
        """Set context data"""
        self.context = json.dumps(data) 