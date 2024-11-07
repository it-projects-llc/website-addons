from datetime import datetime, timedelta

from odoo import fields
from odoo.tests.common import TransactionCase


class TestCase(TransactionCase):
    def setUp(self):
        super().setUp()
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
                "question_ids": [
                    (
                        0,
                        0,
                        {
                            "title": "Name",
                            "question_type": "name",
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "title": "Email",
                            "question_type": "email",
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "title": "Country",
                            "question_type": "partner_field",
                            "partner_field": self.env.ref(
                                "base.field_res_partner__country_id"
                            ).id,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "title": "Function",
                            "question_type": "partner_field",
                            "partner_field": self.env.ref(
                                "base.field_res_partner__function"
                            ).id,
                        },
                    ),
                ],
            }
        )
