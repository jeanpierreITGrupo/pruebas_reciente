# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date, datetime

class hrDepartamentAnalitycIT(models.Model):
    _inherit = 'hr.department'

    analytical_account = fields.Many2one('account.analytic.account','Cuenta Analítica')

class resPartnerDepartamentIT(models.Model):
    _inherit = 'res.partner'

    departament_analytic = fields.Many2one('hr.department','Departamento')

class crossoveredBudgetLinesDapartamentIT(models.Model):
    _inherit = 'crossovered.budget.lines'

    user_depa_analytic = fields.Many2one('account.analytic.account','Cuenta Analítica', default=lambda self: self.env.user.partner_id.departament_analytic.analytical_account)

    # @api.depends('crossovered_budget_id')
    def _compute_user_depa_analytic(self):
        for line in self:
            if self.env.user.departament_analytic.analytical_account:
                line.user_depa_analytic = self.env.user.partner_id.departament_analytic.analytical_account
            else:
                line.user_depa_analytic = False
            # line.user_depa_analytic = 1
            print('DEPA USUARIO',line.user_depa_analytic)

    @api.onchange('crossovered_budget_id') 
    def onchange_get_value_c(self): 
        print('Entro al onchange')
        for rec in self:
            return {'domain': {'crossovered_budget_id': [('analytic_account_id','=', rec.user_depa_analytic)]}}

class crossoveredBudgetDapartamentIT(models.Model):
    _inherit = 'crossovered.budget'

    user_depa_analytic = fields.Many2one('account.analytic.account','Cuenta Analítica',default=lambda self: self.env.user.partner_id.departament_analytic.analytical_account)
    domain_compute = fields.Char('Prueba', compute="_compute_domain_compute")

    # @api.depends('crossovered_budget_id')
    def _compute_user_depa_analytic(self):
        for line in self:
            if self.env.user.departament_analytic.analytical_account:
                line.user_depa_analytic = self.env.user.partner_id.departament_analytic.analytical_account
            else:
                line.user_depa_analytic = False
            # line.user_depa_analytic = 1
            print('DEPA USUARIO',line.user_depa_analytic)


    def _compute_domain_compute(self): 
        print('Entro al onchange')
        for rec in self:
            for line in  rec.crossovered_budget_line:
                linea_verificar = self.env["crossovered.budget.lines"].search([('id', '=', line.id)])
                return {'domain': {'crossovered_budget_line': [('analytic_account_id','=', rec.user_depa_analytic)]}}


