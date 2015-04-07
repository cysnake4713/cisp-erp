# -*- coding: utf-8 -*-
{
    'name': 'CISP Department Module',
    'version': '0.2',
    'category': 'base',
    'complexity': "easy",
    'description': """
CISP Department Module""",
    'author': 'Matt Cai',
    'website': 'http://odoosoft.com',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/department_view.xml',
        'views/menu.xml',
    ],
    'qweb': [
        'static/src/xml/*.xml',
    ],
    'demo': [],
    'application': True
}
