from odoo import fields, models, api, _


class PlantillaRatios(models.Model):
    _name = 'plantilla.ratios'
    name = fields.Char(required=True)
    #is_default = fields.Boolean()
    order_line = fields.One2many('plantilla.ratios.line', 'order_id', string='Order Lines', copy=True)
    period = fields.Many2one('account.period',
                             string="Periodo",
                             required=True ,
                             domain=[('is_opening_close','!=',True),('close','!=',True)])

    _sql_constraints = [
        ('unique_period', 'unique(period)', 'Solo puede haber un periodo por ratio')
    ]

    @api.model
    def create(self, values):
        res = super(PlantillaRatios, self).create(values)
        # here you can do according
        if not res.order_line:
            names_array = [
                'MOD',
                'MOI - Operativo',
                'MOI - Production',
                'MOI - Control',
                'ALQUILER',
                'DEPRECIACION',
                'MANTENIMIENTO',
                'COMBUSTIBLE - FAMILIA 2',
                'ENERGIA ELECTRICA'
            ]
            for n in names_array:
                res.order_line += self.env['plantilla.ratios.line'].new({
                    'name': n
                })

        return res


class PlantillaRatiosLine(models.Model):
    _name = 'plantilla.ratios.line'
    name = fields.Char(required=True)
    #price_unit = fields.Float(string="Costo Unitario")
    order_id = fields.Many2one('plantilla.ratios', ondelete='restrict')
    cost_projected = fields.Float(string="Costo Proyectado")
    cost_real = fields.Float(string="Costo Real")
