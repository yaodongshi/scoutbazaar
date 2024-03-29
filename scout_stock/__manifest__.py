# -*- coding: utf-8 -*-

{
    "name" : "Scout Stock",
    "summary": 'scout stock Website Page',
    "description":"""
        """,
    "version" : "12.0.0.7",
    "author"  : "Geminate Consultancy Services",
    "website" : "http://www.geminatecs.com",
    "depends" : ['scout_vendor','scout_customize','jt_express','delivery_ups','payment_paymaya','delivery_easypost'],
    'data': ['security/ir.model.access.csv',
             'data/res_config_demo.xml',
             'views/scout_stock.xml',
             'views/product_product_views.xml',
             'views/res_partner_NSO.xml',
             'views/sale_order_view.xml',
             'views/email_template.xml',
             'views/delivery_carrier_views.xml',
             'views/website_templates.xml',
             'views/scout_bazaar_menu.xml',
             'views/website_payment_templates.xml',
             'views/shipping_address_view.xml',
             'views/res_config_views.xml',
             ],
    'installable': True,
    'auto_install': False,
}
