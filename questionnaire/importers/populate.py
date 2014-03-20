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
from random import randrange
from optparse import OptionParser
from datetime import timedelta, datetime

import numpy.random as nr

from cubicweb.dataimport import SQLGenObjectStore

from cubes.brainomics.importers.helpers import (get_image_info, import_genes,
                                                import_chromosomes, import_snps)


PROJECT_DATETIMES = (datetime.strptime('1/1/2010 1:30 PM', '%m/%d/%Y %I:%M %p'),
                     datetime.strptime('1/1/2013 4:50 AM', '%m/%d/%Y %I:%M %p'))


###############################################################################
### UTILITY FUNCTIONS #########################################################
###############################################################################
def random_date(_type=None):
    """
    This function will return a random datetime between two datetime
    objects.
    From http://stackoverflow.com/questions/553303/generate-a-random-date-between-two-other-dates
    """
    if _type=='age':
        start, end = AGE_DATETIMES[0], AGE_DATETIMES[1]
    else:
        start, end = PROJECT_DATETIMES[0], PROJECT_DATETIMES[1]
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return (start + timedelta(seconds=random_second))

def import_questionnaire(store, subject_eid, center_eid, study_eid,
                         questionnaire_eid, questions, label):
    date = random_date()
    assessment = store.create_entity('Assessment', identifier=u'%s_%s' % (label, subject_eid),
                                     datetime=date, protocol=u'Demo questionnaire')
    store.relate(assessment.eid, 'related_study', study_eid, subtype='Assessment')
    store.relate(center_eid, 'holds', assessment.eid)
    store.relate(subject_eid, 'concerned_by', assessment.eid)
    user_ident = nr.randint(10)
    user_ident = u'parent' if user_ident>8 else u'subject'
    q_qrun = store.create_entity('QuestionnaireRun', identifier=u'%s_%s' % (label, subject_eid),
                                   user_ident=user_ident, datetime=date,
                                   iteration=1, completed=True, valid=True,
                                   instance_of=questionnaire_eid)
    store.relate(q_qrun.eid, 'related_study', study_eid)
    store.relate(q_qrun.eid, 'concerns', subject_eid, subjtype='QuestionnaireRun')
    store.relate(assessment.eid, 'generates', q_qrun.eid, subjtype='Assessment')
    for name, (question, _min, _max) in questions.iteritems():
        score_value = store.create_entity('Answer', value=nr.randint(_min, _max),
                                          question=question, datetime=date,
                                          questionnaire_run=q_qrun.eid)


