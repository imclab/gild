# -*- coding: utf-8 -*-
##########################################################################
# Copyright (C) CEA - Neurospin, 2014
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

from cubes.questionnaire.schema import QuestionnaireRun
from cubes.questionnaire.schema import Questionnaire
from cubes.neuroimaging.schema import Scan
from cubes.genomics.schema import GenomicMeasure
from cubes.medicalexp.schema import Configuration
from cubes.medicalexp.schema import Protocol
from cubes.medicalexp.schema import Assessment
from cubes.medicalexp.schema import GenericMeasure
from cubes.medicalexp.schema import ProcessingRun
from cubes.medicalexp.schema import GenericTest
from cubes.medicalexp.schema import GenericTestRun
from cubes.medicalexp.schema import inputs
from cubes.medicalexp.schema import outputs
from cubes.medicalexp.schema import Subject


from yams.buildobjs import EntityType
from yams.buildobjs import RelationDefinition
from yams.buildobjs import SubjectRelation
from yams.buildobjs import String
from yams.buildobjs import RichString
from yams.buildobjs import Int
from yams.buildobjs import Float
from yams.buildobjs import Boolean


"""cubicweb-gild schema"""


class FileEntry(EntityType):
    """ Any resource file """
    name = String(maxsize=256)
    filepath = String(required=True, indexed=True, maxsize=256)
    size = Int()
    md5 = String(maxsize=32)


class FileSet(EntityType):
    """ A composite resource file set """
    name = String(maxsize=256, required=True)
    format = String(maxsize=256)
    file_entries = SubjectRelation('FileEntry', cardinality='**')
    related_study = SubjectRelation('Study', cardinality='1*', inlined=True, composite='object')
    other_studies = SubjectRelation('Study', cardinality='**')


class FileParameter(EntityType):
    parameter = String(required=True, indexed=True)
    file_set = SubjectRelation('FileSet', cardinality='1*', inlined=True)



Subject.add_relation(String(required=True, fulltextindexed=True,indexed=True),
                     name='code_in_study')

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

Configuration.remove_relation("external_resources")
Configuration.add_relation(SubjectRelation('FileSet',
                                           cardinality='**',
                                           composite='subject'),
                           name='external_resources')
Protocol.remove_relation("external_resources")
Protocol.add_relation(SubjectRelation('FileSet',
                                      cardinality='**',
                                      composite='subject'),
                      name='external_resources')

Assessment.remove_relation("external_resources")
Assessment.add_relation(SubjectRelation('FileSet',
                                        cardinality='**',
                                        composite='subject'),
                        name='external_resources')

GenericMeasure.remove_relation("external_resources")
GenericMeasure.add_relation(SubjectRelation('FileSet',
                                            cardinality='**',
                                            composite='subject'),
                            name='external_resources')

ProcessingRun.remove_relation("external_resources")
ProcessingRun.add_relation(SubjectRelation('FileSet',
                                           cardinality='**',
                                           composite='subject'),
                           name='external_resources')

GenericTest.remove_relation("external_resources")
GenericTest.add_relation(SubjectRelation('FileSet',
                                         cardinality='**',
                                         composite='subject'),
                         name='external_resources')

GenericTestRun.remove_relation("external_resources")
GenericTestRun.add_relation(SubjectRelation('FileSet',
                                            cardinality='**',
                                            composite='subject'),
                            name='external_resources')

Questionnaire.remove_relation("external_resources")
Questionnaire.add_relation(SubjectRelation('FileSet',
                                           cardinality='*1',
                                           composite='subject'),
                              name='external_resources')

QuestionnaireRun.remove_relation("external_resources")
QuestionnaireRun.add_relation(SubjectRelation('FileSet',
                                              cardinality='*1',
                                              composite='subject'),
                              name='external_resources')

Scan.remove_relation("external_resources")
Scan.add_relation(SubjectRelation('FileSet',
                                  cardinality='*1',
                                  composite='subject'),
                  name='external_resources')

GenomicMeasure.remove_relation("external_resources")
GenomicMeasure.add_relation(SubjectRelation('FileSet',
                                            cardinality='*1',
                                            composite='subject'),
                            name='external_resources')

inputs.object = ('GenericTestRun', 'ScoreValue', 'FileParameter')
outputs.object = ('GenericTestRun', 'ScoreValue', 'FileParameter')
