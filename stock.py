##############################################################################
#
# Copyright (c) 2010-2012 NaN Projectes de Programari Lliure, S.L.
#                         All Rights Reserved.
#                         http://www.NaN-tic.com
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################

from osv import osv, fields
import netsvc

class stock_production_lot( osv.osv ):
    _inherit = 'stock.production.lot'
    
    # stock.production.lot
    def get_available_states(self, cr, uid, context=None):
        """
        Adds the new state 'pending_sample' before 'pending_test' state.
        """
        states_list = super(stock_production_lot, self).get_available_states(cr,
                uid, context)
        pending_index = states_list.index(('pending_test', 'Waiting QC Test'))
        
        states_list.insert(pending_index, ('pending_sample', "Pending Sample"))
        return states_list
    
    
    # stock.production.lot
    def _calc_sample_library_ro(self, cr, uid, ids, fieldname, args, 
            context=None):
        res = {}
        for lot in self.browse(cr, uid, ids, context):
            res[lot.id] =  lot.requires_sample_library
        return res
    
    _columns = {
        'requires_sample_library': fields.boolean('Requires Sample Library', 
                readonly=True, states={'draft': [('readonly',False)]}),
        # Read Only version of previous field. Better solutions are wellcome
        'requires_sample_library_ro': fields.function(_calc_sample_library_ro, 
                method=True, type='boolean', string='Requires Sample Library', 
                store = {
                    'stock.production.lot': (
                            lambda self, cr, uid, ids, c=None: ids, 
                            ['requires_sample_library'], 10),
                }),
        
        'sample_library_code': fields.char('Sample Library Code',  size=64,
                readonly=True),
    }
    
    def _default_requires_sample_library(self, cr, uid, context=None):
        if context and context.get('product_id'):
            product = self.pool.get('product.product').browse(cr, uid, 
                    context['product_id'], context)
            return product.requires_sample_library
        return False
    
    _defaults = {
        'requires_sample_library': _default_requires_sample_library,
    }
    
    
    # stock.production.lot
    def onchange_product_id(self, cr, uid, ids, product_id, context):
        if not product_id:
            return {}
        
        product = self.pool.get('product.product').browse(cr, uid, product_id, 
                context)
        return {
            'value': {
                'requires_sample_library': product.requires_sample_library,
            }}
    
    
    # stock.production.lot
    def test_pending_sample(self, cr, uid, ids, context=None):
        """
        Returns True if any of Lot's requires Sample Library
        @param ids: IDs of stock.production.lot instances 
        """
        for lot in self.browse(cr, uid, ids, context):
            if lot.requires_sample_library and not lot.sample_library_code:
                return True
        return False
    
    
    # stock.production.lot
    def action_wofkflow_pending_sample(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'pending_sample'}, context)
        return True
    
    
    # stock.production.lot
    def action_sample_library(self, cr, uid, ids, context=None):
        sequence_proxy = self.pool.get('ir.sequence')
        wf_service = netsvc.LocalService("workflow")
        
        for prodlot in self.browse(cr, uid, ids, context):
            if not prodlot.requires_sample_library:
                continue
            
            self.write(cr, uid, [prodlot.id], {
                    'sample_library_code': sequence_proxy.get(cr, uid, 
                            'stock.prodlot.sample_library'),
                }, context)
            wf_service.trg_validate(uid, 'stock.production.lot', prodlot.id, 
                    'sample_get', cr)
        return True
    
    
    # stock.production.lot
    def create(self, cr, uid, vals, context=None):
        if 'requires_sample_library' not in vals:
            product = self.pool.get('product.product').browse(cr, uid, 
                    vals['product_id'], context)
            vals['requires_sample_library'] =  product.requires_sample_library
        
        return super(stock_production_lot, self).create(cr, uid, vals, context)
stock_production_lot()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
