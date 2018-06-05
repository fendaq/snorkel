import bz2
import cPickle
import os

from snorkel.contrib.babble import Explanation

def get_user_lists():
    ctd_pickle_path = os.path.join(os.environ['SNORKELHOME'], 
                                   'tutorials/cdr/data/ctd.pkl.bz2') 
    print('Loading canonical ID ontologies...')
    with bz2.BZ2File(ctd_pickle_path, 'rb') as ctd_f:
        ctd_unspecified, ctd_therapy, ctd_marker = cPickle.load(ctd_f)
    print('Finished loading canonical ID ontologies.')
    user_lists = {
        'uncertain': ['combin', 'possible', 'unlikely'],
        'causal': ['causes', 'caused', 'induce', 'induces', 'induced', 'associated with'],
        'treat': ['treat', 'effective', 'prevent', 'resistant', 'slow', 'promise', 'therap'],
        'procedure': ['inject', 'administrat'],
        'patient': ['in a patient with', 'in patients with'],
        'weak': ['none', 'although', 'was carried out', 'was conducted', 'seems', 
                 'suggests', 'risk', 'implicated', 'the aim', 'to investigate',
                 'to assess', 'to study'],
        'ctd_unspecified': ctd_unspecified,
        'ctd_therapy': ctd_therapy,
        'ctd_marker': ctd_marker,
    }
    return user_lists

