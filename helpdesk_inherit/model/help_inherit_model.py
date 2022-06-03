from odoo import models, fields, api


class HelpdeskModelHerit(models.Model):
    _inherit = 'helpdesk.ticket'

    products_id = fields.Many2one('product.product', string='Article')
    lots_id = fields.Many2one('stock.production.lot', string='Lot/numéro de série', help="Lot/Serial number", domain="[('product_id', '=', products_id)]")
    tracking = fields.Selection(related='products_id.tracking')
    product_serie_id = fields.Many2one('fleetserielarticle', string='Article Serie',domain="[('client_id', '=', partner_id)]")

