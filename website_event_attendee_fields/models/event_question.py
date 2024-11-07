import json

from odoo import fields, models
from odoo.tools.safe_eval import safe_eval

PARTNER_FIELD_DOMAIN = json.dumps(
    [
        ["model_id.model", "=", "res.partner"],
        ["attendee_field", "=", True],
    ]
).replace("true", "True")


class EventQuestion(models.Model):
    _inherit = "event.question"

    question_type = fields.Selection(
        selection_add=[("partner_field", "Contact's field")],
        ondelete={"partner_field": "set default"},
    )

    partner_field = fields.Many2one(
        "ir.model.fields",
        string="Contact field",
        domain=PARTNER_FIELD_DOMAIN,
    )

    partner_field_domain = fields.Char(default="[]", string="Contact field domain")
    partner_field_type = fields.Selection(
        related="partner_field.ttype", compute_sudo=True, store=False
    )
    partner_field_name = fields.Char(
        related="partner_field.name", compute_sudo=True, store=False
    )

    def get_select_options(self):
        self.ensure_one()
        domain = safe_eval(self.partner_field_domain or "[]")
        records = self.env[self.sudo().partner_field.relation].search(domain)
        res = [{"id": r.id, "name": r.display_name} for r in records]
        return res

    def get_value(self, partner, human_readable=False):
        self.ensure_one()
        v = getattr(partner, self.partner_field_name)
        if self.partner_field_type == "many2one":
            if human_readable:
                v = v.display_name
            else:
                v = v.id
        return v

    def _parse_partner_field_answer(self, answer):
        self.ensure_one()

        if self.partner_field_type == "many2one":
            model = self.partner_field.relation
            record_id = int(answer["value_text_box"])

            selected_value = self.env[model].sudo().browse(record_id)
            answer["value_text_box"] = selected_value.display_name
            return record_id
        else:
            return answer["value_text_box"]
