# -*- coding: utf-8 -*-
# copyright 2012 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
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

"""cubicweb-neuroimaging views/forms/actions/components for web ui"""
import cPickle
import StringIO

from logilab.mtconverter import xml_escape

from cubicweb.view import EntityView
from cubicweb.selectors import is_instance


class ScanOutOfContextView(EntityView):
    __regid__ = 'outofcontext'
    __select__ = EntityView.__select__ & is_instance('Scan')

    def cell_call(self, row, col):
        entity = self.cw_rset.get_entity(row, col)
        self.w(u'<div class="thumbnail row">')
        self.w(u'<div class="col-md-2">')
        self.w(u'<a href="#"><img alt="" src="%s"></a>' % entity.image_url)
        self.w(u'</div>')
        self.w(u'<div class="col-md-8">')
        self.w(u'<a href="%s">%s</a>' % (entity.absolute_url(), xml_escape(entity.dc_title())))
        self.w(u'<div class="row">')
        self.w(u'%s <em>%s</em>' % (self._cw._('Type'), entity.type))
        self.w(u' - ')
        self.w(u'%s <em>%s</em>' % (self._cw._('Format'), entity.format))
        self.w(u'</div>')
        self.w(u'</div>')
        self.w(u'<div class="col-md-2">')
        self.w(u'''<button class="btn btn-danger" type="button" style="margin-top:8px" onclick="$('#info-%s').toggle()">%s</button>'''
               % (entity.eid, self._cw._('See more')))
        self.w(u'</div>')
        self.w(u'<div class="col-md-10 well pull-right" id="info-%s" style="display:none">' % entity.eid)
        self.w(u'<dl class="dl-horizontal">')
        self.add_additional_infos(entity)
        if entity.description:
            self.w('<dt>%s</dt><dd>%s</dd>' % (self._cw._('Description'), entity.description))
        if entity.has_data :
            data = entity.has_data[0]
            data.view('scan-data-view', w=self.w)
        self.w(u'</dl>')
        demo = self._cw.vreg.config.get('demo-site', False)
        if not demo:
            self.w(u'<a href="%s"><button class="btn btn-sm btn-primary" type="button">%s</button></a>'
                   % (self._cw.build_url(vid='data-zip', rql='Any X WHERE X eid %s' % entity.eid),
                      self._cw._('Download as a Zip file')))
        self.w(u'</div>')
        self.w(u'</div>')

    def add_additional_infos(self, entity):
        """ Put here additional info, e.g. subject..."""


class MRIDataOutOfContextView(EntityView):
    __regid__ = 'scan-data-view'
    __select__ = EntityView.__select__ & is_instance('MRIData')

    def cell_call(self, row, col):
        entity = self.cw_rset.get_entity(row, col)
        if entity.sequence:
            self.w(u'<dt>%s</dt><dd>%s</dd>' % (self._cw._('Sequence'), entity.sequence))
        if entity.shape_x:
            self.w(u'<dt>%s</dt><dd>%s</dd>' % (self._cw._('Image Shape (x)'), entity.shape_x))
        if entity.shape_y:
            self.w(u'<dt>%s</dt><dd>%s</dd>' % (self._cw._('Image Shape (y)'), entity.shape_y))
        if entity.shape_z:
            self.w(u'<dt>%s</dt><dd>%s</dd>' % (self._cw._('Image Shape (z)'), entity.shape_z))
        if entity.shape_t:
            self.w(u'<dt>%s</dt><dd>%s</dd>' % (self._cw._('Image Shape (t)'), entity.shape_t))
        if entity.voxel_res_x:
            self.w(u'<dt>%s</dt><dd>%s</dd>' % (self._cw._('Voxel resolution (x)'), entity.voxel_res_x))
        if entity.voxel_res_y:
            self.w(u'<dt>%s</dt><dd>%s</dd>' % (self._cw._('Voxel resolution (y)'), entity.voxel_res_y))
        if entity.voxel_res_z:
            self.w(u'<dt>%s</dt><dd>%s</dd>' % (self._cw._('Voxel resolution (z)'), entity.voxel_res_z))
        if entity.fov_x:
            self.w(u'<dt>%s</dt><dd>%s</dd>' % (self._cw._('Fov (x)'), entity.fov_x))
        if entity.fov_y:
            self.w(u'<dt>%s</dt><dd>%s</dd>' % (self._cw._('Fov (y)'), entity.fov_y))
        if entity.tr:
            self.w(u'<dt>%s</dt><dd>%s</dd>' % (self._cw._('Tr'), entity.tr))
        if entity.te:
            self.w(u'<dt>%s</dt><dd>%s</dd>' % (self._cw._('Te'), entity.te))


###############################################################################
### EXPORT VIEWS ##############################################################
###############################################################################
## class AbstractScanNumpyExport(EntityView):
##     __abstract__ = True
##     __select__ = EntityView.__select__ & is_instance('Scan')
##     templatable = False
##     binary = True

##     def call(self, rset=None, **kwargs):
##         rset = rset or self.cw_rset
##         all_arrays = []
##         for entity in rset.entities():
##             all_arrays.append(entity.numpy_data)
##         self.w(self.serialize(all_arrays))

##     def serialize(self, all_arrays):
##         raise NotImplementedError

## class ScanNumpyExportPickle(AbstractScanNumpyExport):
##     __regid__ = 'pickle-export'
##     title = _('download pickle')

##     def serialize(self, all_arrays):
##         return cPickle.dumps(all_arrays, cPickle.HIGHEST_PROTOCOL)
