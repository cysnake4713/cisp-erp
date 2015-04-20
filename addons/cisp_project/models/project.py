# coding=utf-8
__author__ = 'cysnake4713'
from openerp import tools
from openerp import models, fields, api
from openerp.tools.translate import _


class Project(models.Model):
    _name = 'cisp.project.project'
    _inherit = 'odoosoft.workflow.abstract'
    _description = 'Cisp Project'

    name = fields.Char('Name')
    state = fields.Selection([('processing', 'Processing'),
                              ], 'State', default='processing')


# class ProjectCategory(models.Model):
# _name = 'cisp.project.category'
#     _description = 'Cisp Project Category'
#     name = fields.char('Name', required=True)
#     _sql_constraints = [('project_category_name_unique', 'unique(name)', _('name must be unique !'))]


class ProjectBusinessCategory(models.Model):
    _name = 'cisp.project.business.category'
    _description = 'Cisp Project Business Category'

    name = fields.char('Name', required=True)
    type = fields.Selection([('build_project', u'能力建设项目'), ('market_project', u'市场建设项目'), ('goverment', u'政府项目')], 'Type',
                            default='build_project', required=True)

    _sql_constraints = [('project_busniess_category_name_unique', 'unique(name)', _('name must be unique !'))]