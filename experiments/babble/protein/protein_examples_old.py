import csv
import os
import re

from snorkel.contrib.babble import Explanation, link_explanation_candidates

DATA_ROOT = os.environ['SNORKELHOME'] + '/experiments/babble/protein/data/'

def get_user_lists():
    return {
        'int_ind': ['bind', 'interact', 'form', 'complex', 'binding', 'interaction', 'influence', 'phosphorylation'],
        'negative': ['no', 'not', 'none'],
        'uncertain': ['possible', 'unlikely', 'potential', 'putative', 'hypothetic', 'seemingly', 'assume', 'postulated'],
        'phosphory': ['phosphorylation', 'phosphorylate', 'phosphorylated'],
    }


def extract_explanations(fpath):
    explanations = []
    with open(DATA_ROOT + fpath, 'rU') as csvfile:
        csvreader = csv.reader(csvfile)
        csvreader.next()
        for i, row in enumerate(csvreader):
            row = [unicode(cell, 'utf-8') for cell in row]
            try:
                doc_id, entities, span1, span2, direction, description = row[:6]
                if doc_id == 'Pubmed ID':
                    continue

                entity1, entity2 = direction.split('-->')
                
                span1_start, span1_end = span1.split(',')
                span2_start, span2_end = span2.split(',')
                span1_stable_id = "{}::span:{}:{}".format(doc_id, span1_start.strip(), span1_end.strip())
                span2_stable_id = "{}::span:{}:{}".format(doc_id, span2_start.strip(), span2_end.strip())
                protein_stable_id = span1_stable_id if entity1 == 'protein' else span2_stable_id
                kinase_stable_id = span1_stable_id if entity1 == 'kinase' else span2_stable_id
                candidate_stable_id = '~~'.join([protein_stable_id, kinase_stable_id])                

                label_str = re.match(r'(true|false)\,?\s*', description,
                    flags=re.UNICODE | re.IGNORECASE)
                label = label_str.group(1) in ['True', 'true']

                condition = description[len(label_str.group(0)):]
                # Only one of these will fire
                condition = re.sub(r"\"entities:[^\"]+\"", 'them', condition, 
                    flags=re.UNICODE | re.IGNORECASE)
                condition = re.sub(r"\"entity:\s(protein|kinase)_[^\"]+\"", 'the \g<1>', condition, 
                    flags=re.UNICODE | re.IGNORECASE)

                explanation = Explanation(condition, label, candidate_stable_id)
                explanations.append(explanation)
            except ValueError:
                if all(cell == u'' for cell in row):
                    break
                print("Skipping malformed or header row {}...".format(i + 2))
                continue
    return explanations


