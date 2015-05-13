# -*- coding: utf-8 -*-
{
    'name': 'Cisp Project Module',
    'version': '0.2',
    'category': 'cisp_project',
    'complexity': "easy",
    'description': """
Cisp Project Module""",
    'author': 'Matt Cai',
    'website': 'http://odoosoft.com',
    'depends': ['base', 'odoosoft_workflow'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/config_view.xml',
        'views/project_view.xml',
        'views/menu.xml',
    ],
    'qweb': [
        'static/src/xml/*.xml',
    ],
    'demo': [],
    'application': True
}
