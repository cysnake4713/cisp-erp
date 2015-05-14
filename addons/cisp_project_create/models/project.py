# coding=utf-8
__author__ = 'cysnake4713'

from openerp import tools
from openerp import models, fields, api
from openerp.tools.translate import _


class ProjectInherit(models.Model):
    _inherit = 'cisp.project.project'

    create_project = fields.Many2one('cisp.project.project.create', 'Create Project')
    create_project_state = fields.Selection([('draft', u'制作人'),
                                             ('project_manager', u'项目经理审批'),
                                             ('department_manager', u'部门领导审批'),
                                             ('project_admin', u'项目管理员审批'),
                                             ('project_chief', u'项目管理部负责人审批'),
                                             ('finance', u'财务部审批'),
                                             ('vice_chief', u'分管领导审批'),
                                             ('chief', u'主任审批'),
                                             ('finish', u'结束'),
                                             ], 'State', readonly=True, related='create_project.state')

    _sql_constraints = [('project_create_id_unique', 'unique(create_project)', _('create_project be unique!'))]


class ResUserInherit(models.Model):
    _inherit = 'res.users'

    @api.model
    def _get_group(self):
        result = super(ResUserInherit, self)._get_group()
        try:
            result.append(self.env.ref('cisp_project_create.group_maker').id)
        except ValueError:
            # If these groups does not exists anymore
            pass
        return result

    _defaults = {
        'groups_id': _get_group,
    }