# coding=utf-8
__author__ = 'cysnake4713'

from operator import itemgetter
from openerp import tools, exceptions
from openerp import models, fields, api
from openerp.tools.translate import _


class ProjectPlanAbstract(models.AbstractModel):
    _name = 'cisp.project.project.plan.abstract'
    _description = 'Cisp Project Plan Abstract'
    _order = 'date_start'
    _rec_name = 'stage'

    stage = fields.Char('Stage', required=True)
    date_start = fields.Date('Date Start', required=True)
    date_end = fields.Date('Date End', required=True)
    achievement = fields.Char('Achievement')
    manager = fields.Many2one('res.users', 'Manager', required=True)


class ProjectBudgetAbstract(models.AbstractModel):
    _name = 'cisp.project.project.budget.abstract'
    _description = 'Cisp Project Budget Abstract'
    _order = 'money desc'
    _rec_name = 'type'

    type = fields.Many2one('cisp.project.project.create.budget.type', 'Type', required=True)
    detail = fields.Char('Detail')
    money = fields.Float('Money(yuan)')
    department = fields.Many2one('hr.department', 'Pay Department', required=True)


class ProjectMemberAbstract(models.AbstractModel):
    _name = 'cisp.project.project.member.abstract'
    _description = 'Cisp Project Member Abstract'
    _order = 'weight'
    _rec_name = 'user'

    department = fields.Many2one('hr.department', 'Department', required=True)
    role = fields.Selection([('manager', u'项目经理'), ('member', u'项目成员'), ('chief', u'项目负责人')], 'Role', required=True)
    type = fields.Selection([('executive', u'执行'), ('business', u'业务')], 'Type', required=True)
    user = fields.Many2one('res.users', 'Member', required=True)
    content = fields.Char('Content')
    weight = fields.Float('Weight', required=True)


class ProjectCreateBudgetType(models.Model):
    _name = 'cisp.project.project.create.budget.type'
    _rec_name = 'display_name'
    _description = 'Cisp Project Create Budget Type'

    name = fields.Char('Name', required=True)
    display_name = fields.Char('Display Name', compute='_compute_name')
    parent_id = fields.Many2one('cisp.project.project.create.budget.type', 'Parent Type')
    is_show = fields.Boolean('Is Show In List', default=True)

    _sql_constraints = [('project_create_budget_type_name_unique', 'unique(name, parent_id)', _('name must be unique each parent!'))]

    @api.multi
    def _compute_name(self):
        for obj in self:
            if obj.parent_id:
                obj.display_name = (obj.parent_id.display_name or '') + '/' + obj.name
            else:
                obj.display_name = obj.name

    @api.constrains('parent_id')
    def check_cycle(self):
        level = 100
        ids = self.ids
        while len(ids):
            self.env.cr.execute("""\
            SELECT DISTINCT parent_id
            FROM cisp_project_project_create_budget_type
            WHERE id IN %s AND parent_id IS NOT NULL""", [tuple(ids), ])
            ids = map(itemgetter(0), self.env.cr.fetchall())
            if not level:
                raise exceptions.Warning(_('Error! You cannot create recursive Type.'))
            level -= 1