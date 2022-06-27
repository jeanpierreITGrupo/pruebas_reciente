# -*- coding: utf-8 -*-
{
    'name': "Presupuestos en Requerimiento (#10237)",

    'summary': """""",

    'description': """Presupuestos en Requerimiento (#10237)""",

    'author': "ITGRUPO",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base','purchase_requisition','analytic','hr','account_budget'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/purchase_requisition.xml',
        'views/hr_department.xml',
    ],
    'demo': [],
}
