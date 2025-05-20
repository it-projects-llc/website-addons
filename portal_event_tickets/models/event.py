from odoo import fields, models


class Event(models.Model):
    _inherit = "event.event"

    report_template_for_portal = fields.Many2one(
        "ir.actions.report",
        "Badge Template For Portal",
        domain="[('model', '=', 'event.registration')]",
    )

    ticket_transferring = fields.Boolean(
        "Enable Ticket transferring",
        help="Attendee can transfer ticket to another partner",
        default=True,
    )

    ticket_changing = fields.Boolean(
        "Enable Ticket Changing",
        help="Attendee can change ticket to new ticket or products",
        default=True,
    )
