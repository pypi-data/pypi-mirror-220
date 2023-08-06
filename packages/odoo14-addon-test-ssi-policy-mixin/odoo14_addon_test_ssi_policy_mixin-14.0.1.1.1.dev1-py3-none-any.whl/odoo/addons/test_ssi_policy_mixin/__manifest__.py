# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Test Module: Policy Mixin",
    "version": "14.0.1.1.0",
    "category": "Administration",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "LGPL-3",
    "installable": True,
    "depends": [
        "mail",
        "ssi_policy_mixin",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/policy_template_data.xml",
        "views/test_policy_type_view.xml",
        "views/test_policy_view.xml",
    ],
}
