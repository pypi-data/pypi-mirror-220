# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Product Line Mixin - With Accounting",
    "version": "14.0.2.2.0",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "LGPL-3",
    "installable": True,
    "depends": [
        "account",
        "ssi_product_line_price_mixin",
        "ssi_product_usage_account_type",
    ],
    "data": [
        "menu.xml",
        "views/mixin_product_line_mixin_views.xml",
    ],
}
