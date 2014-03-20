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

from cubicweb.web.views.csvexport import CSVRsetView
from cubicweb.selectors import is_instance


class SubjectCSVView(CSVRsetView):
    __select__ = CSVRsetView.__select__ & is_instance('Subject')

    def call(self):
        req = self._cw
        values = {}
        questions = {}
        rows = [('"subject_id"', '"gender"', '"handedness"')]
        for entity in self.cw_rset.entities():
            rows.append([entity.identifier, entity.gender, entity.handedness])
        writer = self.csvwriter()
        writer.writerows(rows)


class ScoreDefinitionCSVView(CSVRsetView):
    __select__ = CSVRsetView.__select__ & is_instance('ScoreDefinition')

    def call(self):
        entity = self.cw_rset.get_entity(0, 0)
        req = self._cw
        rset = self._cw.execute('Any SU,S,V,T,DA,SN WHERE SU related_infos S, SU identifier SN, '
                                'S is ScoreValue, S value V, S text T, '
                                'S datetime DA, S definition D, D eid %(e)s', {'e': entity.eid})
        rows = []
        rows.append(['"subject_id"', '"value"', '"datetime"'])
        for ind in range(len(rset)):
            subj = rset.get_entity(ind, 0)
            score = rset.get_entity(ind, 1)
            rows.append([subj.identifier, score.value or score.text, score.datetime])
        writer = self.csvwriter()
        writer.writerows(rows)


class GenericTestRunCSVView(CSVRsetView):
    __select__ = CSVRsetView.__select__ & is_instance('GenericTestRun')

    def call(self):
        req = self._cw
        values = {}
        questions = {}
        for entity in self.cw_rset.entities():
            subject = entity.concerns[0].identifier
            rset = self._cw.execute('Any S, SD, V, T, CC, NC '
                                    'WHERE QR is GenericTestRun, QR eid %(e)s, '
                                    'S measure QR, S definition SD, S value V, S text T, '
                                    'SD category CC, SD name NC', {'e': entity.eid})
            for ind, row in enumerate(rset.rows):
                answer = rset.get_entity(ind, 0)
                question = rset.get_entity(ind, 1)
                values.setdefault(subject, {})[question.name] = answer.complete_value
                questions[question.name] = question.dc_title()
        rows = []
        headers = ['"subject_id"',]
        headers.extend(['"%s"' % q for q in questions.values()])
        rows.append(headers)
        for subject, _values in values.iteritems():
            row = [subject]
            for question_id in questions:
                row.append(_values.get(question_id))
            rows.append(row)
        writer = self.csvwriter()
        writer.writerows(rows)
