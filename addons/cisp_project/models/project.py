# coding=utf-8
__author__ = 'cysnake4713'
from openerp import tools
from openerp import models, fields, api
from openerp.tools.translate import _


class Project(models.Model):
    _name = 'cisp.project.project'
    _inherit = ['odoosoft.workflow.abstract', 'cisp.project.project.abstract']
    _description = 'Cisp Project'

    state = fields.Selection([('processing', 'Processing'),
                              ], 'State', default='processing')

    # 项目进度计划
    plans = fields.One2many('cisp.project.project.plan', 'project', 'Plans', required=True)
    # 项目预算
    budgets = fields.One2many('cisp.project.project.budget', 'project', 'Budgets')
    # 预算合计
    budgets_sum = fields.Float('Budget Sum(yuan)', compute='_compute_budgets_sum', readonly=True)
    # 项目组成员
    members_role = fields.One2many('cisp.project.project.member', 'project', 'Members Role', required=True)

    @api.multi
    @api.depends('budgets')
    def _compute_budgets_sum(self):
        for create in self:
            create.budgets_sum = sum([b.money for b in create.budgets])


class ProjectBusinessCategory(models.Model):
    _name = 'cisp.project.business.category'
    _description = 'Cisp Project Business Category'

    name = fields.Char('Name', required=True)
    type = fields.Selection([('build_project', u'能力建设项目'), ('market_project', u'市场建设项目'), ('government', u'政府项目')], 'Type',
                            default='build_project', required=True)

    _sql_constraints = [('project_business_category_name_unique', 'unique(name,type)', _('name must be unique in type!'))]


class ProjectPlan(models.Model):
    _name = 'cisp.project.project.plan'
    _inherit = 'cisp.project.project.plan.abstract'
    _description = 'Cisp Project Plan'

    project = fields.Many2one('cisp.project.project', 'Project', ondelete='cascade')


class ProjectBudget(models.Model):
    _name = 'cisp.project.project.budget'
    _inherit = 'cisp.project.project.budget.abstract'
    _description = 'Cisp Project Budget'

    project = fields.Many2one('cisp.project.project', 'Project', ondelete='cascade')


class ProjectMember(models.Model):
    _name = 'cisp.project.project.member'
    _inherit = 'cisp.project.project.member.abstract'
    _description = 'Cisp Project Member'

    project = fields.Many2one('cisp.project.project', 'Project', ondelete='cascade')

