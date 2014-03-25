# -*- coding: utf-8 -*-
##########################################################################
# Copyright (C) CEA - Neurospin, 2014
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

"""cubicweb-gild schema"""

from yams.buildobjs import EntityType
from yams.buildobjs import RelationDefinition
from yams.buildobjs import SubjectRelation
from yams.buildobjs import String
from yams.buildobjs import RichString
from yams.buildobjs import Int
from yams.buildobjs import Float
from yams.buildobjs import Boolean
from yams.buildobjs import Datetime

from cubes.medicalexp.schema import Study


##########################################################################
# Cati schema modification
##########################################################################
class can_read(RelationDefinition):
    subject = 'CWUser'
    object = 'Study'
    cardinality = '**'


class can_modify(RelationDefinition):
    subject = 'CWUser'
    object = 'Study'
    cardinality = '**'


STUDY_PERMISSIONS = {
    'read': ('managers', ERQLExpression('U can_read X')),
    'add': ('managers', ERQLExpression('U can_modify X')),
    'update': ('managers', ERQLExpression('U can_modify X')),
    'delete': ('managers', ERQLExpression('U can_modify X')),
}


ENTITY_PERMISSIONS = {
    'read': ('managers', ERQLExpression('X belong_to S, U can_read S')),
    'add': ('managers', ERQLExpression('X belong_to S, U can_modify S')),
    'update': ('managers', ERQLExpression('X belong_to S, U can_modify S')),
    'delete': ('managers', ERQLExpression('X belong_to S, U can_modify S')),
}


RELATION_PERMISSIONS = {
    'read': ('managers', 'users'),
    'add': ('managers', RRQLExpression('S belong_to ST, U can_modify ST')),
    'delete': ('managers', RRQLExpression('S belong_to ST, U can_modify ST'))
}


Study.__permissions__ = STUDY_PERMISSIONS
