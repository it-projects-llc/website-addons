from datetime import timedelta

from odoo.fields import Datetime
from odoo.tests.common import tagged

from odoo.addons.base.tests.common import HttpCaseWithUserPortal
from odoo.addons.website_event_sale.tests.common import TestWebsiteEventSaleCommon


@tagged("-at_install", "post_install")
class TestTicketUpgrade(TestWebsiteEventSaleCommon, HttpCaseWithUserPortal):
    def setUp(self):
        super().setUp()

        self.ticket_vip = self.env["event.event.ticket"].create(
            {
                "name": "VIP",
                "event_id": self.event_2.id,
                "product_id": self.env.ref("event_sale.product_product_event").id,
                "end_sale_datetime": (Datetime.today() + timedelta(90)).strftime(
                    "%Y-%m-%d"
                ),
                "price": 1500.0,
            }
        )

    def test_ticket_upgrade(self):
        q = self.env["sale.order"].create(
            {
                "company_id": self.env.company.id,
                "partner_id": self.partner_portal.id,
                "pricelist_id": self.pricelist.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.product_event.id,
                            "event_id": self.event_2.id,
                            "event_ticket_id": self.ticket_2.id,
                        },
                    )
                ],
            }
        )

        q.action_confirm()

        reg = q.order_line.registration_ids
        self.assertEqual(len(reg), 1, "Unexpected behavior")

        self.start_tour(
            "/my/tickets",
            "portal_event_tickets.ticket_upgrade_tour",
            login="portal",
            step_delay=500,
        )

        q = self.env["sale.order"].search([], order="id DESC", limit=1)
        q.action_confirm()

        new_reg = q.order_line.registration_ids
        self.assertEqual(len(new_reg), 1, "Unexpected behavior")
        self.assertEqual(reg.state, "cancel")
        self.assertEqual(new_reg.state, "open")
