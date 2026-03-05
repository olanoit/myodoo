# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResCompany(models.Model):
	_inherit = 'res.company'
	vat_search_api = fields.Selection([
        ('apiperu', 'APIPERU'),
        ('apimigo', 'Migo.pe'),
        ('jsonpe', 'JSON-PE')
    ], default="apiperu", string="API to Use", required=True)
	token = fields.Char('Token', default='')