{
    'name': 'POS Session Balance Status',
    'version': '1.0',
    'category': 'Point of Sale',
    'summary': 'Add a status field to POS sessions comparing theoretical vs ending balance.',
    'description': """
        Adds a "الحالة" (Status) field to POS sessions:
        - "متوازن" if Theoretical Closing Balance == Ending Balance
        - "غير متوازن" otherwise
    """,
    'author': 'Antigravity',
    'depends': ['point_of_sale'],
    'data': [
        'views/pos_session_views.xml',
    ],
    'installable': True,
    'license': 'LGPL-3',
}
