import logging

from odoo.addons.website.tools import MockRequest

from ..controllers.main import WebsiteEventControllerExtended
from . import common

_logger = logging.getLogger(__name__)


class TestBackend(common.TestCase):
    def test_question_select_options(self):
        country_question = self.env["event.question"].search(
            [
                ("question_type", "=", "partner_field"),
                ("partner_field.name", "=", "country_id"),
            ],
            limit=1,
        )

        country_question.partner_field_domain = "[('code', '=', 'RU')]"

        self.assertEqual(1, len(country_question.get_select_options()))

        country_question.partner_field_domain = False
        self.assertTrue(1 < len(country_question.get_select_options()))

    def test_registration(self):
        country = self.env.ref("base.ru")
        email_value = "test@example.com"
        self.assertFalse(
            self.env["res.partner"].search([("email", "=", email_value)]),
            "Tests assumed, that partner with email %s doesn't exist" % email_value,
        )
        # emulate registration_confirm controller workflow
        registration_data = {
            "event_id": self.event.id,
            "name": "Test",
            "email": email_value,
            "country_id": country.id,
        }
        registration = self.env["event.registration"].create(registration_data)
        self.assertEqual(email_value, registration.email)
        self.assertEqual(email_value, registration.attendee_partner_id.email)
        self.assertEqual(country.id, registration.attendee_partner_id.country_id.id)

    def test_emails_duplicates(self):
        event = self.event
        name_question = event.question_ids.filtered(lambda q: q.question_type == "name")
        email_question = event.question_ids.filtered(
            lambda q: q.question_type == "email"
        )
        country_question = event.question_ids.filtered(
            lambda q: q.question_type == "partner_field"
            and q.partner_field_name == "country_id"
        )
        email = "email@example.com"
        post = {
            f"1-name-{name_question.id}": "Name1",
            f"1-email-{email_question.id}": email,
            f"1-country_id-{country_question.id}": 1,
            f"2-name-{name_question.id}": "Name2",
            f"2-email-{email_question.id}": email,
            f"2-country_id-{country_question.id}": 2,
        }
        with MockRequest(self.env), self.assertRaises(AssertionError):
            obj = WebsiteEventControllerExtended()
            obj.registration_confirm(event, **post)
