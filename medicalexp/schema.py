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

"""cubicweb-medicalexp schema"""

from yams.buildobjs import (EntityType, RelationDefinition, SubjectRelation,
                            String, RichString, Int, Float, Date, Boolean)


###############################################################################
### PROJECT/SUBJECT SPECIFIC ENTITIES #########################################
###############################################################################
class Subject(EntityType):
    """ The subject """
    identifier = String(required=True, fulltextindexed=True,
                        indexed=True, maxsize=64)
    surname = String(fulltextindexed=True, maxsize=256)
    firstname = String(fulltextindexed=True, maxsize=256)
    gender = String(required=True, indexed=True,
                    vocabulary=('male', 'female', 'unknown'))
    date_of_birth = Date()
    handedness = String(required=True, indexed=True,
                        vocabulary=('right', 'left', 'ambidextrous', 'mixed', 'unknown'))
    related_studies = SubjectRelation('Study', cardinality='**')
    related_groups = SubjectRelation('SubjectGroup', cardinality='**')
    related_infos = SubjectRelation('ScoreValue', cardinality='**', composite='subject')
    related_diseases = SubjectRelation('Disease', cardinality='**')
    related_lesions = SubjectRelation('BodyLocation', cardinality='**')
    related_diagnostics = SubjectRelation('Diagnostic', cardinality='**', composite='subject')
    related_therapies = SubjectRelation('Therapy', cardinality='**', composite='subject')


class Study(EntityType):
    """ The project """
    name = String(required=True, indexed=True, maxsize=256)
    data_filepath = String(required=True, indexed=True, maxsize=2048)
    description = RichString(fulltextindexed=True)
    keywords = String(maxsize=1024)
    themes = SubjectRelation('Theme', cardinality='**')

class Theme(EntityType):
    """ Study theme, etiology """
    name = String(required=True, indexed=True, maxsize=256)
    description = RichString(fulltextindexed=True)

class SubjectGroup(EntityType):
    """ Group of subject """
    identifier = String(required=True, indexed=True, maxsize=64)
    name = String(maxsize=64, required=True, indexed=True)
    related_studies = SubjectRelation('Study', cardinality='**')


###############################################################################
### PROJECT MANAGEMENT ENTITIES ###############################################
###############################################################################
class Investigator(EntityType):
    """ Investigator of a study / PI """
    identifier = String(required=True, indexed=True, maxsize=64)
    firstname = String(maxsize=256)
    lastname = String(maxsize=256)
    title = String(maxsize=16)
    institution = String(maxsize=256)
    department = String(maxsize=256)

class Center(EntityType):
    """ A center used for study """
    identifier = String(required=True, indexed=True, maxsize=64)
    name = String(maxsize=256, required=True)
    department = String(maxsize=256)
    city = String(maxsize=64)
    country = String(maxsize=64)

class Device(EntityType):
    """ Device used in experiments/assessments """
    name = String(maxsize=256, required=True)
    manufacturer = String(maxsize=256)
    model = String(maxsize=256)
    serialnum = String(maxsize=256)
    configurations = SubjectRelation('Configuration', cardinality='*1')
    hosted_by = SubjectRelation('Center', cardinality='1*', inlined=True, composite='object')

class Configuration(EntityType):
    """ Configuration of a device """
    filepath = String(required=True, indexed=True, maxsize=2048)
    start_datetime = Date()
    end_datetime = Date()
    external_resources = SubjectRelation('ExternalResource', cardinality='**', composite='subject')
    results_file = SubjectRelation('File', cardinality='**') # XXX to clarify what happens when a 'File' object is deleted.


class Protocol(EntityType):
    """ A protocol for a study or a measure """
    identifier = String(required=True, indexed=True, maxsize=64)
    name = String(internationalizable=True)
    related_study = SubjectRelation('Study', cardinality='1*', inlined=True, composite='object')
    start_datetime = Date()
    end_datetime = Date()
    external_resources = SubjectRelation('ExternalResource', cardinality='**', composite='subject')


###############################################################################
### GLOSSARY ENTITIES #########################################################
###############################################################################
class Disease(EntityType):
    identifier = String(required=True, indexed=True, maxsize=1024)
    name = String(required=True, fulltextindexed=True,
                  internationalizable=True, maxsize=2048)
    mesh_id = String(maxsize=64)
    icd10 = String(maxsize=64)
    description = RichString(fulltextindexed=True)
    lesion_of = SubjectRelation('BodyLocation', cardinality='**')


class BodyLocation(EntityType):
    identifier = String(required=True, indexed=True, maxsize=1024)
    name = String(required=True, fulltextindexed=True,
                  internationalizable=True, maxsize=2048)
    mesh_id = String(maxsize=64)
    description = RichString(fulltextindexed=True)
    subpart_of = SubjectRelation('BodyLocation', cardinality='?*', inlined=True, composite='object')


class MedicalTechnique(EntityType):
    identifier = String(required=True, indexed=True, maxsize=1024)
    name = String(required=True, fulltextindexed=True,
                  internationalizable=True, maxsize=2048)
    type = String(vocabulary=[_('diagnostic'), _('analysis')])
    description = RichString(fulltextindexed=True)
    broader_technique = SubjectRelation('MedicalTechnique', cardinality='?*', inlined=True, composite='object')


