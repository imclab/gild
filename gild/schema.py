# -*- coding: utf-8 -*-
##########################################################################
# Copyright (C) CEA - Neurospin, 2014
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

from cubes.questionnaire.schema import QuestionnaireRun
from cubes.neuroimaging.schema import Scan
from cubes.genomics.schema import GenomicMeasure

from yams.buildobjs import EntityType
from yams.buildobjs import RelationDefinition
from yams.buildobjs import SubjectRelation
from yams.buildobjs import String
from yams.buildobjs import RichString
from yams.buildobjs import Int
from yams.buildobjs import Float
from yams.buildobjs import Boolean


"""cubicweb-gild schema"""
QuestionnaireRun.remove_relation("concerns")
QuestionnaireRun.add_relation(SubjectRelation(('Subject', 'SubjectGroup'),
                                              cardinality='1*',
                                              inlined=True),
                                              name='concerns')

Scan.remove_relation("concerns")
Scan.add_relation(SubjectRelation(('Subject', 'SubjectGroup'),
                                  cardinality='1*', inlined=True),
                                  name='concerns')

GenomicMeasure.remove_relation("concerns")
GenomicMeasure.add_relation(SubjectRelation(('Subject', 'SubjectGroup'),
                                            cardinality='1*', inlined=True),
                                            name='concerns')