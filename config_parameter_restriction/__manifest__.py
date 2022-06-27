# -*- coding: utf-8 -*-
{
    'name' : 'Grupo No Permitir Cambiar Configuración',
    'version': '1.0',
    'author': 'ITGRUPO',
    'website': '',
    'category': 'base',
    'description':
        """
        Grupo No Permitir Cambiar Configuración
        """,
    'depends' : ['base'],
    #,'fxo_sale_order_approve'
    'data': [
        'security/group.xml',
        'security/ir.model.access.csv'
    ],
    'auto_install': False,
    'installable': True
}