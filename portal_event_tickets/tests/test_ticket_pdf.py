from odoo.tests.common import tagged

from .common import TourCase


@tagged("-at_install", "post_install")
class TicketPDF(TourCase):
    def test_ticket_access_pdf(self):
        self.assertEqual(
            self.ticket1.attendee_partner_id,
            self.user_portal1.partner_id,
            "Wrong attendee_partner_id value before the test",
        )

        login = self.user_portal1.login
        self.authenticate(login, login)

        r = self.url_open(f"/my/tickets/pdf/{self.ticket1.id}", allow_redirects=False)
        self.assertEqual(r.status_code, 200)
