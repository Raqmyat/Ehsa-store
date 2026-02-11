{
    'name': 'Salla Operation Automation',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'Automate Salla Order Status, Invoicing, Returns, and Inventory Sync',
    'depends': ['sale', 'stock', 'account', 'odoo_multi_channel_sale'],
    'data': [
        'data/ir_cron.xml',
        'views/multi_channel_sale.xml'
    ],
    'installable': True,
    'application': False,
}