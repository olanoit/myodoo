# -*- coding: utf-8 -*-
{
    'name': 'POS Hide Odoo Branding(Screen & Receipt)',
    "summary": "Hide Odoo branding from POS Screen, Customer Display, and Receipts for a clean white-label POS experience.",
    "description": """
        This module removes all default Odoo branding elements from the Point of Sale (POS) interface,
        including the POS screen, POS receipts, and the Customer Display screen.
        
        It allows businesses to maintain a clean, professional, and fully white-label POS experience
        without modifying any core Odoo files.

        Key Features:
        ✔ Remove "Powered by Odoo" from POS Receipts
        ✔ Hide Odoo branding from POS Screen
        ✔ Hide Odoo branding from Customer Display Screen
        ✔ Lightweight and performance-friendly
        ✔ Does not override or modify core POS files
        ✔ Auto-applied after installation (no configuration required)

        """,
    "author": "CodeSphere Tech",
    "website": "https://www.codespheretech.in/",
    "category": "Point of Sale",
    "version": "19.0.1.0.0",
    "sequence": 0,
    "currency": "USD",
    "price": "0",
    "depends": ["point_of_sale", ],
    "data": [
    ],
    "assets": {
        'point_of_sale._assets_pos': [
            'cst_pos_hide_odoo_branding/static/src/xml/hide_odoo_screen_receipt.xml',
        ],
        'point_of_sale.customer_display_assets': [
            'cst_pos_hide_odoo_branding/static/src/scss/customer_display.scss',
        ],
    },
    "images": ["static/description/Banner.png"],
    "license": "LGPL-3",
    "installable": True,
    "application": False,
    "auto_install": False,
}
