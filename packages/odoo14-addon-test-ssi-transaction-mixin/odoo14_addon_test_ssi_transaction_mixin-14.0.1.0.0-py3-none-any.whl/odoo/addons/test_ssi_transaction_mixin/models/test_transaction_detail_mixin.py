# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo import fields, models


class TestTransactionDetailMixin(models.Model):
    _name = "test.transaction_detail_mixin"
    _description = "Test Transaction Detail Mixin"
    _inherit = [
        "mixin.product_line_price",
    ]

    test_transaction_id = fields.Many2one(
        string="# Transaction",
        comodel_name="test.transaction_mixin",
        required=True,
        ondelete="cascade",
    )
