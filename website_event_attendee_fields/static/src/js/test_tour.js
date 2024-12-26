/** @odoo-module **/

import {registry} from "@web/core/registry";
registry
    .category("web_tour.tours")
    .add("website_event_attendee_fields_test_tour_base", {
        test: true,
        url: "/event",
        steps: () => [
            {
                content: "Go to the `Events` page",
                trigger: 'a[href*="/event"]:contains("Hockey Tournament"):first',
            },
            {
                content: "Click on Register modal tickets button",
                trigger: 'button:contains("Register")',
                run: "click",
            },
            {
                content: "Select 2 'Free' tickets to buy",
                trigger: "div.modal-body select.form-select",
                run: "text 2",
            },
            {
                content: "Click on `Register` button",
                extra_trigger: "select:eq(0):has(option:contains(2):propSelected)",
                trigger: '.btn-primary:contains("Register")',
            },
            {
                // To ensure, that other fields are editable
                content: "Empty email input field",
                trigger: "input[name^='1-email']",
                run: function () {
                    $("input[name^='1-email']").val("").trigger("change");
                },
            },
            {
                content: "Fill attendees details",
                extra_trigger: "input[name^='1-function']",
                trigger: "input[name^='1-name']",
                run: function () {
                    if ($("input[name^='2-email']").val()) {
                        console.log("error", "Only first attendee can be autofilled");
                    }
                    $("input[name^='1-name']").val("Att1");
                    $("input[name^='1-phone']").val("111 111");
                    $("input[name^='1-email']")
                        .val("att1@example.com")
                        .trigger("change");
                    $("select[name^='1-country_id']").val("1");
                    $("input[name^='1-function']").val("JOB1");

                    $("input[name^='2-name']").val("Att2");
                    $("input[name^='2-phone']").val("222 222");
                    $("input[name^='2-email']").val("Att2@example.com");
                    $("select[name^='2-country_id']").val("1");
                    $("input[name^='2-function']").val("JOB2");
                },
            },
            {
                content: "Validate attendees details",
                extra_trigger: "input[name^='1-name'], input[name^='2-name']",
                trigger: 'button:contains("Confirm")',
            },
            {
                content: "Dummy step to finish loadding of previous step",
                trigger:
                    "h3:contains(Registration confirmed!),a:contains(Return to Cart),h3:contains(Your Address),span:contains(Continue Shopping)",
                run: function () {
                    // It's needed to don't make a click on the link
                },
            },
        ],
    });
