{
    'name': 'No Duplicate Products',
    'version': '1.0.0',
    'summary': 'Prevent duplicate products in Sales, Purchase and Internal Transfers',
    'description': """
This module prevents adding the same product more than once in:
- Sales Orders
- Purchase Orders
- Internal Transfers

It improves data accuracy and avoids duplicated product lines.
    """,
    'author': 'Eng/Mohamed Remah Elgarhy / Ritsol_technology',
    'category': 'Inventory',
    'license': 'LGPL-3',
    'depends': [
        'stock',
        'sale',
        'purchase',
    ],
    'data': [
        # no views needed
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
