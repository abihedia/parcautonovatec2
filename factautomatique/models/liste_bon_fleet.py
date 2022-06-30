from odoo import models, fields, api
from datetime import datetime

class listbonfleet(models.Model):
    _name = 'listboncommandefleet'
    name = fields.Char(string='Bon de commande et matériels')
    fleet_id = fields.Many2one('fleet.vehicle', string='les numéros de série')
    devis_id = fields.Many2one('sale.order', string='Devis')
    
    comp_couleur_diff = fields.Integer(string="Nombre de pages couleur à facturer", compute="compute_couleur_diff")
    comp_noir_diff = fields.Integer(string="Nombre de pages noir à facturer",compute="compute_noir_diff")

    @api.depends('fleet_id')
    def compute_couleur_diff(self):
        for rec in self:
            rec.comp_couleur_diff = rec.fleet_id.comp_couleur_diff
            print(rec.comp_couleur_diff)

    @api.depends('fleet_id')
    def compute_noir_diff(self):
        for rec in self:
            rec.comp_couleur_diff = rec.fleet_id.comp_noir_diff
            print(rec.comp_couleur_diff)

