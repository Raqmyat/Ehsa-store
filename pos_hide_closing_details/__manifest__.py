{
    'name': 'POS Hide Closing Details',
    'version': '1.0',
    'category': 'Point of Sale',
    'summary': 'Hide expected amounts and differences in POS Closing Register popup.',
    'depends': ['point_of_sale'],
    'data': [
        'security/groups.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_hide_closing_details/static/src/app/**/*',
        ],
    },
    'installable': True,
    'license': 'LGPL-3',
}
