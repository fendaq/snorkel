import os

from snorkel.contrib.babble import Explanation

# Read in known Kinase Protein pairs and save as set of tuples
def strip_special(s):
    return "".join(c for c in s if ord(c) < 128)

with open(os.environ['SNORKELHOME'] + "/experiments/babble/protein/data/string_LRRK2_interactors.csv", "rb") as f:
    known_targets = set(
        tuple(strip_special(x).strip().split(",")) for x in f.readlines())

def get_user_lists():
    return {
        'known_targets': known_targets,
        'coimmunopr' : ["coimmunoprecipitat.", "co-immunoprecipitat."],
        'substrate' : ["substrate"],
        'between' : ["between"],
        'bindmid' : ["bind", "bound", "binds", "colocalizes", "co-localizes", "interacts", "interact"],
        'int_ind' : [ "bind", "interact", "form", "complex", "binding", "interaction", "influence", "phosphorylation" ],
        'interaction_indicators' : [ "bind", "interact", "form", "complex", "binding", "interaction", "influence", "phosphorylation", "influences", "influenced", "formed", "formation", "physical" ],
        'interact' : ["interact", "interaction", "interacts", "interacted"],
        'mutations' :["mutate", "mutant", "mutation", "mutations", "null", "dosage", "SNP", "SNPs", "variant", "knockout", "knockdown", "ko", "kd", "-/-", "(-)/(-)","(-/-)", "+/-", "deletion"] ,
        'neg_ind' : [ " no ", " not ", "fail", "absence", "negative", "expression", "DNA", "RNA", 'induc', 'sequenc', 'activ' ],
        'negative' : ["no", "not", "none"],
        'negexp' : ["phosphorylation", "phosphorylate", "phosphorylated", "phosphorylates" ],
        'nucleic_acids' : ["mRNA", "RNA", "DNA"],
        'positive' : ["evidence", "clearly", "indicate", "show"],
        'prep' : ["by", "with"],
        'prep2' : ["on", "in", "to"],
        'signexp' : [ "mitogen", "signal", "cascade", "pathway", "MAPK", "ligand", "signaling" ],
        'work' : ["work", "worked", "works"],
        'phosphory' : [ "phosphorylation", "phosphorylate", "phosphorylated", "phosphorylates" ],
        'influence' : [ "influence", "influenced", "influences", "modulate", "modulated", "modulates" ],
        'uncertain' : [ "possible", "unlikely", "potential", "putative", "hypothetic", "seemingly", "assume", "postulated" ],
        'residue': ['ser', 'serine', 'tyr', 'tyrosine', 'thr', 'threonine'] # approximation of the regex defined down below
    }

