odoo.define("portal_event_tickets.portal", function (require) {
    "use strict";

    var publicWidget = require("web.public.widget");

    publicWidget.registry.transferTicketWidget = publicWidget.Widget.extend({
        selector: "#transfer_ticket",

        start: function () {
            var def = this._super.apply(this, arguments);

            var event_name = this.$el.data("event-name");
            var $modal = $("#modal_attendees_registration");

            /* Show form inline */
            $modal.find("form").attr("action", "/my/tickets/transfer/receive");
            $modal.removeClass("modal fade");

            /* Remove Cancel button; update title */
            var $submit = $modal.find("[type=submit]");
            $submit.parent().empty().append($submit);
            $submit.text("Confirm");

            /* Remove Close button */
            $modal.find(".close").remove();

            /* Make email non-editable */
            $modal.find("[name=1-email]").attr("disabled", "1");

            /* Update title */
            $modal
                .find("h4.modal-title")
                .html("Receive the ticket for <b>" + event_name + "</b>");
            return def;
        },
    });
});
