# -*- encoding: utf-8 -*-
{
	'name': 'Reporte RESULTADO POR NATURALEZA',
	'category': 'account',
	'author': 'ITGRUPO,Glenda Julia Merma Mayhua',
	'depends': ['account_report_menu_it'],
	'version': '1.0',
	'description':"""
	Reporte Resultado por Naturaleza
	""",
	'auto_install': False,
	'demo': [],
	'data':	[
			'security/ir.model.access.csv',
			'wizards/nature_result_wizard.xml'
			],
	'installable': True
}