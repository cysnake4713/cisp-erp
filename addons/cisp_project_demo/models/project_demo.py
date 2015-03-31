# coding=utf-8
__author__ = 'cysnake4713'


# coding=utf-8
from openerp import tools
from openerp import models, fields, api
from openerp.tools.translate import _


class ProjectDemo(models.Model):
    _name = 'cisp.project.project'
    _inherit = 'odoosoft.workflow.abstract'

    name = fields.Char('Name')
    state = fields.Selection([('draft', u'进行中'),
                              ('f', u'取消'),
                              ('1', u'结项'),
                              ('e', u'中断'), ], 'State', default='draft')


class ProjectCreateDemo(models.Model):
    _name = 'cisp.project.project.create'
    _inherit = 'odoosoft.workflow.abstract'

    name = fields.Char('Name')
    state = fields.Selection([('draft', u'制作人'),
                              ('23', u'项目经理审批'),
                              ('f', u'部门领导审批'),
                              ('1', u'项目管理员审批'),
                              ('2', u'项目管理负责人审批'),
                              ('b', u'财务部审批'),
                              ('222', u'分管领导审批'),
                              ('d', u'主任审批'),
                              ('e', u'结束'), ], 'State', default='draft')
