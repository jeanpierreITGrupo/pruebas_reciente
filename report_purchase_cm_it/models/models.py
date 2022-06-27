# -*- coding: utf-8 -*-

from odoo import models, fields, api


class purchaseOrderPaymentIT(models.Model):
    _inherit = 'purchase.order'

    payment_name = fields.Char(string="Termino de pago Nombre", compute="_compute_payment_name")

    def _compute_payment_name(self):
        for record in self:
            if record.payment_term_id:
                record.payment_name = record.payment_term_id.name
                nombre = record.payment_term_id.name
