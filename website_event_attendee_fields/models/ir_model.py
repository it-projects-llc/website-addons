from odoo import fields, models


class IrModelFields(models.Model):
    _inherit = "ir.model.fields"

    attendee_field = fields.Boolean()

    def write(self, vals):
        if not self:
            return True

        if "attendee_field" in vals:
            attendee_field = vals.pop("attendee_field")
            self.env.cr.execute(
                "UPDATE ir_model_fields SET attendee_field = %s WHERE id in %s",
                [attendee_field, tuple(self.ids)],
            )

        return super().write(vals)
