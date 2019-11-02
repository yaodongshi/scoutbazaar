# -*- coding: utf-8 -*-
# Part of SnepTech. See LICENSE file for full copyright and licensing details.##
##################################################################################

from datetime import datetime
from odoo import http, tools, _
from odoo import api, models, fields, _
import logging
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, float_compare, float_round
from werkzeug.exceptions import Forbidden
from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.website_sale.controllers.main import TableCompute
from odoo.addons.website_sale.controllers.main import QueryURL
from odoo.addons.website_sale.controllers import main
from odoo.addons.website.controllers.main import Website
from odoo.addons.web_editor.controllers.main import Web_Editor
from odoo.addons.web.controllers.main import Session
from odoo.addons.web.controllers.main import Home
from odoo.http import route, request
from odoo.addons.mass_mailing.controllers.main import MassMailController
from odoo.addons.website_event.controllers.main import WebsiteEventController
from odoo.addons.website_sale_coupon.controllers.main import WebsiteSale as WebsiteSaleCoupon
from odoo.addons.website_helpdesk.controllers.main import WebsiteHelpdesk
from odoo.addons.website_form.controllers.main import WebsiteForm
from odoo.addons.website_sale_delivery.controllers.main import WebsiteSaleDelivery

from lxml import etree, html
import math
import os
import base64
import uuid
import werkzeug
import json
import requests


PPG = 20  # Products Per Page
PPR = 4   # Products Per Row


class WebsiteSaleCountrySelect(WebsiteSale):
    
    
    # Get ProductCountry======================================
    def get_stock_country(self,categ_id):
        catge_dup = categ_id
        if categ_id.parent_id:
            return self.get_stock_country(categ_id.parent_id)
        elif not categ_id.parent_id:
            c_id = request.env['res.country'].sudo().search([('name','=',categ_id.name.capitalize())],limit=1)
#             return categ_id.name
            if c_id:
                return c_id
            else:
                return False
        else:
            return False
    
    #Get Stock location======================================
    def get_storefront_location(self,categ_id):
        catge_dup = categ_id
        if categ_id.parent_id:
            return self.get_storefront_location(categ_id.parent_id)
        elif not categ_id.parent_id:
            if categ_id.name:
                ss_id = request.env['scout.stock'].sudo().search([('country_id.name','=',categ_id.name)],limit=1)
                if ss_id:
                    if ss_id.location_id:
                        return ss_id.location_id.id
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False
        
    #Set Location id on orderline and calculate delivery cost code===============================================================
    @http.route(['/shop/payment'], type='http', auth="public", website=True)
    def payment(self, **post):
        res = super(WebsiteSaleCountrySelect,self).payment(**post)
        order = request.website.sale_get_order()
        partner_shipping_id = order.partner_shipping_id
        if partner_shipping_id:
            for line in order.order_line:
                if line.product_id.public_categ_ids:
                    stock_country = self.get_stock_country(line.product_id.public_categ_ids)
                    if stock_country:
                        if stock_country == partner_shipping_id.country_id:
                            if partner_shipping_id.state_id:
                                ss_id = request.env['scout.stock'].sudo().search([('country_id','=',stock_country.id),('state_ids','in',partner_shipping_id.state_id.id)],limit=1)
                                if ss_id:
                                    if not line.product_id.type == 'service':
                                        line.location_id = ss_id.location_id
                                else:
                                    sco_id = request.env['scout.stock'].sudo().search([('country_id','=',stock_country.id)],limit=1)
                                    if sco_id:
                                        if not line.product_id.type == 'service':
                                            line.location_id = sco_id.location_id
                            else:
                                scou_id = request.env['scout.stock'].sudo().search([('country_id','=',stock_country.id)],limit=1)
                                if scou_id:
                                    if not line.product_id.type == 'service':
                                        line.location_id = scou_id.location_id
                        else:
                            sc_id = request.env['scout.stock'].sudo().search([('country_id','=',stock_country.id)],limit=1)
                            if sc_id:
                                if not line.product_id.type == 'service':
                                    line.location_id = sc_id.location_id
        order = request.website.sale_get_order()
        if order:
            order._check_order_line_carrier(order)
        return res
    
    #Send NSO Email code======================================
    @http.route(['/shop/confirmation'], type='http', auth="public", website=True)
    def payment_confirmation(self, **post):
        views = super(WebsiteSaleCountrySelect, self).payment_confirmation(**post)
        line_list = []
        sale_order_line_obj = request.env['sale.order.line'].sudo()
        sale_order_id = request.session.get('sale_last_order_id')
        if sale_order_id:
            order = request.env['sale.order'].sudo().browse(sale_order_id)
            for line in order.order_line:
                if not line.location_id.id  in line_list:
                    line_list.append(line.location_id.id)
            if line_list:
                ids = sale_order_line_obj.send_sale_order_email(order,line_list)
        
        return views
    
class MyWebsiteSaleDelivery(WebsiteSale):
    
    @http.route(['/shop/payment'], type='http', auth="public", website=True)
    def payment(self, **post):
        res = super(MyWebsiteSaleDelivery, self).payment(**post)
        order = request.website.sale_get_order()
        acquirers = res.qcontext.get('acquirers')
        paymaya_visible = True
        acquirers_new = []
        # Paymaya Filter Code================================
        for line in order.order_line:
            if line.location_id:
                if line.location_id.nso_location_id:
                    if line.location_id.nso_location_id.country_id:
                        if line.location_id.nso_location_id.country_id.code != 'PH':
                            paymaya_visible = False
        
        if not paymaya_visible:
            for acq_id in acquirers:
                if not acq_id.provider == 'paymaya':
                    acquirers_new.append(acq_id)
            res.qcontext.update({'acquirers':acquirers_new})
    
        return res