explanations = [

    Explanation(
        name="LF_by_with",
        label=True,  
        condition="a prep word is between Protein and Kinase and no negative words are between Protein and Kinase and the total number of words between Protein and Kinase is smaller than 10",
        candidate="10946297::span:893:900~~10946297::span:920:923",
        semantics=('.root', ('.label', ('.bool', True), ('.and', ('.any', ('.map', ('.in', ('.extract_text', ('.between', ('.list', ('.arg', ('.int', 1)), ('.arg', ('.int', 2)))))), ('.user_list', ('.string', u'prep')))), ('.and', ('.none', ('.map', ('.in', ('.extract_text', ('.between', ('.list', ('.arg', ('.int', 1)), ('.arg', ('.int', 2)))))), ('.user_list', ('.string', u'negative')))), ('.call', ('.lt', ('.int', 10)), ('.count', ('.between', ('.list', ('.arg', ('.int', 1)), ('.arg', ('.int', 2))))))))))
    ),
    #These findings demonstrate that the negative regulation of Th2 cytokine production by the JNK1 signaling pathway is essential for generating Th1-polarized immunity against intracellular pathogens, such as Leishmania major.

    Explanation(
        name="LF_NucAc_in_sentence",
        label=False,
        condition="sentence contains a nucleic_acids word",
        candidate="10022881::span:1420:1422~~10022881::span:1509:1512",
        semantics=('.root', ('.label', ('.bool', False), ('.any', ('.map', ('.in', ('.extract_text', ('.sentence',))), ('.user_list', ('.string', u'nucleic_acids'))))))
    ),
    #The elimination of mRNA, protein, and JNK activities lasted 48 and 72 h following a single Lipofectin treatment with antisense JNK1 and JNK2, respectively, indicating sufficient duration for examining the impact of specific elimination on the phenotype.

    Explanation(
        name="LF_activate_B",
        label=True,
        condition="'activ' is within 40 characters between Kinase and Protein ",
        candidate="10022864::span:1054:1058~~10022864::span:1026:1029",
        semantics=('.root', ('.label', ('.bool', True), ('.and', ('.call', ('.in', ('.extract_text', ('.between', ('.list', ('.arg', ('.int', 1)), ('.arg', ('.int', 2)))))), ('.string', u'activ')), ('.call', ('.composite_and_func', ('.list', ('.in', ('.extract_text', ('.within', ('.arg', ('.int', 1)), ('.int', 40), ('.string', 'chars')))), ('.in', ('.extract_text', ('.within', ('.arg', ('.int', 2)), ('.int', 40), ('.string', 'chars')))))), ('.string', u'activ')))))
    ),
    #To investigate the significance of JNK1 for transactivation of c-jun, we analyzed the effect of UV irradiation on c-jun expression under conditions of wortmannin-mediated inhibition of UV-induced stimulation of JNK1.

    Explanation(
        name="LF_activates",
        label=True,
        condition="sentence contains 'activates' and Kinase and Protein are less than 6 words apart.",
        candidate="22724072::span:1248:1253~~22724072::span:1204:1208",
        semantics=('.root', ('.label', ('.bool', True), ('.and', ('.call', ('.contains', ('.string', u'activates')), ('.extract_text', ('.sentence',))), ('.call', ('.in', ('.extract_text', ('.right', ('.arg', ('.int', 2)), ('.string', '.lt'), ('.int', 6), ('.string', 'words')))), ('.arg_to_string', ('.arg', ('.int', 1)))))))
    ),
    # These results provide the first evidence that PINK1 is activated following Deltapsim depolarization and suggest that PINK1 directly phosphorylates and activates Parkin.

    Explanation(
        name="LF_associat_with",
        label=False,
        condition="sentence contains 'associat' and 'with' separated by between 0 and 12 characters",
        candidate="12161751::span:1280:1283~~12161751::span:1304:1307",
        semantics=('.root', ('.label', ('.bool', False), ('.all', ('.map', ('.in', ('.extract_text', ('.sentence',))), ('.list', ('.string', u'associat'), ('.string', u'with')))))) # NOTE: do not have way to check distance between two non-arg words
    ),
    #Failure to survive is associated with decreased expression of Bcl2, and the effect of Jnk1 deficiency can be rescued by transgenic expression of Bcl2

    Explanation(
        name="LF_between_before",
        label=True,
        condition="the word 'between' is within 50 characters before the Protein or the Kinase and the word 'and' is within 40 characters between Protein and Kinase",
        candidate="10449033::span:2577:2579~~10449033::span:2611:2614",
        semantics=('.root', ('.label', ('.bool', True), ('.and', ('.call', ('.composite_or_func', ('.list', ('.in', ('.extract_text', ('.left', ('.arg', ('.int', 1)), ('.string', '.leq'), ('.int', 50), ('.string', 'chars')))), ('.in', ('.extract_text', ('.left', ('.arg', ('.int', 2)), ('.string', '.leq'), ('.int', 50), ('.string', 'chars')))))), ('.string', u'between')), ('.and', ('.call', ('.composite_or_func', ('.list', ('.in', ('.extract_text', ('.within', ('.arg', ('.int', 1)), ('.int', 40), ('.string', 'chars')))), ('.in', ('.extract_text', ('.within', ('.arg', ('.int', 2)), ('.int', 40), ('.string', 'chars')))))), ('.string', u'and')), ('.call', ('.in', ('.extract_text', ('.between', ('.list', ('.arg', ('.int', 1)), ('.arg', ('.int', 2)))))), ('.string', u'and'))))))
    ),
    #Our results provide evidence for a novel connection between p53 status and the basal level of JNK1, a critical enzyme in the stress-activated protein kinase family.

    Explanation(
        name="LF_bind_B_I",
        label=True,
        condition="a bindmid word is between Kinase and Protein and no neg_ind words are in the sentence",
        candidate="11108663::span:863:865~~11108663::span:849:852",
        semantics=('.root', ('.label', ('.bool', True), ('.and', ('.any', ('.map', ('.in', ('.extract_text', ('.between', ('.list', ('.arg', ('.int', 1)), ('.arg', ('.int', 2)))))), ('.user_list', ('.string', u'bindmid')))), ('.none', ('.map', ('.in', ('.extract_text', ('.sentence',))), ('.user_list', ('.string', u'neg_ind')))))))
    ),
    #JNK1 bound to p53, and the amount of JNK1-bound p53 accurately reflected the amount of total cellular p53.

    Explanation(
        name="LF_close_I",
        label=True,
        condition="the number of words between Kinase and Protein is less than 6 and the sentence contains at least one of the int_ind words is in the sentence and none of the negative words are in the sentence and the order of appearance in the sentence is Kinase, Protein and Kinase and Protein are not separated by 'and', 'or', ',' ",
        candidate="10075927::span:431:434~~10075927::span:411:414",
        semantics=('.root', ('.label', ('.bool', True), ('.and', ('.call', ('.lt', ('.int', 6)), ('.count', ('.between', ('.list', ('.arg', ('.int', 1)), ('.arg', ('.int', 2)))))), ('.and', ('.call', ('.geq', ('.int', 1)), ('.sum', ('.map', ('.in', ('.extract_text', ('.sentence',))), ('.user_list', ('.string', u'int_ind'))))), ('.and', ('.none', ('.map', ('.in', ('.extract_text', ('.sentence',))), ('.user_list', ('.string', u'negative')))), ('.and', ('.call', ('.in', ('.extract_text', ('.left', ('.arg', ('.int', 1))))), ('.arg_to_string', ('.arg', ('.int', 2)))), ('.none', ('.map', ('.composite_or', ('.eq',), ('.user_list', ('.string', u'between'))), ('.list', ('.string', u'and'), ('.string', u'or'), ('.string', u','))))))))))
    ),
    #JNK1 phosphorylates E2F1 in vitro, and co-transfection of JNK1 reduces the DNA binding activity of E2F1; treatment of cells with TNFalpha had a similar effect.

    Explanation(
        name="LF_comma",
        label=False,
        condition="there is a ',' between Protein and Kinase with up to 30 characters before and after the ','",
        candidate="10022881::span:449:451~~10022881::span:454:457",
        semantics=('.root', ('.label', ('.bool', False), ('.and', ('.call', ('.in', ('.extract_text', ('.between', ('.list', ('.arg', ('.int', 1)), ('.arg', ('.int', 2)))))), ('.string', u',')), ('.call', ('.composite_and_func', ('.list', ('.in', ('.extract_text', ('.within', ('.arg', ('.int', 1)), ('.int', 30), ('.string', 'chars')))), ('.in', ('.extract_text', ('.within', ('.arg', ('.int', 2)), ('.int', 30), ('.string', 'chars')))))), ('.string', u',')))))
    ),
    #Several isoforms families of JNK, JNK1, JNK2, and JNK3, have been isolated; they arise from alternative splicing of three different genes and have distinct substrate binding properties.
    Explanation(
        name="LF_complex_L",
        label=True,
        condition="'complex' is within 50 characters left of Protein or Kinase and there are between 0 and 50 characters between Protein and Kinase and the sentence does not contain 'not' or 'no' within 50 characters left of Protein or Kinase",
        candidate="17719230::span:441:443~~17719230::span:469:472",
        semantics=('.root', ('.label', ('.bool', True), ('.and', ('.call', ('.composite_or_func', ('.list', ('.in', ('.extract_text', ('.left', ('.arg', ('.int', 1)), ('.string', '.leq'), ('.int', 50), ('.string', 'chars')))), ('.in', ('.extract_text', ('.left', ('.arg', ('.int', 2)), ('.string', '.leq'), ('.int', 50), ('.string', 'chars')))))), ('.string', u'complex')), ('.and', ('.call', ('.leq', ('.int', 50)), ('.count', ('.filter', ('.between', ('.list', ('.arg', ('.int', 1)), ('.arg', ('.int', 2)))), 'chars', None))), ('.none', ('.map', ('.composite_or_func', ('.list', ('.in', ('.extract_text', ('.left', ('.arg', ('.int', 1)), ('.string', '.leq'), ('.int', 50), ('.string', 'chars')))), ('.in', ('.extract_text', ('.left', ('.arg', ('.int', 2)), ('.string', '.leq'), ('.int', 50), ('.string', 'chars')))))), ('.list', ('.string', u'not'), ('.string', u'no'))))))))
    ),
    #Here we show that ASK1, a MAPKKK that activates two SAPKs, c-Jun N-terminal-kinase (JNK) and p38, is present in a complex containing APP, phospho-MKK6, JIP1 and JNK1.#example needed

    Explanation(
        name="LF_complex_R",
        label=True,
        condition="'complex' is within 50 characters right of Protein or Kinase and there are between 0 and 50 characters between Protein and Kinase and the sentence does not contain 'not' or 'no' within 50 signs right of Protein or Kinase",
        candidate="19306499::span:438:443~~19306499::span:432:436",
        semantics=('.root', ('.label', ('.bool', True), ('.and', ('.call', ('.composite_or_func', ('.list', ('.in', ('.extract_text', ('.right', ('.arg', ('.int', 1)), ('.string', '.leq'), ('.int', 50), ('.string', 'chars')))), ('.in', ('.extract_text', ('.right', ('.arg', ('.int', 2)), ('.string', '.leq'), ('.int', 50), ('.string', 'chars')))))), ('.string', u'complex')), ('.and', ('.call', ('.leq', ('.int', 50)), ('.count', ('.filter', ('.between', ('.list', ('.arg', ('.int', 1)), ('.arg', ('.int', 2)))), 'chars', None))), ('.none', ('.map', ('.composite_or_func', ('.list', ('.in', ('.extract_text', ('.left', ('.arg', ('.int', 1)), ('.string', '.leq'), ('.int', 50), ('.string', 'chars')))), ('.in', ('.extract_text', ('.left', ('.arg', ('.int', 2)), ('.string', '.leq'), ('.int', 50), ('.string', 'chars')))))), ('.list', ('.string', u'not'), ('.string', u'no'))))))))
    ),
    #A study in mice,reported by Xiong et al. in this issue of the JCI, demonstrates that Pink1,Parkin, and DJ-1 can form a complex in the cytoplasm, with Pink1 and DJ-1 promoting the E3 ubiquitin ligase activity of Parkin to degrade substrates via the proteasome.

    Explanation(
        name="LF_dist_sup",
        label=True,
        condition="The Kinase and Protein pair correspond to pairs in the list known_targets and the order of appearance in the sentence is Kinase, Protein and Kinase and Protein are separated by less than 8 words",
        candidate="19027715::span:434:436~~19027715::span:379:383",
        semantics=('.root', ('.label', ('.bool', True), ('.and', ('.call', ('.in', ('.user_list', ('.string', u'known_targets'))), ('.tuple', ('.list', ('.arg_to_string', ('.arg', ('.int', 2))), ('.arg_to_string', ('.arg', ('.int', 1)))))), ('.and', ('.call', ('.in', ('.extract_text', ('.left', ('.arg', ('.int', 1))))), ('.arg_to_string', ('.arg', ('.int', 2)))), ('.call', ('.in', ('.extract_text', ('.right', ('.arg', ('.int', 1)), ('.string', '.lt'), ('.int', 8), ('.string', 'words')))), ('.arg_to_string', ('.arg', ('.int', 2))))))))
    ),
    #Recombinant LRRK2 was shown to autophosphorylate and phosphorylate MBP and a peptide (LRRKtide) corresponding to the T558 [corrected] site in moesin.
    #COMMENT: this function works only with a small subset of known interactors. It is subseptible to unrelated co-mentions of Kinases and Proteins.

    Explanation(
        name="LF_distant",
        label=False,
        condition="There are between 150 and 500 characters between Kinase and Protein",
        candidate="10022864::span:1777:1781~~10022864::span:1611:1614",
        semantics=('.root', ('.label', ('.bool', False), ('.and', ('.call', ('.gt', ('.int', 150)), ('.count', ('.filter', ('.between', ('.list', ('.arg', ('.int', 1)), ('.arg', ('.int', 2)))), 'chars', None))), ('.call', ('.lt', ('.int', 500)), ('.count', ('.filter', ('.between', ('.list', ('.arg', ('.int', 1)), ('.arg', ('.int', 2)))), 'chars', None))))))
    ),
    #Based on the data, we suggest that JNK1 stimulation is not essential for transactivation of c-jun after UV exposure, whereas activation of ERK2 is required for UV-induced signaling leading to elevated c-jun expression.

    Explanation(
        name="LF_induc",
        label=False,
        condition="the sentence contains 'induc'.",
        candidate="10022864::span:1534:1538~~10022864::span:1480:1483",
        semantics=('.root', ('.label', ('.bool', False), ('.call', ('.contains', ('.string', u'induc')), ('.extract_text', ('.sentence',)))))
    ),
    #In contrast, the mitogen-activated protein kinase/ERK kinase inhibitor PD98056, which blocked ERK2 but not JNK1 activation by UV irradiation, impaired UV-driven c-Jun protein induction and AP-1 binding.

    Explanation(
        name="LF_influence_B",
        label=True,
        condition="'influenc' within 100 characters between Protein and Kinase",
        candidate="28353286::span:803:817~~28353286::span:751:755",
        semantics=('.root', ('.label', ('.bool', True), ('.call', ('.composite_and_func', ('.list', ('.in', ('.extract_text', ('.within', ('.arg', ('.int', 1)), ('.int', 100), ('.string', 'chars')))), ('.in', ('.extract_text', ('.within', ('.arg', ('.int', 2)), ('.int', 100), ('.string', 'chars')))))), ('.string', u'influenc'))))
    ),
    #Thus, LRRK2 dysfunction may influence the accumulation of alpha-synuclein and its pathology through diverse pathomechanisms altering cellular functions and signaling pathways, including immune system, autophagy, vesicle trafficking, and retromer complex modulation.

    Explanation(
        name="LF_interact_in_sentence",
        label=True,
        condition="sentence contains 'interact' and the number of words between Protein and Kinase is smaller than 8",
        candidate="12503078::span:1258:1260~~12503078::span:1276:1279",
        semantics=('.root', ('.label', ('.bool', True), ('.and', ('.call', ('.contains', ('.string', u'interact')), ('.extract_text', ('.sentence',))), ('.call', ('.lt', ('.int', 8)), ('.count', ('.between', ('.list', ('.arg', ('.int', 1)), ('.arg', ('.int', 2)))))))))
    ),
    #We also demonstrated protein-protein interactions between the p53, p21waf1, and JNK1 proteins in this cell line.

    Explanation(
        name="LF_interaction",
        label=True,
        condition="Sentence contains one or more of interaction_indicators words and Kinase and Protein are less than 8 words apart and none of the neg_ind words are in the sentence and 'induc', 'sequenc', and 'activ' are not in the sentence. ",
        candidate="18932217::span:343:346~~18932217::span:372:375",
        semantics=('.root', ('.label', ('.bool', True), ('.and', ('.any', ('.map', ('.in', ('.extract_text', ('.sentence',))), ('.user_list', ('.string', u'interaction_indicators')))), ('.and', ('.call', ('.lt', ('.int', 8)), ('.count', ('.filter', ('.between', ('.list', ('.arg', ('.int', 1)), ('.arg', ('.int', 2)))), 'words', '\\w+\\S*'))), ('.and', ('.none', ('.map', ('.in', ('.extract_text', ('.sentence',))), ('.user_list', ('.string', u'neg_ind')))), ('.none', ('.map', ('.in', ('.extract_text', ('.sentence',))), ('.list', ('.string', u'induc'), ('.string', u'sequenc'), ('.string', u'activ')))))))))
    ),
    #Co-immunoprecipitation and two-hybrid-based protein-protein interaction studies show now that Daxx and GLUT4 interact with JNK1 through D-sites in their NH(2)-(aa 1-501) and large endofacial loop, respectively.

    Explanation(
        name="LF_levels",
        label=False,
        condition="the word 'level' appears in the sentence",
        candidate="10200552::span:214:218~~10200552::span:290:293",
        semantics=('.root', ('.label', ('.bool', False), ('.call', ('.in', ('.extract_text', ('.sentence',))), ('.string', u'level'))))
    ),
    #We describe here that IL-2 deprivation-induced apoptosis in TS1alphabeta cells does not modify c-Jun protein levels and correlates Bcl-2 downregulation and an increase in JNK1, but not JNK2, activity directly related to the induction of apoptosis.
        
    Explanation(
        name="LF_mutation_list_I",
        label=False,
        condition="The sentence contains a mutations word",
        candidate="10228165::span:861:865~~10228165::span:888:891",
        semantics=('.root', ('.label', ('.bool', False), ('.any', ('.map', ('.in', ('.extract_text', ('.sentence',))), ('.user_list', ('.string', u'mutations'))))))
    ),
    #Whereas NF-kappaB activation by LMP1 was blocked by a dominant-negative TRADD mutant, LMP1 induces JNK1 independently of the TRADD death domain and TRAF2, which binds to TRADD.

    Explanation(
        name="LF_no_B",
        label=False,
        condition="A negative word is within 100 characters between Protein and Kinase",
        candidate="10022864::span:1668:1672~~10022864::span:1611:1614",
        semantics=('.root', ('.label', ('.bool', False), ('.any', ('.map', ('.composite_and_func', ('.list', ('.in', ('.extract_text', ('.within', ('.arg', ('.int', 1)), ('.int', 100), ('.string', 'chars')))), ('.in', ('.extract_text', ('.within', ('.arg', ('.int', 2)), ('.int', 100), ('.string', 'chars')))))), ('.user_list', ('.string', u'negative'))))))
    ),
    #Based on the data, we suggest that JNK1 stimulation is not essential for transactivation of c-jun after UV exposure, whereas activation of ERK2 is required for UV-induced signaling leading to elevated c-jun expression.

    Explanation(
        name="LF_phosphory",
        label=True,
        condition="At least one of the words 'phosphorylation', 'phosphorylate', 'phosphorylated', 'phosphorylates' is found in the sentence and the number of words between Protein and Kinase is smaller than 8 and no neg_ind words in the sentence.",
        candidate="15228592::span:439:441~~15228592::span:405:408",
        semantics=('.root', ('.label', ('.bool', True), ('.and', ('.call', ('.geq', ('.int', 1)), ('.sum', ('.map', ('.in', ('.extract_text', ('.sentence',))), ('.list', ('.string', u'phosphorylation'), ('.string', u'phosphorylate'), ('.string', u'phosphorylated'), ('.string', u'phosphorylates'))))), ('.and', ('.call', ('.lt', ('.int', 8)), ('.count', ('.between', ('.list', ('.arg', ('.int', 1)), ('.arg', ('.int', 2)))))), ('.none', ('.map', ('.in', ('.extract_text', ('.sentence',))), ('.user_list', ('.string', u'neg_ind'))))))))
    ),
    #Here we show that c-Jun N-terminal kinases JNK1, JNK2 and JNK3 phosphorylate tau at many serine/threonine-prolines, as assessed by the generation of the epitopes of phosphorylation-dependent anti-tau antibodies.

    Explanation(
        name="LF_prepositions_I",
        label=True,
        condition="The words 'on', 'in', or 'to' are within 60 characters between Kinase and Protein and there are less than 8 words between Kinase and Protein and no neg_ind words are in the sentence.",
        candidate="11108663::span:863:865~~11108663::span:849:852",
        semantics=('.root', ('.label', ('.bool', True), ('.and', ('.any', ('.map', ('.composite_and_func', ('.list', ('.in', ('.extract_text', ('.within', ('.arg', ('.int', 1)), ('.int', 60), ('.string', 'chars')))), ('.in', ('.extract_text', ('.within', ('.arg', ('.int', 2)), ('.int', 60), ('.string', 'chars')))))), ('.list', ('.string', u'on'), ('.string', u'in'), ('.string', u'to')))), ('.and', ('.call', ('.lt', ('.int', 8)), ('.count', ('.filter', ('.between', ('.list', ('.arg', ('.int', 1)), ('.arg', ('.int', 2)))), 'words', '\\w+\\S*'))), ('.none', ('.map', ('.in', ('.extract_text', ('.sentence',))), ('.user_list', ('.string', u'neg_ind'))))))))
    ),
    #JNK1 bound to p53, and the amount of JNK1-bound p53 accurately reflected the amount of total cellular p53.

    Explanation(
        name="LF_regulate_Betw",
        label=True,
        condition="'regulat' is within 100 characters between Kinase and Protein ",
        candidate="18957282::span:504:509~~18957282::span:468:472",
        semantics=('.root', ('.label', ('.bool', True), ('.call', ('.composite_and_func', ('.list', ('.in', ('.extract_text', ('.within', ('.arg', ('.int', 1)), ('.int', 100), ('.string', 'chars')))), ('.in', ('.extract_text', ('.within', ('.arg', ('.int', 2)), ('.int', 100), ('.string', 'chars')))))), ('.string', u'regulat'))))
    ),
    #PINK1 regulates the localization of Parkin to the mitochondria in its kinase activity-dependent manner.

    Explanation(
        name="LF_residue",
        label=True,
        condition="any of the words in list residue is found in sentence and no neg_ind words are in the sentence and Kinase and Protein are separated by less than 6 words.",
        candidate="20659021::span:545:550~~20659021::span:533:537",
        semantics=('.root', ('.label', ('.bool', True), ('.and', ('.any', ('.map', ('.in', ('.extract_text', ('.sentence',))), ('.user_list', ('.string', u'residue')))), ('.and', ('.none', ('.map', ('.in', ('.extract_text', ('.sentence',))), ('.user_list', ('.string', u'neg_ind')))), ('.call', ('.lt', ('.int', 6)), ('.count', ('.filter', ('.between', ('.list', ('.arg', ('.int', 1)), ('.arg', ('.int', 2)))), 'words', '\\w+\\S*')))))))
    ),
    #We recently established that LRRK2 bound 14-3-3 protein isoforms via its phosphorylation of Ser910 and Ser935.

    #residue = [" S(er)?(ine)?([ ]|-)?[\(]?[0-9]{1,4}([ ]|[\)])", "Tyr(osine)?([ ]|-)?[\(]?[0-9]{1,4}([ ]|[\)])", " T(hr)?(eonine)?([ ]|-)?[\(]?[0-9]{1,4}([ ]|[\)])", " Y([ ]|-)?[\(]?[0-9]{1,4}([ ]|[\)])"]

    Explanation(
        name="LF_same",
        label=False,
        condition="The Protein corresponds to 'c-Jun' and the Kinase corresponds to 'JNK1'.",
        candidate="10206340::span:39:43~~10206340::span:66:69",
        semantics=('.root', ('.label', ('.bool', False), ('.and', ('.call', ('.eq', ('.string', u'c-Jun')), ('.arg_to_string', ('.arg', ('.int', 1)))), ('.call', ('.eq', ('.string', u'JNK1')), ('.arg_to_string', ('.arg', ('.int', 2)))))))
    ),
    #Activation of the caspase proteases by c-Jun N-terminal kinase 1 (JNK1) has been proposed as a mechanism of apoptotic cell death.

    Explanation(
        name="LF_signaling",
        label=False,
        condition="Sentence contains at least one signexp word",
        candidate="10085120::span:252:254~~10085120::span:243:246",
        semantics=('.root', ('.label', ('.bool', False), ('.any', ('.map', ('.in', ('.extract_text', ('.sentence',))), ('.user_list', ('.string', u'signexp'))))))
    ),
    #In HeLa cells, sustained PDT-induced JNK1 and p38 mitogen-activated protein kinase (MAPK) activations overlap the activation of a DEVD-directed caspase activity, poly(ADP-ribose) polymerase (PARP) cleavage, and the onset of apoptosis.

    Explanation(
        name="LF_substrate_B_I",
        label=True,
        condition="the word 'substrate' is between Protein and Kinase and the total number of words between Protein and Kinase is smaller than 8",
        candidate="21384452::span:406:409~~21384452::span:359:362",
        semantics=('.root', ('.label', ('.bool', True), ('.and', ('.call', ('.in', ('.extract_text', ('.between', ('.list', ('.arg', ('.int', 1)), ('.arg', ('.int', 2)))))), ('.string', u'substrate')), ('.call', ('.lt', ('.int', 8)), ('.count', ('.between', ('.list', ('.arg', ('.int', 1)), ('.arg', ('.int', 2)))))))))
    ),
    #The ability of active JNK1 or JNK2 to phosphorylate their substrate, ATF2, is inhibited by two naturally occurring GSTpi haplotypes (Ile105/Ala114, WT or haplotype A, and Val105/Val114, haplotype C).

    Explanation(
        name="LF_transfect",
        label=False,
        condition="'transfect' is in the sentence.",
        candidate="10865940::span:889:891~~10865940::span:918:921",
        semantics=('.root', ('.label', ('.bool', False), ('.call', ('.in', ('.extract_text', ('.sentence',))), ('.string', u'transfect'))))
    ),
    #Following cotransfection with JNK[K-M], a kinase-deficient JNK1, the PDTC-increased AP-1-driven-luciferase activity was attenuated.

    Explanation(
        name="LF_uncertain",
        label=False,
        condition="sentence contains an uncertain word",
        candidate="17095157::span:312:315~~17095157::span:321:325",
        semantics=('.root', ('.label', ('.bool', False), ('.any', ('.map', ('.in', ('.extract_text', ('.sentence',))), ('.user_list', ('.string', u'uncertain'))))))
    ),
    #Recently a direct gene/protein interaction between two of the most common genetic causes of parkinsonism PRKN and LRRK2 has been postulated.

    Explanation(
        name="LF_sequenc_in_sentence",
        label=False,
        condition="the sentence contains 'sequenc'",
        candidate="15970950::span:456:461~~15970950::span:474:478",
        semantics=('.root', ('.label', ('.bool', False), ('.call', ('.contains', ('.string', u'sequenc')), ('.extract_text', ('.sentence',)))))
    ),
    #To detect small sequence alterations in Parkin, DJ-1, and PINK1, we performed a conventional mutational analysis (SSCP/dHPLC/sequencing) of all coding exons of these genes.
]