explanations = [

    Explanation(
        name='LF_by_with',
        label=True,  
        condition="""the words "by" or "with" are between Protein and Kinase and none of the words "no", "not" or "none" are between them and the total number of words between them is smaller than 10""",
        candidate='24889144::span:758:760~~24889144::span:765:768'),
    # Based on a bioinformatics approach, we estimated the potential phosphorylation site of angulin-1/LSR by JNK1 to be serine 288 and experimentally confirmed that JNK1 directly phosphorylates angulin-1/LSR at this site.

    Explanation(
        name='LF_close',
        label=True,
        condition="""the number of words between them is less than 8 and at least one int_ind word is in the sentence and the Protein is after the Kinase and there are no negative words in the sentence.""", #  
        candidate='28641777::span:478:483~~28641777::span:468:472',
        semantics=('.root', ('.label', ('.bool', True), ('.and', ('.call', 
            ('.lt', ('.int', 8)), ('.count', ('.between', ('.list', ('.arg', 
            ('.int', 1)), ('.arg', ('.int', 2)))))), ('.and', ('.call', ('.geq', 
            ('.int', 1)), ('.sum', ('.map', ('.in', ('.extract_text', 
            ('.sentence',))), ('.user_list', ('.string', u'int_ind'))))), 
            ('.and', ('.call', ('.in', ('.extract_text', ('.right', ('.arg', 
            ('.int', 2))))), ('.arg_to_string', ('.arg', ('.int', 1)))), 
            ('.call', ('.eq', ('.int', 0)), ('.sum', ('.map', ('.in', 
            ('.extract_text', ('.sentence',))), ('.user_list', 
            ('.string', u'negative'))))))))))),
    #METHODS: Expression of presenilin associated rhomboid-like protein (PARL), PINK1 and Parkin, as well as the interaction among these proteins was temporally examined during adipogenesis.

    Explanation(
        name='LF_treatment',
        label=False,  
        condition="""the sentence contains the word 'treatment'""",
        candidate='27941886::span:1006:1009~~27941886::span:838:841'),
    #We found that knockdown of JNK1 or JNK2 or treatment with JNK-IN-8, an adenosine triphosphate-competitive irreversible pan-JNK inhibitor, significantly reduced cell proliferation, the ALDH1+ and CD44+/CD24- CSC subpopulations, and mammosphere formation, indicating that JNK promotes CSC self-renewal and maintenance in TNBC.

    Explanation(
        name='LF_transfect',
        label=False,
        condition="""sentence contains the word 'transfect'""",
        candidate='12401814::span:348:350~~12401814::span:459:462'),
    #To analyze the effects of a single JNK isoform on neuronal cell death and differentiation, we transfected PC12 cells, which normally express only JNK1 and JNK2, with JNK3-p54

    Explanation(
        name='LF_distant_supervision_I',
        label=True,
        condition="""Protein and Kinase appear in a list of known interacting pairs""",
        candidate=None),
    #Nonetheless, both Tc and human PINK1 phosphorylate Parkin and Ubiquitin, two physiological substrates of PINK1.
    #Note: I could not identify the spans for this LF

    Explanation(
        name='LF_levels',
        label=False,
        condition="""the word "levels" appears in the sentence""",
        candidate='26721933::span:761:765~~26721933::span:705:709'),
    #Augmented Delta1 PINK1 fragment levels suggest an inhibitory effect over PARK2 translocation to the mitochondria, causing the accumulation of activated PINK1.

    Explanation(
        name='LF_between_before',
        label=True,
        condition="""the word "between" is within 50 caracters before the Protein or the Kinase and the word "and" is between Protein and Kinase""",
        candidate=None),
    #Specifically, JNK and ERK1/2 inhibition also dramatically blocked the interaction between PINK1 and Parkin.


    Explanation(
        name='LF_sequenc_in_sentence',
        label=False,
        condition="""the sentence contains 'sequenc'""",
        candidate='15970950::span:456:461~~15970950::span:474:478'),
    #To detect small sequence alterations in Parkin, DJ-1, and PINK1, we performed a conventional mutational analysis (SSCP/dHPLC/sequencing) of all coding exons of these genes.

    Explanation(
        name='LF_Ser_Tyr',
        label=True,
        condition="""'Ser' or 'Tyr' are within 10 characters of the Protein""",
        candidate=None),

    #Investigation of insulin signaling revealed that bradykinin enhanced insulin receptor substrate-1 (IRS-1) Tyr phosphorylation, Akt/protein kinase B phosphorylation, and GLUT4 translocation.

    Explanation(
        name='LF_expression',
        label=False,
        condition="""the sentence contains 'expression'""",
        candidate='19681889::span:1541:1544~~19681889::span:1525:1528'),
    #In addition, SP600125 and dominant-negative JNK1 suppressed BAG3 promoter-driven reporter gene expression.

    Explanation(
        name='LF_uncertain',
        label=False,
        condition="""sentence contains any uncertain word""",
        candidate='25478574::span:344:358~~25478574::span:337:341'),
        
    #To investigate a potential use for urine exosomes as a tool for PD diagnosis, we compared levels of LRRK2, alpha-synuclein, and DJ-1 in urine exosomes isolated from Korean PD patients and non-PD controls.
    #uncertain = ['possible', 'unlikely','potential','putative', 'hypothetic', 'seemingly', 'assume', 'postulated']

    Explanation(
        name='LF_influence_B',
        label=True,
        condition="""'influenc' within 100 caracters of Protein and Kinase""",
        candidate=None),
    #Knockdown of total alpha-synuclein with potent antisense oligonucleotides substantially reduces inclusion formation in G2019S-LRRK2-expressing neurons, suggesting that LRRK2 influences alpha-synuclein inclusion formation by altering alpha-synuclein levels.

    Explanation(
        name='LF_substrate_B',
        label=True,
        condition="""the word 'substrate' is between Protein and Kinase and the total number of words between Protein and Kinase is smaller than 8""",
        candidate= ''),
    #A new study published in the Biochemical Journal by Ito et al. establishes that a 'Phos-tag'-binding assay can be exploited to measure phosphorylation of a recently identified LRRK2 substrate (Ras-related protein in brain 10 (Rab10)), and to compare and contrast relative catalytic output from disease-associated LRRK2 mutants.

    Explanation(
        name='LF_phosphory_B',
        label=True,
        condition="""any word between Protein and Kinase is in the phosphory dictionary and the number of words between Protein and Kinase is smaller than 8""",
        candidate=None), #'10506143::span:1101:1103~~10506143::span:1025:1028'),

    #Immunoblotting analysis indicated that JNK1 was phosphorylated by JNKK2 in the fusion protein on both Thr(183) and Tyr(185) residues.
    #phosphory = {'phosphorylation', 'phosphorylate', 'phosphorylated'}

    Explanation(
        name='LF_interact_in_sentence',
        label=True,
        condition="""sentence contains "interact" and the number of words between Protein and Kinase is at most 8""",
        candidate='23933751::span:385:389~~23933751::span:465:469'),
    #Here we show that Fbxo7 participates in mitochondrial maintenance through direct interaction with PINK1 and Parkin and acts in Parkin-mediated mitophagy.

    Explanation(
        name='LF_activate_B',
        label=True,
        condition="""'activ' is within 40 characters of Kinase and Protein """,
        candidate='27941886::span:1233:1237~~27941886::span:1170:1173'),
    #We further demonstrated that both JNK1 and JNK2 regulated Notch1 transcription via activation of c-Jun and that the JNK/c-Jun signaling pathway promoted CSC phenotype through Notch1 signaling in TNBC.

    Explanation(
        name='LF_bind_B',
        label=True,
        condition="""'bind' or 'bound' is within 100 characters of Kinase and Protein """,
        candidate='10471813::span:27:29~~10471813::span:125:128'),
    #We have identified a novel Jun N-terminal kinase (JNK)-binding protein, termed JNKBP1, and examined its binding affinity for JNK1, JNK2, JNK3, and extracellular signal-regulated kinase 2 (ERK2) in COS-7 cells.

    Explanation(
        name='LF_regulate_Betw',
        label=True,
        condition="""'regulate' is between the Kinase and Protein and there are less than 100 characters between them""",
        candidate='23949442::span:1458:1463~~23949442::span:1399:1403'),
    # Combined, these data suggest that LRRK2 may regulate neurotransmitter release via control of Snapin function by inhibitory phosphorylation.

    Explanation(
        name='LF_complex_L',
        label=True,
        condition="""'complex' is within 50 characters left of Protein or Kinase and there are between 0 and 50 characters between Protein and Kinase and the sentence does not contain "not" or "no" within 50 characters left of Protein or Kinase""",
        candidate=None),
    #Similar conformational changes occur in a complex between ERK2 and a MEK2 (MAP/ERK kinase-2)-derived D motif peptide (pepMEK2).

    Explanation(
        name='LF_complex_R',
        label=True,
        condition="""'complex' is within 50 characters right of Protein or Kinase and there are between 0 and 50 characters between Protein and Kinase and the sentence does not contain "not" or "no" within 50 characters right of Protein or Kinase""",
        candidate=None),
    #The exact function of LRRK2 is currently unknown but the presence of multiple protein interaction domains including WD40 and ankyrin indicates that it may act a scaffold for assembly of a multi-protein signaling complex.

    Explanation(
        name='LF_distant',
        label=False,
        condition="""Kinase and Protein are between 150 and 500 characters apart""",
        candidate='16401616::span:970:975~~16401616::span:815:819'),
    #The clinical characteristics of 12 PINK1 patients and 114 parkin patients were similar, even for signs such as dystonia at onset and increased reflexes, which were thought to be specific to parkin.

    Explanation(
        name='LF_and_or',
        label=False,
        condition="""Kinase and Protein are separated by 'and', 'or', or ',' """,
        candidate='19684592::span:23:27~~19684592::span:13:17'),
    #Mutations in PINK1 and PARK2 cause autosomal recessive parkinsonism, a neurodegenerative disorder that is characterized by the loss of dopaminergic neurons.


    Explanation(
        name='LF_whereas',
        label=False,
        condition="""'whereas' is within 100 characters of Kinase and Protein""",
        candidate=None),
    #After TCR costimulation, MEKK1 predominantly induces JNK1 activation, whereas the related kinase MEKK2 regulates ERK5 activation.

    Explanation(
        name='LF_mutat_B',
        label=False,
        condition="""'mutat' is within 100 characters of Kinase and Protein""",
        candidate='17846883::span:788:790~~17846883::span:722:726'),
    #CONCLUSIONS: HMRA allowed us to rapidly characterize a large number of samples for the LRRK2 G2019S mutation, which results as absent in a large AD data set.

    Explanation(
        name='LF_NucAc_in_sentence',
        label=False,
        condition="""sentence contains "mRNA", "DNA", or "RNA".""",
        candidate='22506991::span:1428:1431~~22506991::span:1253:1257'),
    #More importantly, the zebrafish pink1 mRNA as well as the human PINK1 mRNA, but not kinase-dead nor Parkinson's disease-linked mutant PINK1 mRNA, also rescued the morphant phenotype, providing evidence that Parl genes may function upstream of Pink1, as part of a conserved pathway in vertebrates.

    Explanation(
        name='LF_genes_L',
        label=False,
        condition="""'genes' is in the words left of Protein""",
        candidate='27341347::span:948:950~~27341347::span:953:957'),
    #Four of these validated variants were nonsense mutations, six were observed in genes directly or indirectly related to neurodegenerative disorders (NDs), such as LPA, LRRK2, and FGF20.
        
    Explanation(
        name='LF_drug',
        label=False,
        condition="""sentence contains the word 'drug'""",
        candidate=None),

    #In addition, in contrast to drug-treated, immortalized cells in vitro, mature motor neurons rarely displayed Parkin-dependent mitophagy.

    Explanation(
        name='LF_genes_R',
        label=False,
        condition="""the word "genes" is within 20 characters right of Kinase or Protein and there are between 0 and 30 characters between Kinase and Protein""",
        candidate='23986421::span:1029:1033~~23986421::span:1039:1043'),
    #RESULTS: Mutations were identified only in the PARK2 and PINK1 genes with the frequency of 4.7% and 2.7% of subjects, respectively.

    Explanation(
        name='LF_comma',
        label=False,
        condition="""there are two "," between Protein and Kinase with less than 30 characters between them""",
        candidate='17914726::span:1339:1342~~17914726::span:1353:1357'),
    #These results show that PD-MLPA assay can simultaneously and effectively detect rearrangements in most PD genes (SNCA, Parkin, PINK1, and DJ-1) as well as the LRRK2 G2019S common mutation.

    Explanation(
        name='LF_no_B',
        label=False,
        condition="""The words "no", "not" or "none" are within 100 characters of Protein and Kinase""",
        candidate='9213219::span:1008:1011~~9213219::span:966:969'),
    #However, other serine/threonine protein kinases, including the MAP kinases JNK1, p38, and ERK2, do not phosphorylate IRF2.
]

def get_explanations():
    return explanations