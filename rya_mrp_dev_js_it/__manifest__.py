# -*- encoding: utf-8 -*-
{
    'name': 'RYA DESARROLLO',
    'category': 'uncategorize',
    'author': 'ITGRUPO',
    'depends': ['mrp_account_enterprise','account_base_it'],
    'version': '1.0',
    'description':"""
     Descripcion
    """,

    'auto_install': False,
    'demo': [],
    'data': [
        'data/ir_sequence_data.xml',
        'security/ir.model.access.csv',
        'security/grupo.xml',
        'views/mrp_production.xml',
        'views/solicitud_material.xml',
        'views/mrp_bom.xml',
        'views/plantilla_ratios.xml',
        'views/cost_structure_report.xml',
         'views/mrp_account_view.xml',
        'views/mrp_production.xml',
        'views/mrp_unbuild.xml',
        'views/stock_production_lot.xml',

        ],
    'installable': True
}