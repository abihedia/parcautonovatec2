from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class PartnerInvoiceHerit(models.Model):
    _inherit = 'res.partner'

    pfr = fields.Monetary('PFR')
    code_service = fields.Char('Code service')
    augmentation_sav = fields.Float(string='Augmentation SAV')
    augmentation_sav_bool= fields.Boolean(string="Augmentation SAV")





