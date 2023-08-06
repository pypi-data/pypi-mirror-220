# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class TestMasterDataDateDuration(models.Model):
    _name = "test.master_data_date_duration"
    _description = "Test Custom Information"
    _inherit = [
        "mixin.master_data",
        "mixin.date_duration",
    ]
    _date_start_required = True
    _date_end_required = False
    _date_start_readonly = True
    _date_end_readonly = False
    _date_end_string = "Date Finish"
