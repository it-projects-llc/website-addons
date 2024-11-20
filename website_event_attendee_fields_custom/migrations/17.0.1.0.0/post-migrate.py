def migrate(cr, installed_version):
    from odoo import SUPERUSER_ID, api

    env = api.Environment(cr, SUPERUSER_ID, {"lang": None})
    q_ref = {}

    cr.execute(
        """
select eaf.id, f.id, f.name, f.field_description, f.domain, eaf.is_required
from event_event_attendee_field eaf
left join ir_model_fields f on eaf.field_id = f.id
    """
    )
    for row in cr.fetchall():
        af_id = row[0]
        field_id = row[1]
        field_name = row[2]
        q_title = env["ir.model.fields"].browse(field_id).field_description

        cr.execute(
            "UPDATE ir_model_fields SET attendee_field = TRUE WHERE id = %s", [field_id]
        )
        if field_name in ("company_name", "phone", "email", "name"):
            q_ref[af_id] = {
                "question_type": field_name,
                "title": q_title,
            }
        else:
            if field_name in ("firstname", "lastname"):
                q_title += " as on ID"

            q_ref[af_id] = {
                "question_type": "partner_field",
                "partner_field": field_id,
                "partner_field_domain": row[4] or "[]",
                "title": q_title,
                "is_mandatory_answer": row[5] or False,
            }

    cr.execute(
        """
select event_event_id, array_agg(event_event_attendee_field_id)
from event_event_event_event_attendee_field_rel
group by event_event_id;
    """
    )
    for row in cr.fetchall():
        event_id = row[0]

        cr.execute("DELETE FROM event_question WHERE event_id = %s", [event_id])

        for af_id in sorted(row[1]):
            vals = {
                "event_id": event_id,
                "sequence": 10 * af_id,
            }
            q_vals = q_ref.get(af_id) or {}

            vals.update(q_vals)
            env["event.question"].create(vals)
