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

"""cubicweb-medicalexp entity's classes"""
import os.path as osp

from cubicweb.selectors import is_instance
from cubicweb.view import EntityAdapter
from cubicweb.entities import AnyEntity, fetch_config


def compute_fullfilepath(entity):
    study_path = entity.related_study[0].data_filepath
    if study_path:
        filepath = entity.filepath
        if filepath.startswith('/'):
            filepath = filepath[1:]
        return osp.join(study_path, filepath)
    return entity.filepath


class Subject(AnyEntity):
    __regid__ = 'Subject'
    fetch_attrs, fetch_order = fetch_config(('gender', 'handedness'))

    def dc_title(self):
        if hasattr(self, "identifier"):
            return self.identifier
        elif hasattr(self, "subject_code"):
            return self.subject_code
        else:
            return "Cannot find title"

    @property
    def symbol(self):
        if self.gender == 'male':
            return '&#x2642;'
        elif self.gender == 'female':
            return '&#x2640;'
        else:
            return '&nbsp;'

    @property
    def age_of_subjects(self):
        rset = self._cw.execute('Any A WHERE S concerned_by X, S eid %(e)s, X age_of_subject A',
                                {'e': self.eid})
        if rset.rowcount:
            return (min(r[0] for r in rset), max(r[0] for r in rset))
        else:
            return None, None

    def display_age_of_subjects(self):
        age_min, age_max = self.age_of_subjects
        if age_min and age_max and age_min != age_max:
            age = '%s-%s' % (age_min, age_max)
        elif age_min:
            age = str(age_min)
        elif age_max:
            age = str(age_max)
        else:
            age = None
        return age

    @property
    def related_centers(self):
        rset = self._cw.execute('DISTINCT Any X WHERE X holds A, S concerned_by A, S eid %(e)s',
                                {'e': self.eid})
        return list(rset.entities())


class Assessment(AnyEntity):
    __regid__ = 'Assessment'

    def dc_title(self):
        return self.identifier


class Center(AnyEntity):
    __regid__ = 'Center'

    def dc_title(self):
        return self.name

class Study(AnyEntity):
    __regid__ = 'Study'

    def dc_title(self):
        return self.name

class Device(AnyEntity):
    __regid__ = 'Device'

    def dc_title(self):
        return self.name

class SubjectGroup(AnyEntity):
    __regid__ = 'SubjectGroup'

    def dc_title(self):
        return self.name

class Protocol(AnyEntity):
    __regid__ = 'Protocol'

    def dc_title(self):
        if self.name:
            return '%s (%s)' % (self.name, self.identifier)
        return self.identifier

class ProcessingRun(AnyEntity):
    __regid__ = 'ProcessingRun'

    def dc_title(self):
        return u'ProcessingRun (%s) - %s' % (self.category, self.name)

class ScoreDefinition(AnyEntity):
    __regid__ = 'ScoreDefinition'

    def dc_title(self):
        return u'%s (%s)' % (self.category, self.name)

class ScoreValue(AnyEntity):
    __regid__ = 'ScoreValue'

    def dc_title(self):
        _def = self.definition[0]
        _def_title = self._cw._(_def.dc_title())
        return u'%s : %s (%s)' % (_def_title, self.value, self.datetime)

    @property
    def subject(self):
        if self.reverse_related_infos:
            return self.reverse_related_infos[0]
        if self.measure:
            return self.measure[0].concerns[0]

    @property
    def complete_value(self):
        return self.value or self.text


class ExternalResource(AnyEntity):
    __regid__ = 'ExternalResource'

    def dc_title(self):
        main_entity = self.reverse_external_resources[0]
        if main_entity.__regid__ == 'Assessment' and not len(main_entity.generates):
            # This is an external resource link to an assessment only used to store file
            return '%s (%s)' % (main_entity.identifier, self.name)
        return self.name

    @property
    def full_filepath(self):
        return compute_fullfilepath(self)

class GenericMeasure(AnyEntity):
    __regid__ = 'GenericMeasure'

    @property
    def full_filepath(self):
        return compute_fullfilepath(self)

class GenericTestRun(AnyEntity):
    __regid__ = 'GenericTestRun'

    def dc_title(self):
        return self.identifier

    @property
    def full_filepath(self):
        return compute_fullfilepath(self)

    @property
    def formatted_datetime(self):
        if not self.datetime:
            return 'missing'
        else:
            return self.datetime.dc_title()


class ScoreGroup(AnyEntity):
    __regid__ = 'ScoreGroup'

    def get_score(self, name):
        return [(v, v.definition[0]) for v in self.scores if v.definition[0].name == name]


class Disease(AnyEntity):
    __regid__ = 'Disease'

    def dc_title(self):
        return self.name


class BodyLocation(AnyEntity):
    __regid__ = 'BodyLocation'

    def dc_title(self):
        if not self.subpart_of:
            return self.name
        return '%s (%s)' % (self.subpart_of[0].dc_title(), self.name)


class MedicalTechnique(AnyEntity):
    __regid__ = 'MedicalTechnique'

    def dc_title(self):
        return self.name


class TechnicalAnalysis(AnyEntity):
    __regid__ = 'TechnicalAnalysis'

    def dc_title(self):
        return u'%s : %s' % (self._cw._('TechnicalAnalysis'), self.technique_type[0].dc_title())


class Diagnostic(AnyEntity):
    __regid__ = 'Diagnostic'

    def dc_title(self):
        return u'%s : %s - %s' % (self._cw._('Diagnostic'),
                                  self.diagnostic_location[0].dc_title(),
                                  self.diagnosed_disease[0].dc_title())
