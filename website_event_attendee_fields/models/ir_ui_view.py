from odoo import models


class IrUiView(models.Model):
    _inherit = "ir.ui.view"

    def _render_template(self, template, values=None):
        if template == "website_event.registration_attendee_details":
            tickets = values["tickets"]
            event = values["event"]

            are_tickets_different = len(set(map(lambda x: x["id"], tickets))) > 1
            user = self.env.user
            partners = (
                self.sudo()
                .env["res.partner"]
                .search([("email_normalized", "=", user.email_normalized)])
            )

            if (
                are_tickets_different
                or user._is_public()
                or event.partners_are_participating(partners.ids)
            ):
                values["default_first_attendee"] = {}

            else:
                partner = self.env.user.partner_id
                for q in event.question_ids:
                    if q.question_type != "partner_field":
                        continue

                    values["default_first_attendee"][
                        q.partner_field_name
                    ] = q.get_value(partner)

        return super()._render_template(template, values)
