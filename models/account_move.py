# -*- coding: utf-8 -*-

from odoo import api, fields, models, Command, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError
from odoo.tools import float_compare, date_utils, email_split, email_re, html_escape, is_html_empty
from odoo.tools.misc import formatLang, format_date, get_lang

from datetime import date, timedelta
from collections import defaultdict
from contextlib import contextmanager
from itertools import zip_longest
from hashlib import sha256
from json import dumps

import ast
import json
import re
import warnings
import logging

class AccountMove(models.Model):
    _inherit = "account.move"

    def action_post(self):
        #inherit of the function from account.move to validate if the client exceeds the credit limit
        res = super(AccountMove, self).action_post()
        self.verificacion_credito()

    def verificacion_credito(self):
        if self.move_type == 'out_invoice':
            limite_credito = self.env['res.partner'].search([('id', '=', self.partner_id.id), ('credit_limit', '>', 0)])
            facturas = self.env['account.move'].search([('partner_id.id', '=', self.partner_id.id), ('amount_residual', '>', 0)])
            adeudado = 0
            for factura in facturas:
                logging.warning(factura.partner_id.name +' '+ factura.move_type +' ' + str(factura.partner_id.id) +'  amount_residual '+ str(factura.amount_residual))
                adeudado += factura.amount_residual
                if adeudado >= limite_credito.credit_limit:
                    raise UserError(_('El cliente '+factura.partner_id.name+ ' tiene un limite de credito de: Q'+str(limite_credito.credit_limit)))
                    # logging.warning('Su credito necesita ser menor a: ' + str(limite_credito.credit_limit))

        return True
