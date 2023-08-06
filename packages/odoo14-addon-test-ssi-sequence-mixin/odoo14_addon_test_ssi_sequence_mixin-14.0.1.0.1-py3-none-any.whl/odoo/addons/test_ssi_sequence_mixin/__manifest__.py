# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Test Module - Sequence Policy Mixin",
    "version": "14.0.1.0.1",
    "category": "Administration",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "LGPL-3",
    "installable": True,
    "depends": [
        "mail",
        "ssi_sequence_mixin",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/test_sequence_view.xml",
    ],
}
