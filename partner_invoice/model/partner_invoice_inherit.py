from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class PartnerInvoiceHerit(models.Model):
    _inherit = 'res.partner'

    pfr = fields.Monetary('PFR')
    code_service = fields.Char('Code service')
    augmentation_sav = fields.Float(string='Augmentation SAV')
    augmentation_sav_bool= fields.Boolean(string="Augmentation SAV")
    type_facture = fields.Selection([('par_dossier', 'facture par dossier'),('tout_dossiers', 'facturer tout les dossiers')],default='par_dossier')