def get_explanations():
    return explanations

#####################################
## END OF EXPLANATIONS USED IN RUN ##
#####################################

# ## THE FOLLOWING EXPLANATIONS CAN BE USED AS SUBSTITUTES IF ANY OF THE ABOVE EXPLANATIONS FAIL TO PARSE ##

# Explanation(
# 	name="LF_sequenc_in_sentence",
# 	label=False,
# 	condition="the sentence contains 'sequenc'",
# 	candidate="15970950::span:456:461~~15970950::span:474:478",
# semantics=None
#),
# #To detect small sequence alterations in Parkin, DJ-1, and PINK1, we performed a conventional mutational analysis (SSCP/dHPLC/sequencing) of all coding exons of these genes.

# Explanation(
# 	name="LF_expression",
# 	label=False,
# 	condition="the sentence contains 'expression'",
# 	candidate="19681889::span:1541:1544~~19681889::span:1525:1528",
# semantics=None
#),
# #In addition, SP600125 and dominant-negative JNK1 suppressed BAG3 promoter-driven reporter gene expression.


# Explanation(
# 	name="LF_and_or",
# 	label=False,
# 	condition="Kinase and Protein are separated by 'and', 'or', ',' ",
# 	candidate="19684592::span:23:27~~19684592::span:13:17",
# semantics=None
#),
# #Mutations in PINK1 and PARK2 cause autosomal recessive parkinsonism, a neurodegenerative disorder that is characterized by the loss of dopaminergic neurons.