###############################################################################
### QUESTIONNAIRES ############################################################
###############################################################################
# ADOS
name = u'Autism Diagnostic Observation Schedule Module (ADOS)'
ados_questionnaire_eid = store.create_entity('Questionnaire', name=name,language=u'en', version=u'v 0.2.1', identifier=u'ados', type=u'behavioral').eid
ados_questions = {}
text = u'Autism Diagnostic Observation Schedule Module'
ados_questions['ados_module'] = (store.create_entity('Question', identifier=u'ados_module', position=0, text=text, type=u'numerical', questionnaire=ados_questionnaire_eid, possible_answers=u'1-4').eid, 1, 4)
text = u'Classical Total ADOS Score (Communication subscore + Social Interaction subscore)'
ados_questions['ados_total'] = (store.create_entity('Question', identifier=u'ados_total', position=1, text=text, type=u'numerical', questionnaire=ados_questionnaire_eid, possible_answers=u'0-22').eid, 0, 22)
text = u'Communication Total Subscore of the Classic ADOS'
ados_questions['ados_comm'] = (store.create_entity('Question', identifier=u'ados_comm', position=2, text=text, type=u'numerical', questionnaire=ados_questionnaire_eid, possible_answers=u'0-8').eid, 0, 8)
text = u'Social Total Subscore of the Classic ADOS'
ados_questions['ados_social'] = (store.create_entity('Question', identifier=u'ados_social', position=3, text=text, type=u'numerical', questionnaire=ados_questionnaire_eid, possible_answers=u'0-14').eid, 0, 14)
text = u'Stereotyped Behaviors and Restricted Interests Total Subscore of the Classic ADOS'
ados_questions['ados_stereo_behav'] = (store.create_entity('Question', identifier=u'ados_stereo_behav', position=4, text=text, type=u'numerical', questionnaire=ados_questionnaire_eid, possible_answers=u'0-8').eid, 0, 8)
text = u'Was ADOS scored and administered by research reliable personnel?'
possible_answers = u'0 = not research reliable; 1 = research reliable'
ados_questions['ados_rsrch_reliable'] = (store.create_entity('Question', identifier=u'ados_rsrch_reliable', position=5, text=text, type=u'boolean', questionnaire=ados_questionnaire_eid, possible_answers=possible_answers).eid, 0, 1)
text = u'Social Affect Total Subscore for Gotham Algorithm of the ADOS'
ados_questions['ados_gotham_soc_affect'] = (store.create_entity('Question', identifier=u'ados_gotham_soc_affect', position=6, text=text, type=u'numerical', questionnaire=ados_questionnaire_eid, possible_answers=u'0-20').eid, 0, 20)
text = u'Restrictive and Repetitive Behaviors Total Subscore for Gotham Algorithm of the ADOS'
ados_questions['ados_gotham_rrb'] = (store.create_entity('Question', identifier=u'ados_gotham_rrb', position=7, text=text, type=u'numerical', questionnaire=ados_questionnaire_eid, possible_answers=u'0-8').eid, 0, 8)
text = u'Social Affect Total + Restricted and Repetitive Behaviors Total'
ados_questions['ados_gotham_total'] = (store.create_entity('Question', identifier=u'ados_gotham_total', position=8, text=text, type=u'numerical', questionnaire=ados_questionnaire_eid, possible_answers=u'0-28').eid, 0, 28)
text = u'Individually Calibrated Severity Score for Gotham Algorithm of the ADOS'
ados_questions['ados_gotham_severity'] = (store.create_entity('Question', identifier=u'ados_gotham_severity', position=9, text=text, type=u'numerical', questionnaire=ados_questionnaire_eid, possible_answers=u'1-10').eid, 1, 10)

