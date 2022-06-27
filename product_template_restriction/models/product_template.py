# -*- coding: utf-8 -*-

from ast import Pass
from pickle import PicklingError
from shutil import move
from odoo import models, fields, api, _
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo import tools

class product_template(models.Model):
    _inherit = 'product.template'
    
    def unlink(self):
        if self.env.user.has_group("product_template_restriction.group_product_template_restriction"):
            t = super(product_template,self).unlink()
            return t
        else:
            raise UserError("No Tiene Los Permisos de 'Manejo Creacion de Productos'")

    @api.model
    def create(self,vals):
        if self.env.user.has_group("product_template_restriction.group_product_template_restriction"):
            t = super(product_template,self).create(vals)
            return t
        else:
            raise UserError("No Tiene Los Permisos de 'Manejo Creacion de Productos'")
           
    def write(self,vals):
        if 'seller_ids' in vals or 'name' in vals  or 'route_ids' in vals  or 'sale_ok' in vals  or 'purchase_ok' in vals  or 'detailed_type' in vals  or 'invoice_policy' in vals  or 'expense_policy' in vals  or 'uom_id' in vals  or 'uom_po_id' in vals  or 'description' in vals  or 'list_price' in vals  or 'taxes_id' in vals  or 'categ_id' in vals  or 'default_code' in vals or 'barcode' in vals or 'l10n_pe_edi_unspsc' in vals or 'company_id' in vals or 'attribute_line_ids' in vals or 'purchase_requisition' in vals or 'supplier_taxes_id' in vals or 'purchase_method' in vals or 'description_purchase' in vals or 'description_sale' in vals or 'sale_line_warn' in vals or 'property_stock_production' in vals or 'property_stock_inventory' in vals or 'responsible_id' in vals or 'weight' in vals or 'volume' in vals or 'produce_delay' in vals or 'sale_delay' in vals or 'packaging_ids' in vals or 'description_pickingin' in vals or 'description_picking' in vals or 'description_pickingout' in vals or 'property_account_income_id' in vals or 'property_account_expense_id' in vals or 'asset_category_id' in vals or 'property_account_creditor_price_difference' in vals or 'service_to_purchase' in vals or 'is_landed_cost' in vals:
        #if 'seller_ids' or 'name' or 'route_ids' or 'sale_ok' or 'purchase_ok' or 'detailed_type' or 'invoice_policy' or 'expense_policy' or 'uom_id' or 'uom_po_id' or 'description' or 'list_price' or 'taxes_id' or 'categ_id' or 'default_code' or 'barcode' or 'l10n_pe_edi_unspsc' or 'company_id' or 'attribute_line_ids' or 'purchase_requisition' or 'supplier_taxes_id' or 'purchase_method' or 'description_purchase' or 'description_sale' or 'sale_line_warn' or 'property_stock_production' or 'property_stock_inventory' or 'responsible_id' or 'weight' or 'volume' or 'produce_delay' or 'sale_delay' or 'packaging_ids' or 'description_pickingin' or 'description_picking' or 'description_pickingout' or 'property_account_income_id' or 'property_account_expense_id' or 'asset_category_id' or 'property_account_creditor_price_difference' or 'service_to_purchase' or 'is_landed_cost' in vals:
            if self.env.user.has_group("product_template_restriction.group_product_template_restriction"):
                t = super(product_template,self).write(vals)
                return t
            else:
                raise UserError("No Tiene Los Permisos de 'Manejo Creacion de Productos'")
        else:
            t = super(product_template,self).write(vals)
            return t
            