# NOTE: Candidates may come from any of the three splits, though most will be from dev.
basic = [
    # LF_c_cause_d
    Explanation(
        name='LF_c_cause_d',
        # original_condition="""any causal phrase is between the 
        #     chemical and the disease and the word 'not' is not between the 
        #     chemical and the disease""",
        condition="""between the chemical and the disease, 
            there is a causal word and the word 'not' is not between them.""",
        candidate="19211690::span:638:649~~19211690::span:688:699",
        label=True,
        semantics=('.root', ('.label', ('.bool', True), ('.and', ('.any', ('.map', ('.in', ('.extract_text', ('.between', ('.list', ('.arg', ('.int', 1)), ('.arg', ('.int', 2)))))), ('.user_list', ('.string', u'causal')))), ('.not', ('.call', ('.in', ('.extract_text', ('.between', ('.list', ('.arg', ('.int', 1)), ('.arg', ('.int', 2)))))), ('.string', u'not'))))))),
    # LF_c_d
    Explanation(
        name='LF_c_d',
        # original_condition="the disease is immediately after the chemical",
        condition="""the disease is immediately preceded by the chemical.""",
        candidate="18541230::span:38:62~~18541230::span:64:72",
        label=True,
        semantics=('.root', ('.label', ('.bool', True), ('.call', ('.in', ('.extract_text', ('.right', ('.arg', ('.int', 1)), ('.string', '.eq'), ('.int', 1), ('.string', 'words')))), ('.arg_to_string', ('.arg', ('.int', 2))))))),
    # LF_c_induced_d
    Explanation(
        name='LF_c_induced_d',
        # original_condition="""the disease is immediately after the 
        #     chemical and 'induc' or 'assoc' is in the chemical""",
        condition="""the disease is immediately preceded by the chemical, 
            and the chemical name contains an "induc" or "assoc" word.""",
        candidate="17285209::span:918:930~~17285209::span:932:941",
        label=True,
        semantics=('.root', ('.label', ('.bool', True), ('.and', ('.call', ('.in', ('.extract_text', ('.right', ('.arg', ('.int', 1)), ('.string', '.eq'), ('.int', 1), ('.string', 'words')))), ('.arg_to_string', ('.arg', ('.int', 2)))), ('.call', ('.composite_or', ('.contains',), ('.list', ('.string', u'induc'), ('.string', u'assoc'))), ('.arg_to_string', ('.arg', ('.int', 1)))))))),
    # LF_c_treat_d
    Explanation(
        name='LF_c_treat_d',
        # original_condition="""any word between the chemical and 
        #     the disease contains a treat word and the chemical is within 100 
        #     characters to the left of the disease""",
        condition="""the chemical precedes the disease by no more than 100 characters, 
            and a word between the disease and the chemical contains a word in the treat dictionary.""",
        candidate="9848575::span:1326:1332~~9848575::span:1374:1387",
        label=False,
        semantics=('.root', ('.label', ('.bool', False), ('.and', ('.call', ('.in', ('.extract_text', ('.left', ('.arg', ('.int', 2)), ('.string', '.leq'), ('.int', 100), ('.string', 'chars')))), ('.arg_to_string', ('.arg', ('.int', 1)))), ('.any', ('.map', ('.composite_or', ('.contains',), ('.user_list', ('.string', u'treat'))), ('.filter', ('.between', ('.list', ('.arg', ('.int', 1)), ('.arg', ('.int', 2)))), 'words', '\\w+\\S*'))))))),
    # LF_c_treat_d_wide
    Explanation(
        name='LF_c_treat_d_wide',
        # original_condition="""any word between the chemical and 
        #     the disease contains a treat word and the chemical is left of the 
        #     disease""",
        condition="""the chemical comes before the disease, 
            and a word between them contains a treat word.""",
        candidate="8841157::span:243:251~~8841157::span:365:376",
        label=False,
        semantics=('.root', ('.label', ('.bool', False), ('.and', ('.call', ('.in', ('.extract_text', ('.left', ('.arg', ('.int', 2))))), ('.arg_to_string', ('.arg', ('.int', 1)))), ('.any', ('.map', ('.composite_or', ('.contains',), ('.user_list', ('.string', u'treat'))), ('.filter', ('.between', ('.list', ('.arg', ('.int', 1)), ('.arg', ('.int', 2)))), 'words', '\\w+\\S*'))))))),
    # LF_ctd_marker_c_d
    Explanation(
        name='LF_ctd_marker_c_d',
        # original_condition="""the disease is immediately after the 
        #     chemical and the pair of canonical ids of the chemical and disease 
        #     is in ctd_marker""",
        condition="""the disease is immediately preceded by the chemical, 
            and the pair of the chemical and the disease canonical IDs appears in the ctd_marker dictionary.""",
        candidate="871943::span:35:49~~871943::span:51:56",
        label=True,
        semantics=('.root', ('.label', ('.bool', True), ('.and', ('.call', ('.in', ('.extract_text', ('.right', ('.arg', ('.int', 1)), ('.string', '.eq'), ('.int', 1), ('.string', 'words')))), ('.arg_to_string', ('.arg', ('.int', 2)))), ('.call', ('.in', ('.user_list', ('.string', u'ctd_marker'))), ('.tuple', ('.map', ('.cid',), ('.list', ('.arg', ('.int', 1)), ('.arg', ('.int', 2)))))))))),
    # LF_ctd_therapy_treat
    Explanation(
        name='LF_ctd_therapy_treat',
        # original_condition="""
        #     (any word between the chemical and the disease contains a treat word and the chemical is left of the 
        #     disease)
        #     and 
        #     (the pair of canonical ids of the chemical and disease is in ctd_therapy)""",
        condition="""Label false because
            (the chemical comes before the disease, and a word between them contains a treat word)
            and
            (the pair of the chemical and the disease canonical IDs appears in the ctd_therapy dictionary.)""",
        candidate="10728962::span:0:10~~10728962::span:50:60",
        label=False,
        semantics=('.root', ('.label', ('.bool', False), ('.and', ('.and', ('.call', ('.in', ('.extract_text', ('.left', ('.arg', ('.int', 2))))), ('.arg_to_string', ('.arg', ('.int', 1)))), ('.any', ('.map', ('.composite_or', ('.contains',), ('.user_list', ('.string', u'treat'))), ('.filter', ('.between', ('.list', ('.arg', ('.int', 1)), ('.arg', ('.int', 2)))), 'words', '\\w+\\S*')))), ('.call', ('.in', ('.user_list', ('.string', u'ctd_therapy'))), ('.tuple', ('.map', ('.cid',), ('.list', ('.arg', ('.int', 1)), ('.arg', ('.int', 2)))))))))),
    # LF_ctd_unspecified_treat
    Explanation(
        name='LF_ctd_unspecified_treat',
        # original_condition="""
        #     (any word between the chemical and the disease contains a treat word and the chemical is left of the 
        #     disease)
        #     and 
        #     (the pair of canonical ids of the chemical and disease is in ctd_unspecified)""",
        condition="""Label false because
            (the chemical comes before the disease, and a word between them contains a treat word)
            and
            (the pair of the chemical and the disease canonical IDs appears in the ctd_unspecified dictionary.)""",
        candidate="8841157::span:216:229~~8841157::span:365:376",
        label=False,
        semantics=('.root', ('.label', ('.bool', False), ('.and', ('.and', ('.call', ('.in', ('.extract_text', ('.left', ('.arg', ('.int', 2))))), ('.arg_to_string', ('.arg', ('.int', 1)))), ('.any', ('.map', ('.composite_or', ('.contains',), ('.user_list', ('.string', u'treat'))), ('.filter', ('.between', ('.list', ('.arg', ('.int', 1)), ('.arg', ('.int', 2)))), 'words', '\\w+\\S*')))), ('.call', ('.in', ('.user_list', ('.string', u'ctd_unspecified'))), ('.tuple', ('.map', ('.cid',), ('.list', ('.arg', ('.int', 1)), ('.arg', ('.int', 2)))))))))),
    # LF_d_following_c
    Explanation(
        name='LF_d_following_c',
        # original_condition="""'following' is between the disease 
        #     and the chemical and any word after the chemical contains a 
        #     procedure word""",
        condition="""'following' and a procedure word appear between the 
            chemical and the disease and the chemical comes after the disease.""",
        candidate='2312209::span:61:80~~2312209::span:0:20',
        label=True,
        semantics=('.root', ('.label', ('.bool', True), ('.and', ('.call', ('.in', ('.extract_text', ('.between', ('.list', ('.arg', ('.int', 1)), ('.arg', ('.int', 2)))))), ('.string', u'following')), ('.and', ('.any', ('.map', ('.in', ('.extract_text', ('.between', ('.list', ('.arg', ('.int', 1)), ('.arg', ('.int', 2)))))), ('.user_list', ('.string', u'procedure')))), ('.call', ('.in', ('.extract_text', ('.right', ('.arg', ('.int', 2))))), ('.arg_to_string', ('.arg', ('.int', 1))))))))),
    # LF_d_induced_by_c
    Explanation(
        name='LF_d_induced_by_c',
        # original_condition="""'induced by', 'caused by', or 'due to' 
        #     is between the disease and the chemical.""",
        condition=""""induced by", "caused by", or "due to" 
        appears between the chemical and the disease.""",
        candidate="11999899::span:1310:1318~~11999899::span:1278:1286",
        label=True,
        semantics=('.root', ('.label', ('.bool', True), ('.any', ('.map', ('.in', ('.extract_text', ('.between', ('.list', ('.arg', ('.int', 1)), ('.arg', ('.int', 2)))))), ('.list', ('.string', u'induced by'), ('.string', u'caused by'), ('.string', u'due to'))))))),
    # LF_d_induced_by_c_tight
    Explanation(
        name='LF_d_induced_by_c_tight',
        # original_condition="""'induced by', 'caused by', or 'due to' 
        #     is between the disease and the chemical and 'by' or 'to' is 
        #     immediately to the left of the chemical.""",
        condition="""the chemical is immediately preceded by 
            the word "by" or "to", and the words "induced by", "caused by", or "due to" 
            appear between the chemical and the disease.""",
        candidate="19721134::span:1065:1073~~19721134::span:1017:1026",
        label=True,
        semantics=('.root', ('.label', ('.bool', True), ('.and', ('.any', ('.map', ('.in', ('.extract_text', ('.left', ('.arg', ('.int', 1)), ('.string', '.eq'), ('.int', 1), ('.string', 'words')))), ('.list', ('.string', u'by'), ('.string', u'to')))), ('.call', ('.geq', ('.int', 1)), ('.sum', ('.map', ('.in', ('.extract_text', ('.between', ('.list', ('.arg', ('.int', 1)), ('.arg', ('.int', 2)))))), ('.list', ('.string', u'induced by'), ('.string', u'caused by'), ('.string', u'due to'))))))))),
    # LF_d_treat_c
    Explanation(
        name='LF_d_treat_c',
        # original_condition="""any word between the chemical and 
        #     the disease contains a treat word and the chemical is within 100
        #     characters to the right of the disease""",
        condition="""the disease precedes the chemical by no more than 100 characters, 
            and at least word between them contains a treat word.""",
        candidate="10091616::span:448:458~~10091616::span:125:134",
        label=False,
        semantics=('.root', ('.label', ('.bool', False), ('.and', ('.call', ('.in', ('.extract_text', ('.left', ('.arg', ('.int', 1)), ('.string', '.leq'), ('.int', 100), ('.string', 'chars')))), ('.arg_to_string', ('.arg', ('.int', 2)))), ('.any', ('.map', ('.in', ('.filter', ('.between', ('.list', ('.arg', ('.int', 1)), ('.arg', ('.int', 2)))), 'words', '\\w+\\S*')), ('.user_list', ('.string', u'treat')))))))),
    # LF_develop_d_following_c
    Explanation(
        name='LF_develop_d_following_c',
        # original_condition="""any word before the chemical contains 
        #     'develop' and 'following' is between the disease and the chemical""",
        condition="""a word containing 'develop' appears somewhere before the chemical, 
            and the word 'following' is between the disease and the chemical.""",
        candidate="19803309::span:292:304~~19803309::span:136:153",
        label=True,
        semantics=('.root', ('.label', ('.bool', True), ('.and', ('.call', ('.in', ('.extract_text', ('.left', ('.arg', ('.int', 1))))), ('.string', u'develop')), ('.call', ('.in', ('.extract_text', ('.between', ('.list', ('.arg', ('.int', 1)), ('.arg', ('.int', 2)))))), ('.string', u'following')))))),
    # LF_far_c_d
    Explanation(
        name='LF_far_c_d',
        # original_condition="""Label false if the disease is more than 100 characters
        #     to the right of the chemical.""",
        condition="""the chemical appears more than 100 characters before the disease.""",
        candidate="8841157::span:460:468~~8841157::span:365:376",
        label=False,
        semantics=('.root', ('.label', ('.bool', False), ('.call', ('.in', ('.extract_text', ('.left', ('.arg', ('.int', 2)), ('.string', '.gt'), ('.int', 100), ('.string', 'chars')))), ('.arg_to_string', ('.arg', ('.int', 1))))))),
    # LF_far_d_c
    Explanation(
        name='LF_far_d_c',
        # original_condition="""Label false if the chemical is more than 100 characters
        #     to the right of the disease.""",
        condition="""the disease appears more than 100 characters before the chemical.""",
        candidate="8841157::span:478:487~~8841157::span:365:376",
        label=False,
        semantics=('.root', ('.label', ('.bool', False), ('.call', ('.in', ('.extract_text', ('.left', ('.arg', ('.int', 1)), ('.string', '.gt'), ('.int', 100), ('.string', 'chars')))), ('.arg_to_string', ('.arg', ('.int', 2))))))),
    # LF_improve_before_disease
    Explanation(
        name='LF_improve_before_disease',
        # original_condition="""Label false if any word before the disease starts with 'improv'""",
        condition="""a word starting with "improv" appears before the chemical.""",
        candidate="19721134::span:1177:1180~~19721134::span:1017:1026",
        label=False,
        semantics=('.root', ('.label', ('.bool', False), ('.call', ('.geq', ('.int', 1)), ('.sum', ('.map', ('.startswith', ('.string', u'improv')), ('.filter', ('.left', ('.arg', ('.int', 1))), 'words', '\\w+\\S*'))))))),
    # LF_in_ctd_unspecified
    Explanation(
        name='LF_in_ctd_unspecified',
        # original_condition="""Label false if the pair of canonical ids of the chemical 
        #     and disease is in ctd_unspecified""",
        condition="""the pair of canonical IDs of the 
            chemical and the disease are in the ctd_unspecified dictionary.""",
        candidate="3780697::span:219:226~~3780697::span:103:121",
        label=False,
        semantics=('.root', ('.label', ('.bool', False), ('.call', ('.in', ('.user_list', ('.string', u'ctd_unspecified'))), ('.tuple', ('.map', ('.cid',), ('.list', ('.arg', ('.int', 1)), ('.arg', ('.int', 2))))))))),
    # LF_in_ctd_therapy
    Explanation(
        name='LF_in_ctd_therapy',
        # original_condition="""Label false if the pair of canonical ids of the chemical 
        #     and disease is in ctd_therapy""",
        condition="""the pair of canonical IDs of the 
            chemical and the disease are in the ctd_therapy dictionary.""",
        candidate="8841157::span:280:289~~8841157::span:365:376",
        label=False,
        semantics=('.root', ('.label', ('.bool', False), ('.call', ('.in', ('.user_list', ('.string', u'ctd_therapy'))), ('.tuple', ('.map', ('.cid',), ('.list', ('.arg', ('.int', 1)), ('.arg', ('.int', 2))))))))),
    # LF_in_ctd_marker
    Explanation(
        name='LF_in_ctd_marker',
        # original_condition="""Label true if the pair of canonical ids of the chemical 
        #     and disease is in ctd_marker""",
        condition="""the pair of canonical IDs of the 
            chemical and the disease are in the ctd_marker dictionary.""",
        candidate="8766220::span:531:538~~8766220::span:450:463",
        label=True,
        semantics=('.root', ('.label', ('.bool', True), ('.call', ('.in', ('.user_list', ('.string', u'ctd_marker'))), ('.tuple', ('.map', ('.cid',), ('.list', ('.arg', ('.int', 1)), ('.arg', ('.int', 2))))))))),
    # LF_in_patient_with
    Explanation(
        name='LF_in_patient_with',
        # original_condition="""Label false if any patient phrase is within four words 
        #     before the disease""",
        condition="""a patient phrase comes no more than 
            four words before the disease.""",
        candidate="11284996::span:46:57~~11284996::span:101:121",
        label=False,
        semantics=('.root', ('.label', ('.bool', False), ('.any', ('.map', ('.in', ('.extract_text', ('.left', ('.arg', ('.int', 2)), ('.string', '.leq'), ('.int', 4), ('.string', 'words')))), ('.user_list', ('.string', u'patient'))))))),
    # LF_induce
    Explanation(
        name='LF_induce',
        # original_condition="""any word between the chemical and the 
        #     disease contains 'induc'""",
        condition="""a word between the chemical and the 
            disease contains "induc".""",
        candidate="6728084::span:1197:1211~~6728084::span:1284:1315",
        label=True,
        semantics=('.root', ('.label', ('.bool', True), ('.any', ('.map', ('.contains', ('.string', u'induc')), ('.filter', ('.between', ('.list', ('.arg', ('.int', 1)), ('.arg', ('.int', 2)))), 'words', '\\w+\\S*')))))),
    # LF_induce_name
    Explanation(
        name='LF_induce_name',
        # original_condition="the chemical contains 'induc'",
        condition="""the chemical contains "induc".""",
        candidate="3131282::span:213:224~~3131282::span:230:254",
        label=True,
        semantics=('.root', ('.label', ('.bool', True), ('.call', ('.contains', ('.string', u'induc')), ('.arg_to_string', ('.arg', ('.int', 1))))))),
    # LF_induced_other
    Explanation(
        name='LF_induced_other',
        # original_condition="""Label false if any word between the chemical and the 
        #     disease ends with 'induced'""",
        condition="""a word between the chemical and the 
            disease ends with "induced".""",
        candidate="1564236::span:1176:1187~~1564236::span:1241:1257",
        label=False,
        semantics=('.root', ('.label', ('.bool', False), ('.any', ('.map', ('.endswith', ('.string', u'induced')), ('.filter', ('.between', ('.list', ('.arg', ('.int', 1)), ('.arg', ('.int', 2)))), 'words', '\\w+\\S*')))))),
    # LF_level
    Explanation(
        name='LF_level',
        # original_condition="""'level' comes after the chemical""",
        condition="""the word "level" comes after the chemical.""",
        candidate="8643973::span:167:171~~8643973::span:328:341",
        label=False,
        semantics=('.root', ('.label', ('.bool', False), ('.call', ('.in', ('.extract_text', ('.right', ('.arg', ('.int', 1))))), ('.string', u'level'))))),
    # LF_measure
    Explanation(
        name='LF_measure',
        # original_condition="""any word before the chemical starts 
        #     with 'measur'""",
        condition="""a word before the chemical starts 
            with "measur".""",
        candidate="18239197::span:367:381~~18239197::span:313:321",
        label=False,
        semantics=('.root', ('.label', ('.bool', False), ('.any', ('.map', ('.startswith', ('.string', u'measur')), ('.filter', ('.left', ('.arg', ('.int', 1))), 'words', '\\w+\\S*')))))),
    # LF_neg_d
    Explanation(
        name='LF_neg_d',
        # original_condition="""'none', 'not', or 'no' is within 30 
        #     characters to the left of the disease""",
        condition=""""none", "not", or "no" precedes the 
            disease by no more than 30 characters.
        """,
        candidate="14659530::span:1916:1919~~14659530::span:1850:1857",
        label=False,
        semantics=('.root', ('.label', ('.bool', False), ('.any', ('.map', ('.in', ('.extract_text', ('.left', ('.arg', ('.int', 2)), ('.string', '.leq'), ('.int', 30), ('.string', 'chars')))), ('.list', ('.string', u'none'), ('.string', u'not'), ('.string', u'no'))))))),
    # LF_risk_d
    Explanation(
        name='LF_risk_d',
        # original_condition="""the phrase 'risk of' occurs before 
        #     the disease""",
        condition=""""risk of" comes before the disease.""",
        candidate="7421734::span:393:401~~7421734::span:476:496",
        label=True,
        semantics=('.root', ('.label', ('.bool', True), ('.call', ('.in', ('.extract_text', ('.left', ('.arg', ('.int', 2))))), ('.string', u'risk of'))))),
    # LF_treat_d
    Explanation(
        name='LF_treat_d',
        # original_condition="""at least one treat word is less than
        #     50 characters before the disease""",
        condition="""there is at least one treat word 
            no more than 50 characters before the disease.""",
        candidate="14568327::span:932:935~~14568327::span:1075:1078",
        label=False, 
        semantics=('.root', ('.label', ('.bool', False), ('.call', ('.geq', ('.int', 1)), ('.sum', ('.map', ('.in', ('.extract_text', ('.left', ('.arg', ('.int', 2)), ('.string', '.leq'), ('.int', 50), ('.string', 'chars')))), ('.user_list', ('.string', u'treat')))))))),
    # LF_uncertain
    Explanation(
        name='LF_uncertain',
        # original_condition="""Label false if any word before the chemical starts with 
        #     an uncertain word""",
        condition="""the chemical is preceded by a word 
            that starts with a word that appears in the uncertain dictionary.
        """,
        candidate='11302406::span:985:993~~11302406::span:934:943',
        label=False,
        semantics=('.root', ('.label', ('.bool', False), ('.any', ('.map', ('.composite_or', ('.startswith',), ('.user_list', ('.string', u'uncertain'))), ('.filter', ('.left', ('.arg', ('.int', 1))), 'words', '\\w+\\S*')))))),
    # LF_weak_assertions
    Explanation(
        name='LF_weak_assertions',
        # original_condition="""at least one weak phrase is in 
        #     the sentence""",
        condition="""at least one weak phrase is in the sentence.""",
        candidate="10354657::span:1809:1815~~10354657::span:1732:1746",
        label=False,
        semantics=('.root', ('.label', ('.bool', False), ('.call', ('.geq', ('.int', 1)), ('.sum', ('.map', ('.in', ('.extract_text', ('.sentence',))), ('.user_list', ('.string', u'weak')))))))),
]

