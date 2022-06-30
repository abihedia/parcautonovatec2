from odoo import models, fields, api




class CompteurCouleurModel(models.Model):
    _name        = 'compteurcoleurmodel'
    _description = 'Compteur Couleur'
    compteur_Couleur = fields.Integer('Compteur Couleur')
    numero_serie     = fields.Char('N° serie')
    fleet_id         = fields.Many2one("fleet.vehicle", string='Matériels')
    @api.onchange("compteur_Couleur")
    def update_serie_after(self):
        for rec in self:
            rec.fleet_id.comp_couleur_after =rec.compteur_Couleur
        



class CompteurNoirModel(models.Model):
    _name        = 'compteurnoirmodel'
    _description = 'Compteur Noir'
    compteur_Noir = fields.Integer('Compteur NB')
    numero_serie  = fields.Char('N° serie')
    fleet_id      = fields.Many2one("fleet.vehicle", string='Matériels')
    @api.onchange("compteur_Noir")
    def update_serie_after(self):
        for rec in self:
            rec.fleet_id.comp_noir_after = rec.compteur_Noir
        



class FleetContINHERITFact(models.Model):
    _inherit = 'fleet.vehicle'
    ############facture
    comp_couleur_after  = fields.Integer(string="Compteur Couleur",default='0')
    comp_couleur_before = fields.Integer(string="Compteur Couleur",default='0')
    comp_noir_after     = fields.Integer(string="Compteur NB",default='0')
    comp_noir_before    = fields.Integer(string="Compteur NB",default='0')
    comp_noir_ids       = fields.One2many('compteurnoirmodel', inverse_name='fleet_id', string="Historique Compteur NB")
    comp_coleur_ids     = fields.One2many('compteurcoleurmodel', inverse_name='fleet_id', string="Historique Compteur Couleur")
    ######
    comp_couleur_diff = fields.Integer(string="Nombre de pages couleur à facturer")
    comp_noir_diff = fields.Integer(string="Nombre de pages noir à facturer")

    couleur_supp = fields.Integer(string="Quantité couleur supplémentaire à facturer")
    noir_supp = fields.Integer(string="Quantité noir supplémentaire à facturer")

    ########## smart button to compteur
    count_comp_noir = fields.Integer(string="Compteur NB", compute="compute_noir_count")
    def compute_noir_count(self):
        for rec in self:
            order_count = self.env['compteurnoirmodel'].search_count([('fleet_id', '=', rec.id)])
            rec.count_comp_noir = order_count
    def action_open_comp_noir(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Compteur NB',
            'res_model': 'compteurnoirmodel',
            'view_type': 'form',
            'domain': [('fleet_id', '=', self.id)],
            'view_mode': 'tree,form',
            'target': 'current',

        }
    ########## smart button to compteur
    count_comp_coleur = fields.Integer(string="Compteur Couleur", compute="compute_Couleur_count")

    def compute_Couleur_count(self):
        for rec in self:
            order_count = self.env['compteurcoleurmodel'].search_count([('fleet_id', '=', rec.id)])
            rec.count_comp_coleur = order_count

    def action_open_comp_coleur(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Compteur Coleur',
            'res_model': 'compteurcoleurmodel',
            'view_type': 'form',
            'domain': [('fleet_id', '=', self.id)],
            'view_mode': 'tree,form',
            'target': 'current',
        }
    def preview_art(self):
        if self.fleet_marque.id:
            ######### add odoo.sh
            result = self.env['product.product'].search(
                [('product_marque', '=', self.fleet_marque.id), ('product_Modele', '=', self.fleet_Modele.id)])
            if result:
                self.fleet_artic_id = result[0]
            #########
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'product.product',
            'target': 'current',
            'res_id': self.fleet_artic_id.id,
            'type': 'ir.actions.act_window',
        }
    def preview_devis(self):
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sale.order',
            'target': 'current',
            'res_id': self.fleet_devis_id.id,
            'type': 'ir.actions.act_window',
        }




class ReadingAnexcel(models.Model):
    _name = 'excelfile'
    _description = 'Reading an excel file'

    matricule  = fields.Char(string="Matricule")
    Nb_pages_C = fields.Char(string="Nb pages C")
    Nb_pages_N = fields.Char(string="Nb pages N")

    def create(self, vals):
        res = super(ReadingAnexcel, self).create(vals)
        res.delete_last_import()

        return res

    def delete_last_import(self):
        ids=self.env['excelfile'].search([("matricule", "=", self.matricule)])
        id = self.env['fleet.vehicle'].search([("fleet_serie", "=", self.matricule)])
        if id:
            id.comp_couleur_before = id.comp_couleur_after
            id.comp_couleur_after  = self.Nb_pages_C
            id.comp_noir_before = id.comp_noir_after
            id.comp_noir_after = self.Nb_pages_N
            id.comp_couleur_diff = id.comp_couleur_after - id.comp_couleur_before
            id.comp_noir_diff = id.comp_noir_after - id.comp_noir_before

            if id.comp_couleur_diff > id.fleet_forfait_couleur:
                id.couleur_supp = id.comp_couleur_diff - id.fleet_forfait_couleur
            else:
                id.couleur_supp =0
            if id.comp_noir_diff > id.fleet_forfait_nb:
                id.noir_supp = id.comp_noir_diff - id.fleet_forfait_nb
            else:
                id.noir_supp = 0
            print("quantité couleur à facturer",id.comp_couleur_diff)
            print("quantité noir à facturer", id.comp_noir_diff)
            id.etat_serie = 'a_jour'

            self.env['compteurnoirmodel'].create(
                {'compteur_Noir':self.Nb_pages_N,
                 'numero_serie': id.fleet_serie,
                 'fleet_id': id.id,

                 })
            self.env['compteurcoleurmodel'].create(
                {'compteur_Couleur': self.Nb_pages_C,
                 'numero_serie': id.fleet_serie,
                 'fleet_id': id.id,

                 })

        for rec in ids:
            if rec.id != self.id:
                rec.unlink()



