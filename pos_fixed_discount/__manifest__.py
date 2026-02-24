{
    'name': 'POS Fixed Discount',
    'version': '1.0',
    'category': 'Point of Sale',
    'summary': 'Apply fixed amount discounts in POS',
    'description': """
        This module adds a button in the POS to apply a fixed amount discount 
        to the selected order line.
    """,
    'depends': ['point_of_sale'],
    'data': [],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_fixed_discount/static/src/app/screens/product_screen/control_buttons/control_buttons.xml',
            'pos_fixed_discount/static/src/app/screens/product_screen/control_buttons/control_buttons.js',
        ],
    },
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
