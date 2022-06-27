# -*- coding: utf-8 -*-

from odoo import api, fields, models

class saleOrderLineQtyIT(models.Model):
    _inherit = "sale.order.line"

    qty_no_delivered = fields.Float('Ctdad No Enviada', compute='_compute_qty_no_delivered', store=True)

    @api.depends('product_uom_qty','qty_delivered')
    def _compute_qty_no_delivered(self):
        for line in self:
            no_delivered = 0
            if line.product_uom_qty > 0:
                no_delivered = line.product_uom_qty - line.qty_delivered
            line.qty_no_delivered = no_delivered

class SaleReportIT(models.Model):
    _inherit = "sale.report"

    qty_no_delivered = fields.Float('Ctdad No Enviada')
    purchase_price_line = fields.Float('Costo')
    margin_line = fields.Float('Márgen Linea')
    margin_percent_line = fields.Float('Márgen (%)')

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        fields['qty_no_delivered'] = ", l.qty_no_delivered as qty_no_delivered"
        fields['purchase_price_line'] = ", l.purchase_price as purchase_price_line"
        fields['margin_line'] = ", l.margin as margin_line"
        fields['margin_percent_line'] = ", l.margin_percent as margin_percent_line"
        groupby += ', l.qty_no_delivered'
        groupby += ', l.purchase_price'
        groupby += ', l.margin'
        groupby += ', l.margin_percent'
        return super(SaleReportIT, self)._query(with_clause, fields, groupby, from_clause)

        
