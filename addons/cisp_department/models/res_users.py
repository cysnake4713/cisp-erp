__author__ = 'cysnake4713'
# coding=utf-8
from openerp import tools
from openerp import models, fields, api
from openerp.tools.translate import _


class TempDepartment(models.Model):
    _name = 'hr.department'
    _rec_name = 'name'

    name = fields.Char('Name', required=True)
    director = fields.Many2one('res.users', 'Director')
    second_director = fields.Many2one('res.users', 'Second Director')
    users = fields.One2many('res.users', 'department', 'Users')


class ResUsersInherit(models.Model):
    _inherit = 'res.users'

    department = fields.Many2one('hr.department', 'Department')