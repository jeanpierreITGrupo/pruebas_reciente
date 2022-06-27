# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo import tools

class account_move(models.Model):
    _inherit = 'account.move'
    

    @api.onchange('partner_id')
    def _onchange_get_porcentaje_comision(self):
        for i in self:            
            if i.move_type == 'out_invoice' or i.move_type == 'out_refound':
                if i.partner_id.id:
                    if i.partner_id.is_partner_retencion == True:
                        i.l10n_pe_dte_retention_type = '01'                        
                        i._onchange_l10n_pe_retention_calc()
                    else:
                        i.l10n_pe_dte_retention_type = False                        
                        i._onchange_l10n_pe_retention_calc()
                else:
                    i.l10n_pe_dte_retention_type = False
                    i._onchange_l10n_pe_retention_calc()
    