/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.TransferTicketWidget = publicWidget.Widget.extend({
    selector: "#transfer_ticket",

    async willStart() {
        await this._super(...arguments);

        const event_name = this.$el.data("event-name");
        const $modal = $("#modal_attendees_registration");

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
    },
});
