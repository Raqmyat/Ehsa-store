{
    'name': 'Custom Arabic POS Receipt (SA)',
    'version': '1.0',
    'category': 'Point of Sale',
    'summary': 'Customized Arabic POS receipt layout for Saudi Arabia',
    'description': 'This module modifies the POS receipt to match the Saudi Arabian simplified tax invoice layout.',
    'depends': ['point_of_sale'],
    'data': [],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_custom_receipt_sa/static/src/css/pos_receipt.css',
            'pos_custom_receipt_sa/static/src/xml/pos_receipt.xml',
        ],
    },
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
