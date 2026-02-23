{
    'name': 'POS No Negative Stock',
    'version': '18.0.1.0',
    'summary': 'Prevent selling products with negative stock in POS',
    'author': 'Your Name',
    'category': 'Point of Sale',
    'depends': [
        'point_of_sale',
        'stock',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_no_negative_stock/static/src/js/pos_check_stock.js',
        ],
    },
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
