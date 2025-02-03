odoo.define("website_event_attendee_fields.registration_form", [], function (require) {
    "use strict";
    const {jsonrpc} = require("@web/core/network/rpc_service");
    const {_t} = require("@web/core/l10n/translation");
    require("website_event.website_event");

    var rows = {};
    function get_row($row) {
        var counter = $row.attr("data-counter");
        var row = rows[counter];
        if (row) {
            return row;
        }
        var $modal = $row.parents(".modal");
        row = {
            counter: counter,
            $row: $row,
            $modal: $modal,
            $submit: $modal.find('button[type="submit"]'),
            get_email: function () {
                return $.trim(this.$row.find("input[type='email']").val());
            },
            show_msg: function (msg, color) {
                var $msg = $("<span/>").html(msg);
                if (color) {
                    $msg.css("color", color);
                }
                this.$row.find(".message").html("").append($msg);
            },
            block: function () {
                this.$row
                    .find("input,select")
                    .not("[type='email']")
                    .attr("disabled", 1);
                this.$row.addClass("blocked");
                this.$submit.attr("disabled", "1");
            },
            set_field_value: function (value, field) {
                return this.$row
                    .find("[name^=" + this.counter + "-" + field + "-]")
                    .val(value);
            },
            disable_known_field: function (value, field) {
                this.set_field_value(value, field).attr("disabled", 1);
            },
            reset: function () {
                // Remove message and restrictions
                this.$row.find("input,select").removeAttr("disabled");
                this.$row.find(".message").html("");
                this.$row.removeClass("blocked");
                if (!this.$modal.find(".row.blocked").length) {
                    this.$submit.removeAttr("disabled");
                }
            },
        };
        rows[counter] = row;
        return row;
    }

    function duplicate_email_check(row) {
        var email = row.get_email();
        return Object.values(rows).some((r) => {
            if (r.counter === row.counter) {
                // Don't compare with itself
                return false;
            }
            if (email !== r.get_email()) {
                // Emails are different
                return false;
            }
            var msg = _t("Sorry, but each attendee has to have unique email.");
            row.show_msg(msg);
            row.block();

            return true;
        });
    }

    function api_check_email(event_id, $row) {
        // Check form
        var row = get_row($row);
        var email = row.get_email();

        var has_duplicate = duplicate_email_check(row);

        if (!email) {
            row.reset();
            return $.when();
        }

        if (has_duplicate) {
            // Already have an error. No need to ask backend.
            return $.when();
        }

        // Check backend
        return jsonrpc("/website_event_attendee_fields/check_email", {
            event_id: event_id,
            email: email,
        }).then(function (data) {
            if (data.email_not_allowed) {
                row.show_msg(data.email_not_allowed, "red");
                row.block();
            } else if (data.known_fields && Object.keys(data.known_fields).length) {
                var msg = _t(
                    "This email address already has an account. Data will be taken from this account"
                );
                row.show_msg(msg);

                var do_not_disable_fields = data.do_not_disable_fields || {};
                for (const [field, value] of Object.entries(data.known_fields)) {
                    if (do_not_disable_fields[field]) {
                        row.set_field_value(value, field);
                    } else {
                        row.disable_known_field(value, field);
                    }
                }
            } else if (!duplicate_email_check(row)) {
                row.reset();
            }
        });
    }

    function onchange_email(input, event_id) {
        var $input = $(input);
        var $row = $input.parents(".modal-body");
        return api_check_email(event_id, $row);
    }
    function init() {
        rows = {};
    }

    odoo.registration_form_init = init;
    odoo.registration_form_onchange_email = onchange_email;
});
