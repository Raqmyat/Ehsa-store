{
    'name': 'Multi Location Internal Transfer',
    'version': '18.0.1.0.0',
    'category': 'Inventory',
    'author': 'Eng/Mohamed Ramah Elgarhy--Ritsol Technical',
    'summary': 'Internal transfer to multiple destination locations',
    'depends': ['stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/wizard_view.xml',
        'views/menu.xml',
    ],
    'application': False,
    'installable': True,
}
