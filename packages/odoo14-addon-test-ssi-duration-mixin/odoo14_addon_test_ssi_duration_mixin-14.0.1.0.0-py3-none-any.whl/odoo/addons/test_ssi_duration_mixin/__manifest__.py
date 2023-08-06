# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Test Module: Duration Mixin",
    "version": "14.0.1.0.0",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "category": "Tools",
    "license": "LGPL-3",
    "installable": True,
    "depends": [
        "ssi_duration_mixin",
        "ssi_master_data_mixin",
        "ssi_transaction_done_mixin",
        "ssi_transaction_cancel_mixin",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/test_master_data_date_duration_views.xml",
        "views/test_transaction_date_duration_views.xml",
    ],
}
