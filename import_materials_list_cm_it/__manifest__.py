# -*- encoding: utf-8 -*-
{
	'name': 'Importador de Acuerdos de Compra',
	'category': 'purchase',
	'author': 'ITGRUPO',
	'depends': ['product','mrp'],
	'version': '1.0',
	'description':"""
	Importador de Acuerdos de Compra
	""",
	'auto_install': False,
	'demo': [],
	'data':	[
		#'security/security.xml',
		'security/ir.model.access.csv',
		'data/attachment_sample.xml',
		'wizard/import_purchase_requisition.xml',
		# 'views/delete_journal_entry_import.xml'
		],
	'installable': True
}
