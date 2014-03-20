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

"""cubicweb-medicalexp views/forms/actions/components for web ui"""

from logilab.mtconverter import xml_escape

from cubicweb.predicates import is_instance
from cubicweb.view import EntityView
from cubicweb.web.views.baseviews import SameETypeListView


###############################################################################
### SUBJECTS ##################################################################
###############################################################################
class SubjectOutOfContextView(EntityView):
    __regid__ = 'outofcontext'
    __select__ = EntityView.__select__ & is_instance('Subject')

    def cell_call(self, row, col):
        entity = self.cw_rset.get_entity(row, col)
        self.w(u'<div class="row">')
        self.w(u'<div class="col-md-2">')
        self.w(u'<h1>%s</h1>' % entity.symbol)
        self.w(u'</div>')
        self.w(u'<div class="col-md-8">')
        self.w(u'<h4><a href="%s">%s</a></h4>' % (entity.absolute_url(), entity.dc_title()))
        self.w(u'<div class="row">')
        age = entity.display_age_of_subjects()
        if age:
            self.w(u'Age <em>%s</em> - ' % age)
        if entity.handedness:
            self.w(u'Handedness <em>%s</em>' % entity.handedness)
        self.w(u'</div>')
        self.w(u'</div>')
        self.w(u'</div>')


###############################################################################
### ASSESSMENT ################################################################
###############################################################################
class AssessmentOutOfContextView(EntityView):
    __regid__ = 'outofcontext'
    __select__ = EntityView.__select__ & is_instance('Assessment')

    def cell_call(self, row, col):
        entity = self.cw_rset.get_entity(row, col)
        self.w(u'<div class="row">')
        self.w(u'<div class="col-md-2">')
        self.w(u'</div>')
        self.w(u'<div class="col-md-8">')
        self.w(u'<h4><a href="%s">%s</a></h4>' % (entity.absolute_url(), entity.dc_title()))
        subject = entity.reverse_concerned_by
        if subject:
            self.w(u'Subject <em>%s</em>' % subject[0].view('incontext'))
        self.w(u'</div>')
        self.w(u'</div>')


###############################################################################
### SCORES ####################################################################
###############################################################################
class ScoreValueOutOfContextView(EntityView):
    __regid__ = 'outofcontext'
    __select__ = EntityView.__select__ & is_instance('ScoreValue')

    def cell_call(self, row, col):
        entity = self.cw_rset.get_entity(row, col)
        sdef = entity.definition[0]
        self.w(u'<a href="%s">%s</a> - %s' % (xml_escape(sdef.absolute_url()),
                                              xml_escape(sdef.dc_title()),
                                              entity.text or entity.value))


###############################################################################
### THERAPY ###################################################################
###############################################################################
class TherapyOutOfContextView(EntityView):
    __regid__ = 'outofcontext'
    __select__ = EntityView.__select__ & is_instance('Therapy')

    def cell_call(self, row, col):
        entity = self.cw_rset.get_entity(row, col)
        self.w(u'<div class="row">')
        self.w(u'<div class="col-md-2"></div>')
        self.w(u'<div class="col-md-8">')
        self.w(u'<h4><a href="%s">%s</a></h4>' % tuple(map(xml_escape,
                                                           (entity.absolute_url(), entity.dc_title()))))
        self.w(u'%s :<em>%s</em>' % (xml_escape(self._cw._('subject')),
                                     entity.reverse_related_therapies[0].view('incontext')))
        if entity.start_date:
            self.w(u' - %s :<em>%s</em>' % (xml_escape(self._cw._('start_date')), entity.start_date))
        if entity.stop_date:
            self.w(u' - %s :<em>%s</em>' % (xml_escape(self._cw._('stop_date')), entity.stop_date))
        if entity.therapy_for:
            self.w(u' - %s :<em>%s</em>' % (xml_escape(self._cw._('therapy_for')),
                                            entity.therapy_for[0].view('incontext')))
        self.w(u'</div>')
        self.w(u'</div>')


