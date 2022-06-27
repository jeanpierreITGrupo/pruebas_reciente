from odoo import fields, models , api , _
from odoo.exceptions import UserError

class MrpBom(models.Model):
    _inherit = 'mrp.bom'
    #active_material = fields.Boolean()
    active = fields.Boolean(tracking=True)

    bom_line_ids = fields.One2many('mrp.bom.line', 'bom_id',tracking=True )
    byproduct_ids = fields.One2many('mrp.bom.byproduct', 'bom_id', tracking=True)
    product_qty = fields.Float(tracking=True)
    product_uom_id = fields.Many2one('uom.uom', tracking=True)

    total_percentaje = fields.Float(compute="get_totals_js",string="Total Porcentaje")
    total_quantity = fields.Float(compute="get_totals_js",string="Total Cantidad")

    @api.depends('bom_line_ids.percentaje','bom_line_ids.product_qty')
    def get_totals_js(self):
        for record in self:
            TP = 0
            TC = 0
            for l in record.bom_line_ids:
                if l.calculo:
                    TP += l.percentaje
                    TC += l.product_qty
            record.total_percentaje = TP
            record.total_quantity = TC

    @api.onchange('product_tmpl_id')
    def change_product(self):
        act = True
        if self.product_tmpl_id:

            domain = ['|', ('product_tmpl_id', '=', self.product_tmpl_id.id),
                      ('byproduct_ids.product_id.product_tmpl_id', '=', self.product_tmpl_id.id)]
            exist = self.env['mrp.bom'].search(domain)
            if exist:
                act = False
            #raise ValueError(self.product_tmpl_id.display_name)

        if self.product_id:
            domain = [('product_id', '=', self.product_id.id)]
            exist = self.env['mrp.bom'].search(domain)
            if exist:
                act = False

        self.active = act

    def write(self, values):


        res = super(MrpBom, self).write(values)

        if self.active:
            if self.product_tmpl_id:

                domain = ['|', ('product_tmpl_id', '=', self.product_tmpl_id.id),
                          ('byproduct_ids.product_id.product_tmpl_id', '=', self.product_tmpl_id.id)]
                exist = self.env['mrp.bom'].search(domain)
                if exist:
                    for e in exist:
                        if e.active and e != self:
                            raise UserError('Ya existe una lista de material activa')

                # raise ValueError(self.product_tmpl_id.display_name)

            if self.product_id:
                domain = [('product_id', '=', self.product_id.id)]
                exist = self.env['mrp.bom'].search(domain)
                if exist:
                    for e in exist:
                        if e.active and e != self:
                            raise UserError('Ya existe una lista de material activa')

        return res






