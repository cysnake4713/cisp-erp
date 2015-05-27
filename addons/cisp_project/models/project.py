# coding=utf-8
__author__ = 'cysnake4713'
from openerp import tools
from openerp import models, fields, api
from openerp.tools.translate import _


class Project(models.Model):
    _name = 'cisp.project.project'
    _inherit = 'odoosoft.workflow.abstract'
    _description = 'Cisp Project'

    name = fields.Char('Name', required=True)
    state = fields.Selection([('processing', 'Processing'),
                              ], 'State', default='processing')

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
    # 项目进度计划
    plans = fields.One2many('cisp.project.project.plan', 'project', 'Plans', required=True)
    # 项目预算
    budgets = fields.One2many('cisp.project.project.budget', 'project', 'Budgets')
    # 预算合计
    budgets_sum = fields.Float('Budget Sum(yuan)', compute='_compute_values', readonly=True)
    # 项目组成员
    members_role = fields.One2many('cisp.project.project.member', 'project', 'Members Role', required=True)

    @api.one
    def _inverse_expected_income(self):
        if not self.type == 'government':
            self.expected_income_store = self.expected_income

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

