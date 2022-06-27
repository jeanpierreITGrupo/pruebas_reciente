from odoo import fields, models , api , _
from odoo.exceptions import UserError

class EmpaqueStockMove(models.Model):
    _name = 'empaque.stock.mv'
    mrp_production_id = fields.Many2one('mrp.production',readonly=1)
    mrp_production = fields.Many2one('mrp.production',readonly=1)
    sub_producto = fields.Many2one('stock.move',readonly=1)

    name = fields.Char(compute="dame_el_nombre_xd")
    def dame_el_nombre_xd(self):
        for record in self:
            name = ''
            if record.mrp_production:
                if record.mrp_production.product_id:
                    name += record.mrp_production.product_id.display_name
                name += ' / '+ record.mrp_production.display_name

            if record.sub_producto:
                if record.sub_producto.product_id:
                    name += record.sub_producto.product_id.display_name
                name += ' / '+  str(record.sub_producto.product_uom_qty)
            record.name = name
