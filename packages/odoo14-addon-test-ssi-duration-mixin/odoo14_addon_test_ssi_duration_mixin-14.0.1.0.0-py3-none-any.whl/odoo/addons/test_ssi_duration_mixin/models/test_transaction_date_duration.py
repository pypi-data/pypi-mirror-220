# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class TestTransactionDataDateDuration(models.Model):
    _name = "test.transaction_date_duration"
    _description = "Test Date Duration Mixin on Transaction Object"
    _inherit = [
        "mixin.transaction_done",
        "mixin.transaction_cancel",
        "mixin.date_duration",
    ]
    _date_start_required = True
    _date_end_required = False
    _date_start_readonly = True
    _date_end_readonly = True
    _date_end_string = "Date Finish"
    _date_start_states_list = ["draft"]
    _date_start_states_readonly = ["draft"]
    _date_end_states_list = ["draft"]
    _date_end_states_readonly = ["draft"]

    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("done", "Done"),
            ("cancel", "Cancelled"),
        ],
        default="draft",
        copy=False,
    )