# Explanation(
# 	name="LF_whereas",
# 	label=False,
# 	condition="'whereas' is within 100 characters between Kinase and Protein",
# 	candidate="",
# semantics=None
#),
# #After TCR costimulation, MEKK1 predominantly induces JNK1 activation, whereas the related kinase MEKK2 regulates ERK5 activation.

# Explanation(
# 	name="LF_mutat_B",
# 	label=False,
# 	condition="'mutat' is within 100 characters between Kinase and Protein",
# 	candidate="17846883::span:788:790~~17846883::span:722:726",
# semantics=None
#),
# #CONCLUSIONS: HMRA allowed us to rapidly characterize a large number of samples for the LRRK2 G2019S mutation, which results as absent in a large AD data set.


# Explanation(
# 	name="LF_genes_L",
# 	label=False,
# 	condition="'genes' is within the words left of Protein",
# 	candidate="27341347::span:948:950~~27341347::span:953:957",
# semantics=None
#),
# #Four of these validated variants were nonsense mutations, six were observed in genes directly or indirectly related to neurodegenerative disorders (NDs), such as LPA, LRRK2, and FGF20.
	

# Explanation(
# 	name="LF_genes_R",
# 	label=False,
# 	condition="the word 'genes' is within 20 characters right of Kinase or Protein and there are between 0 and 30 characters between Kinase and Protein",
# 	candidate="23986421::span:1029:1033~~23986421::span:1039:1043",
# semantics=None
#),
# #RESULTS: Mutations were identified only in the PARK2 and PINK1 genes with the frequency of 4.7% and 2.7% of subjects, respectively.

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# #############################
# #CONSTANTS
# #############################

