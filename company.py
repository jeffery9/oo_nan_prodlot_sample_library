##############################################################################
#
# Copyright (c) 2012 NaN Projectes de Programari Lliure, S.L.
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

class res_company(osv.osv):
    '''
    Adds the field 'requires_sample_library' to configure the default behaviour
    of Company's products
    '''
    _inherit = 'res.company'
    
    _columns = {
        'requires_sample_library': fields.boolean('Requires Sample Library', 
                help="It defines the default value which will be used when a "
                "Product is created. Only the Product's field define the final "
                "behavior of its lots."),
    }
res_company()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
