# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import base64
import logging

_logger = logging.getLogger(__name__)

class OcrBulkDigitizeWizard(models.TransientModel):
    _name = 'ocr.bulk.digitize.wizard'
    _description = 'Asistente de Digitalización Masiva IA'

    name = fields.Char(string="Referencia", default=lambda self: _('Lote %s') % fields.Datetime.now())
    
    line_ids = fields.One2many(
        'ocr.bulk.digitize.line', 
        'wizard_id', 
        string="Documentos"
    )
    
    state = fields.Selection([
        ('draft', 'Carga'),
        ('processing', 'Procesando'),
        ('done', 'Completado')
    ], default='draft', string="Estado")

    def action_process_files(self):
        """Procesa todos los archivos cargados"""
        self.ensure_one()
        if not self.line_ids:
            raise UserError(_("Por favor, cargue al menos un archivo."))

        self.state = 'processing'
        
        # Iteramos sobre cada línea
        for line in self.line_ids:
            if line.state == 'done':
                continue # Saltar los que ya se hicieron si se re-ejecuta
            
            try:
                line.action_process_single()
                # Hacemos commit por cada archivo para guardar progreso si algo falla después
                self.env.cr.commit()
            except Exception as e:
                line.state = 'error'
                line.error_message = str(e)
                _logger.error(f"Error procesando archivo {line.filename}: {e}")

        self.state = 'done'
        
        # Recargamos la vista para mostrar resultados
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'ocr.bulk.digitize.wizard',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
        }

    def action_view_invoices(self):
        """Botón inteligente para ver las facturas creadas"""
        self.ensure_one()
        invoices = self.line_ids.mapped('invoice_id')
        return {
            'name': _('Facturas Generadas'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'list,form',
            'domain': [('id', 'in', invoices.ids)],
        }


class OcrBulkDigitizeLine(models.TransientModel):
    _name = 'ocr.bulk.digitize.line'
    _description = 'Línea de Documento a Digitalizar'

    wizard_id = fields.Many2one('ocr.bulk.digitize.wizard')
    
    file_content = fields.Binary(string="Archivo", required=True)
    filename = fields.Char(string="Nombre Archivo", required=True)
    
    invoice_id = fields.Many2one('account.move', string="Factura Creada", readonly=True)
    
    state = fields.Selection([
        ('draft', 'Pendiente'),
        ('done', 'Éxito'),
        ('error', 'Error')
    ], default='draft', string="Estado")
    
    error_message = fields.Char(string="Mensaje de Error")

    def action_process_single(self):
        """
        Magia pura: Crea la factura vacía, adjunta el PDF y dispara 
        la lógica que ya creamos en extract_mixin.
        """
        self.ensure_one()
        
        # 1. Crear Factura Vacía (Borrador)
        invoice = self.env['account.move'].create({
            'move_type': 'in_invoice', # Factura de Proveedor
            'state': 'draft',
        })
        
        # 2. Crear el Adjunto (Attachment)
        attachment = self.env['ir.attachment'].create({
            'name': self.filename,
            'datas': self.file_content,
            'res_model': 'account.move',
            'res_id': invoice.id,
            'type': 'binary',
        })
        
        # 3. Vincular como adjunto principal (Trigger para OCR en Odoo estándar)
        invoice.message_main_attachment_id = attachment.id
        
        # 4. Disparar nuestro Mixin Refactorizado
        # Esto llamará a _upload_to_extract en ocr_manager/models/extract_mixin.py
        # Usamos try/except aquí para atrapar errores específicos de la IA
        try:
            success = invoice._upload_to_extract()
            
            if success:
                self.invoice_id = invoice.id
                self.state = 'done'
            else:
                self.state = 'error'
                self.error_message = "El motor OCR no devolvió resultados o está desactivado."
                
        except Exception as e:
            self.state = 'error'
            self.error_message = f"Fallo en IA: {str(e)}"
            # Opcional: Borrar la factura si falló totalmente para no dejar basura
            # invoice.unlink()