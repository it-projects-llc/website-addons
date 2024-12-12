from odoo import models


class EventRegistration(models.Model):
    _inherit = "event.registration"

    def _update_attendee_partner_id(self, vals):
        vals = super()._update_attendee_partner_id(vals)
        if not vals.get("attendee_partner_id"):
            return vals

        if not vals.get("event_id"):
            return vals

        Partner = self.env["res.partner"].sudo()
        Users = self.env["res.users"].sudo()
        Events = self.env["event.event"].sudo()

        event = Events.browse(vals["event_id"])
        if not event.attendee_signup:
            return vals

        attendee_partner = Partner.browse(vals["attendee_partner_id"])
        if attendee_partner.user_ids:
            # already has user
            return vals

        login = attendee_partner.email
        if not login:
            return vals

        user = Users.search([("login", "=ilike", login)])
        if user:
            # already has user with given address
            return vals

        user = Users._signup_create_user(
            {"login": login, "partner_id": attendee_partner.id}
        )
        user.partner_id.signup_prepare()
        return vals
