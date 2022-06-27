# -*- coding: utf-8 -*-
{
    'name' : 'Añadir Posicion Fiscal Vista Tree Facturas',
    'version': '1.0',
    'author': 'ITGRUPO',
    'website': '',
    'category': 'account',
    'description':
        """
        Añadir Posicion Fiscal Vista Tree Facturas
        """,
    'depends' : ['account','base'],
    #,'fxo_sale_order_approve'
    'data': [
        'views/account_posicion_fiscal.xml',
    ],
    'auto_install': False,
    'installable': True
}