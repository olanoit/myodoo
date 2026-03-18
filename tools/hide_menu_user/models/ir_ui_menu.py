# -*- coding: utf-8 -*-

from odoo import fields, models


class IrUiMenu(models.Model):
    """
    Model to restrict the menu for specific users.
    """
    _inherit = 'ir.ui.menu'

    restrict_user_ids = fields.Many2many(
        'res.users', string="Restricted Users",
        help='Users restricted from accessing this menu.')

    def _filter_visible_menus(self):
        """
        Override to filter out menus restricted for current user.
        Applies only to the current user context.
        """
        menus = super()._filter_visible_menus()

        # Allow system admin to see everything
        if self.env.user.role == 'group_system':
            return menus
        return menus.filtered(
            lambda menu: self.env.user.id not in menu.restrict_user_ids.ids)