# VINELAND
vineland_questionnaire_eid = store.create_entity('Questionnaire', name=u'Vineland Adaptive Behavior Scales', identifier=u'vineland', language=u'fr', version=u'v 0.1.0', type=u'behavioral').eid
vineland_questions = {}
text = u'Vineland Adaptive Behavior Scales Receptive Language V Scaled Score'
vineland_questions['vineland_receptive_v_scaled'] = (store.create_entity('Question', identifier=u'vineland_receptive_v_scaled', position=0, text=text, type=u'numerical', questionnaire=vineland_questionnaire_eid, possible_answers=u'1-24').eid, 1, 24)
text = u'Vineland Adaptive Behavior Scales Expressive Language V Scaled Score'
vineland_questions['vineland_expressive_v_scaled'] = (store.create_entity('Question', identifier=u'vineland_expressive_v_scaled', position=1, text=text, type=u'numerical', questionnaire=vineland_questionnaire_eid, possible_answers=u'1-24').eid, 1, 24)
text = u'Vineland Adaptive Behavior Scales Written Language V Scaled Score'
vineland_questions['vineland_written_v_scaled'] = (store.create_entity('Question', identifier=u'vineland_written_v_scaled', position=2, text=text, type=u'numerical', questionnaire=vineland_questionnaire_eid, possible_answers=u'1-24').eid, 1, 24)
text = u'Vineland Adaptive Behavior Scales Communication Standard Score'
vineland_questions['vineland_communication_standard'] = (store.create_entity('Question', identifier=u'vineland_communication_standard', position=3, text=text, type=u'numerical', questionnaire=vineland_questionnaire_eid, possible_answers=u'20-160').eid, 20, 160)
text = u'Vineland Adaptive Behavior Scales Personal Daily Living Skills V Scaled Score'
vineland_questions['vineland_personal_v_scaled'] = (store.create_entity('Question', identifier=u'vineland_personal_v_scaled', position=4, text=text, type=u'numerical', questionnaire=vineland_questionnaire_eid, possible_answers=u'1-24').eid, 1, 24)
text = u'Vineland Adaptive Behavior Scales Domestic Daily Living Skills V Scaled Score'
vineland_questions['vineland_domestic_v_scaled'] = (store.create_entity('Question', identifier=u'vineland_domestic_v_scaled', position=5, text=text, type=u'numerical', questionnaire=vineland_questionnaire_eid, possible_answers=u'1-24').eid, 1, 24)
text = u'Vineland Adaptive Behavior Scales Community Daily Living Skills V Scaled Score'
vineland_questions['vineland_community_v_scaled'] = (store.create_entity('Question', identifier=u'vineland_community_v_scaled', position=6, text=text, type=u'numerical', questionnaire=vineland_questionnaire_eid, possible_answers=u'1-24').eid, 1, 24)
text = u'Vineland Adaptive Behavior Scales Daily Living Skills Standard Score'
vineland_questions['vineland_dailylvng_standard'] = (store.create_entity('Question', identifier=u'vineland_dailylvng_standard', position=7, text=text, type=u'numerical', questionnaire=vineland_questionnaire_eid, possible_answers=u'20-160').eid, 20, 160)
text = u'Vineland Adaptive Behavior Scales Interpersonal Relationships V Scaled Score'
vineland_questions['vineland_interpersonal_v_scaled'] = (store.create_entity('Question', identifier=u'vineland_interpersonal_v_scaled', position=8, text=text, type=u'numerical', questionnaire=vineland_questionnaire_eid, possible_answers=u'1-24').eid, 1, 24)
text = u'Vineland Adaptive Behavior Scales Play and Leisure Time V Scaled Score'
vineland_questions['vineland_play_v_scaled'] = (store.create_entity('Question', identifier=u'vineland_play_v_scaled', position=9, text=text, type=u'numerical', questionnaire=vineland_questionnaire_eid, possible_answers=u'1-24').eid, 1, 24)
text = u'Vineland Adaptive Behavior ScalesCoping Skills V Scaled Score'
vineland_questions['vineland_coping_v_scaled'] = (store.create_entity('Question', identifier=u'vineland_coping_v_scaled', position=10, text=text, type=u'numerical', questionnaire=vineland_questionnaire_eid, possible_answers=u'1-24').eid, 1, 24)
text = u'Vineland Adaptive Behavior Scales Socialization Standard Score'
vineland_questions['vineland_social_standard'] = (store.create_entity('Question', identifier=u'vineland_social_standard', position=11, text=text, type=u'numerical', questionnaire=vineland_questionnaire_eid, possible_answers=u'20-160').eid, 20, 160)
text = u'Sum of Vineland Standard Scores (Communication + Daily Living Skills + Socialization)'
vineland_questions['vineland_sum_scores'] = (store.create_entity('Question', identifier=u'vineland_sum_scores', position=12, text=text, type=u'numerical', questionnaire=vineland_questionnaire_eid, possible_answers=u'76-480').eid, 76, 480)
text = u'Vineland Adaptive Behavior Composite Standard score'
vineland_questions['vineland_abc_standard'] = (store.create_entity('Question', identifier=u'vineland_abc_standard', position=13, text=text, type=u'numerical', questionnaire=vineland_questionnaire_eid, possible_answers=u'20-160').eid, 20, 160)
text = u'Vineland Adaptive Behavior Scales Informant'
vineland_questions['vineland_informant'] = (store.create_entity('Question', identifier=u'vineland_informant', position=14, text=text, type=u'numerical', questionnaire=vineland_questionnaire_eid, possible_answers=u'1 = parent; 2 = self').eid, 1, 2)

store.flush()
store.commit()
