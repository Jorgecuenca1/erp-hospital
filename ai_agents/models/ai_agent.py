# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import json
import logging

_logger = logging.getLogger(__name__)

class AIAgent(models.Model):
    _name = 'ai.agent'
    _description = 'AI Conversational Agent'
    _order = 'name'
    
    name = fields.Char(string='Agent Name', required=True)
    description = fields.Text(string='Description')
    active = fields.Boolean(default=True)
    
    # Agent Configuration
    agent_type = fields.Selection([
        ('medical', 'Medical Assistant'),
        ('administrative', 'Administrative Assistant'),
        ('customer_service', 'Customer Service'),
        ('technical', 'Technical Support'),
        ('sales', 'Sales Assistant'),
        ('general', 'General Purpose')
    ], string='Agent Type', required=True, default='general')
    
    # AI Model Configuration
    model_provider = fields.Selection([
        ('openai', 'OpenAI'),
        ('anthropic', 'Anthropic'),
        ('local', 'Local Model'),
        ('custom', 'Custom API')
    ], string='Model Provider', default='openai')
    
    model_name = fields.Char(string='Model Name', default='gpt-4')
    temperature = fields.Float(string='Temperature', default=0.7, help='Controls randomness of responses')
    max_tokens = fields.Integer(string='Max Tokens', default=1000)
    
    # Knowledge Base
    knowledge_base_ids = fields.Many2many('ai.knowledge.base', string='Knowledge Bases')
    system_prompt = fields.Text(string='System Prompt', help='Instructions for the AI agent')
    
    # Permissions
    department_ids = fields.Many2many('hr.department', string='Allowed Departments')
    user_ids = fields.Many2many('res.users', string='Allowed Users')
    
    # Analytics
    conversation_count = fields.Integer(string='Conversations', compute='_compute_conversation_count')
    avg_response_time = fields.Float(string='Avg Response Time (s)', compute='_compute_avg_response_time')
    satisfaction_score = fields.Float(string='Satisfaction Score', compute='_compute_satisfaction_score')
    
    # Configuration
    auto_learn = fields.Boolean(string='Auto Learn', default=True, help='Learn from conversations')
    context_window = fields.Integer(string='Context Window', default=10, help='Number of previous messages to consider')
    
    @api.depends('conversation_ids')
    def _compute_conversation_count(self):
        for agent in self:
            agent.conversation_count = len(agent.conversation_ids)
    
    @api.depends('conversation_ids.response_time')
    def _compute_avg_response_time(self):
        for agent in self:
            conversations = agent.conversation_ids.filtered('response_time')
            if conversations:
                agent.avg_response_time = sum(conversations.mapped('response_time')) / len(conversations)
            else:
                agent.avg_response_time = 0.0
    
    @api.depends('conversation_ids.satisfaction_rating')
    def _compute_satisfaction_score(self):
        for agent in self:
            conversations = agent.conversation_ids.filtered('satisfaction_rating')
            if conversations:
                agent.satisfaction_score = sum(conversations.mapped('satisfaction_rating')) / len(conversations)
            else:
                agent.satisfaction_score = 0.0
    
    conversation_ids = fields.One2many('ai.conversation', 'agent_id', string='Conversations')
    
    def chat(self, message, user_id=None, context=None):
        """Main chat method to interact with the AI agent"""
        if not user_id:
            user_id = self.env.user.id
        
        # Check permissions
        if not self._check_user_permission(user_id):
            raise ValidationError(_('You do not have permission to use this AI agent.'))
        
        # Create conversation record
        conversation = self.env['ai.conversation'].create({
            'agent_id': self.id,
            'user_id': user_id,
            'user_message': message,
            'context': json.dumps(context or {})
        })
        
        # Generate response
        response = self._generate_response(message, conversation, context)
        
        # Update conversation with response
        conversation.write({
            'agent_response': response,
            'status': 'completed'
        })
        
        return response
    
    def _check_user_permission(self, user_id):
        """Check if user has permission to use this agent"""
        user = self.env['res.users'].browse(user_id)
        
        # If no restrictions, allow everyone
        if not self.department_ids and not self.user_ids:
            return True
        
        # Check user-specific permissions
        if self.user_ids and user in self.user_ids:
            return True
        
        # Check department permissions
        if self.department_ids and user.employee_id.department_id in self.department_ids:
            return True
        
        return False
    
    def _generate_response(self, message, conversation, context):
        """Generate AI response based on agent configuration"""
        try:
            # Prepare prompt
            full_prompt = self._prepare_prompt(message, conversation, context)
            
            # Call AI API based on provider
            if self.model_provider == 'openai':
                response = self._call_openai_api(full_prompt)
            elif self.model_provider == 'anthropic':
                response = self._call_anthropic_api(full_prompt)
            elif self.model_provider == 'local':
                response = self._call_local_model(full_prompt)
            else:
                response = self._call_custom_api(full_prompt)
            
            return response
        except Exception as e:
            _logger.error(f"Error generating AI response: {e}")
            return _("I'm sorry, I encountered an error while processing your request. Please try again later.")
    
    def _prepare_prompt(self, message, conversation, context):
        """Prepare the full prompt for the AI model"""
        # System prompt
        prompt = self.system_prompt or f"You are a helpful {self.agent_type} assistant."
        
        # Add knowledge base context
        if self.knowledge_base_ids:
            kb_context = self._get_knowledge_base_context(message)
            if kb_context:
                prompt += f"\n\nRelevant information:\n{kb_context}"
        
        # Add conversation history
        if self.context_window > 0:
            history = self._get_conversation_history(conversation, self.context_window)
            if history:
                prompt += f"\n\nConversation history:\n{history}"
        
        # Add current message
        prompt += f"\n\nUser: {message}\nAssistant:"
        
        return prompt
    
    def _get_knowledge_base_context(self, message):
        """Get relevant context from knowledge bases"""
        context = []
        for kb in self.knowledge_base_ids:
            relevant_docs = kb.search(message, limit=3)
            context.extend(relevant_docs)
        return '\n'.join(context)
    
    def _get_conversation_history(self, current_conversation, limit):
        """Get recent conversation history"""
        # Get previous conversations from same user
        previous_conversations = self.env['ai.conversation'].search([
            ('agent_id', '=', self.id),
            ('user_id', '=', current_conversation.user_id.id),
            ('id', '!=', current_conversation.id),
            ('status', '=', 'completed')
        ], order='create_date desc', limit=limit)
        
        history = []
        for conv in reversed(previous_conversations):
            history.append(f"User: {conv.user_message}")
            history.append(f"Assistant: {conv.agent_response}")
        
        return '\n'.join(history)
    
    def _call_openai_api(self, prompt):
        """Call OpenAI API"""
        # Placeholder for OpenAI API integration
        return "OpenAI API response would go here"
    
    def _call_anthropic_api(self, prompt):
        """Call Anthropic API"""
        # Placeholder for Anthropic API integration
        return "Anthropic API response would go here"
    
    def _call_local_model(self, prompt):
        """Call local AI model"""
        # Placeholder for local model integration
        return "Local model response would go here"
    
    def _call_custom_api(self, prompt):
        """Call custom API"""
        # Placeholder for custom API integration
        return "Custom API response would go here"
    
    def train(self):
        """Train the agent with conversation data"""
        # Placeholder for training logic
        pass
    
    def reset_analytics(self):
        """Reset agent analytics"""
        self.conversation_ids.unlink() 