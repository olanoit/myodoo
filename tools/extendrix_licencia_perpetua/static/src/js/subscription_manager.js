/** @odoo-module **/

import { registry } from "@web/core/registry";
import { session } from "@web/session";
import { deserializeDateTime } from "@web/core/l10n/dates";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";

const { DateTime } = luxon;
import { Component, xml, useState } from "@odoo/owl";

export class SubscriptionManager {
    constructor(env, { orm, notification }) {
        this.env = env;
        this.orm = orm;
        this.notification = notification;

        // Configuración perpetua
        this.expirationDate = DateTime.utc().plus({ years: 100 });
        this.expirationReason = "enterprise";
        this.hasInstalledApps = true;
        this.warningType = null;
        this.lastRequestStatus = null;
        this.isWarningHidden = true;
    }

    get formattedExpirationDate() {
        return _t("Licencia Válida");
    }

    get daysLeft() {
        return 36500; // 100 años
    }

    get unregistered() {
        return false;
    }

    hideWarning() {
        this.isWarningHidden = true;
    }

    async buy() {
        // No hacer nada
    }

    async submitCode(code) {
        this.lastRequestStatus = "success";
        return;
    }

    async checkStatus() {
        this.lastRequestStatus = "update";
    }

    async sendUnlinkEmail() {
        // No hacer nada
    }

    async renew() {
        // No hacer nada
    }

    async upsell() {
        // No hacer nada
    }
}

class ExpiredSubscriptionBlockUI extends Component {
    static props = {};
    static template = xml`<t/>`; // Vacío
    static components = {};
    setup() {
        this.subscription = useState(useService("enterprise_subscription"));
    }
}

export const enterpriseSubscriptionService = {
    name: "enterprise_subscription",
    dependencies: ["orm", "notification"],
    start(env, { orm, notification }) {
        registry
            .category("main_components")
            .add("expired_subscription_block_ui", { Component: ExpiredSubscriptionBlockUI });

        console.log("✅ Licencia Perpetua Activada");

        return new SubscriptionManager(env, { orm, notification });
    },
};

registry.category("services").add("enterprise_subscription", enterpriseSubscriptionService);