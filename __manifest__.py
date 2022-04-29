# -*- coding: utf-8 -*-
{
    'name': "customer_credit_limit",

    'summary': """ Limite de credito para el cliente """,

    'description': """
        Limite de credito del cliente
    """,

    'author': "JS",
    'website': "",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['account'],

    'data': [
        # 'security/ir.model.access.csv',
        'views/res_partner_views.xml',
    ],
}
