from odoo import fields, models , api , _
from odoo.tools import float_compare, float_round, float_is_zero, OrderedSet
class StockMove(models.Model):
    _inherit = 'stock.move'
    solicitud_production_line = fields.Many2one('solicitud.production.line',string="SM")
    solicitud_production = fields.Many2one('solicitud.production',related='solicitud_production_line.order_id')
    stage_id = fields.Many2one('stage.mrpline', string="Etapa")
    should_consume_qty_store = fields.Float('Cantidad Original',
                                      digits='Product Unit of Measure')
    empaque_line = fields.Many2one('empaque.stock.mv', string="PT")

    rs_unit_cost = fields.Float()
    rs_value = fields.Float()





