# coding=utf-8
__author__ = 'cysnake4713'
from openerp import tools
from openerp import models, fields, api
from openerp.tools.translate import _


a = [('draft', u'制作人'),
     ('project_manager', u'项目经理审批'),
     ('department_manager', u'部门领导审批'),
     ('project_admin', u'项目管理员审批'),
     ('project_chief', u'项目管理负责人审批'),
     ('finance', u'财务部审批'),
     ('vice_chief', u'分管领导审批'),
     ('chief', u'主任审批'),
     ('finish', u'结束'),
     ]


class Project(models.Model):
    _name = 'cisp.project.project'
    _inherit = 'odoosoft.workflow.abstract'

    name = fields.Char('Name')
    state = fields.Selection([('processing', 'Processing'),
                              ], 'State', default='processing')
