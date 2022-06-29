from odoo import models, fields, api
from datetime import datetime

class factAuto(models.Model):
    _name = 'facturationauto'

    def create_facturation(self):
        list_client_par_dossier = {}
        list_client_tout_dossier = {}
        for rec in self.env['res.partner'].search([]):

            list_vente = {}

            for vente in rec.sale_order_ids:
                list_fleet = []
                for fleet in vente.sale_parc_ids:
                    if fleet.etat_serie == 'a_jour':
                        list_fleet.append(fleet)
                        fleet.etat_serie = 'n_ajour'
                if list_fleet != []:
                    list_vente[vente] = list_fleet


            if list_vente != {}:

                print('type', rec.type_facture)
                if rec.type_facture == 'par_dossier':
                    list_client_par_dossier[rec] = list_vente
                if rec.type_facture == 'tout_dossiers':
                    list_client_tout_dossier[rec] = list_vente

        print('par dossier',list_client_par_dossier)
        print('tout dossier', list_client_tout_dossier)

        #################### par dossier

        for i in list_client_par_dossier.items():
            purchase_id = False
            print(i[0].name)
            list_numero_dossier_par_dossier = []
            for j in i[1].items():
                if j[0].sale_dossier not in list_numero_dossier_par_dossier:
                    list_numero_dossier_par_dossier.append(j[0].sale_dossier)
                    sale_vals = {
                        'company_id': j[0].company_id.id,
                        'date_order': datetime.now(),
                        'partner_id': j[0].partner_id.id,
                        'partner_invoice_id': j[0].partner_invoice_id.id,
                        'partner_shipping_id': j[0].partner_shipping_id.id,
                        'picking_policy': j[0].picking_policy,
                        'pricelist_id': j[0].pricelist_id.id,
                        'warehouse_id': j[0].warehouse_id.id,
                        'state': 'sale',
                    }
                    purchase_id1 = self.env['sale.order'].sudo().create(sale_vals)
                    purchase_id = purchase_id1.id
                    print(purchase_id)
                    res = {
                        'order_id': purchase_id,
                        'display_type': 'line_section',
                        'name': "Dossier N°"+str(j[0].sale_dossier),
                    }
                    self.env['sale.order.line'].sudo().create(res)

                qte_by_dossier_forfait_coleur = 0
                qte_by_dossier_forfait_noir = 0
                qte_by_dossier_sup_coleur = 0
                qte_by_dossier_sup_noir = 0
                qte_by_dossier_abonnement_service = 0
                qte_by_dossier_autre = 0


                for k in j[1]:
                    ######### create devis fleet liste
                    res = {
                        'fleet_id': k.id,
                        'devis_id': purchase_id,
                    }
                    self.env['listboncommandefleet'].sudo().create(res)
                    ################### fin

                    qte_by_dossier_forfait_coleur +=  k.fleet_forfait_couleur
                    qte_by_dossier_forfait_noir += k.fleet_forfait_nb
                    qte_by_dossier_abonnement_service += k.fleet_abonnement_service
                    qte_by_dossier_autre += k.fleet_autre
                    qte_by_dossier_sup_coleur += k.couleur_supp
                    qte_by_dossier_sup_noir += k.noir_supp

                print(j[0].sale_dossier)
                print('qtecoleur',qte_by_dossier_forfait_coleur)
                print('qtecoleur sup', qte_by_dossier_sup_coleur)
                print('qtenoir', qte_by_dossier_forfait_noir)
                print('qtenoir sup', qte_by_dossier_sup_noir)
                print('autre', qte_by_dossier_autre)
                print('abonnement', qte_by_dossier_abonnement_service)
                print('autre', qte_by_dossier_autre)

                if purchase_id:
                     if j[0].sale_forfait_signe_col:
                        res = {
                            'order_id': purchase_id,
                            'product_id': j[0].cout_copie_coleurs.id,
                            'name': j[0].cout_copie_coleurs.name,
                            'price_unit': j[0].sale_cout_signe_col,
                            'product_uom_qty': j[0].sale_forfait_signe_col,
                        }
                        self.env['sale.order.line'].sudo().create(res)

                    if j[0].sale_forfait_signe_nb:
                        res = {
                            'order_id': purchase_id,
                            'product_id': j[0].cout_copie_noires.id,
                            'name': j[0].cout_copie_noires.name,
                            'price_unit': j[0].sale_cout_signe_nb,
                            'product_uom_qty':j[0].sale_forfait_signe_nb ,
                        }
                        self.env['sale.order.line'].sudo().create(res)

                    if qte_by_dossier_sup_coleur:
                        res = {
                            'order_id': purchase_id,
                            'product_id': j[0].cout_copie_coleurs_sup.id,
                            'name': j[0].cout_copie_coleurs_sup.name,
                            'price_unit': j[0].sale_cout_signe_col,
                            'product_uom_qty': qte_by_dossier_sup_coleur,
                        }
                        self.env['sale.order.line'].sudo().create(res)

                    if qte_by_dossier_sup_noir:
                        res = {
                            'order_id': purchase_id,
                            'product_id': j[0].cout_copie_noires_sup.id,
                            'name': j[0].cout_copie_noires_sup.name,
                            'price_unit': j[0].sale_cout_signe_nb,
                            'product_uom_qty': qte_by_dossier_sup_noir,
                        }
                        self.env['sale.order.line'].sudo().create(res)

                    if j[0].sale_abonnement_service:
                        res = {
                            'order_id': purchase_id,
                            'product_id': j[0].abonnements.id,
                            'name': j[0].abonnements.name,
                            'price_unit': j[0].sale_abonnement_service,
                            'product_uom_qty': '1',
                        }
                        self.env['sale.order.line'].sudo().create(res)

                    if j[0].sale_autre_frais:
                        res = {
                            'order_id': purchase_id,
                            'product_id': j[0].services.id,
                            'name': j[0].services.name,
                            'price_unit': j[0].sale_autre_frais,
                            'product_uom_qty': '1',
                        }
                        self.env['sale.order.line'].sudo().create(res)

        #################### tout dossier
        for i in list_client_tout_dossier.items():
            purchase_id = False
            print(i[0].name)
            list_numero_dossier_par_dossier = []
            for j in i[1].items():
                if j[0].sale_dossier not in list_numero_dossier_par_dossier:
                    list_numero_dossier_par_dossier.append(j[0].sale_dossier)
                    if len(list_numero_dossier_par_dossier) <=1:
                        sale_vals = {
                            'company_id': j[0].company_id.id,
                            'date_order': datetime.now(),
                            'partner_id': j[0].partner_id.id,
                            'partner_invoice_id': j[0].partner_invoice_id.id,
                            'partner_shipping_id': j[0].partner_shipping_id.id,
                            'picking_policy': j[0].picking_policy,
                            'pricelist_id': j[0].pricelist_id.id,
                            'warehouse_id': j[0].warehouse_id.id,
                            'state': 'sale',
                        }
                        purchase_id1 = self.env['sale.order'].sudo().create(sale_vals)
                        purchase_id = purchase_id1.id
                        print(purchase_id)


                qte_by_dossier_forfait_coleur = 0
                qte_by_dossier_forfait_noir = 0
                qte_by_dossier_sup_coleur = 0
                qte_by_dossier_sup_noir = 0
                qte_by_dossier_abonnement_service = 0
                qte_by_dossier_autre = 0


                for k in j[1]:
                    ######### create devis fleet liste
                    res = {
                        'fleet_id': k.id,
                        'devis_id': purchase_id,
                    }
                    id=self.env['listboncommandefleet'].sudo().create(res)




                    qte_by_dossier_forfait_coleur +=  k.fleet_forfait_couleur
                    qte_by_dossier_forfait_noir += k.fleet_forfait_nb
                    qte_by_dossier_abonnement_service += k.fleet_abonnement_service
                    qte_by_dossier_autre += k.fleet_autre
                    qte_by_dossier_sup_coleur += k.couleur_supp
                    qte_by_dossier_sup_noir += k.noir_supp

                print(j[0].sale_dossier)
                print('qtecoleur',qte_by_dossier_forfait_coleur)
                print('qtecoleur sup', qte_by_dossier_sup_coleur)
                print('qtenoir', qte_by_dossier_forfait_noir)
                print('qtenoir sup', qte_by_dossier_sup_noir)
                print('autre', qte_by_dossier_autre)
                print('abonnement', qte_by_dossier_abonnement_service)
                print('autre', qte_by_dossier_autre)

                res = {
                    'order_id': purchase_id,
                    'display_type': 'line_section',
                    'name': "Dossier N°" + str(j[0].sale_dossier),
                }
                self.env['sale.order.line'].sudo().create(res)


                if purchase_id:
                    if j[0].sale_forfait_signe_col:
                        res = {
                            'order_id': purchase_id,
                            'product_id': j[0].cout_copie_coleurs.id,
                            'name': j[0].cout_copie_coleurs.name,
                            'price_unit': j[0].sale_cout_signe_col,
                            'product_uom_qty': j[0].sale_forfait_signe_col,
                        }
                        self.env['sale.order.line'].sudo().create(res)

                    if j[0].sale_forfait_signe_nb:
                        res = {
                            'order_id': purchase_id,
                            'product_id': j[0].cout_copie_noires.id,
                            'name': j[0].cout_copie_noires.name,
                            'price_unit': j[0].sale_cout_signe_nb,
                            'product_uom_qty':j[0].sale_forfait_signe_nb ,
                        }
                        self.env['sale.order.line'].sudo().create(res)

                    if qte_by_dossier_sup_coleur:
                        res = {
                            'order_id': purchase_id,
                            'product_id': j[0].cout_copie_coleurs_sup.id,
                            'name': j[0].cout_copie_coleurs_sup.name,
                            'price_unit': j[0].sale_cout_signe_col,
                            'product_uom_qty': qte_by_dossier_sup_coleur,
                        }
                        self.env['sale.order.line'].sudo().create(res)

                    if qte_by_dossier_sup_noir:
                        res = {
                            'order_id': purchase_id,
                            'product_id': j[0].cout_copie_noires_sup.id,
                            'name': j[0].cout_copie_noires_sup.name,
                            'price_unit': j[0].sale_cout_signe_nb,
                            'product_uom_qty': qte_by_dossier_sup_noir,
                        }
                        self.env['sale.order.line'].sudo().create(res)

                    if j[0].sale_abonnement_service:
                        res = {
                            'order_id': purchase_id,
                            'product_id': j[0].abonnements.id,
                            'name': j[0].abonnements.name,
                            'price_unit': j[0].sale_abonnement_service,
                            'product_uom_qty': '1',
                        }
                        self.env['sale.order.line'].sudo().create(res)

                    if j[0].sale_autre_frais:
                        res = {
                            'order_id': purchase_id,
                            'product_id': j[0].services.id,
                            'name': j[0].services.name,
                            'price_unit': j[0].sale_autre_frais,
                            'product_uom_qty': '1',
                        }
                        self.env['sale.order.line'].sudo().create(res)





    ###################### creer facture pour chaque client



