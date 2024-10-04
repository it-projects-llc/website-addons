# ruff: noqa: E501
import re

from odoo import http
from odoo.http import request
from odoo.models import BaseModel

from odoo.addons.website_event.controllers.main import (
    UserError,
    WebsiteEventController,
    _,
    fields,
)


# fmt: off
def _process_attendees_form(self, event, form_details):
    """ Process data posted from the attendee details form.

    :param form_details: posted data from frontend registration form, like
        {'1-name': 'r', '1-email': 'r@r.com', '1-phone': '', '1-event_ticket_id': '1'}
    """
    allowed_fields = request.env['event.registration']._get_website_registration_allowed_fields()
    registration_fields = {key: v for key, v in request.env['event.registration']._fields.items() if key in allowed_fields}
    # change: added res.partner fields
    registration_fields.update({key: v for key, v in request.env['res.partner']._fields.items() if key in allowed_fields})
    for ticket_id in list(filter(lambda x: x is not None, [form_details[field] if 'event_ticket_id' in field else None for field in form_details.keys()])):
        if int(ticket_id) not in event.event_ticket_ids.ids and len(event.event_ticket_ids.ids) > 0:
            raise UserError(_("This ticket is not available for sale for this event"))
    registrations = {}
    global_values = {}
    for key, value in form_details.items():
        counter, attr_name = key.split('-', 1)
        field_name = attr_name.split('-')[0]
        if field_name not in registration_fields:
            continue
        elif isinstance(registration_fields[field_name], (fields.Many2one, fields.Integer)):
            value = int(value) or False  # 0 is considered as a void many2one aka False
        else:
            value = value

        if counter == '0':
            global_values[attr_name] = value
        else:
            registrations.setdefault(counter, dict())[attr_name] = value
    for key, value in global_values.items():
        for registration in registrations.values():
            registration[key] = value

    return list(registrations.values())
# fmt: on

WebsiteEventController._process_attendees_form = _process_attendees_form


class WebsiteEventControllerExtended(WebsiteEventController):
    @http.route()
    def registration_confirm(self, event, **post):
        """Check that threre are no email duplicates.
        There is a check on frontend, but that is easy to get around."""
        registrations = self._process_attendees_form(event, post)
        emails = [r.get("email", "").strip() for r in registrations]
        assert len(emails) == len(set(emails))
        res = super(WebsiteEventControllerExtended, self).registration_confirm(
            event, **post
        )
        if res.location:
            # If super redirect (to /shop/checkout)
            url = (
                event.sudo()
                .env["ir.config_parameter"]
                .get_param("website_event_sale.redirection")
                or res.location
            )
            return request.redirect(url)
        else:
            return res

    def _process_attendees_form(self, event, form_details):
        """Remove spaces in emails"""
        res = super(WebsiteEventControllerExtended, self)._process_attendees_form(
            event, form_details
        )
        for registration in res:
            if registration.get("email"):
                registration["email"] = registration.get("email").strip()
        return res

    @http.route(
        ["/website_event_attendee_fields/check_email"],
        type="json",
        auth="public",
        methods=["POST"],
        website=True,
    )
    def check_email(self, event_id, email):
        partner = (
            request.env["res.partner"].sudo().search([("email", "=", email)], limit=1)
        )
        if not partner:

            def remove_spaces(s):
                s = re.sub(r"^\s*", "", s)
                s = re.sub(r"\s*$", "", s)
                return s

            email = remove_spaces(email)
            partner = (
                request.env["res.partner"]
                .sudo()
                .search(
                    [
                        "|",
                        "|",
                        ("email", "=ilike", "% " + email),
                        ("email", "=ilike", "% " + email + " %"),
                        ("email", "=ilike", email + " %"),
                    ],
                    limit=1,
                )
            )
            if not partner:
                return {}
            partner_email = remove_spaces(partner.email)
            # It's a workaround in order to prevent duplicating partner accounts when buying a ticket
            partner.write({"email": partner_email})

        event = request.env["event.event"].sudo().browse(event_id)
        error_msg = event.check_partner_for_new_ticket(partner.id)
        if error_msg:
            return {"email_not_allowed": error_msg}

        known_fields = {}
        for f in event.attendee_field_ids:
            if f.field_name == "email":
                continue
            if getattr(partner, f.field_name):
                if partner != request.env.user.partner_id:
                    known_fields[f.field_name] = ""
                else:
                    value = partner[f.field_name]
                    if isinstance(value, BaseModel):
                        known_fields[f.field_name] = value.id or ""
                    else:
                        known_fields[f.field_name] = value

        return {"known_fields": known_fields}
