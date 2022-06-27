# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import date, datetime


class purchaseRequisitionCrossoveredIT(models.Model):
    _inherit = 'purchase.requisition'

    def crossovered(self):
        # presupuesto = self.env['crossovered.budget'].search([('date_from','<=',date.today()),('date_to','>=',date.today())],limit=1)
        # print('presupuestps',presupuesto)
        # if presupuesto:
        #     return {
        #         'name': "Presupuesto del mes",
        #         'res_model': 'crossovered.budget',
        #         'view_mode': 'tree',
        #         # 'view_id': self.env.ref('purchase_requisition_crossovered_cm_it.crossovered_budget_view_domain_analytic_form').id,
        #         'view_type': 'tree',
        #         'type': 'ir.actions.act_window',
        #         'target': 'new',
        #         # 'res_id': presupuesto.id,
        #     }
        # else:
        #     return self.env['popup.it'].get_message(u'LO SENTIMOS, NO EXISTEN PRESUPUESTOS PARA ESTE MES.')
        view_tree = self.env.ref('account_budget.crossovered_budget_view_tree', False)
        view_form = self.env.ref('account_budget.crossovered_budget_view_form', False)

        view_tree_new_form = self.env.ref('purchase_requisition_crossovered_cm_it.crossovered_budget_2_view_tree', False)

        return {
                'name': "Presupuesto del mes",
                'res_model': 'crossovered.budget',
                'view_mode': 'tree',
                'views': [(view_tree_new_form.id, 'tree')],
                'view_id': view_tree_new_form.id,
                # 'view_id': self.env.ref('account_budget.crossovered_budget_view_tree').id,
                'view_type': 'form',
                'type': 'ir.actions.act_window',
                'target': 'new',
                # 'res_id': presupuesto.id,
            }

class crossoveredBudgetButtonIT(models.Model):
    _inherit = 'crossovered.budget'

    def view_form(self):
        view_form = self.env.ref('purchase_requisition_crossovered_cm_it.crossovered_budget_view_2_form', False)
        print('view_form', view_form)

        return {
            'name': "Presupuesto del mes",
            'res_model': 'crossovered.budget',
            'view_mode': 'form',
            'views': [(view_form.id, 'form')],
            'view_id': view_form.id,
            # 'view_id': self.env.ref('purchase_requisition_crossovered_cm_it.crossovered_budget_view_domain_analytic_form').id,
            'view_type': 'form',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'res_id': self.id,
        }