###############################################################################
### DIAGNOSTIC AND ANALYSIS ###################################################
###############################################################################
class Diagnostic(EntityType):
    """ Diagnostic attributes and links.
    Diagnostic may be based on specific measures, and holds a conclusion
    on BodyLocation/Disease"""
    diagnostic_date = Date()
    conclusion = String(maxsize=256, fulltextindexed=True)
    diagnostic_location = SubjectRelation('BodyLocation', cardinality='1*', inlined=True)
    diagnosed_disease = SubjectRelation('Disease', cardinality='1*', inlined=True)
    technique_type = SubjectRelation('MedicalTechnique', cardinality='?*', inlined=True)
    leads_to_therapies = SubjectRelation('Therapy', cardinality='**')


class TechnicalAnalysis(EntityType):
    """ Analysis attributes and links.
    An analysis is done with a given technique and give some results
    """
    analysis_date = Date()
    results = String(maxsize=2048, fulltextindexed=True)
    conclusion = String(maxsize=256, fulltextindexed=True)
    technique_type = SubjectRelation('MedicalTechnique', cardinality='1*', inlined=True)
    performed_in_therapy = SubjectRelation('Therapy', cardinality='?*', inlined=True)


###############################################################################
### THERAPY AND DRUG ##########################################################
###############################################################################
class Therapy(EntityType):
    """ Therapy attributes and links"""
    identifier = String(required=True, indexed=True, maxsize=1024)
    start_date = Date()
    stop_date = Date()
    relevant_anomaly = String(maxsize=1024)
    therapy_for = SubjectRelation('Disease', cardinality='**')
    based_on_diagnostic = SubjectRelation('Diagnostic', cardinality='**')
    description = RichString(fulltextindexed=True)

class DrugTake(EntityType):
    """ Drug take """
    start_taking_date = Date(required=True)
    # Stop taking date is not required as the treatment could still exist
    stop_taking_date = Date()
    # Order for multiple drugs if it is relevant
    take_order = Int()
    dosis = Int()
    unit = Int()#quantity = dosis * unit
    number_of_cycles = Int()
    dosis_percentage = Float(description=u'dosis percentage, w.r.t. the expansion cohort')
    reduced_dosis = Boolean()
    taken_in_therapy = SubjectRelation('Therapy', cardinality='1*', inlined=True, composite='object')
    drug = SubjectRelation('Drug', cardinality='1*', inlined=True)

class Drug(EntityType):
    """ Drug attributes """
    identifier = String(required=True, indexed=True, maxsize=1024)
    name = String(required=True, maxsize=2048)
    description = RichString(fulltextindexed=True)
    # Ids
    pubchem_id = String(maxsize=64)
    drugbank_id = String(maxsize=128)
    unii_id = String(maxsize=128)
    cas_number = String(maxsize=128)
    iupac_name = String(maxsize=128)
    routes_of_administration = String(maxsize=2048)
    metabolism = String(maxsize=2048)
    drug_for = SubjectRelation('Disease', cardinality='**')
    acts_on = SubjectRelation('BodyLocation', cardinality='**')


###############################################################################
### ASSESSMENT/MEASURE ENTITIES ###############################################
###############################################################################
class Assessment(EntityType):
    """ Store information about a visit """
    identifier = String(required=True, indexed=True, maxsize=64)
    datetime = Date()
    age_of_subject = Int(indexed=True)
    timepoint = String(maxsize=64)
    external_resources = SubjectRelation('ExternalResource', cardinality='**', composite='subject')
    results_file = SubjectRelation('File', cardinality='**') # XXX What happens when a 'File' is deleted?
    related_study = SubjectRelation('Study', cardinality='1*', inlined=True, composite='object')

class GenericMeasure(EntityType):
    """ Generic measure used to store non base type measures
    (e.g. referential, numerical values...) """
    identifier = String(required=True, indexed=True, maxsize=64)
    name = String(maxsize=256, required=True)
    type = String(maxsize=256, required=True)
    filepath = String(indexed=True, maxsize=2048)
    external_resources = SubjectRelation('ExternalResource', cardinality='**', composite='subject')
    results_file = SubjectRelation('File', cardinality='**') # XXX What happens when a 'File' is deleted?
    related_study = SubjectRelation('Study', cardinality='1*', inlined=True, composite='object')
    other_studies = SubjectRelation('Study', cardinality='**')

class ProcessingRun(EntityType):
    name = String(maxsize=256)
    tool = String(maxsize=256)
    datetime = Date()
    category = String(maxsize=256)
    version = String(maxsize=64)
    parameters = String(maxsize=256)
    note = RichString(fulltextindexed=True)
    external_resources = SubjectRelation('ExternalResource', cardinality='**', composite='subject')
    results_file = SubjectRelation('File', cardinality='**') # XXX What happens when a 'File' is deleted?
    followed_by = SubjectRelation('ProcessingRun' , cardinality='??', inlined=True)


