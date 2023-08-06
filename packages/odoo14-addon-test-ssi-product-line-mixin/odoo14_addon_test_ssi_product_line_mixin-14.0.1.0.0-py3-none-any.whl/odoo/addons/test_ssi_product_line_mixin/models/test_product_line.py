# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class TestProductLine(models.Model):
    _name = "test.product_line"
    _description = "Test Product Line"
    _inherit = [
        "mixin.product_line",
    ]
