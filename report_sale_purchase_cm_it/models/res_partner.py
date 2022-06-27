# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError

class resPartnerIndustriesIT(models.Model):
    _inherit = 'res.partner'

    category_it_id = fields.Many2one('partner.category.it', string="Categorias de cliente")

class resPartnerCategoryIT(models.Model):
    _name = 'partner.category.it'

    name = fields.Char(string="Nombre")

class saleReportIndustriesIT(models.Model):
    _inherit = 'sale.report'

    category_partner_id = fields.Many2one('partner.category.it', string="Categorias Cliente")

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        fields['category_partner_id'] = ", partner.category_it_id as category_partner_id"

        groupby += ', partner.category_it_id'
        return super(saleReportIndustriesIT, self)._query(with_clause, fields, groupby, from_clause)