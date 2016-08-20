# -*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp.tools.translate import _
from openerp.exceptions import Warning as UserError
import logging
_logger = logging.getLogger(__name__)
# python force_create_picking
# este codigo crea el picking para las siguientes condiciones
#	- picking_id vacio, y
# 	- estado facturado
# objeto que hay que heredar: pos.order
# funcion que hay que ejecutar
# point_of_sale.pos_order.create_picking()
# ver si va el pos_order o anda solo. creo que no hace falta
# porque hereda a ese objeto, y en ese objeto ya está la clase
'''
Clase que hereda el pos.order
@autor: Daniel Blanco daniel[at]blancomartin.cl
@version: 2016-08-19
'''
class pos_order(models.Model):
    _inherit="pos.order"
    _description="Force the picking to be created"

    '''
    Funcion para forzar la creacion del picking
    @autor: Daniel Blanco daniel[at]blancomartin.cl
    @version: 2016-08-19
    '''
    #"@api.model
    @api.multi
    def force_create_picking(self):
        for po in self:
            if po.picking_id.id == 0:
                _logger.info('Order: {}, picking DOES NOT EXIST'.format(po.name))
                if 1==1: #try:
                    _logger.info(
                        'antes de hacer')
                    po.create_picking()
                    _logger.info(
                        'despes de hacer')
                else: #except:
                    _logger.info('Order: {}, picking COULD NOT BEEN CREATED'.format(po.name))
            else:
                pass
                _logger.info('Order: {}, picking {} is OK'.format(po.name, po.picking_id.name))

    picking_id_id = fields.Integer('Picking ID',
                                   compute='_get_picking_id')
    state = fields.Selection(selection_add=[
        ('picking_exception', 'Picking Exception')])

    @api.multi
    @api.depends('picking_id')
    def _get_picking_id(self):
        for po in self:
            if all(t == 'service' for t in po.lines.mapped('product_id.type')):
                _logger.info('no hay productos almacenables y consumibles en la venta')
                po.picking_id_id = 99999999
            else:
                po.picking_id_id = po.picking_id.id
                if po.picking_id_id == 0:
                    po.state = 'picking_exception'