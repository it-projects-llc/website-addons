/** @odoo-module **/

import {registry} from "@web/core/registry";
import wsTourUtils from "@website_sale/js/tours/tour_utils";

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
            trigger: ".modal-dialog button[type=submit]",
        },
        {
            content: "Open the register modal",
            trigger: 'button:contains("Register")',
        },
        {
            content: "Select 1 unit of `VIP` ticket type",
            extra_trigger:
                '#wrap:not(:has(a[href*="/event"]:contains("Conference for Architects")))',
            trigger: "select:eq(1)",
            run: "text 1",
        },
        {
            content: "Click on `Order Now` button",
            extra_trigger: "select:eq(1):has(option:contains(1):propSelected)",
            trigger: '.btn-primary:contains("Register")',
        },
        {
            content: "Fill attendees details",
            trigger: 'form[id="attendee_registration"] .btn[type=submit]',
            run: function () {
                if ($("input[name*='1-email']").val()) {
                    // Website_event_attendee_fields automatically filled in data
                    return;
                }
                $("input[name*='1-name']").val("Att1");
                $("input[name*='1-phone']").val("111 111");
                $("input[name*='1-email']").val("att1@example.com");
            },
        },
        {
            content: "Validate attendees details",
            extra_trigger: "input[name*='1-name']",
            trigger: "button[type=submit]",
        },
        wsTourUtils.goToCart({quantity: 2}),
    ],
});
