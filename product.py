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

class product_product(osv.osv):
    """
    Adds the new property field 'requires_sample_library' for Quality Control templates for Lots: generic and
    specific templates for input and produced lots. If they are empty, the lots 
    won't require to pass test.
    The generic templates get it's default value from company.
    """
    _inherit = 'product.product'
    
    # product.product
    def _search_by_requires_sample_library(self, cr, uid, obj, name, args, 
            context):
        property_proxy = self.pool.get('ir.property')
        
        res = []
        for fieldname, operator, condition in args:
            opposite = False
            if operator in ('!=', '<>'):
                operator = '='
                opposite = True
            
            prop_ids = property_proxy.search(cr, uid, [
                        ('name', '=', fieldname),
                        ('res_id', 'like', 'res.partner,%'),
                        ('value_integer', operator, condition),
                    ], context=context)
            
            product_ids = []
            for property in property_proxy.browse(cr, uid, prop_ids, context):
                product_ids.append(property.res_id.id)
            
            operator = 'in'
            if opposite:
                operator = 'not in'
            res.append(('id', operator, product_ids))
        return res
    
    
    _columns = {
        'requires_sample_library': fields.property('product.product', 
                type='boolean', string="Requires Sample Library", method=True, 
                view_load=True, fnct_search=_search_by_requires_sample_library),
    }
    
    # product.product
    def _default_requires_sample_library(self, cr, uid, context):
        user = self.pool.get('res.users').browse(cr, uid, uid, context)
        return user.company_id.requires_sample_library
    
    _defaults = {
        'requires_sample_library': _default_requires_sample_library,
    }
product_product()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
