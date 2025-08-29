/** @odoo-module **/

import {registry} from "@web/core/registry";

registry.category("web_tour.tours").add("ticket_transfer_receive", {
    test: true,
    url: "/my/registrations/transfer/receive",
    steps: () => [
        {
            content: "Fill attendees details",
            trigger: "input[type='email']",
            run: function () {
                // Fill:
                // * phone (optional)
                $("input[name^='1-phone']").val("111 111");
            },
        },
        {
            content: "Validate attendees details",
            trigger: 'button:contains("Confirm")',
        },
        {
            content: "We are redirected to /my/registrations page",
            trigger: ".breadcrumb-item:contains(Tickets)",
            run: function () {
                // It's needed to don't make a click on the link
            },
        },
    ],
});
