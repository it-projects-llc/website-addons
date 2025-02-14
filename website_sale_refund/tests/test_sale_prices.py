from odoo.tests import tagged

from odoo.addons.sale.tests.common import SaleCommon


@tagged("post_install", "-at_install")
class TestSalePrices(SaleCommon):
    def test_update_prices(self):
        old_sale_order = self.sale_order
        old_order_line = old_sale_order.order_line.filtered("price_unit")[0]

        new_sale_order = self.env["sale.order"].create(
            {
                "partner_id": old_sale_order.partner_id.id,
            }
        )
        refund_qty = 1
        expected_refund_price = -old_order_line.price_unit * refund_qty
        refund_order_line = new_sale_order.add_refund_line(
            old_order_line, "Test refund order line", qty=refund_qty
        )

        self.assertEqual(refund_order_line.price_unit, expected_refund_price)
        new_sale_order._recompute_prices()
        self.assertEqual(refund_order_line.price_unit, expected_refund_price)