redundant = [
    # LF_ctd_unspecified_induce
    Explanation(
        name='LF_ctd_unspecified_induce',
        # original_condition="""Label True because
        #     (
        #         (the disease is immediately after the chemical and the chemical contains 'induc' or 'assoc')
        #         or
        #         ('induced by', 'caused by', or 'due to' is between the disease and the chemical)
        #     )
        #     and 
        #     (the pair of canonical ids of the chemical and disease is in ctd_unspecified)""",
        condition="""
            (
                (the disease is immediately preceded by the chemical, and the chemical name contains an "induc" or "assoc" word)
                or 
                ("induced by", "caused by", or "due to" appears between the chemical and the disease)
            )
            and
            (the pair of the chemical and the disease canonical IDs appears in the ctd_unspecified dictionary.)""",
        candidate=None,
        label=True,
        semantics=None),
    # LF_ctd_marker_induce
    Explanation(
        name='LF_ctd_marker_induce',
        # original_condition="""Label True because
        #     (
        #         (the disease is immediately after the chemical and the chemical contains 'induc' or 'assoc')
        #         or
        #         ('induced by', 'caused by', or 'due to' is between the disease and the chemical)
        #     )
        #     and 
        #     (the pair of canonical ids of the chemical and disease is in ctd_marker)""",
        condition="""
            (
                (the disease is immediately preceded by the chemical, and the chemical name contains an "induc" or "assoc" word)
                or 
                ("induced by", "caused by", or "due to" appears between the chemical and the disease)
            )
            and
            (the pair of the chemical and the disease canonical IDs appears in the ctd_marker dictionary.)""",
        candidate=None,
        label=True,
        semantics=None),
]

advanced = [
    # LF_closer_chem
    Explanation(
        name='LF_closer_chem',
        # original_condition=None,
        condition="",
        candidate=None,
        label=False,
        semantics=None),
    # LF_closer_dis
    Explanation(
        name='LF_closer_dis',
        # original_condition=None,
        condition="",
        candidate=None,
        label=False,
        semantics=None),
]

explanations = basic # + redundant + advanced

def get_explanations():
    return explanations

# DEPRECATED
# def load_examples(domain, candidates):
#     if domain == 'test':
#         examples = test_examples + 
#     elif domain == 'spouse':
#         examples = spouse_examples
#     elif domain == 'cdr':
#         examples = cdr_examples
#     else:
#         raise Exception("Invalid example set provided.")
    
#     candidate_dict = {hash(c) : c for c in candidates}
#     for example in examples:
#         if example.candidate and not isinstance(example.candidate, tuple):
#             example.candidate = candidate_dict[hash(example.candidate)]
#     # assert(example.candidate is not None for example in examples)
#     return examples