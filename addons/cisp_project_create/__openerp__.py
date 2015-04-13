# -*- coding: utf-8 -*-
{
    'name': 'Cisp Project Create Module',
    'version': '0.2',
    'category': 'cisp_project_create',
    'complexity': "easy",
    'description': """
Cisp Project Create Module""",
    'author': 'Matt Cai',
    'website': 'http://odoosoft.com',
    'depends': ['base', 'cisp_project'],
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
