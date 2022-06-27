# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from collections import defaultdict

from odoo import api, fields, models
from odoo.tools import float_round

class MrpCostStructure(models.AbstractModel):
    _inherit = 'report.mrp_account_enterprise.mrp_cost_structure'

    def get_lines(self, productions):
        ProductProduct = self.env['product.product']
        StockMove = self.env['stock.move']
        res = []
        currency_table = self.env['res.currency']._get_query_currency_table({'multi_company': True, 'date': {'date_to': fields.Date.today()}})
        for product in productions.mapped('product_id'):
            mos = productions.filtered(lambda m: m.product_id == product)
            total_cost = 0.0
            # variables to calc cost share (i.e. between products/byproducts) since MOs can have varying distributions
            total_cost_by_mo = defaultdict(float)
            component_cost_by_mo = defaultdict(float)
            operation_cost_by_mo = defaultdict(float)

            # Get operations details + cost
            operations = []
            Workorders = self.env['mrp.workorder'].search([('production_id', 'in', mos.ids)])
            if Workorders:
                query_str = """SELECT
                                    wo.production_id,
                                    wo.id,
                                    op.id,
                                    wo.name,
                                    partner.name,
                                    sum(t.duration),
                                    CASE WHEN wo.costs_hour = 0.0 THEN wc.costs_hour ELSE wo.costs_hour END AS costs_hour,
                                    currency_table.rate
                                FROM mrp_workcenter_productivity t
                                LEFT JOIN mrp_workorder wo ON (wo.id = t.workorder_id)
                                LEFT JOIN mrp_workcenter wc ON (wc.id = t.workcenter_id)
                                LEFT JOIN res_users u ON (t.user_id = u.id)
                                LEFT JOIN res_partner partner ON (u.partner_id = partner.id)
                                LEFT JOIN mrp_routing_workcenter op ON (wo.operation_id = op.id)
                                LEFT JOIN {currency_table} ON currency_table.company_id = t.company_id
                                WHERE t.workorder_id IS NOT NULL AND t.workorder_id IN %s
                                GROUP BY wo.production_id, wo.id, op.id, wo.name, wc.costs_hour, partner.name, t.user_id, currency_table.rate
                                ORDER BY wo.name, partner.name
                            """.format(currency_table=currency_table,)
                self.env.cr.execute(query_str, (tuple(Workorders.ids), ))
                for mo_id, dummy_wo_id, op_id, wo_name, user, duration, cost_hour, currency_rate in self.env.cr.fetchall():
                    cost = duration / 60.0 * cost_hour * currency_rate
                    total_cost_by_mo[mo_id] += cost
                    operation_cost_by_mo[mo_id] += cost
                    operations.append([user, op_id, wo_name, duration / 60.0, cost_hour * currency_rate])

            # Get the cost of raw material effectively used
            raw_material_moves = []



            query_str = """SELECT
                                sm.product_id,
                                mo.id,
                                abs(SUM(svl.quantity)),
                                abs(SUM(svl.value)),
                                currency_table.rate ,
                                sm.id 
                             FROM stock_move AS sm
                       INNER JOIN stock_valuation_layer AS svl ON svl.stock_move_id = sm.id
                       LEFT JOIN mrp_production AS mo on sm.raw_material_production_id = mo.id
                       LEFT JOIN {currency_table} ON currency_table.company_id = mo.company_id
                            WHERE sm.raw_material_production_id in %s AND sm.state != 'cancel' AND sm.product_qty != 0 AND scrapped != 't'
                         GROUP BY sm.product_id, mo.id, currency_table.rate , sm.id """.format(currency_table=currency_table,)

            #SE QUITO LA CANTIDAD 0
            query_str = """SELECT
                                            sm.product_id,
                                            mo.id,
                                            abs(SUM(svl.quantity)),
                                            abs(SUM(svl.value)),
                                            currency_table.rate ,
                                            sm.id 
                                         FROM stock_move AS sm
                                   INNER JOIN stock_valuation_layer AS svl ON svl.stock_move_id = sm.id
                                   LEFT JOIN mrp_production AS mo on sm.raw_material_production_id = mo.id
                                   LEFT JOIN {currency_table} ON currency_table.company_id = mo.company_id
                                        WHERE sm.raw_material_production_id in %s AND sm.state != 'cancel' AND scrapped != 't'
                                     GROUP BY sm.product_id, mo.id, currency_table.rate , sm.id """.format(
                currency_table=currency_table, )



            self.env.cr.execute(query_str, (tuple(mos.ids), ))
            fetch = self.env.cr.fetchall()
            #raise ValueError(fetch)
            for product_id, mo_id, qty, cost, currency_rate , sm in fetch :
                cost *= currency_rate
                sm_x = StockMove.browse(sm)
                cost_unit = cost / qty if qty != 0 else 0
                raw_material_moves.append({
                    'qty': qty,
                    'cost': cost,
                    'cost_unit': cost_unit ,
                    'product_id': ProductProduct.browse(product_id),
                    'sm': sm_x,
                    'cost_origin': sm_x.should_consume_qty_store * ( cost / qty ) if qty != 0 else sm_x.should_consume_qty_store ,
                    'request_production': sm_x.solicitud_production,
                    'pt': sm_x.empaque_line
                })
                total_cost_by_mo[mo_id] += cost
                component_cost_by_mo[mo_id] += cost
                total_cost += cost

            # Get the cost of scrapped materials
            scraps = StockMove.search([('production_id', 'in', mos.ids), ('scrapped', '=', True), ('state', '=', 'done')])

            # Get the byproducts and their total + avg per uom cost share amounts
            total_cost_by_product = defaultdict(float)
            qty_by_byproduct = defaultdict(float)
            qty_by_byproduct_w_costshare = defaultdict(float)
            cost_empaque_byproduct_w_costshare = defaultdict(float)
            component_cost_by_product = defaultdict(float)
            operation_cost_by_product = defaultdict(float)
            # tracking consistent uom usage across each byproduct when not using byproduct's product uom is too much of a pain
            # => calculate byproduct qtys/cost in same uom + cost shares (they are MO dependent)
            byproduct_moves = mos.move_byproduct_ids.filtered(lambda m: m.state != 'cancel')
            for move in byproduct_moves:

                qty_by_byproduct[move.product_id] += move.product_qty
                # byproducts w/o cost share shouldn't be included in cost breakdown
                if move.cost_share != 0:
                    qty_by_byproduct_w_costshare[move.product_id] += move.product_qty
                    for rmv in raw_material_moves:
                        if rmv['pt']:
                            if rmv['pt'].sub_producto:
                                if rmv['pt'].sub_producto == move:
                                    cost_empaque_byproduct_w_costshare[move.product_id] += rmv['cost_unit']


                    cost_share = move.cost_share / 100
                    total_cost_by_product[move.product_id] += total_cost_by_mo[move.production_id.id] * cost_share
                    component_cost_by_product[move.product_id] += component_cost_by_mo[move.production_id.id] * cost_share
                    operation_cost_by_product[move.product_id] += operation_cost_by_mo[move.production_id.id] * cost_share

            #raise  ValueError(cost_empaque_byproduct_w_costshare)

            # Get product qty and its relative total + avg per uom cost share amount
            uom = product.uom_id
            mo_qty = 0
            for m in mos:
                cost_share = float_round(1 - sum(m.move_finished_ids.mapped('cost_share')) / 100, precision_rounding=0.0001)
                total_cost_by_product[product] += total_cost_by_mo[m.id] * cost_share
                component_cost_by_product[product] += component_cost_by_mo[m.id] * cost_share
                operation_cost_by_product[product] += operation_cost_by_mo[m.id] * cost_share
                qty = sum(m.move_finished_ids.filtered(lambda mo: mo.state == 'done' and mo.product_id == product).mapped('product_uom_qty'))
                if m.product_uom_id.id == uom.id:
                    mo_qty += qty
                else:
                    mo_qty += m.product_uom_id._compute_quantity(qty, uom)

            ratios = self.env['mrp.ratios.lines'].search([('order_id', 'in', mos.ids)])
            total_ratiox = 0.0
            for m in ratios:
                total_ratiox += m.price_total

            cantidad_total = 0

            for m in mos:
                cantidad_total += m.product_uom_qty
                for r in m.move_byproduct_ids:
                    cantidad_total += r.quantity_done

            amount_to_cost = 0
            avg_cost = 0
            here_package = False
            weight_total_components = 0

            for r in raw_material_moves:
                if not r['pt']:
                    amount_to_cost += r['cost_origin']
                    avg_cost += r['cost']
                    weight_total_components += r['qty']
                else:
                    here_package = True


            total_production_cost = avg_cost + total_ratiox

            avg_cost_unit = avg_cost / cantidad_total if cantidad_total != 0 else avg_cost
            total_origin_unit = amount_to_cost / cantidad_total if cantidad_total != 0 else amount_to_cost
            total_operation_unit = total_production_cost / cantidad_total if cantidad_total != 0 else total_ratiox


            avg_cost_unit_kilo = 0
            total_origin_unit_kilo = 0
            total_operation_unit_kilo = 0
            #cambios a calculos por kilos cuando hay sub productos
            weight_total = mo_qty
            if qty_by_byproduct:
                #weight_total = product.weight * mo_qty


                for sp in qty_by_byproduct.items():
                    weight_total += sp[1] * sp[0].weight



                avg_cost_unit_kilo = avg_cost / weight_total if weight_total != 0 else 0
                avg_cost_unit  = avg_cost_unit_kilo

                total_origin_unit_kilo = amount_to_cost / weight_total_components if weight_total_components != 0 else 0
                total_origin_unit = total_origin_unit_kilo

                total_operation_unit_kilo = total_production_cost / weight_total if weight_total != 0 else 0
                total_operation_unit = total_operation_unit_kilo


            #avg_cost_unit =
            cost_empaque = 0

            for pts in productions:
                for rmv in raw_material_moves:
                    if rmv['pt']:
                        if rmv['pt'].mrp_production:
                            if rmv['pt'].mrp_production == pts:
                                cost_empaque += rmv['cost_unit']
                                here_package = True

            subproductos = []
            for byproduct in qty_by_byproduct_w_costshare.items():
                cost_empaque = cost_empaque_byproduct_w_costshare[byproduct[0]]
                total_origin_unit_kilo_k = (total_origin_unit_kilo * byproduct[0].weight) + cost_empaque
                avg_cost_unit_kilo_k = (avg_cost_unit_kilo * byproduct[0].weight) + cost_empaque
                total_operation_unit_kilo_k = (total_operation_unit_kilo * byproduct[0].weight) + cost_empaque

                weight_sb = byproduct[0].weight

                origin_x_kilo = total_origin_unit_kilo_k / weight_sb if  weight_sb != 0 else 0
                avg_x_kilo = avg_cost_unit_kilo_k / weight_sb if weight_sb != 0 else 0
                operation_x_kilo = total_operation_unit_kilo_k / weight_sb if weight_sb != 0 else 0

                subproductos.append(dict(
                    product=byproduct[0],
                    cost_empaque=cost_empaque,
                    total_origin_unit_kilo=total_origin_unit_kilo_k,
                    avg_cost_unit_kilo=avg_cost_unit_kilo_k,
                    total_operation_unit_kilo=total_operation_unit_kilo_k,
                    origin_x_kilo=origin_x_kilo,
                    avg_x_kilo=avg_x_kilo,
                    operation_x_kilo=operation_x_kilo

                ))

            origin_x_kilo_line =  total_origin_unit_kilo + cost_empaque
            avg_x_kilo_line = avg_cost_unit_kilo + cost_empaque
            operation_x_kilo_line = total_operation_unit + cost_empaque

            res.append({
                'product': product,
                'mo_qty': mo_qty,
                'mo_uom': uom,
                'operations': operations,
                'currency': self.env.company.currency_id,
                'raw_material_moves': raw_material_moves,
                'total_cost': avg_cost,
                #'total_cost': total_cost,
                'scraps': scraps,
                'mocount': len(mos),
                'byproduct_moves': byproduct_moves,
                'component_cost_by_product': component_cost_by_product,
                'operation_cost_by_product': operation_cost_by_product,
                'qty_by_byproduct': qty_by_byproduct,
                'subproductos': subproductos,
                #'qty_by_byproduct_w_costshare':qty_by_byproduct_w_costshare
                'total_cost_by_product': total_cost_by_product ,
                'ratios': ratios ,
                'total_ratio': total_ratiox ,
                'total_origin_unit':  total_origin_unit ,
                'total_operation_unit': total_operation_unit ,
                'amount_to_cost': amount_to_cost ,
                'avg_cost':avg_cost,
                'avg_cost_unit': avg_cost_unit ,
                'avg_cost_unit_kilo': avg_cost_unit_kilo ,
                'total_origin_unit_kilo': total_origin_unit_kilo ,
                'total_operation_unit_kilo': total_operation_unit_kilo ,
                'weight_total': weight_total,
                'weight_total_components': weight_total_components ,
                'here_package':here_package ,
                'cost_empaque_byproduct_w_costshare': cost_empaque_byproduct_w_costshare ,
                'cost_empaque': cost_empaque,
                'origin_x_kilo' : origin_x_kilo_line,
                'avg_x_kilo' : avg_x_kilo_line,
                'operation_x_kilo' : operation_x_kilo_line

            })
        return res