###############################################################################
### GENERICTESTRUN  ###########################################################
###############################################################################
class GenericTestRunOutOfContextView(SameETypeListView):
    __select__ = SameETypeListView.__select__ & is_instance('GenericTestRun')

    def cell_call(self, row, col):
        entity = self.cw_rset.get_entity(row, col)
        self.w(u'<div class="row">')
        self.w(u'<div class="col-md-2">')
        #self.w(u'<img alt="" src="%s">' % entity.image_url)
        self.w(u'</div>')
        self.w(u'<div class="col-md-8">')
        self.w(u'<h4><a href="%s">%s</a></h4>' % (entity.absolute_url(), entity.identifier))
        self.w(u'<div class="row">')
        self.w(u'Date <em>%s</em>' % entity.formatted_datetime)
        self.w(u'</div>')
        self.w(u'</div>')
        self.w(u'</div>')


###############################################################################
### EXTERNAL RESOURCES ########################################################
###############################################################################
class ExternalResourcesSummaryView(SameETypeListView):
    __select__ = SameETypeListView.__select__ & is_instance('ExternalResource')

    def call(self, rset=None):
        self.w(u'<table class="table table-striped table-bordered table-condensed">')
        self.w(u'<tr>')
        self.w(u'<th>%s</th><th>%s</th>' % (self._cw._('External Resource'), self._cw._('Full filepath')))
        for exres in self.cw_rset.entities():
            self.w(u'<tr>')
            self.w(u'<th>%s</th>' % exres.view('incontext'))
            self.w(u'<th>%s</th>' % exres.full_filepath)
            self.w(u'</tr>')
        self.w(u'</table>')


###############################################################################
### STUDY #####################################################################
###############################################################################
class StudiesSummaryView(SameETypeListView):
    __select__ = SameETypeListView.__select__ & is_instance('Study')

    def call(self, rset=None):
        # XXX Cleaner way ?
        possible_measures = [r.type for r in self._cw.vreg.schema.rschema('related_study').subjects()]
        self.w(u'<table class="table table-striped table-bordered table-condensed">')
        self.w(u'<tr>')
        for label in [self._cw._('study'),
                      self._cw._('number of subjects'),
                      ## self._cw._('description'),
                      self._cw._('data_filepath'),]:
            self.w(u'<th>%s</th>' % self._cw._(label))
        for measure in possible_measures:
            self.w(u'<th>%s</th>' % self._cw._(measure))
        self.w(u'</tr>')
        for study in self.cw_rset.entities():
            self.w(u'<tr>')
            self.w(u'<th>%s</th>' % study.view('incontext'))
            rset = self._cw.execute('Any COUNT(SU) WHERE SU is Subject, '
                                    'SU related_studies S, S eid %(e)s',
                                    {'e': study.eid})
            url = self._cw.build_url(rql='Any X WHERE X related_studies S, S eid %(e)s'
                                     % {'e': study.eid})
            self.w(u'<th><a href="%s">%s</a></th>' % (url, rset[0][0]))
            ## self.w(u'<th>%s</th>' % study.description)
            self.w(u'<th>%s</th>' % study.data_filepath)
            for measure in possible_measures:
                rset = self._cw.execute('Any COUNT(SU) WHERE SU is %s, '
                                        'SU related_study S, S eid %%(e)s'
                                        % measure, {'e': study.eid})
                count_measure = rset[0][0]
                if not count_measure:
                    self.w(u'<th>-</a></th>')
                else:
                    url = self._cw.build_url(rql='Any X WHERE X is %(et)s, X related_study S, S eid %(e)s'
                                             % {'et': measure, 'e': study.eid})
                    self.w(u'<th><a href="%s">%s</a></th>' % (url, count_measure))
            self.w(u'</tr>')
        self.w(u'</table>')


