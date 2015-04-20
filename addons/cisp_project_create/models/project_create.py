# coding=utf-8
__author__ = 'cysnake4713'
from openerp import tools
from openerp import models, fields, api
from openerp.tools.translate import _


class ProjectCreate(models.Model):
    _name = 'cisp.project.project.create'
    _inherit = 'odoosoft.workflow.abstract'
    _description = 'Cisp Project Create'
    _order = 'create_date desc'

    state = fields.Selection([('draft', u'制作人'),
                              ('project_manager', u'项目经理审批'),
                              ('department_manager', u'部门领导审批'),
                              ('project_admin', u'项目管理员审批'),
                              ('project_chief', u'项目管理负责人审批'),
                              ('finance', u'财务部审批'),
                              ('vice_chief', u'分管领导审批'),
                              ('chief', u'主任审批'),
                              ('finish', u'结束'),
                              ], 'State', default='draft')
    # 名称
    name = fields.Char('Name')
    # 编号
    code = fields.Char('Code')
    # 项目分类
    type = fields.Selection([('build_project', u'能力建设项目'), ('market_project', u'市场建设项目'), ('goverment', u'政府项目')], 'Type',
                            default='build_project')

    # 合同号
    contract_code = fields.Char('Contract Code')
    # 承担单位 能力建设项目 政府项目
    undertake_unit = fields.Selection([('1', u'工业和信息化部软件与集成电路促进中心'), ('2', u'北京赛普信科技术有限公司'), ('3', u'中国电子工业科学技术交流中心')], 'Undertake Unit')
    # TODO:可能和上面是一个 市场项目 -> 委托方名称

    # 业务负责人
    business_manager = fields.Many2one('res.users', 'Business Manager')
    # 项目开始时间
    date_start = fields.Date('Date Start')
    # 项目结束时间
    date_end = fields.Date('Date End')
    # 业务分类
    business_category = fields.Many2one('cisp.project.business.category', 'Business Category')
    # 项目类别
    category = fields.Selection([('a', u'A类自主'), ('b', u'B类外协')], 'Project Category')
    # 所属部门
    department = fields.Many2one('hr.department', 'Department')
    # 项目经理
    manager = fields.Many2one('res.users', 'Project Manager')
    # TODO:项目预期(确认)收入 能力建设 市场有 收入 政府项目叫 项目总金额
    expected_income = fields.Float('Expected Income')
    # 项目立项人
    create_user = fields.Many2one('res.users', 'Project Creator')
    # 以下只有政府项目有

    # 中央财政资金
    central_government_funds = fields.Float('Central Government Funds')
    # 地方财政资金
    local_government_funds = fields.Float('Local Government Funds')
    # 单位自筹资金
    company_funds = fields.Float('Company Funds')

    # 项目主管部门
    in_charge_department = fields.Char('In Charge Department')
    # 组织实施单位
    implementation_company = fields.Char('Implementation Company')
    # 财务项目号
    financial_project_code = fields.Char('Financial Code')

    # 项目进度计划
    plans = fields.One2many('cisp.project.project.create.plan', 'project_create', 'Plans')
    # 项目预算
    budgets = fields.One2many('cisp.project.project.create.budget', 'project_create', 'Budgets')
    # 项目组成员
    members = fields.One2many('cisp.project.project.create.member', 'project_create', 'Members')

    partners = fields.Many2many('res.partner', 'cisp_project_create_partner_rel', 'create_id', 'partner_id', 'Partners')


class ProjectCreatePlan(models.Model):
    _name = 'cisp.project.project.create.plan'
    _description = 'Cisp Project Create Plan'
    _order = 'sequence'
    _rec_name = 'stage'

    project_create = fields.Many2one('cisp.project.project.create', 'Project Create', ondelete='cascade')
    # TODO: 感觉没啥必要,如果不需要排序的话
    # sequence = fields.Integer('Sequence', default=1)
    stage = fields.Char('Stage')
    date_start = fields.Date('Date Start')
    date_end = fields.Date('Date End')
    achievement = fields.Char('Achievement')
    # TODO: many2one? many2many
    manager = fields.Many2many('res.users', 'cisp_project_create_plan_user_rel', 'plan_id', 'user_id', 'Manager')


class ProjectCreateBudget(models.Model):
    _name = 'cisp.project.project.create.budget'
    _description = 'Cisp Project Create Budget'
    _order = 'sequence'
    _rec_name = 'type'

    project_create = fields.Many2one('cisp.project.project.create', 'Project Create', ondelete='cascade')
    # sequence = fields.Integer('Sequence', default=1)
    type = fields.Many2one('cisp.project.project.create.budget.type', 'Type')
    detail = fields.Char('Detail')
    money = fields.Float('Money')
    department = fields.Many2one('hr.department', 'Pay Department')


class ProjectCreateMember(models.Model):
    _name = 'cisp.project.project.create.member'
    _description = 'Cisp Project Create Member'
    _order = 'sequence'
    _rec_name = 'name'

    project_create = fields.Many2one('cisp.project.project.create', 'Project Create', ondelete='cascade')
    # sequence = fields.Integer('Sequence', default=1)
    department = fields.Many2one('hr.department', 'Department')
    role = fields.Selection([('manager', u'项目经理'), ('member', u'项目成员'), ('chief', u'项目负责人')], 'Role')
    type = fields.Selection([('executive', u'执行'), ('business', u'业务')], 'Type')
    # TODO: many2one ? many2many?
    user = fields.Many2one('res.users', 'Member')
    content = fields.Char('Content')
    weight = fields.Float('Weight')


class NewModule(models.Model):
    _name = 'cisp.project.project.create.budget.type'
    _rec_name = 'name'
    _description = 'Cisp Project Create Budget Type'

    name = fields.Char('Name', required=True)

    _sql_constraints = [('project_create_budget_type_name_unique', 'unique(name)', _('name must be unique !'))]

