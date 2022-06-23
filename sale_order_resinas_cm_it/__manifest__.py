# -*- coding: utf-8 -*-
{
    'name': "Modificaciones en OV Resinas",

    'summary': """""",

    'description': """Modificaciones en OV Resinas""",

    'author': "ITGRUPO",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base','sale','sale_margin'],
    'data': [
        'security/ir.model.access.csv',
        'security/groups.xml',
        'views/sale_order.xml',
        'views/res_config.xml',
        'views/margin.xml',
        'views/template_sale_order.xml'
    ],
    'demo': [],
}
