from odoo import fields, models , api , _

class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'
    calculo = fields.Boolean(default=True)
    stage_id = fields.Many2one('stage.mrpline',string="Etapa")
    percentaje = fields.Float(string="Porcentaje")





    def write(self, vals):
        # if 'price_unit' in vals and 'prodyct_uom_qty' in vals:

        origins_values = dict()

        array_keys = [('product_id','Producto'),
                      ('percentaje','Porcentaje'),
                      ('product_qty','Cantidad'),
                      ('product_uom_id','Unidad'),
                      ('stage_id','Etapa')]
        for a in array_keys:
            if a[0] in vals:
                if self[a[0]]:
                    if a[0] in ['stage_id', 'product_id']:
                        origins_values[a[0]] = self[a[0]].display_name
                    else:
                        origins_values[a[0]] = self[a[0]]
                else:
                    origins_values[a[0]] = ''

        res = super(MrpBomLine, self).write(vals)

        for a in array_keys:
            if a[0] in origins_values:
                ky  = origins_values[a[0]]
                #raise ValueError([a[1],str(ky),])
                new = self[a[0]]
                if a[0] in ['stage_id', 'product_id']:
                    new = self[a[0]].display_name if  'display_name' in self[a[0]] else ''

                texto =  "<li type='circle'> {} : {} ->  {}".format(a[1],str(ky),new)
                self.bom_id.message_post(
                    message_type='comment',
                    body=texto,
                    subject="Actualizando Valor",
                )

        return res

class StageMrpBomLine(models.Model):
    _name = 'stage.mrpline'
    name = fields.Char()