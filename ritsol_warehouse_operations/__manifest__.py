{
    'name': 'Ritsol Warehouse Operations',
    'version': '18.0.1.0.0',
    'category': 'Inventory/Inventory',
    'summary': 'Advanced Warehouse Transfer Operations Management',
    'description': """
        Ritsol Warehouse Operations
        ============================
        - Multiple destination locations support
        - Real-time stock availability display
        - Transfer management between warehouses
        - Stock tracking and reporting
    """,
    'author': 'Ritsol Technical',
    'website': 'https://www.ritsol.com',
    'depends': ['stock', 'product'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/stock_picking_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}