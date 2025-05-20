from odoo import _, http
from odoo.http import request
from odoo.tools.mail import email_normalize

from odoo.addons.website_event.controllers.main import WebsiteEventController


class WebsiteEventControllerExtended(WebsiteEventController):
    @http.route()
    def registration_confirm(self, event, **post):
        """Check that threre are no email duplicates.
        There is a check on frontend, but that is easy to get around."""
        registrations = self._process_attendees_form(event, post)
        emails = [r.get("email", "").strip() for r in registrations]
        assert len(emails) == len(set(emails))
        return super().registration_confirm(event, **post)

    def _process_attendees_form(self, event, form_details):
        res = super()._process_attendees_form(event, form_details)

        specific_question_ids = event.specific_question_ids.ids

        for registration in res:
            if registration.get("email"):
                # Remove spaces in emails
                registration["email"] = registration.get("email").strip()

            partner_vals = request.env[
                "event.registration"
            ]._parse_answers_for_partner_questions(registration, specific_question_ids)

            if partner_vals:
                registration.update(partner_vals)

        return res

    @http.route(
        ["/website_event_attendee_fields/check_email"],
        type="json",
        auth="public",
        methods=["POST"],
        website=True,
    )
    def check_email(self, event_id, email):
        if not email:
            return {}

        Partners = request.env["res.partner"].sudo()
        email = email_normalize(email, True)

        if not email:
            return {"email_not_allowed": _("Invalid email")}

        current_user = request.env.user
        partner = Partners.search([("email_normalized", "=", email)])
        if not partner:
            return {}

        event = request.env["event.event"].sudo().browse(event_id)
        error_msg = event.check_partner_for_new_ticket(partner.ids)
        if error_msg:
            return {"email_not_allowed": error_msg}

        if current_user.partner_id in partner:
            partner = current_user.partner_id
        else:
            partner = partner.sorted("id", reverse=True)[0]

        known_fields = {}
        do_not_disable_fields = {}

        for q in event.specific_question_ids:
            if q.question_type == "email":
                continue

            fname = None
            value = None
            if q.question_type == "partner_field":
                fname = q.partner_field_name
                value = q.get_value(partner) or ""
            elif q.question_type in ["name", "phone", "company_name"]:
                fname = q.question_type
                value = getattr(partner, fname) or ""

            if fname and value:
                if partner == current_user.partner_id:
                    known_fields[fname] = value
                else:
                    known_fields[fname] = ""

        # Special case for firstname and lastname fields
        # If one of the is given and not the other,
        # then we consider that we name is not fully known
        # and we add mark not to disable them
        if partner == request.env.user.partner_id:
            firstname = known_fields.get("firstname")
            lastname = known_fields.get("lastname")

            if (lastname and not firstname) or (firstname and not lastname):
                do_not_disable_fields["firstname"] = True
                do_not_disable_fields["lastname"] = True

        return {
            "known_fields": known_fields,
            "do_not_disable_fields": do_not_disable_fields,
        }