###############################################################################
### CENTER ####################################################################
###############################################################################
class CentersSummaryView(SameETypeListView):
    __select__ = SameETypeListView.__select__ & is_instance('Center')

    def call(self, rset=None):
        self.w(u'<table class="table table-striped table-bordered table-condensed">')
        self.w(u'<tr>')
        for label in [self._cw._('centers'), self._cw._('assessments'),
                      self._cw._('devices'), self._cw._('number of subjects'),
                      self._cw._('Investigators')]:
            self.w(u'<th>%s</th>' % self._cw._(label))
        self.w(u'</tr>')
        for center in self.cw_rset.entities():
            self.w(u'<tr>')
            self.w(u'<th>%s</th>' % center.view('incontext'))
            # Assessments
            url = self._cw.build_url(rql='Any X WHERE C holds X, C eid %(e)s' % {'e': center.eid})
            self.w(u'<th><a href="%s">%s (%s)</a></th>'
                   % (url, self._cw._('See the assessments'), len(center.holds)))
            # Devices
            url = self._cw.build_url(rql='Any X WHERE X hosted_by C, C eid %(e)s' % {'e': center.eid})
            self.w(u'<th><a href="%s">%s (%s)</a></th>'
                   % (url, self._cw._('See the devices'), len(center.reverse_hosted_by)))
            # Subjects
            url = self._cw.build_url(rql='DISTINCT Any S WHERE C holds X, S concerned_by X, C eid %(e)s'
                                     % {'e': center.eid})
            count = len(self._cw.execute('DISTINCT Any S WHERE C holds X, S concerned_by X, C eid %(e)s'
                                         % {'e': center.eid}))
            self.w(u'<th><a href="%s">%s (%s)</a></th>' % (url, self._cw._('See the subjects'), count))
            # Investigators
            url = self._cw.build_url(rql='DISTINCT Any S WHERE C holds X, X conducted_by S, C eid %(e)s'
                                     % {'e': center.eid})
            count = len(self._cw.execute('DISTINCT Any S WHERE C holds X, X conducted_by S, C eid %(e)s'
                                         % {'e': center.eid}))
            self.w(u'<th><a href="%s">%s (%s)</a></th>' % (url, self._cw._('See the investigators'), count))
            self.w(u'</tr>')
        self.w(u'</table>')


###############################################################################
### GLOSSARY ##################################################################
###############################################################################
class MedicalTechniqueOutOfContextView(EntityView):
    __regid__ = 'outofcontext'
    __select__ = EntityView.__select__ & is_instance('MedicalTechnique')

    def cell_call(self, row, col):
        entity = self.cw_rset.get_entity(row, col)
        self.w(u'<div class="row">')
        self.w(u'<div class="col-md-2"></div>')
        self.w(u'<div class="col-md-8">')
        self.w(u'<h4><a href="%s">%s</a></h4>' % (entity.absolute_url(), entity.dc_title()))
        self.w(u'%s :<em>%s</em>' % (self._cw._('Type'), entity.type))
        if entity.broader_technique:
            self.w(u'- %s :<em>%s</em>' % (self._cw._('broader_technique'),
                                           entity.broader_technique[0].view('incontext')))
        self.w(u'</div>')
        self.w(u'</div>')


class DiseaseOutOfContextView(EntityView):
    __regid__ = 'outofcontext'
    __select__ = EntityView.__select__ & is_instance('Disease')

    def cell_call(self, row, col):
        entity = self.cw_rset.get_entity(row, col)
        self.w(u'<div class="row">')
        self.w(u'<div class="col-md-2"></div>')
        self.w(u'<div class="col-md-8">')
        self.w(u'<h4><a href="%s">%s</a></h4>' % (entity.absolute_url(), entity.dc_title()))
        if entity.lesion_of:
            self.w(u'- %s :<em>%s</em>' % (self._cw._('lesion_of'),
                                          entity.lesion_of[0].view('incontext')))
        self.w(u'</div>')
        self.w(u'</div>')


class BodyLocationOutOfContextView(EntityView):
    __regid__ = 'outofcontext'
    __select__ = EntityView.__select__ & is_instance('BodyLocation')

    def cell_call(self, row, col):
        entity = self.cw_rset.get_entity(row, col)
        self.w(u'<div class="row">')
        self.w(u'<div class="col-md-2"></div>')
        self.w(u'<div class="col-md-8">')
        self.w(u'<h4><a href="%s">%s</a></h4>' % (entity.absolute_url(), entity.dc_title()))
        if entity.subpart_of:
            self.w(u'- %s :<em>%s</em>' % (self._cw._('subpart_of'),
                                           entity.subpart_of[0].view('incontext')))
        self.w(u'</div>')
        self.w(u'</div>')

