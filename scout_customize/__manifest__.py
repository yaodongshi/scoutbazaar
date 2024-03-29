# -*- coding: utf-8 -*-
{
    "name" : "Scout Customize",
    "summary": 'Scout Customization -- Backend and Frontend',
    "description":"""
        """,
    "version" : "12.0.0.9",
    "author"  : "Geminate Consultancy Services",
    "website" : "http://www.geminatecs.com",
    "depends" : ['alan_customize'],
    'data': [
             'security/return_order_security.xml',
             'security/ir.model.access.csv',
             'data/ir_sequence_data.xml',
             'views/school_list.xml',
             'views/school_list_template.xml',
             'views/scout_program.xml',
             'views/troop_event_view.xml',
             'views/res_partner.xml',
             'views/assets.xml',
             'views/product_template_views.xml',
             'views/sale_order_views.xml',
             'views/website_templates.xml',
             'views/auth_signup_views.xml',
             'views/event_views.xml',
             'views/res_company_views.xml',
             'views/return_order_view.xml',
             'views/sale_order_report_view.xml',
             'views/vendor_account.xml',
             'views/res_config_setting.xml'
             ],
    'installable': True,
    'auto_install': False,
}
