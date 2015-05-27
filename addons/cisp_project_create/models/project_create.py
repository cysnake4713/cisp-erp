# coding=utf-8
__author__ = 'cysnake4713'

from openerp import tools, exceptions
from openerp import models, fields, api
from openerp.tools.translate import _


class ProjectCreate(models.Model):
    _name = 'cisp.project.project.create'
    _inherit = ['odoosoft.workflow.abstract', 'cisp.project.project']
    _description = 'Cisp Project Create'
    _order = 'id desc'

    state = fields.Selection([('draft', u'制作人'),
                              ('project_manager', u'项目经理审批'),
                              ('department_manager', u'部门领导审批'),
                              ('project_admin', u'项目管理员审批'),
                              ('project_chief', u'项目管理部负责人审批'),
                              ('finance', u'财务部审批'),
                              ('vice_chief', u'分管领导审批'),
                              ('chief', u'主任审批'),
                              ('finish', u'结束'),
                              ], 'State', default='draft', copy=False)
    # 项目进度计划
    plans = fields.One2many('cisp.project.project.create.plan', 'project_create', 'Plans', required=True)
    # 项目预算
    budgets = fields.One2many('cisp.project.project.create.budget', 'project_create', 'Budgets')
    # 预算合计
    budgets_sum = fields.Float('Budget Sum(yuan)', compute='_compute_values', readonly=True)
    # 项目组成员
    members_role = fields.One2many('cisp.project.project.create.member', 'project_create', 'Members Role', required=True)

    members = fields.Many2many('res.users', 'project_create_res_user_rel', 'create_id', 'user_id', 'Project Members', readonly=True,
                               compute='_compute_values')

    partners = fields.Many2many('res.partner', 'cisp_project_create_partner_rel', 'create_id', 'partner_id', 'Partners')

    # signature
    draft_user = fields.Many2one('res.users', 'Draft User', copy=False)
    draft_datetime = fields.Datetime('Draft Datetime', copy=False)
    project_manager_user = fields.Many2one('res.users', 'Project Manager User', copy=False)
    project_manager_datetime = fields.Datetime('Project Manager Datetime', copy=False)
    department_manager_user = fields.Many2one('res.users', 'Department Manager User', copy=False)
    department_manager_datetime = fields.Datetime('Department Manager Datetime', copy=False)
    project_admin_user = fields.Many2one('res.users', 'Project Admin User', copy=False)
    project_admin_datetime = fields.Datetime('Project Admin Datetime', copy=False)
    project_chief_user = fields.Many2one('res.users', 'Project Chief User', copy=False)
    project_chief_datetime = fields.Datetime('Project Chief Datetime', copy=False)
    finance_user = fields.Many2one('res.users', 'Finance User', copy=False)
    finance_datetime = fields.Datetime('Finance Datetime', copy=False)
    vice_chief_user = fields.Many2one('res.users', 'Vice Chief User', copy=False)
    vice_chief_datetime = fields.Datetime('Vice Chief Datetime', copy=False)
    chief_user = fields.Many2one('res.users', 'Chief User', copy=False)
    chief_datetime = fields.Datetime('Chief Datetime', copy=False)
    # 分管领导
    department_chief = fields.Many2one('res.users', 'Department Chief', related='department.chief', readonly=True)
    is_rejected = fields.Boolean('Is Published', default=False)

    _state_field_map = {
        'draft': True,
        'project_manager': True,
        'department_manager': True,
        'project_admin': True,
        'project_chief': True,
        'finance': True,
        'vice_chief': True,
        'chief': True,
    }

    @api.multi
    @api.depends('name')
    def name_get(self):
        result = []
        for create in self:
            result.append((create.id, create.name + u'--<<项目立项表单>>'))
        return result

    @api.one
    @api.constrains('members_role', 'plans')
    def _compute_constrains(self):
        if len(self.members_role) == 0 or len(self.plans) == 0:
            raise exceptions.Warning(_('Project Members or Plans must have at least one record!'))

    @api.onchange('members_role')
    def _onchange_member_roles(self):
        self.members = [r.user.id for r in self.members_role]

    @api.multi
    def button_department_apply(self):
        department_manager = self.env['res.users'].sudo().search(
            [('department', '=', self.department.id), ('groups_id', '=', self.env.ref('cisp_project_create.group_department_manager').id)])
        self.with_context(message_users=[u.id for u in department_manager]).common_apply()

    @api.multi
    def button_reject(self):
        clear_fields = {}
        for s_field in self._state_field_map.keys():
            clear_fields.update({
                s_field + '_user': False,
                s_field + '_datetime': False,
            })
        self.write(clear_fields)
        self.is_rejected = True
        self.common_reject()

    @api.multi
    def button_create_project(self):
        # build values
        values = self.pool['cisp.project.project.create'].copy_data(self.env.cr, 1, self.ids[0], context=dict(self.env.context))
        # build many type field
        values.pop('state')
        # plans
        values['plans'] = [(0, 0, self.pool['cisp.project.project.create.plan'].copy_data(self.env.cr, 1, obj.id, context=dict(self.env.context))) for
                           obj in self.plans]
        # members_role
        values['members_role'] = [
            (0, 0, self.pool['cisp.project.project.create.member'].copy_data(self.env.cr, 1, obj.id, context=dict(self.env.context))) for
            obj in self.members_role]
        # budgets
        values['budgets'] = [
            (0, 0, self.pool['cisp.project.project.create.budget'].copy_data(self.env.cr, 1, obj.id, context=dict(self.env.context))) for
            obj in self.budgets]
        # create project
        values['create_project'] = self.ids[0]
        self.env['cisp.project.project'].sudo().create(values)
        self.common_apply()


class ProjectCreatePlan(models.Model):
    _name = 'cisp.project.project.create.plan'
    _inherit = 'cisp.project.project.plan.abstract'
    _description = 'Cisp Project Create Plan'

    project_create = fields.Many2one('cisp.project.project.create', 'Project Create', ondelete='cascade')


class ProjectCreateBudget(models.Model):
    _name = 'cisp.project.project.create.budget'
    _inherit = 'cisp.project.project.budget.abstract'
    _description = 'Cisp Project Create Budget'

    project_create = fields.Many2one('cisp.project.project.create', 'Project Create', ondelete='cascade')


class ProjectCreateMember(models.Model):
    _name = 'cisp.project.project.create.member'
    _inherit = 'cisp.project.project.member.abstract'
    _description = 'Cisp Project Create Member'

    project_create = fields.Many2one('cisp.project.project.create', 'Project Create', ondelete='cascade')