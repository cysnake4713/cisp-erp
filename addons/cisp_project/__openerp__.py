# -*- coding: utf-8 -*-
{
    'name': 'Cisp Project Module',
    'version': '0.2',
    'category': 'Category',
    'complexity': "easy",
    'description': """
Cisp Project Module""",
    'author': 'Matt Cai',
    'website': 'http://odoosoft.com',
    'depends': ['base', 'odoosoft_workflow'],
    'data': [
        'views/project_view.xml',
        'views/menu.xml',
    ],
    'qweb': [
        'static/src/xml/*.xml',
    ],
    'demo': [],
    'application': True
}
