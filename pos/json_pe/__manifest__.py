# -*- coding: utf-8 -*-
{
    'name': 'Consulta DNI y RUC',
    'version': '19.0.1.0.0',
    'category': 'Localization/Peru',
    'summary': 'Integración con API de json.pe para consultar DNI y RUC peruanos',
    'description': """
        Módulo para consultar información de DNI y RUC peruanos mediante la API de json.pe
        
        Características:
        * Configuración de API TOKEN en Settings
        * Consulta de DNI desde el formulario de Partner
        * Consulta de RUC desde el formulario de Partner
        * Autocompletado de campos del partner con la información obtenida
        * Manejo de errores y mensajes informativos
    """,
    'author': 'Json.pe',
    'website': 'https://json.pe',
    'license': 'LGPL-3',
    'icon': 'static/description/icon.png',
    'images': [
        'static/description/cover.png',
    ],
    'depends': [
        'base',
        'contacts',
    ],
    'external_dependencies': {
        'python': ['requests'],
    },
    'data': [
        'security/ir.model.access.csv',
        'views/res_config_settings_views.xml',
        'views/res_partner_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
