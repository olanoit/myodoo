# -*- coding: utf-8 -*-

{
    'name': 'Hide Any Menu User Wise',
    'version': '19.0.1.0.0',
    'category': 'Extra Tools',
    'summary': 'This Module Helps To Hide any Menu items user wise.',
    'description': """This module provides functionality to hide or restrict menu 
    items on a per-user basis in Odoo.
    With this feature, administrators can manage which menus each user is allowed 
    to see. It ensures that users only have access to the relevant parts of the system,
     improving both security and usability.""",
    'author': 'Cybrosys Techno Solutions',
    'company': 'Cybrosys Techno Solutions',
    'maintainer': 'Cybrosys Techno Solutions',
    'website': "https://www.cybrosys.com",
    'depends': ['base'],
    'data': [
        'views/res_users_views.xml',
        'views/ir_ui_menu_views.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
