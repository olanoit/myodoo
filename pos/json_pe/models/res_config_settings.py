# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    json_pe_api_token = fields.Char(
        string='API Token JSON.PE',
        config_parameter='json_pe.api_token',
        help='Token de autenticación para la API de json.pe. '
             'Crea tu cuenta y obtén tu token en https://app.json.pe',
        required=False,
    )
