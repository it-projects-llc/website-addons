import logging

from odoo import _, api, models
from odoo.tools.mail import email_normalize

_logger = logging.getLogger(__name__)


class EventRegistration(models.Model):
    _inherit = "event.registration"

    @api.model
    def create(self, vals):
        partner_exists = False
        Partner = self.env["res.partner"]
        if vals.get("email"):
            email = vals.get("email").replace("%", "").replace("_", "\\_")
            partner_exists = Partner.search([("email", "=ilike", email)], limit=1)

        if "event_id" not in vals and "sale_order_line_id" in vals:
            so_line_vals = self._synchronize_so_line_values(
                self.env["sale.order.line"].browse(vals["sale_order_line_id"])
            )
            vals.update(so_line_vals)
            partner_exists = self.env["res.partner"].browse(vals["partner_id"])

        elif vals.get("attendee_partner_id"):
            partner_exists = self.env["res.partner"].browse(vals["attendee_partner_id"])

        event = self.env["event.event"].browse(vals["event_id"])
        general_question_ids = event.general_question_ids.ids

        partner_vals = self._prepare_partner_for_attendee_fields(vals)
        booked_by_partner_vals = self._parse_answers_for_partner_questions(
            vals, general_question_ids
        )

        if partner_exists:
            vals["attendee_partner_id"] = partner_exists.id
        else:
            vals["attendee_partner_id"] = Partner.sudo().create(partner_vals).id

        res = super().create(vals)

        if booked_by_partner_vals:
            res.partner_id.write(booked_by_partner_vals)

        if res.attendee_partner_id:
            # be sure, that name and phone in registration are ones from Attendee,
            # because built-in modules take them from Partner (buyer)
            # if ones are no presented
            res.name = res.attendee_partner_id.name
            res.phone = res.attendee_partner_id.phone

            if partner_exists:
                # Update attendee details, if user buys (register) ticket for himself
                # self.env.user is Administrator here, so just trust to partner_id field
                if res.attendee_partner_id == res.partner_id:
                    res.attendee_partner_id.sudo().write(partner_vals)

                elif len(partner_vals) > 1:
                    # If vals has more than email address
                    # Here we update other partners' date which email was given

                    attendee = res.attendee_partner_id

                    # Updating only values, that are not set before
                    partner_vals_to_set = {}
                    partner_vals_to_ignore = {}
                    for k, v in partner_vals.items():
                        if k == "email":
                            continue

                        if attendee[k]:
                            partner_vals_to_ignore[k] = v
                        else:
                            partner_vals_to_set[k] = v

                    if partner_vals_to_set:
                        attendee.sudo().write(partner_vals_to_set)

                    # Add a note about posible problems with updating fields
                    if partner_vals_to_ignore:
                        res.message_post(
                            author_id=self.env.ref("base.partner_root").id,
                            body=_(
                                "Attendee partner record are not updated for security reasons:<br/> %s "  # noqa: E501
                            )
                            % partner_vals_to_ignore,
                        )

        return res

    def _prepare_partner_for_attendee_fields(self, vals):
        res = {}
        for fname in ("name", "email", "phone"):
            res[fname] = vals.get(fname, False)

        event = self.env["event.event"].browse(vals["event_id"])
        for q in event.partner_questions:
            fname = q.partner_field_name
            res[fname] = vals.pop(fname, False)

        if res.get("email"):
            res["email"] = email_normalize(res["email"])

        # Don't pass empty value, because it removes previous value.
        # E.g. when partner with email is specified
        # And known fields are not filled at the form
        return {k: v for k, v in res.items() if v}

    @api.model
    def _parse_answers_for_partner_questions(self, reg_vals, question_ids):
        Question = self.env["event.question"]
        partner_vals = {}

        if not reg_vals.get("registration_answer_ids"):
            return partner_vals

        for tuple_answer in reg_vals["registration_answer_ids"]:
            if tuple_answer[0] != 0:
                continue

            answer = tuple_answer[2]

            qid = answer["question_id"]
            if qid not in question_ids:
                continue

            q = Question.browse(qid)
            if q.question_type != "partner_field":
                continue

            partner_field_name = q.partner_field_name
            partner_vals[partner_field_name] = q._parse_partner_field_answer(answer)

        return partner_vals
