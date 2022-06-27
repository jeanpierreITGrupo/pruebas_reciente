from odoo import fields, models , api
from odoo.exceptions import UserError
class MrpProduction(models.Model):
    _inherit = 'stock.valuation.layer'
    origin_unit_cost = fields.Float()
    origin_value = fields.Float()