class SaleOrderHeritage(models.Model):
    _inherit = 'sale.order'
    cout_copie_noires = fields.Many2one('product.product', string="Copies noires",
                                        default=lambda self: self.env['product.product'].search([('id', '=', 66)]))
    cout_copie_coleurs = fields.Many2one('product.product', string="Copies couleurs",
                                         default=lambda self: self.env['product.product'].search([('id', '=', 67)]))
    cout_copie_noires_sup = fields.Many2one('product.product', string="Copies noires supplémentaires",
                                            default=lambda self: self.env['product.product'].search([('id', '=', 68)]))
    cout_copie_coleurs_sup = fields.Many2one('product.product', string="Copies couleurs supplémentaires",
                                             default=lambda self: self.env['product.product'].search([('id', '=', 69)]))
    services = fields.Many2one('product.product', string="Services",
                               default=lambda self: self.env['product.product'].search([('id', '=', 70)]))
    abonnements = fields.Many2one('product.product', string="Montant abonnement",
                                             default=lambda self: self.env['product.product'].search([('id', '=', 72)]))

    sale_commande_fleet_ids = fields.One2many('listboncommandefleet', inverse_name='devis_id', string="Matériels bon de commande")


class PartnerInherit(models.Model):
    _inherit = 'res.partner'
    type_facture = fields.Selection([('par_dossier', 'facture par dossier'),('tout_dossiers', 'facturer tout les dossiers')],default='par_dossier')

#add field periodicité
class FleetEtatINHERIT(models.Model):
    _inherit = 'fleet.vehicle'
    etat_serie = fields.Selection([('a_jour', 'à facturer'),('n_ajour', 'ne pas facturer')],default='n_ajour')


