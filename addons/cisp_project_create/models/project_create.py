# coding=utf-8
__author__ = 'cysnake4713'

from operator import itemgetter
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
                              ], 'State', default='draft')
    # 名称
    expected_income = fields.Float('Expected Income(yuan)', compute='_compute_values', inverse='_inverse_expected_income', required=True)
    expected_income_store = fields.Float('Expected Income Store(yuan)')

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
    draft_user = fields.Many2one('res.users', 'Draft User')
    draft_datetime = fields.Datetime('Draft Datetime')
    project_manager_user = fields.Many2one('res.users', 'Project Manager User')
    project_manager_datetime = fields.Datetime('Project Manager Datetime')
    department_manager_user = fields.Many2one('res.users', 'Department Manager User')
    department_manager_datetime = fields.Datetime('Department Manager Datetime')
    project_admin_user = fields.Many2one('res.users', 'Project Admin User')
    project_admin_datetime = fields.Datetime('Project Admin Datetime')
    project_chief_user = fields.Many2one('res.users', 'Project Chief User')
    project_chief_datetime = fields.Datetime('Project Chief Datetime')
    finance_user = fields.Many2one('res.users', 'Finance User')
    finance_datetime = fields.Datetime('Finance Datetime')
    vice_chief_user = fields.Many2one('res.users', 'Vice Chief User')
    vice_chief_datetime = fields.Datetime('Vice Chief Datetime')
    chief_user = fields.Many2one('res.users', 'Chief User')
    chief_datetime = fields.Datetime('Chief Datetime')
    # 分管领导
    department_chief = fields.Many2one('res.users', 'Department Chief', related='department.chief', readonly=True)

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


    @api.one
    @api.constrains('members_role', 'plans')
    def _compute_constrains(self):
        if len(self.members_role) == 0 or len(self.plans) == 0:
            raise exceptions.Warning(_('Project Members or Plans must have at least one record!'))

    @api.onchange('members_role')
    def _onchange_member_roles(self):
        self.members = [r.user.id for r in self.members_role]

    @api.multi
    @api.depends('type', 'central_government_funds', 'local_government_funds', 'company_funds', 'expected_income_store', 'budgets', 'members_role')
    def _compute_values(self):
        for create in self:
            if create.type == 'government':
                create.expected_income = create.central_government_funds + create.local_government_funds + create.company_funds
            else:
                create.expected_income = create.expected_income_store
            create.budgets_sum = sum([b.money for b in create.budgets])
            create.members = [r.user.id for r in create.members_role]

    @api.one
    def _inverse_expected_income(self):
        if not self.type == 'government':
            self.expected_income_store = self.expected_income

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
        self.common_reject()


class ProjectCreatePlan(models.Model):
    _name = 'cisp.project.project.create.plan'
    _description = 'Cisp Project Create Plan'
    _order = 'date_start'
    _rec_name = 'stage'

    project_create = fields.Many2one('cisp.project.project.create', 'Project Create', ondelete='cascade')
    stage = fields.Char('Stage', required=True)
    date_start = fields.Date('Date Start', required=True)
    date_end = fields.Date('Date End', required=True)
    achievement = fields.Char('Achievement')
    manager = fields.Many2one('res.users', 'Manager', required=True)


class ProjectCreateBudget(models.Model):
    _name = 'cisp.project.project.create.budget'
    _description = 'Cisp Project Create Budget'
    _order = 'money desc'
    _rec_name = 'type'

    project_create = fields.Many2one('cisp.project.project.create', 'Project Create', ondelete='cascade')
    type = fields.Many2one('cisp.project.project.create.budget.type', 'Type', required=True)
    detail = fields.Char('Detail')
    money = fields.Float('Money(yuan)')
    department = fields.Many2one('hr.department', 'Pay Department', required=True)


class ProjectCreateMember(models.Model):
    _name = 'cisp.project.project.create.member'
    _description = 'Cisp Project Create Member'
    _order = 'weight'
    _rec_name = 'user'

    project_create = fields.Many2one('cisp.project.project.create', 'Project Create', ondelete='cascade')
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