# coimmunopr = ["coimmunoprecipitat.", "co-immunoprecipitat."]
# substrate = {"substrate"}
# between = {"between"}
# bindmid = {"bind", "bound", "binds", "colocalizes", "co-localizes", "interacts", "interact"}
# int_ind = [ "bind", "interact", "form", "complex", "binding", "interaction", "influence", "phosphorylation" ]
# interaction_indicators = { "bind", "interact", "form", "complex", "binding", "interaction", "influence", "phosphorylation", "influences", "influenced", "formed", "formation", "physical" }
# interact = {"interact", "interaction", "interacts", "interacted"}
# mutations= {"mutate", "mutant", "mutation", "mutations", "null", "dosage", "SNP", "SNPs", "variant", "knockout", "knockdown", "ko", "kd", "-/-", "(-)/(-)","(-/-)", "+/-", "deletion"} 
# neg_ind = [ " no ", " not ", "fail", "absence", "negative", "expression", "DNA", "RNA" ]
# negative = {"no", "not", "none"}
# negexp = ["phosphorylation", "phosphorylate", "phosphorylated", "phosphorylates" ]
# nucleic_acids = ["mRNA", "RNA", "DNA"]
# positive = {"evidence", "clearly", "indicate", "show"}
# prep = {"by", "with"}
# prep2 = {"on", "in", "to"}
# signexp = { "mitogen", "signal", "cascade", "pathway", "MAPK", "ligand", "signaling" }
# work = {"work", "worked", "works"}
# phosphory = { "phosphorylation", "phosphorylate", "phosphorylated", "phosphorylates" }
# influence = { "influence", "influenced", "influences", "modulate", "modulated", "modulates" }
# uncertain = { "possible", "unlikely", "potential", "putative", "hypothetic", "seemingly", "assume", "postulated" }
# negat_ind = { "no", "not", "fail", "absence", "negative", "expression", "DNA", "RNA" }
# residue = [" S(er)?(ine)?([ ]|-)?[\(]?[0-9]{1,4}([ ]|[\)])", "Tyr(osine)?([ ]|-)?[\(]?[0-9]{1,4}([ ]|[\)])", " T(hr)?(eonine)?([ ]|-)?[\(]?[0-9]{1,4}([ ]|[\)])", " Y([ ]|-)?[\(]?[0-9]{1,4}([ ]|[\)])"]

