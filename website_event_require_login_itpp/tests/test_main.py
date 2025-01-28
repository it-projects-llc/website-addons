from datetime import timedelta

from odoo import fields
from odoo.tests import HttpCase

from odoo.addons.website_event.tests.common import TestEventOnlineCommon


class TestCorrectRendering(HttpCase, TestEventOnlineCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.event = cls.env["event.event"].create(
            {
                "name": "Design Fair New York",
                "date_begin": fields.Datetime.now() - timedelta(days=15),
                "date_end": fields.Datetime.now() + timedelta(days=15),
                "event_ticket_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "First Ticket",
                        },
                    ),
                ],
                "website_published": True,
            }
        )

    def test_cache_reset(self):
        self.authenticate(None, None)

        resp = self.url_open("/event/%i/register" % self.event.id)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"Sign in (Sign up) to proceed", resp.content)

        # now we enter as portal user, we can register here
        self.authenticate("portal_test", "portal_test")

        resp = self.url_open("/event/%i/register" % self.event.id)
        self.assertEqual(resp.status_code, 200)
        self.assertNotIn(b"Sign in (Sign up) to proceed", resp.content)
