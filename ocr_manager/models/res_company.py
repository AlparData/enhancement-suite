# -*- coding: utf-8 -*-
from odoo import models, fields

class ResCompany(models.Model):
    _inherit = 'res.company'

    ocr_manager_enabled = fields.Boolean(
        string='Habilitar OCR Manager',
        default=False,
        help="Activa el motor de IA generativa propio."
    )
    
    ocr_provider = fields.Selection([
        ('google', 'Google Gemini'),
        ('openai', 'OpenAI'),
        ('azure', 'Azure'),
    ], string="Proveedor IA", default='google')
    
    ocr_api_key = fields.Char(string="API Key", copy=False)
    ocr_ai_model = fields.Char(
        string="Modelo IA", 
        default="gemini-1.5-flash-002", 
        help="Ej: gemini-1.5-flash-002, gemini-1.5-pro-002"
    )
    ocr_prompt_id = fields.Many2one(
        'ocr.prompt', 
        string="Prompt a Utilizar",
        domain="[('provider_type', '=', ocr_provider)]", # Filtra por el proveedor seleccionado (Google/OpenAI)
        help="Si se selecciona, se usará este prompt específico ignorando los códigos por defecto."
    )