# compartments= []
# with open("./protein/data/compartment_dictionary.csv", mode ="r") as l:
# 	for line in l: 		
# 		compartments.append(line.strip())

# #############################
# #HELPER FUNCTIONS
# #############################
# def get_all_tokens(c):
#     return chain(
#         get_left_tokens(c), get_between_tokens(c), get_right_tokens(c))


# # List to parenthetical
# def ltp(x):
#     return "(" + "|".join(x) + ")"


# #helper function that looks for words between candidates disregarding their order of appearance
# def btw_AB_or_BA(candidate, pattern, sign):
#     return sign if re.search(
#         r"{{(A|B)}}" + pattern + r"{{(B|A)}}",
#         get_tagged_text(candidate),
#         flags=re.I) else 0

# def rule_regex_search_btw_AB(candidate, pattern, sign):
#     return sign if re.search(
#         r"{{A}}" + pattern + r"{{B}}", get_tagged_text(candidate),
#         flags=re.I) else 0

# def HF_and_or(c):
#     return re.search(
#         r"{{(A|B)}}.{0,1}(and|or|,).{{(B|A)}}", get_tagged_text(c), flags=re.I)


# def HF_negexp(c):
#     return (re.search(ltp(negexp), get_tagged_text(c), flags=re.I))


# def HF_signaling_related(c):
#     return (re.search(ltp(signexp), get_tagged_text(c), flags=re.I))


