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
                    ("partner_id", "=", partner_id),
                    ("state", "=", "open"),
                ]
            )
        )
        return registration
