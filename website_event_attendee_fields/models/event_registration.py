import logging

from odoo import _, api, models

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

        partner_vals = self._prepare_partner(vals)

        if partner_exists:
            vals["attendee_partner_id"] = partner_exists.id
        else:
            vals["attendee_partner_id"] = Partner.sudo().create(partner_vals).id

        res = super(EventRegistration, self).create(vals)

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

    def _prepare_partner(self, vals):
        """method from partner_event module"""
        event = self.env["event.event"].browse(vals["event_id"])
        if not event.attendee_field_ids:
            # attendee_field_ids is not configure
            # May happen in tests of other modules, which don't suppose that this module is installed.  # noqa: E501
            # Just return super values.
            return super(EventRegistration, self)._prepare_partner(vals)

        # copy partner fields to return and removes non-registration fields from vals
        res = {}
        partner_fields = self.env["res.partner"]._fields
        _logger.debug("registration vals before removing: %s", vals)
        for field in event.attendee_field_ids:
            fn = field.field_name
            if field.field_model == "res.partner" or fn in partner_fields:
                # partner fields
                value = vals.get(field.field_name)
                if value:
                    # Don't pass empty value, because it removes previous value.
                    # E.g. when partner with email is specified and known fields are not filled at the form  # noqa: E501
                    res[fn] = value

            if fn not in self._fields:
                # non-registration fields
                if fn in vals:
                    del vals[fn]

        _logger.debug("registration vals after removing: %s", vals)
        _logger.debug("partner values: %s", res)
        return res

    def _get_website_registration_allowed_fields(self):
        res = super(EventRegistration, self)._get_website_registration_allowed_fields()
        res.update(
            self.env["event.event.attendee_field"]
            .sudo()
            .search([])
            .mapped("field_name")
        )
        return res
