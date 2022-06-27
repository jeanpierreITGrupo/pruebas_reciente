from odoo import fields, models , api , _
from odoo.exceptions import UserError

class StockProductionLote(models.Model):
    _inherit = 'stock.production.lot'
    file_certificate = fields.Binary(string="Certificado")
    name_file_certificate = fields.Char()
