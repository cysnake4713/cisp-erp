# coding=utf-8
__author__ = 'cysnake4713'

from operator import itemgetter
from openerp import tools, exceptions
from openerp import models, fields, api
from openerp.tools.translate import _


class ProjectAbstract(models.AbstractModel):
    _name = 'cisp.project.project.abstract'
    _description = 'Cisp Project Abstract'

    name = fields.Char('Name', required=True)
    # 编号
    code = fields.Char('Code')
    # 项目分类
    type = fields.Selection([('build_project', u'能力建设项目'), ('market_project', u'市场建设项目'), ('government', u'政府项目')], 'Type',
                            default='build_project', required=True)

    # 合同号
    contract_code = fields.Char('Contract Code', required=True)
    # 承担单位
    undertake_unit = fields.Selection([('1', u'工业和信息化部软件与集成电路促进中心'), ('2', u'北京赛普信科技术有限公司'), ('3', u'中国电子工业科学技术交流中心')], 'Undertake Unit',
                                      required=True)
    # 业务负责人
    business_manager = fields.Many2one('res.users', 'Business Manager', required=True)
    # 项目开始时间
    date_start = fields.Date('Date Start', required=True)
    # 项目结束时间
    date_end = fields.Date('Date End', required=True)
    # 业务分类
    business_category = fields.Many2one('cisp.project.business.category', 'Business Category', required=True)
    # 项目类别
    category = fields.Selection([('a', u'A类自主'), ('b', u'B类外协')], 'Project Category', required=True)
    # 所属部门
    department = fields.Many2one('hr.department', 'Department', required=True)
    # 项目经理
    manager = fields.Many2one('res.users', 'Project Manager', required=True)
    # 项目预期(确认)收入 能力建设 市场有 收入 政府项目叫 项目总金额
    expected_income = fields.Float('Expected Income(yuan)', compute='_compute_values', inverse='_inverse_expected_income', required=True)
    expected_income_store = fields.Float('Expected Income Store(yuan)')
    # 项目立项人
    # create_uid = fields.Many2one('res.users', 'Project Creator')
    # 以下只有政府项目有
    # 中央财政资金
    central_government_funds = fields.Float('Central Government Funds(yuan)')
    # 地方财政资金
    local_government_funds = fields.Float('Local Government Funds(yuan)')
    # 单位自筹资金
    company_funds = fields.Float('Company Funds(yuan)')

    # 项目主管部门
    in_charge_department = fields.Char('In Charge Department')
    # 组织实施单位
    implementation_company = fields.Char('Implementation Company')
    # 财务项目号
    financial_project_code = fields.Char('Financial Code')

    partners = fields.Many2many('res.partner', 'cisp_project_partner_rel', 'project_id', 'partner_id', 'Partners')
    # 分管领导
    department_chief = fields.Many2one('res.users', 'Department Chief', related='department.chief', readonly=True)

    @api.multi
    @api.depends('type', 'central_government_funds', 'local_government_funds', 'company_funds', 'expected_income_store')
    def _compute_values(self):
        for create in self:
            if create.type == 'government':
                create.expected_income = create.central_government_funds + create.local_government_funds + create.company_funds
            else:
                create.expected_income = create.expected_income_store

    def _inverse_expected_income(self):
        if not self.type == 'government':
            self.expected_income_store = self.expected_income


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
    _order = 'weight desc'
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