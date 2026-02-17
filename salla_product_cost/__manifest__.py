# -*- coding: utf-8 -*-
{
    'name': 'Salla Product Cost Manager',
    'version': '18.0.1.0.0',
    'category': 'Sales',
    'summary': 'Add visible cost field that syncs with standard_price for Salla products',
    'description': """
Salla Product Cost Manager
===========================
This module adds a custom cost field (x_salla_cost) that is always visible and editable.
Any changes to this field automatically update the standard_price field.

Features:
---------
* Always visible cost field regardless of user permissions
* Auto-sync: x_salla_cost ↔ standard_price
* Works with Salla-imported products
* Works with manually created products
    """,
    'author': 'Estol Elehsaa',
    'website': '',
    'depends': ['product', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_template_views.xml',
        'views/product_product_views.xml',
        'wizard/fix_salla_product_cost_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
