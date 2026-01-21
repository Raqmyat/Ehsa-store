{
    'name': 'Internal Transfer Available Quantity',
    'version': '18.0.1.0.0',
    'category': 'Inventory',
    'summary': 'Show available quantity in source and destination for internal transfers',
    'description': """
This module shows:
- Available quantity in Source Location
- Available quantity in Destination Location
When creating Internal Transfers.
""",
    'author': 'Your Company',
    'depends': ['stock','sale','purchase'],
    'data': [
        'views/stock_move_line_view.xml',
    ],
    'installable': True,
    'application': False,
}
