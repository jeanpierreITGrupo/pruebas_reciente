from odoo import fields, models , api , _
class SolicitudProduction(models.Model):
    _name = 'solicitud.production'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    name = fields.Char()
    mrp_production = fields.Many2one('mrp.production',string="Orden de Produccion",
                                     ondelete='restrict',required=True)
    state = fields.Selection([('draft','Borrador'),('comfirm','Aprobada')],default='draft')
    order_line = fields.One2many('solicitud.production.line', 'order_id', string='Order Lines', copy=True)
    date_order = fields.Datetime(string='Order Date', required=True, readonly=True, index=True,
                                 copy=False,
                                 default=fields.Datetime.now,
                                 help="Creation date of draft/sent orders,\nConfirmation date of confirmed orders.")
    user_id = fields.Many2one(
        'res.users', string='Salesperson', index=True, tracking=2, default=lambda self: self.env.user,
    )
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True,
                                 default=lambda self: self.env.company)
    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            seq_date = None
            if 'date_order' in vals:
                seq_date = fields.Datetime.context_timestamp(self, fields.Datetime.to_datetime(vals['date_order']))
            if 'company_id' in vals:
                vals['name'] = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code(
                    'solicitud.production', sequence_date=seq_date) or _('New')
            else:
                vals['name'] = self.env['ir.sequence'].next_by_code('solicitud.production', sequence_date=seq_date) or _('New')

        result = super(SolicitudProduction, self).create(vals)
        return result

    def fun_aprobar(self):
        if not self.order_line:
            raise ValueError('No tiene Lineas de Productos')
        self.state = 'comfirm'
        for l in self.order_line:
            #raise ValueError(l.order_id.mrp_production.production_location_id.id)
            '''
            dx = {
                'product_id': l.product_id.id ,
                'name':  l.product_id.display_name,
                'quantity_done': l.consumed,
                'product_uom': l.product_id.uom_id.id,
                'location_id': 	l.order_id.mrp_production.location_src_id.id,
                'location_dest_id': l.order_id.mrp_production.location_dest_id.id ,
                'solicitud_production': l.order_id.id ,

            }
            '''

            dx  = l.order_id.mrp_production._get_move_raw_values(l.product_id, l.consumed,l.product_id.uom_id, False, False)
            dx['solicitud_production_line'] = l.id
            self.mrp_production.move_raw_ids += self.env['stock.move'].new(dx)


class SolicitudProductionLine(models.Model):
    _name = 'solicitud.production.line'
    name = fields.Char(related="product_id.display_name")
    order_id = fields.Many2one('solicitud.production',ondelete='restrict')
    product_id = fields.Many2one('product.product',string="Producto",ondelete='restrict',required=True)
    consumed = fields.Float()



