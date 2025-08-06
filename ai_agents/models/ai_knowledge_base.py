# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import re
import logging

_logger = logging.getLogger(__name__)

class AIKnowledgeBase(models.Model):
    _name = 'ai.knowledge.base'
    _description = 'AI Knowledge Base'
    _order = 'name'
    
    name = fields.Char(string='Knowledge Base Name', required=True)
    description = fields.Text(string='Description')
    active = fields.Boolean(default=True)
    
    # Content
    content = fields.Html(string='Content')
    documents = fields.Text(string='Documents', help='Text documents for training')
    
    # Categorization
    category = fields.Selection([
        ('medical', 'Medical Knowledge'),
        ('policies', 'Policies & Procedures'),
        ('faq', 'Frequently Asked Questions'),
        ('products', 'Product Information'),
        ('services', 'Service Information'),
        ('general', 'General Knowledge')
    ], string='Category', default='general')
    
    tags = fields.Char(string='Tags', help='Comma-separated tags')
    
    # Usage
    agent_ids = fields.Many2many('ai.agent', string='Used by Agents')
    usage_count = fields.Integer(string='Usage Count', default=0)
    
    # Metadata
    source = fields.Char(string='Source')
    last_updated = fields.Datetime(string='Last Updated', default=fields.Datetime.now)
    
    def search(self, query, limit=5):
        """Search knowledge base for relevant information"""
        if not query:
            return []
        
        # Simple text search - can be enhanced with vector search
        results = []
        
        # Search in content
        if self.content:
            content_text = re.sub(r'<[^>]+>', '', self.content)  # Remove HTML tags
            if self._matches_query(content_text, query):
                results.append({
                    'source': self.name,
                    'content': content_text[:500],  # First 500 chars
                    'score': self._calculate_score(content_text, query)
                })
        
        # Search in documents
        if self.documents:
            if self._matches_query(self.documents, query):
                results.append({
                    'source': self.name,
                    'content': self.documents[:500],  # First 500 chars
                    'score': self._calculate_score(self.documents, query)
                })
        
        # Update usage count
        self.usage_count += 1
        
        # Sort by score and return top results
        results.sort(key=lambda x: x['score'], reverse=True)
        return [result['content'] for result in results[:limit]]
    
    def _matches_query(self, text, query):
        """Check if text matches query"""
        query_words = query.lower().split()
        text_lower = text.lower()
        
        # Simple word matching
        matches = sum(1 for word in query_words if word in text_lower)
        return matches > 0
    
    def _calculate_score(self, text, query):
        """Calculate relevance score"""
        query_words = query.lower().split()
        text_lower = text.lower()
        
        score = 0
        for word in query_words:
            # Count occurrences of each query word
            score += text_lower.count(word)
        
        # Normalize by text length
        if len(text) > 0:
            score = score / len(text) * 1000  # Scale up for better comparison
        
        return score
    
    def update_content(self, new_content):
        """Update knowledge base content"""
        self.write({
            'content': new_content,
            'last_updated': fields.Datetime.now()
        })
    
    def add_document(self, document_text):
        """Add a new document to the knowledge base"""
        if self.documents:
            self.documents += f"\n\n{document_text}"
        else:
            self.documents = document_text
        
        self.last_updated = fields.Datetime.now()
    
    def get_tags_list(self):
        """Get tags as list"""
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',')]
        return []
    
    def set_tags_list(self, tags_list):
        """Set tags from list"""
        self.tags = ', '.join(tags_list) 