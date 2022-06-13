from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class PartnerInvoiceHerit(models.Model):
    _inherit = 'res.partner'

    pfr = fields.Monetary('PFR')
    code_service = fields.Char('Code service')
    augmentation_sav = fields.Float(string='Augmentation SAV')
    augmentation_sav_bool= fields.Boolean(string="Augmentation SAV")
    siret_customer = fields.Char('Siret')


    @api.constrains('siret_customer')
    def _check_phone_number(self):

        for rec in self:
            if rec.siret_customer and len(str(rec.siret_customer)) != 14 :
                raise ValidationError(_("Wrong value enter"))
            else:
                return False
        return {}