# ######################################################
# #END HELPER FUNCTIONS                              ###
# ######################################################

# def LF_by_with(c):
#     return 1 if len(
#         prep.intersection(
#             get_between_tokens(
#                 c, attrib="words", case_sensitive=False)
#             )) > 0 and len(
#                     negative.intersection(
#                         get_between_tokens(
#                             c, attrib="words",
#                             case_sensitive=False))) == 0 and len(
#                                 list(get_between_tokens(c))) < 10 else 0


# def LF_NucAc_in_sentence(c):
#     return -1 if re.search(
#         ltp(nucleic_acids), get_tagged_text(c), flags=re.I) else 0


# def LF_activate_B(c):
#     return btw_AB_or_BA(c, ".{0,20}activ.{0,20}", 1)


# def LF_activates(c):
#     return 1 if re.search(r"activates", get_tagged_text(c), flags=re.I) and len(list(get_between_tokens(c))) < 6 else 0

# def LF_associat_with(c):
#     return -1 if re.search(
#         r"associat.{0,12}with", get_tagged_text(c), flags=re.I) else 0

# def LF_between_before(c):
#     return 1 if re.search(
#         r"between.{0,50}{{(A|B)}}.{0,20}and.{0,20}{{(A|B)}}",
#         get_tagged_text(c),
#         flags=re.I) else 0

# def LF_bind_B_I(c):
#     return 1 if len(
#         bindmid.intersection(get_between_tokens(
#             c, case_sensitive=False))) > 0 and not HF_negexp(c) else 0

