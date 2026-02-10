{
    'name': 'sale_prevent_unavailable_qty',
    'version': '18.0.1.0.0',
    'summary': 'Prevent confirming sales orders with unavailable product quantities per warehouse',
    'description': """
        Sale Prevent Unavailable Quantity
        ================================
        This module prevents users from adding or confirming sales order lines
        when the requested quantity exceeds the available quantity
        in the selected warehouse.
        
        Features:
        - Computes available quantity per warehouse
        - Prevents saving or confirming sales orders with unavailable quantities
        - Supports multi-warehouse and multi-company environments
        - Compatible with Odoo 17 and Odoo 18
        """,
    'category': 'Sales',
    'author': 'Eng/Mohamed Ramah Elgarhy / Ritsol Technology',
    'website': 'https://ritsol.com',
    'license': 'LGPL-3',
    'depends': ['sale', 'account', 'stock', 'sale_stock'],
    'data': [
        'views/sale_order_line.xml',
    ],
    'installable': True,
    'application': False,
}
