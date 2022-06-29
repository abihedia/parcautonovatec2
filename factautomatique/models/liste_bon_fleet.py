from odoo import models, fields, api
from datetime import datetime

class listbonfleet(models.Model):
    _name = 'listboncommandefleet'
    name = fields.Char(string='Bon de commande et matériels')
    fleet_id = fields.Many2one('fleet.vehicle', string='les numéros de série')
    devis_id = fields.Many2one('sale.order', string='Devis')

