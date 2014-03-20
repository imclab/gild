# -*- coding: utf-8 -*-
# copyright 2013 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# copyright 2013 CEA (Saclay, FRANCE), all rights reserved.
# contact http://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/>.

from cubicweb.view import AnyRsetView, EntityView
from cubicweb.selectors import is_instance

###############################################################################
### VIEWS #####################################################################
###############################################################################
class GenomicMeasureOutOfContextView(EntityView):
    __regid__ = 'outofcontext'
    __select__ = EntityView.__select__ & is_instance('GenomicMeasure')

    def cell_call(self, row, col):
        entity = self.cw_rset.get_entity(row, col)
        self.w(u'<div class="thumbnail row">')
        self.w(u'<div class="col-md-2">')
        self.w(u'<img alt="" src="%s">' % entity.image_url)
        self.w(u'</div>')
        self.w(u'<div class="col-md-8">')
        self.w(u'<h4><a href="%s">%s</a></h4>' % (entity.absolute_url(), entity.dc_title()))
        self.w(u'<div class="row">')
        self.w(u'Type <em>%s</em>' % entity.type)
        self.w(u'</div>')
        self.w(u'</div>')
        self.w(u'</div>')
