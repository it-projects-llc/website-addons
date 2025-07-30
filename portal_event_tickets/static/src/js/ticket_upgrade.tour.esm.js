/** @odoo-module **/

import {registry} from "@web/core/registry";

registry.category("web_tour.tours").add("portal_event_tickets.ticket_upgrade_tour", {
    test: true,
    url: "/my/tickets",
    steps: () => [
        {
            content: "Choose first ticket",
            trigger: "a.ticket-id",
        },
        {
            content: "Click on upgrade ticket",
            trigger: "a:contains('Upgrade / Change ticket')",
        },
        {
            content: "Confirm upgrade",
            trigger: "#changeTicketModal button[type=submit]",
        },
        {
            content: "Open the register modal",
            trigger: 'button:contains("Register")',
        },
        {
            content: "Select 1 unit of `VIP` ticket type",
            extra_trigger:
                '#wrap:not(:has(a[href*="/event"]:contains("Conference for Architects")))',
            trigger: "select:eq(0)",
            run: "text 1",
        },
    ],
});
