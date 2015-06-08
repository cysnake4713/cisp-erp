# coding=utf-8
__author__ = 'cysnake4713'
from openerp.report import report_sxw

from openerp import tools
from openerp.osv import osv, fields
from openerp.tools.translate import _


class ProjectCreateReport(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context):
        super(ProjectCreateReport, self).__init__(cr, uid, name, context)

class wrapped_report(osv.AbstractModel):
    _name = 'report.cisp_project_create.report_project_create'
    _inherit = 'report.abstract_report'
    _template = 'cisp_project_create.report_project_create'
    _wrapped_report_class = ProjectCreateReport