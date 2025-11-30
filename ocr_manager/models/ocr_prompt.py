# -*- coding: utf-8 -*-
from odoo import models, fields

class OcrPrompt(models.Model):
    _name = 'ocr.prompt'
    _description = 'Plantillas de Prompt para OCR'
    _order = 'name'

    name = fields.Char(string="Nombre", required=True)
    code = fields.Char(string="Código Técnico", required=True, 
                      help="Identificador único (ej: invoice_google).")
    active = fields.Boolean(default=True)
    
    provider_type = fields.Selection([
        ('google', 'Google Gemini'),
        ('openai', 'OpenAI'),
        ('azure', 'Azure'),
        ('custom', 'Personalizado'),
    ], string="Proveedor IA", required=True)

    document_type = fields.Selection([
        ('invoice', 'Factura'),
        ('expense', 'Recibo/Gasto'),
        ('other', 'Otro'),
    ], string="Tipo de Documento", default='invoice', required=True)

    template = fields.Text(string="Plantilla del Prompt", required=True, 
                          default="Analiza la imagen y extrae los datos en JSON.")

    _sql_constraints = [
        ('code_uniq', 'unique (code)', 'El código del prompt debe ser único.')
    ]