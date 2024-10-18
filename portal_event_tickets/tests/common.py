from datetime import datetime, timedelta

from odoo import fields
from odoo.tests.common import HttpCase


class TourCase(HttpCase):
    def setUp(self):
        super().setUp()

        # create Event
        self.event = self.env["event.event"].create(
            {
                "name": "TestEvent",
                "create_partner": True,
                "date_begin": fields.Datetime.to_string(
                    datetime.today() + timedelta(days=1)
                ),
                "date_end": fields.Datetime.to_string(
                    datetime.today() + timedelta(days=15)
                ),
                "website_published": True,
            }
        )
        self.ticket_type_1 = self.env.ref("event.event_0_ticket_1").copy(
            {"event_id": self.event.id}
        )
        self.ticket_type_2 = self.env.ref("event.event_0_ticket_2").copy(
            {"event_id": self.event.id}
        )

        self.event.write(
            {
                "attendee_field_ids": [
                    (
                        6,
                        0,
                        [
                            self.env.ref(
                                "website_event_attendee_fields.attendee_field_name"
                            ).id,
                            self.env.ref(
                                "website_event_attendee_fields.attendee_field_email"
                            ).id,
                            self.env.ref(
                                "website_event_attendee_fields.attendee_field_phone"
                            ).id,
                            self.env.ref(
                                "website_event_attendee_fields.attendee_field_country_id"
                            ).id,
                            self.env.ref(
                                "website_event_attendee_fields.attendee_field_function"
                            ).id,
                        ],
                    )
                ]
            }
        )

        # create Portal User
        self.user_portal1 = self.env.ref("portal_event_tickets.user_portal1")

        sale_order, self.ticket1 = self._create_ticket(
            ticket_type=self.ticket_type_1,
            partner=self.user_portal1.partner_id,
            event=self.event,
        )
        sale_order.action_confirm()

        self.user_portal2 = self.env.ref("portal_event_tickets.user_portal2")

    def _create_ticket(self, ticket_type, partner, event):
        product = ticket_type.product_id

        # I create a sale order
        sale_order = self.env["sale.order"].create(
            {
                "partner_id": partner.id,
                "note": "Invoice after delivery",
            }
        )
        sale_order.onchange_partner_id()

        # In the sale order I add some sale order lines. i choose event product
        sale_order_line = self.env["sale.order.line"].create(
            {
                "product_id": product.id,
                # we set price_unit to 0
                # to confirm registration via registration.editor
                "price_unit": 0,
                "product_uom": self.env.ref("uom.product_uom_unit").id,
                "product_uom_qty": 1.0,
                "order_id": sale_order.id,
                "name": "sale order line",
                "event_id": event.id,
                "event_ticket_id": ticket_type.id,
            }
        )

        # In the event registration I add some attendee detail lines.
        # I choose event product
        register_person = self.env["registration.editor"].create(
            {
                "sale_order_id": sale_order.id,
                "event_registration_ids": [
                    (
                        0,
                        0,
                        {
                            "event_id": event.id,
                            "name": partner.name,
                            "email": partner.email,
                            "sale_order_line_id": sale_order_line.id,
                        },
                    )
                ],
            }
        )

        # I click apply to create attendees
        register_person.action_make_registration()

        return (
            sale_order,
            self.env["event.registration"].search(
                [("sale_order_id", "=", sale_order.id)]
            ),
        )
