__author__ = 'cysnake4713'

# coding=utf-8
from openerp import tools
from openerp import models, fields, api
from openerp.tools.translate import _


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
