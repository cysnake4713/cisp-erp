# coding=utf-8
__author__ = 'cysnake4713'
from openerp import tools
from openerp import models, fields, api
from openerp.tools.translate import _


class Project(models.Model):
    _name = 'cisp.project.project'
    _inherit = 'odoosoft.workflow.abstract'
    _description = 'Cisp Project'

    name = fields.Char('Name')
    state = fields.Selection([('processing', 'Processing'),
                              ], 'State', default='processing')


class ProjectBusinessCategory(models.Model):
    _name = 'cisp.project.business.category'
    _description = 'Cisp Project Business Category'

    name = fields.Char('Name', required=True)
    type = fields.Selection([('build_project', u'能力建设项目'), ('market_project', u'市场建设项目'), ('government', u'政府项目')], 'Type',
                            default='build_project', required=True)

    _sql_constraints = [('project_business_category_name_unique', 'unique(name,type)', _('name must be unique in type!'))]


class ResUserInherit(models.Model):
    _inherit = 'res.users'

    @api.model
    def _get_group(self):
        result = super(ResUserInherit, self)._get_group()
        try:
            result.append(self.env.ref('cisp_project.group_user').id)
        except ValueError:
            # If these groups does not exists anymore
            pass
        return result

    _defaults = {
        'groups_id': _get_group,
    }