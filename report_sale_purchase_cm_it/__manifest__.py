# -*- coding: utf-8 -*-
{
    'name': "Observaciones despligue ventas (#10772)",

    'summary': """""",

    'description': """Observaciones despligue ventas (#10772)""",

    'author': "ITGRUPO",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base','sale','sale_order_resinas_cm_it','sale_report_reserva'],
    'data': [
        'security/ir.model.access.csv',
        'views/purchase_report.xml',
        'views/sale_report.xml',
        'views/sale_order.xml',
        'views/res_partner.xml'
    ],
    'demo': [],
}
