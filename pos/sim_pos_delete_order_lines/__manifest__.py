# -*- coding: utf-8 -*-
{
    'name': "Remove Order Line In POS",
    'version': '19.0.0.0.0',
    'category': 'Point of Sale',
    'summary': """Remove Individual Order lines In Point Of Sale. 
    Remove individual order lines with one click,Clear all order lines instantly,X button for fast line removal,User-friendly POS interface,Works seamlessly with Odoo POS,Improves cashier speed & accuracy,Ideal for retail & restaurant POS,Faster checkout process,Reduced cashier errors,Better POS order control,Improved customer experience,No disruption to existing POS workflow,Retail stores,Supermarkets,Restaurants & cafés,POS cashiers,Businesses using Odoo POS
    """,
    'description': """Remove Individual Order lines In Point Of Sale. 
    Remove individual order lines with one click,Clear all order lines instantly,X button for fast line removal,User-friendly POS interface,Works seamlessly with Odoo POS,Improves cashier speed & accuracy,Ideal for retail & restaurant POS,Faster checkout process,Reduced cashier errors,Better POS order control,Improved customer experience,No disruption to existing POS workflow,Retail stores,Supermarkets,Restaurants & cafés,POS cashiers,Businesses using Odoo POS
    """,
    'author': 'SimBeez IT Solutions LLP',
    'website': 'https://simbeez.com/',
    'license': 'OPL-1',

    'maintainer': 'SimBeez IT Solutions LLP',

    'depends': ['point_of_sale'],
    'assets': {
        'point_of_sale._assets_pos': [
            'sim_pos_delete_order_lines/static/src/css/button.css',
            'sim_pos_delete_order_lines/static/src/app/control_buttons/control_buttons.js',
            'sim_pos_delete_order_lines/static/src/app/control_buttons/control_buttons.xml',
            'sim_pos_delete_order_lines/static/src/app/screens/product_screen/product_screen.js',
            'sim_pos_delete_order_lines/static/src/app/screens/product_screen/product_screen.xml',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}
