from odoo import _, api, fields, models


class Event(models.Model):
    _inherit = "event.event"

    partner_questions = fields.Many2many(
        "event.question", compute="_compute_partner_questions", store=False
    )

    @api.depends("question_ids.question_type")
    def _compute_partner_questions(self):
        for event in self:
            event.partner_questions = event.question_ids.filtered(
                lambda q: q.question_type == "partner_field"
            )

    def check_partner_for_new_ticket(self, partner_id):
        if self.partner_is_participating(partner_id):
            return _("This email address is already signed up for the event")
        return None

    def partner_is_participating(self, partner_id):
        self.ensure_one()
        registration = (
            self.env["event.registration"]
            .sudo()
            .search(
                [
                    ("event_id", "=", self.id),
                    "|",
                    ("attendee_partner_id", "=", partner_id),
                    "&",
                    ("attendee_partner_id", "=", False),
                    ("partner_id", "=", partner_id),
                    ("state", "=", "open"),
                ]
            )
        )

        SaleOrderLine = self.env["sale.order.line"].sudo()
        if "refund_source_line_id" in SaleOrderLine._fields:
            # special case, when using portal_event_tickets
            # User starts upgrading ticket
            # Ticket that is being upgraded must be excluded from search
            # That ticket is marked as refund in cart

            currently_refunding_order_lines = SaleOrderLine.search(
                [
                    (
                        "refund_source_line_id",
                        "in",
                        registration.sale_order_line_id.ids,
                    ),
                    ("state", "in", ("draft",)),
                ]
            ).refund_source_line_id

            registration = registration.filtered(
                lambda x: x.sale_order_line_id not in currently_refunding_order_lines
            )

        return registration