###############################################################################
### SATELLITE ENTITIES ########################################################
###############################################################################
class ExternalResource(EntityType):
    """ An external resource file """
    name = String(maxsize=256, required=True)
    filepath = String(required=True, indexed=True, maxsize=2048)
    related_study = SubjectRelation('Study', cardinality='1*', inlined=True, composite='object')
    other_studies = SubjectRelation('Study', cardinality='**')

class ScoreDefinition(EntityType):
    """ A score definition """
    name = String(maxsize=256, required=True, indexed=True)
    category = String(maxsize=64, indexed=True)
    type = String(required=True, indexed=True, vocabulary=('string', 'numerical', 'logical'),)
    unit = String(maxsize=16, indexed=True)
    possible_values = String(maxsize=256)

# XXX Two different etypes for string/numerical values ?
class ScoreValue(EntityType):
    """ A score value """
    definition = SubjectRelation('ScoreDefinition', cardinality='1*', inlined=True, composite='object')
    text = String(maxsize=2048, indexed=True)
    value = Float(indexed=True)
    datetime = Date()

class ScoreGroup(EntityType):
    """ A group of score values that should be considered together """
    identifier = String(required=True, indexed=True, maxsize=64)
    scores = SubjectRelation('ScoreValue', cardinality='**')


###############################################################################
### GENERIC TEST (BEHAVIORAL/BIOLOGICAL...) ###################################
###############################################################################
class GenericTest(EntityType):
    """ A generic test type """
    name = String(maxsize=256, required=True)
    identifier = String(required=True, indexed=True, maxsize=64)
    type = String(maxsize=256, required=True)
    version = String(maxsize=16)
    language = String(maxsize=16)
    note = RichString(fulltextindexed=True)
    external_resources = SubjectRelation('ExternalResource', cardinality='**', composite='subject')
    results_file = SubjectRelation('File', cardinality='**') # XXX What happens when a 'File' is deleted?
    definitions = SubjectRelation('ScoreDefinition', cardinality='*?')


class GenericTestRun(EntityType):
    """ A generic test run """
    identifier = String(required=True, indexed=True, maxsize=64)
    user_ident = String(required=True, indexed=True, maxsize=64)
    datetime = Date()
    iteration = Int(indexed=True)
    completed = Boolean(indexed=True)
    valid = Boolean(indexed=True)
    instance_of = SubjectRelation('GenericTest', cardinality='1*', inlined=True, composite='object')
    external_resources = SubjectRelation('ExternalResource', cardinality='**', composite='subject')
    results_file = SubjectRelation('File', cardinality='**') # XXX What happens when a 'File' is deleted?
    related_study = SubjectRelation('Study', cardinality='1*', inlined=True, composite='object')
    other_studies = SubjectRelation('Study', cardinality='**')


###############################################################################
### RELATIONS #################################################################
###############################################################################
class concerned_by(RelationDefinition):
    subject = 'Subject'
    object = 'Assessment'
    cardinality = '*+'
    composite='subject'

class conducted_by(RelationDefinition):
    subject = 'Assessment'
    object = 'Investigator'
    cardinality = '**'

class holds(RelationDefinition):
    subject = 'Center'
    object = 'Assessment'
    cardinality = '*1'
    composite='subject'

class inputs(RelationDefinition):
    subject = 'ProcessingRun'
    object = ('GenericTestRun', 'ScoreValue')
    cardinality = '**'

class outputs(RelationDefinition):
    subject = 'ProcessingRun'
    object = ('GenericTestRun', 'ScoreValue')
    cardinality = '**'

class related_processing(RelationDefinition):
    subject = 'Assessment'
    object = 'ProcessingRun'
    cardinality = '**'

class performed_on(RelationDefinition):
    subject = ('Diagnostic', 'TechnicalAnalysis')
    object = ('GenericMeasure', 'GenericTestRun')
    cardinality = '**'
    composite = 'object'

class concerns(RelationDefinition):
    subject = ('GenericMeasure', 'GenericTestRun')
    object = ('Subject', 'SubjectGroup')
    cardinality = '1*'
    inlined = True
    composite='object'

class uses(RelationDefinition):
    subject = 'Assessment'
    object = 'GenericTestRun'
    cardinality = '**'

class generates(RelationDefinition):
    subject = 'Assessment'
    object = 'GenericTestRun'
    cardinality = '?*'

class uses_device(RelationDefinition):
    subject = 'GenericTestRun'
    object = 'Device'
    cardinality = '?*'
    inlined = True

class measure(RelationDefinition):
    subject = 'ScoreValue'
    object = ('GenericMeasure', 'GenericTestRun')
    cardinality = '?*'
    inlined = True
    composite='object'

class protocols(RelationDefinition):
    subject = ('Assessment', 'ScoreDefinition', 'ScoreGroup',
               'Diagnostic', 'TechnicalAnalysis')
    object = 'Protocol'
    cardinality = '**'

class participates_in(RelationDefinition):
    subject = 'Center'
    object = 'Study'
    cardinality = '**'