class product_product(models.Model):
    _inherit = 'product.product'
    
    def unlink(self):
        if self.env.user.has_group("product_template_restriction.group_product_template_restriction"):
            t = super(product_product,self).unlink()
            return t
        else:
            raise UserError("No Tiene Los Permisos de 'Manejo Creacion de Productos'")

    @api.model
    def create(self,vals):
        if self.env.user.has_group("product_template_restriction.group_product_template_restriction"):
            t = super(product_product,self).create(vals)
            return t
        else:
            raise UserError("No Tiene Los Permisos de 'Manejo Creacion de Productos'")
           
    def write(self,vals):
        if 'seller_ids' in vals or 'name' in vals  or 'route_ids' in vals  or 'sale_ok' in vals  or 'purchase_ok' in vals  or 'detailed_type' in vals  or 'invoice_policy' in vals  or 'expense_policy' in vals  or 'uom_id' in vals  or 'uom_po_id' in vals  or 'description' in vals  or 'list_price' in vals  or 'taxes_id' in vals  or 'categ_id' in vals  or 'default_code' in vals or 'barcode' in vals or 'l10n_pe_edi_unspsc' in vals or 'company_id' in vals or 'attribute_line_ids' in vals or 'purchase_requisition' in vals or 'supplier_taxes_id' in vals or 'purchase_method' in vals or 'description_purchase' in vals or 'description_sale' in vals or 'sale_line_warn' in vals or 'property_stock_production' in vals or 'property_stock_inventory' in vals or 'responsible_id' in vals or 'weight' in vals or 'volume' in vals or 'produce_delay' in vals or 'sale_delay' in vals or 'packaging_ids' in vals or 'description_pickingin' in vals or 'description_picking' in vals or 'description_pickingout' in vals or 'property_account_income_id' in vals or 'property_account_expense_id' in vals or 'asset_category_id' in vals or 'property_account_creditor_price_difference' in vals or 'service_to_purchase' in vals or 'is_landed_cost' in vals:
            if self.env.user.has_group("product_template_restriction.group_product_template_restriction"):
                t = super(product_product,self).write(vals)
                return t
            else:
                raise UserError("No Tiene Los Permisos de 'Manejo Creacion de Productos'")
        else:
            t = super(product_product,self).write(vals)
            return t
            





class purchase_order(models.Model):
    _inherit = 'purchase.order'
    
    def _add_supplier_to_product(self):
        # Add the partner in the supplier list of the product if the supplier is not registered for
        # this product. We limit to 10 the number of suppliers for a product to avoid the mess that
        # could be caused for some generic products ("Miscellaneous").
        for line in self.order_line:
            # Do not add a contact as a supplier
            partner = self.partner_id if not self.partner_id.parent_id else self.partner_id.parent_id
            if line.product_id and partner not in line.product_id.seller_ids.mapped('name') and len(line.product_id.seller_ids) <= 10:
                # Convert the price in the right currency.
                currency = partner.property_purchase_currency_id or self.env.company.currency_id
                price = self.currency_id._convert(line.price_unit, currency, line.company_id, line.date_order or fields.Date.today(), round=False)
                # Compute the price for the template's UoM, because the supplier's UoM is related to that UoM.
                if line.product_id.product_tmpl_id.uom_po_id != line.product_uom:
                    default_uom = line.product_id.product_tmpl_id.uom_po_id
                    price = line.product_uom._compute_price(price, default_uom)

                supplierinfo = self._prepare_supplier_info(partner, line, price, currency)
                # In case the order partner is a contact address, a new supplierinfo is created on
                # the parent company. In this case, we keep the product name and code.
                seller = line.product_id._select_seller(
                    partner_id=line.partner_id,
                    quantity=line.product_qty,
                    date=line.order_id.date_order and line.order_id.date_order.date(),
                    uom_id=line.product_uom)
                if seller:
                    supplierinfo['product_name'] = seller.product_name
                    supplierinfo['product_code'] = seller.product_code
                vals = {
                    'seller_ids': [(0, 0, supplierinfo)],
                }
                try:
                    if self.env.user.has_group("product_template_restriction.group_product_template_restriction"):
                        line.product_id.write(vals)
                    else:
                        grupo_editor = self.env.ref('product_template_restriction.group_product_template_restriction')
                        grupo_editor.sudo().write({'users':[(4, self.env.user.id)]
                                                   })
                        line.product_id.write(vals)
                        grupo_editor.sudo().write({'users':[(3, self.env.user.id)]
                                                   })
                        
                except AccessError:  # no write access rights -> just ignore
                    break