# def LF_close_I(c):
#     return 1 if len(list(get_between_tokens(c))) < 6 and re.search(
#         ltp(int_ind), get_tagged_text(c), flags=re.I) and len(
#             negative.intersection(
#                 get_between_tokens(c, attrib="words", case_sensitive=False))
#         ) == 0 and is_inverted(c) and not HF_and_or(c) else 0

# def LF_comma(c):
#     return -1 if re.search(r"{{(A|B)}}.{0,30},.{0,30}{{(B|A)}}", get_tagged_text(c), flags=re.I) else 0

# def LF_complex_L(c):
#     return 1 if re.search(
#         r"complex.{0,50}{{(A|B)}}.{0,50}{{(A|B)}}",
#         get_tagged_text(c),
#         flags=re.I) and not re.search(
#             r"(not|no).{0,50}.{{(A|B)}}.{0,50}{{(A|B)}}",
#             get_tagged_text(c),
#             flags=re.I) else 0

# def LF_complex_R(c):
#     return 1 if re.search(
#         r"{{(A|B)}}.{0,50}{{(B|A)}}.{0,50}complex",
#         get_tagged_text(c),
#         flags=re.I) and not re.search(
#             r"{{(A|B)}}.{0,50}{{(B|A)}}.{0,50}(no|not)",
#             get_tagged_text(c),
#             flags=re.I) else 0

# def LF_dist_sup(c):
#     p1, p2 = c.protein.get_span(), c.kinase.get_span()
#     return 1 if (p1, p2) in known_targets and is_inverted(c) and len(
#         list(get_between_tokens(c))) < 8 else 0

# def LF_distant(c):
#     return -1 if re.search(
#         r"{{(A|B)}}.{150,500}{{(A|B)}}", get_tagged_text(c), flags=re.I) else 0


# def LF_induc(c):
#     return -1 if re.search(r"induc", get_tagged_text(c), flags=re.I) else 0

# def LF_influence_B(c):
#     return btw_AB_or_BA(c, ".{0,50}influenc.{0,50}.", 1)

# def LF_interact_in_sentence(c):
#     return 1 if re.search(
#         r"interact", get_tagged_text(c),
#         flags=re.I) and len(list(get_between_tokens(c))) < 8 else 0

# def LF_interaction(c):
#     return 1 if len(interaction_indicators.intersection(get_all_tokens(c))) > 0 and len(list(get_between_tokens(c))) < 8 and not HF_negexp(c) else 0

# def LF_levels(c):
#     return -1 if re.search(r"level", get_tagged_text(c), flags=re.I) else 0

# def LF_mutation_list_I(c):
#     return -1 if len(mutations.intersection(get_all_tokens(c))) > 0 else 0

# def LF_no_B(c):
#     return btw_AB_or_BA(c, ".{0,50}(no|not|none).{0,50}", -1)

# def LF_phosphory(c):
# 	return 1 if len(phosphory.intersection(get_all_tokens(c))) > 0 and len(list(
# 		get_between_tokens(c))) < 8 and not HF_negexp(c) else 0

# def LF_prepositions_I(c):
#     return 1 if re.search(
#         r"{{B}}.{0,30}( on | in | to ).{0,30}{{A}}",
#         get_tagged_text(c),
#         flags=re.I) and len(list(
#             get_between_tokens(c))) < 8 and not HF_negexp(c) else 0

# def LF_regulate_Betw(c):
#     return btw_AB_or_BA(c, ".{0,50}regulat.{0,50}", 1)

# def LF_residue(c):
#      return 1 if re.search(
#         ltp(residue),
#         get_tagged_text(c), flags=re.I) and not HF_negexp(c) and len(
#             list(get_between_tokens(c))) < 6 else 0

# def LF_same(c):
#     p1, p2 = c.protein.get_span(), c.kinase.get_span()
#     return -1 if p1 == "c-Jun" and p2 == "JNK1" else 0

# def LF_signaling(c):
#     return -1 if HF_signaling_related(c) else 0

# def LF_substrate_B_I(c):
#     return 1 if len(
#         substrate.intersection(
#             get_between_tokens(c, attrib="words",
#                                case_sensitive=False))) > 0 and len(
#                                    list(get_between_tokens(c))) < 8 else 0

# def LF_transfect(c):
#     return -1 if re.search(
#         r".{0,50}transfect.{0,50}", get_tagged_text(c), flags=re.I) else 0

# def LF_uncertain(c):
#     return -1 if len(uncertain.intersection(get_all_tokens(c))) > 0 else 0

# ####################################
# ### 	SUBSTITUTE FUNCTIONS     ###
# ####################################

# def LF_sequenc_in_sentence(c):
#     return -1 if r"sequenc" in get_tagged_text(c) else 0

# def LF_expression(c):
#     return -1 if re.search(
#         r"expression", get_tagged_text(c), flags=re.I) else 0

# def LF_and_or(c):
#     return -1 if re.search(
#         r"{{(A|B)}}.{0,1}(and|or|,).{{(B|A)}}", get_tagged_text(c),
#         flags=re.I) else 0

# def LF_whereas_B(c):
#     return btw_AB_or_BA(c, ".{0,50}whereas.{0,50}", -1)

# def LF_mutat_B(c):
#     return btw_AB_or_BA(c, ".{0,50}.mutat.{0,50}", -1)

# def LF_genes_L(c):
#     return rule_regex_search_before_A(c, "(gene |genes|genet).*", -1)

# def LF_genes_R(c):
#     return -1 if re.search(
#         r"{{(A|B)}}.{0,30}{{(B|A)}}.{0,20}(gene |genes|genet)",
#         get_tagged_text(c),
#         flags=re.I) else 0

