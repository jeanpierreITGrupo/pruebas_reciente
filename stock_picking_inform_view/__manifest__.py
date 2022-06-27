# -*- coding: utf-8 -*-
{
    'name' : 'Permitir a Usuarios Logistica Ver Informes',
    'version': '1.0',
    'author': 'ITGRUPO',
    'website': '',
    'category': 'stock',
    'description':
        """
        Permitir a Usuarios Logistica Ver Informes
        """,
    'depends' : ['base','stock','stock_enterprise','stock_account'],
    #,'fxo_sale_order_approve'
    'data': [
        'views/stock_show_inform.xml',
        'views/ir.model.access.csv'
    ],
    'auto_install': False,
    'installable': True
}