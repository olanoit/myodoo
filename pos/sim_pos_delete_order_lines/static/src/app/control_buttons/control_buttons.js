/** @odoo-module **/

import {ConfirmationDialog} from "@web/core/confirmation_dialog/confirmation_dialog";
import {
    SelectPartnerButton
} from "@point_of_sale/app/screens/product_screen/control_buttons/select_partner_button/select_partner_button";
import {patch} from "@web/core/utils/patch";
import {_t} from "@web/core/l10n/translation";
import {useService} from "@web/core/utils/hooks";


patch(SelectPartnerButton.prototype, {
    setup() {
        super.setup();
        this.dialog = useService("dialog");
        this.notification = useService("notification");
    },

    async onClearLines() {
        const order = this.pos.getOrder();
        const lines = order?.getOrderlines() || [];

        if (lines.length) {
            this.dialog.add(ConfirmationDialog, {
                title: _t("¿Órdenes claras?"),
                body: _t("¿Está seguro de que desea eliminar todos los artículos de su carrito?"),
                confirm: () => {
                    lines.forEach(line => order.removeOrderline(line));
                    this.notification.add(_t("Todas las líneas de pedido procesadas."), {type: "success"});
                },
                confirmLabel: _t("Borrar"),
                cancelLabel: _t("Cancelar"),
            });
        } else {
            this.notification.add(_t("Tu carrito ya está vacío."), {type: "warning"});
        }
    },
});
