import streamlit as st
from datetime import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="HemePath Reporter Pro", layout="wide")

# ==========================================
# 0. STATE MANAGEMENT & TEXT GENERATION
# ==========================================

# Initialize session state for inputs if they don't exist
def init_state():
    defaults = {
        # PB Inputs
        'rbc_morph': ["unremarkable morphology"],
        'plt_morph': ["small and well granulated"],
        'neut_morph': ["normal morphology with appropriate granulation and segmentation"],
        'lymph_morph': ["appear small and mature"], # NEW
        'pb_blast_pct': 0,
        'pb_blast_desc': [],
        'pb_auer': "No Auer rods seen",
        
        # Aspirate Inputs
        'asp_status': "Adequate quality for interpretation",
        'asp_reasons': [],
        'me_ratio': "2:1",
        'bm_blast_pct': 1,
        'bm_blast_desc': [],
        'bm_auer': "No Auer rods seen",
        'ery_maturation': "shows full spectrum maturation with no dysplasia",
        'ery_dysplasia': [],
        'gran_maturation': "shows full spectrum maturation with no dysplasia",
        'gran_dysplasia': [],
        'meg_number': "Normal",
        'meg_morph': ["unremarkable with no dysplastic features"],
        'asp_plasma_morph': [], # NEW
        'asp_mast_cells': "No increase in mast cells", # NEW
        'iron_stores': "Normal",
        'ring_sideroblasts': "No ring sideroblasts seen",
        
        # Biopsy Inputs
        'bx_quality': "adequate quality for interpretation",
        'cellularity': 40,
        'streaming_status': "No obvious streaming to suggest fibrosis is present",
        'erythroid_island_status': "Erythroid islands are present in expected numbers",
        'bx_granulocytes': "Granulocytes are well represented and show full spectrum maturation", # NEW
        'arch_features': ["Bone marrow architecture is preserved and orderly", "Trilineage hematopoiesis present", "No blast clusters are identified", "No lymphoid aggregates are seen", "No non-hematopoietic elements present"],
        'meg_dist': "Randomly distributed",
        
        # Report Drafts
        'pb_report_draft': "",
        'asp_report_draft': "",
        'bx_report_draft': "",
        'ihc_report_draft': "",
        'saved_reports': ""
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    # Run initial text generation if drafts are empty
    if not st.session_state['pb_report_draft']:
        update_pb_text()
    if not st.session_state['asp_report_draft']:
        update_asp_text()
    if not st.session_state['bx_report_draft']:
        update_bx_text()

# --- TEXT GENERATION FUNCTIONS (CALLBACKS) ---

def update_pb_text():
    # RBC Logic
    rbc_list = st.session_state.rbc_morph
    if "unremarkable morphology" in rbc_list or not rbc_list:
        rbc_str = "Red blood cells show unremarkable morphology."
    elif "non-specific morphology" in rbc_list:
        rbc_str = "Red blood cells show non-specific morphology."
    else:
        rbc_str = f"Red blood cells show {', '.join(rbc_list)}."
    
    # Neutrophil Logic
    neut_list = st.session_state.neut_morph
    if "normal morphology with appropriate granulation and segmentation" in neut_list or not neut_list:
        neut_str = "Neutrophils show normal morphology with appropriate granulation and segmentation."
    else:
        neut_str = f"Neutrophils show {', '.join(neut_list)}."

    # Lymphocyte Logic (NEW)
    lymph_list = st.session_state.lymph_morph
    if "appear small and mature" in lymph_list or not lymph_list:
        lymph_str = "Lymphocytes appear small and mature."
    else:
        # If multiple selections, join them.
        lymph_str = f"Lymphocytes {', '.join(lymph_list)}."

    # Platelet Logic
    plt_list = st.session_state.plt_morph
    if "small and well granulated" in plt_list or not plt_list:
        plt_str = "Platelets are small and well granulated."
    else:
        plt_str = f"Platelets are {', '.join(plt_list)}."

    # Blast Logic
    pct = st.session_state.pb_blast_pct
    desc = st.session_state.pb_blast_desc
    auer = st.session_state.pb_auer
    
    if pct == 0:
        blast_str = "No blasts are identified."
    else:
        desc_text = f" exhibiting {', '.join(desc)}" if desc else ""
        auer_text = f" {auer}." if auer == "Auer rods present" else ""
        blast_str = f"Blasts account for {pct}% of leukocytes{desc_text}.{auer_text}"

    # Combine into one paragraph
    st.session_state['pb_report_draft'] = f"{rbc_str} {neut_str} {lymph_str} {plt_str} {blast_str}"

def update_asp_text():
    # Quality
    qual = st.session_state.asp_status
    reasons = st.session_state.asp_reasons
    qual_str = f"{qual}"
    if reasons:
        qual_str += f" due to {', '.join(reasons)}"
    
    # Blasts
    pct = st.session_state.bm_blast_pct
    desc = st.session_state.bm_blast_desc
    auer = st.session_state.bm_auer
    
    blast_str = f"Blasts account for {pct}% of the differential count"
    if pct > 0:
        desc_text = f", exhibiting {', '.join(desc)}" if desc else ""
        auer_text = f". {auer}." if auer == "Auer rods identified" else "."
        blast_str += f"{desc_text}{auer_text}"
    else:
        blast_str = ". No blasts are identified."

    # Erythroid
    ery_mat = st.session_state.ery_maturation
    ery_dys = st.session_state.ery_dysplasia
    ery_str = f"Erythropoiesis {ery_mat}"
    if ery_dys:
        ery_str += f" with dysplastic features including {', '.join(ery_dys)}."
    else:
        ery_str += "."

    # Granulocytic
    gran_mat = st.session_state.gran_maturation
    gran_dys = st.session_state.gran_dysplasia
    gran_str = f"Granulopoiesis {gran_mat}"
    if gran_dys:
        gran_str += f" with dysplastic features including {', '.join(gran_dys)}."
    else:
        gran_str += "."

    # Megs
    meg_num = st.session_state.meg_number
    meg_morph_list = st.session_state.meg_morph
    
    if "unremarkable with no dysplastic features" in meg_morph_list:
        meg_morph_str = "have unremarkable morphology"
    else:
        meg_morph_str = f"display {', '.join(meg_morph_list)}"
        
    meg_str = f"Megakaryocytes are {meg_num.lower()} and {meg_morph_str}."

    # Plasma Cells (NEW)
    plasma_list = st.session_state.asp_plasma_morph
    if plasma_list:
        plasma_str = f"Plasma cells are identified showing {', '.join(plasma_list)}."
    else:
        plasma_str = "Plasma cells are unremarkable."

    # Mast Cells (NEW)
    mast_str = f"{st.session_state.asp_mast_cells}."

    # Iron
    iron = st.session_state.iron_stores
    ring = st.session_state.ring_sideroblasts
    iron_str = f"Iron staining shows {iron.lower()} iron stores. {ring}."

    # Combine
    text = f"The bone marrow aspirate is of {qual_str}. The myeloid-to-erythroid (M:E) ratio is {st.session_state.me_ratio}. {blast_str} {ery_str} {gran_str} {meg_str} {plasma_str} {mast_str} {iron_str}"
    st.session_state['asp_report_draft'] = text

def update_bx_text():
    # Cellularity
    cell = st.session_state.cellularity
    age_val = st.session_state.age_input if 'age_input' in st.session_state else 60
    
    expected = 100 - age_val
    if cell > (expected + 15):
        c_status = "hypercellular"
    elif cell < (expected - 15):
        c_status = "hypocellular"
    else:
        c_status = "normocellular"
    
    cell_str = f"The bone marrow biopsy is of {st.session_state.bx_quality}. The cellularity is approximately {cell}%, which is {c_status} for age."

    # Architecture
    arch_list = st.session_state.arch_features
    arch_str = f"{'. '.join(arch_list)}." if arch_list else "Bone marrow architecture is preserved."
    
    # Granulocytes (NEW)
    gran_str = f"{st.session_state.bx_granulocytes}."

    # Specifics
    ery_island = st.session_state.erythroid_island_status
    streaming = st.session_state.streaming_status
    meg_d = st.session_state.meg_dist
    
    text = f"{cell_str} {arch_str} {gran_str} {ery_island}. {streaming}. Megakaryocytes are {meg_d.lower()}. Trabecular bone is unremarkable."
    st.session_state['bx_report_draft'] = text

# Initialize State
init_state()


# ==========================================
# 1. USER NOTES DATABASE
# ==========================================
USER_NOTES_DATABASE = {
    "AML": """
    - AML with t(8;21): Salmon colored granules, perinuclear hofu, long sharp Auer rods.
    - APL: Bilobed nuclei, hypergranular (faggot cells) or hypogranular (butterfly nucleus).
    - Monoblastic: Large cells, abundant cytoplasm, vacuoles, delicate lacey chromatin.
    """,
    "MDS": """
    - Erythroid: Nuclear budding, internuclear bridging, megaloblastoid change, ring sideroblasts.
    - Myeloid: Hypogranularity, Pseudo-Pelger-Huet (sunglasses), abnormal chromatin clumping.
    - Megs: Micromegakaryocytes, separated nuclear lobes (pawn ball), hypolobation.
    """,
    "MPN": """
    - CML: Dwarf megakaryocytes, basophilia, leukocytosis, left shift.
    - ET: Staghorn nuclei, loose clusters, no fibrosis, platelet anisocytosis.
    - PMF: Cloud-like nuclei, bulbous megs, dense clustering, sinusoidal hematopoiesis.
    """,
    "MDS/MPN": """
    - CMML: Monocytosis ≥0.5, dysplasia, +/- fibrosis.
    - aCML: Dysplastic neutrophilia, <10% monos, +/- membrane defects.
    - JMML: Monocytosis in kids <50% HbF for age.
    """,
    "Lymphoid": """
    - LPL: Plasmacytoid lymphs, Dutcher bodies, mast cells.
    - HCL: Fried egg appearance, annexin A1+, BRAF V600E.
    - CLL: Prolymphocytes <15% (typical), >15% (accelerated), >55% (PLL).
    """
}

# ==========================================
# 2. HEME CLASSIFICATION REFERENCE DATABASES
# ==========================================
ICC_DATA = {
    "Acute Myeloid Leukemia (AML)": {
        "AML with Recurrent Genetic Abnormalities": {
            "Definition": "AML defined by specific genetic fusions or mutations. The ICC lowers the blast cutoff to ≥10% for most entities in this group.",
            "Entities & Criteria": [
                "**AML with t(15;17)/PML::RARA:** ≥10% blasts (or promyelocytes).",
                "**AML with t(8;21)/RUNX1::RUNX1T1:** ≥10% blasts.",
                "**AML with inv(16)/CBFB::MYH11:** ≥10% blasts.",
                "**AML with t(9;11)/KMT2A rearrangements:** ≥10% blasts.",
                "**AML with mutated NPM1:** ≥10% blasts. Note: Can be <10% if well-documented history.",
                "**AML with in-frame bZIP CEBPA mutations:** ≥10% blasts. Replaces 'biallelic CEBPA'. Can be mono- or biallelic as long as bZIP is affected.",
                "**AML with t(9;22)/BCR::ABL1:** Requires **≥20%** blasts to distinguish from CML blast phase.",
                "**AML with mutated TP53:** Requires **≥20%** blasts. Usually complex karyotype."
            ],
            "Key Mutations": "NPM1, CEBPA (bZIP), TP53, KIT (in core binding factor AML).",
            "Pearl": "TP53-mutated AML has a dismal prognosis (median OS <1 year) regardless of blast count."
        },
        "AML with Myelodysplasia-related Gene Mutations": {
            "Definition": "AML (≥20% blasts) defined by specific somatic mutations, regardless of morphology or history. Replaces part of the old 'AML-MRC'.",
            "Defining Mutations": [
                "ASXL1", "BCOR", "EZH2", "RUNX1", "SF3B1", "SRSF2", "STAG2", "U2AF1", "ZRSR2"
            ],
            "Caveats": "These mutations are >95% specific for secondary AML ontogeny."
        },
        "AML with Myelodysplasia-related Cytogenetics": {
            "Definition": "AML (≥20% blasts) with complex karyotype (≥3 abnormalities) or specific unbalanced abnormalities.",
            "Cytogenetics": "-7/del(7q), -5/del(5q), i(17q), -17/del(17p), del(12p), del(20q), idic(X)(q13)."
        }
    },
    "Myelodysplastic Syndromes (MDS) & MDS/AML": {
        "MDS/AML (New Category)": {
            "Definition": "Myeloid neoplasm with **10–19% blasts** in BM or PB. Replaces 'MDS-EB2'.",
            "Criteria": [
                "Blasts: 10–19%",
                "Cytopenias: Required (unless early phase)",
                "No AML-defining recurrent genetics (e.g. no t(8;21), no inv(16))",
                "No NPM1 mutation or CEBPA-bZIP mutation (these are now AML regardless of blast %)."
            ],
            "Subtypes": "Can be qualified as 'with mutated TP53', 'with myelodysplasia-related gene mutations', or 'NOS'."
        },
        "MDS with mutated SF3B1": {
            "Definition": "MDS with **SF3B1 mutation (VAF ≥10%)**. Ring sideroblasts are frequent but **not required** for diagnosis.",
            "Criteria": [
                "Cytopenias",
                "<5% blasts in BM, <2% in PB",
                "SF3B1 mutation",
                "Absence of: del(5q), -7/del(7q), complex karyotype, or multi-hit TP53."
            ],
            "Pearl": "Associated with favorable prognosis. Replaces 'MDS with Ring Sideroblasts'."
        },
        "MDS with mutated TP53": {
            "Definition": "MDS with **multi-hit (biallelic)** TP53 alteration.",
            "Criteria": [
                "Multi-hit TP53: Two distinct mutations, OR mutation + 17p deletion, OR mutation + VAF >50% (implies LOH).",
                "Blasts: 0–19% (Blast count does not impact the poor prognosis)."
            ],
            "Pearl": "Mono-allelic TP53 does not qualify for this specific high-risk entity."
        },
        "MDS with del(5q)": {
            "Definition": "MDS with isolated del(5q) or del(5q) + 1 other abnormality (except -7).",
            "Criteria": "<5% blasts BM. No multi-hit TP53."
        }
    },
    "MDS/MPN Overlap": {
        "Chronic Myelomonocytic Leukemia (CMML)": {
            "Definition": "Persistent monocytosis and clonality.",
            "Revised Criteria": [
                "**Monocytosis:** ≥0.5 x 10^9/L (lowered from 1.0) AND ≥10% of WBC.",
                "**Clonality:** Must demonstrate clonal mutation (e.g., TET2, SRSF2, ASXL1). If no clonality, monocytosis must be ≥1.0 x 10^9/L with dysplasia.",
                "**Subtypes:** CMML-1 (<5% PB blasts, <10% BM blasts) and CMML-2 (5-19% PB, 10-19% BM). CMML-0 is eliminated."
            ],
            "Genetics": "TET2 & SRSF2 co-mutation is highly suggestive."
        },
        "MDS/MPN with SF3B1 mutation and thrombocytosis": {
            "Definition": "Anemia + Thrombocytosis (≥450) + SF3B1 mutation.",
            "Criteria": [
                "SF3B1 mutation (VAF ≥10%)",
                "Ring sideroblasts often present but **not required**.",
                "Blasts <1% PB, <5% BM."
            ],
            "Pearl": "Replaces 'MDS/MPN-RS-T'. If SF3B1 is absent, diagnose as 'MDS/MPN-RS-T, NOS'."
        },
        "Atypical CML (aCML)": {
            "Definition": "Leukocytosis (≥13) with dysplastic neutrophils. 'BCR::ABL1 negative' dropped from name.",
            "Criteria": [
                "Leukocytosis ≥13 x 10^9/L",
                "Neutrophil precursors ≥10%",
                "**Dysgranulopoiesis** (hypogranular, hypolobated)",
                "Minimal monocytosis (<10%)",
                "**SETBP1** and **ETNK1** mutations common."
            ]
        }
    },
    "Myeloproliferative Neoplasms (MPN)": {
        "Chronic Myeloid Leukemia (CML)": {
            "Accelerated Phase (AP)": "Defined by 10–19% blasts, OR Basophils ≥20%, OR Additional Clonal Cytogenetics (ACA). Note: Platelet count criteria removed.",
            "Blast Phase (BP)": "≥20% blasts or myeloid sarcoma."
        },
        "Essential Thrombocythemia (ET) vs Pre-Fibrotic PMF": {
            "Differentiation": "Crucial distinction based on Megakaryocyte morphology.",
            "ET": "Mature, enlarged megs with hyperlobulated (staghorn) nuclei. Loose clusters. No fibrosis.",
            "Pre-PMF": "Atypical megs (cloud-like, bulbous, hyperchromatic). **Dense/Tight clusters**. Granulocytic proliferation."
        },
        "Chronic Neutrophilic Leukemia (CNL)": {
            "Criteria": "WBC ≥13 (if CSF3R mutated). **CSF3R T618I** is the hallmark mutation (80-100% of cases)."
        }
    },
    "Eosinophilic Disorders (M/LN-eo)": {
        "M/LN-eo with Tyrosine Kinase Fusions": {
            "Definition": " neoplasms with eosinophilia and specific gene fusions. Name updated from 'M/LN-eo with gene rearrangement'.",
            "New Entities": [
                "**ETV6::ABL1:** mimics CML or AML.",
                "**FLT3 rearrangements:** t(12;13) ETV6::FLT3.",
                "**PCM1::JAK2:** Now a formal entity (formerly provisional). Erythroid microtumors are characteristic."
            ],
            "Classic Entities": "PDGFRA (FIP1L1), PDGFRB (t(5;12)), FGFR1 (8p11).",
            "Therapy": "PDGFRA/B respond to Imatinib. FGFR1/FLT3 do not."
        },
        "Chronic Eosinophilic Leukemia, NOS (CEL, NOS)": {
            "New Criteria": "Requires **abnormal BM morphology** (dysplasia, fibrosis) AND blast count <20%. Must exclude all reactive causes and TK fusions.",
            "Cutoff": "Absolute Eos ≥1.5 AND Relative Eos ≥10%."
        }
    },
    "Plasma Cell Neoplasms": {
        "IgM MGUS": {
            "New Subtypes": [
                "**IgM MGUS, Plasma Cell Type:** No B-cell component, MYD88 WT, MM-type cytogenetics (t(11;14)). Precursor to IgM Myeloma.",
                "**IgM MGUS, NOS:** MYD88 mutated, or B-cell component present. Precursor to Waldenstrom."
            ]
        },
        "Multiple Myeloma (MM)": {
            "Genetic Subgroups": "ICC formally subdivides MM into: 1. MM with CCND translocations (t(11;14)), 2. MM with MAF translocations, 3. MM with NSD2 (t(4;14)), 4. MM with Hyperdiploidy.",
            "Smoldering MM": "Use 20/2/20 risk stratification. 10-60% plasma cells."
        },
        "Localized Amyloidosis": {
            "Update": "Localized AL amyloidosis (e.g., 'amyloidoma' of lung/bladder) is now a distinct entity from Systemic AL. Excellent prognosis."
        }
    }
}

WHO5_DATA = {
    "WHO5 AML broad categories": {
        "AML with defining genetic abnormalities": "6 fusion proteins, 3 rearrangements and 2 mutations",
        "AML, defined by differentiation": [
            "AML with minimal differentiation - blasts are negative for MPO and express 2 or more myeloid antigens such as CD13, CD33, CD117",
            "AML without maturation - blasts are positive for MPO and 2 or more myeloid antigens, maturing granulocytes represent less than 10% of bone marrow cellularity",
            "AML with maturation - blasts positive for MPO, neutrophils over 10% of cellularity, monocytes less than 20% of cellularity, two or more myeloid antigens such as CD13, CD33, CD117",
            "Acute basophilic, myelomonocytic (greater than 20% monos and greater than 20% neutrophils and related precursors, blasts positive for MPO), monocytic (greater than 80% monos/promonocytes and express at least two monocytic markers CD11c, CD14, CD36, CD64), erythroid (greater than 30% immature erythroid (proerythroblast)) and megakaryoblastic leukaemia (express one or more CD41, CD61 or CD42b)"
        ]
    },
    "I. Acute Myeloid Neoplasms (AML)": {
        "AML with Recurrent Genetic Alterations (No blast cutoff, except AML with BCR:ABL1 and CEBPA mutation (can be either biallelic and single mutations located in the bZIP region))": [
            "AML with **t(8;21)(q22;q22.1); RUNX1::RUNX1T1** - can do RT-qPCR MRD",
            "AML with **inv(16)(p13.1q22) or t(16;16)(p13.1;q22); CBFB::MYH11** - can do RT-qPCR MRD ",
            "AML with **t(15;17)(q22;q12); PML::RARA** - (Prognostically favorable) - can do RT-qPCR MRD",
            "AML with **t(6;9)(p23;q34.1); DEK::NUP214** (Poor prognosis)",
            "AML with **KMT2A rearrangement** - replaces t(9;11) due to 80 KMT2A fusion partners - MLLT3, MLLT10 most common (both in children show megakaryoblastic differentiation with low blast count, in adults show monocytic differentiation with high blast count",
            "AML with **NUP98 rearrangement**",
            "AML with **MECOM rearrangement** replaces inv(3)(q21.3q26.2) or t(3;3)(q21.3;q26.2); GATA2, MECOM (Poor prognosis)",
            "AML with **t(1;22)(p13.3;q13.3); RBM15::MRTFA** (Specific to Acute Megakaryoblastic Leukemia)",
            "AML with **mutated NPM1** (VAF > 3%) - irrespective of blast count",
            "AML with **CEBPA mutation** - can be either biallelic or single mutations located in the bZIP region",
        ],
        "AML, Defined by other criteria": [
            "AML **Myelodysplasia-Related (AML-MR)**: (Defined by VAF ≥ 10% in ASXL1, BCOR, EZH2, RUNX1, SF3B1, SRSF2, STAG2, U2AF1, ZRSR2)",
            "AML with **Myelodysplasia-Related Cytogenetics (AML-MR)**: (Includes Complex Karyotype -ie. 3 or more abnormalities, -7/del(7q), -5/del(5q), 11q deletion, 12p deletion, monosomy 13 or 13q, 17p deletion, isochrome 17q, idic(X)q13)",
            "**Acute Erythroid Leukemia** (Pure Erythroid Leukemia)",
            "**Acute Megakaryoblastic Leukemia (AMKL)** (NOS, t(1;22) excluded)",
            "**Acute Basophilic Leukemia** (Rare)",
            "**Acute Panmyelosis with Myelofibrosis** (APMF)",
            "**Myeloid Sarcoma** (Extramedullary AML)",
            "**AML with other defined genetic alterations** - reserved for new often rare and emerging entities",
            "**AML with mutated TP53** (Requires ≥20% blasts, associated with poor prognosis/MRGC)",
            "**Therapy-Related Myeloid Neoplasms (t-MN)** (≥20% blasts, no longer a separate AML subtype group but a modifier)",
        ]
    },
    "II. Myelodysplastic Syndromes (MDS)": {
        "MDS, Defined by Genetic Alteration (0-9% Blasts)": [
            "**MDS with mutated SF3B1**: (VAF ≥10% in a cytopenic patient, Ring Sideroblasts not required)",
            "**MDS with multi-hit/biallelic TP53 alteration** (0-19% blasts, if ≥20% it is AML with mutated TP53)",
        ],
        "MDS, Morphologic Categories (0-9% Blasts)": [
            "**MDS with Low Blast Count (MDS-LBC)**: (0-4% blasts in BM, <2% in PB)",
            "**MDS with Increased Blasts (MDS-IB)**: (5-9% blasts in BM, 2-9% in PB)",
            "**MDS, NOS**: (To be used when specific genetic/morphologic criteria are not met)",
        ]
    },
    "III. MDS/AML (New Transitional Category)": {
        "**MDS/AML**": [
            "Myeloid Neoplasm with **10–19% blasts** in Bone Marrow or Peripheral Blood.",
            "Lacks an AML-defining recurrent genetic alteration (RGA).",
            "This category replaces most cases previously classified as **MDS-EB2** (and some MDS/MPN-U)."
        ]
    },
    "IV. Myeloproliferative Neoplasms (MPN)": {
        "Chronic Myeloid Leukemia (CML), BCR::ABL1-Positive": [
            "CML, Chronic Phase",
            "CML, Accelerated Phase (Simplified criteria: 10-19% blasts, or persistent high counts/splenomegaly despite therapy)",
            "CML, Blast Phase (≥20% blasts, now including cases with T-cell lineage involvement)",
        ],
        "MPN - BCR::ABL1-Negative (Classical)": [
            "**Polycythemia Vera (PV)** (JAK2 V617F/Exon 12+ or Hgb criteria met)",
            "**Essential Thrombocythemia (ET)** (Requires JAK2, CALR, or MPL mutation or triple-negative with *no* significant reticulin fibrosis)",
            "**Primary Myelofibrosis (PMF)** (Pre-fibrotic and Overtly Fibrotic phases; Requires JAK2, CALR, or MPL or triple-negative with fibrosis and morphology)",
        ],
        "MPN - Other/NOS": [
            "**Chronic Neutrophilic Leukemia (CNL)** (CSF3R mutation is key)",
            "**Primary Hypereosinophilia (P-HE)** (Replaces Chronic Eosinophilic Leukemia, NOS and Idiopathic Hypereosinophilic Syndrome)",
            "**Mastocytosis** (New emphasis on KIT D816V and mast cell numbers/morphology): Includes Cutaneous Mastocytosis, Systemic Mastocytosis (SM), SM with an associated hematological neoplasm (SM-AHN), Mast Cell Leukemia, etc.",
        ]
    },
    "V. Myelodysplastic/Myeloproliferative Neoplasms (MDS/MPN)": {
        "MDS/MPN Overlap Entities": [
            "**Chronic Myelomonocytic Leukemia (CMML)**: (Requires persistent monocytosis: **≥0.5 x 10^9/L** AND **≥10% of WBC**)",
            "**Atypical Chronic Myeloid Leukemia, BCR::ABL1-Negative (aCML)**",
            "**Juvenile Myelomonocytic Leukemia (JMML)**: (RAS pathway mutation required)",
            "**Myeloid Neoplasm with SF3B1 mutation and Thrombocytosis (MN-SF3B1-T)** (New entity, replaces most MDS/MPN-RS-T)",
            "**MDS/MPN, Not Otherwise Specified (NOS)**",
        ]
    },
    "VI. Myeloid/Lymphoid Neoplasms with Tyrosine Kinase Fusions (M/LN-TK)": {
        "M/LN-TK Entities (Formerly M/LN-Eos)": [
            "M/LN-TK with **PDGFRA** rearrangement (FIP1L1::PDGFRA, ETV6::PDGFRA, etc.)",
            "M/LN-TK with **PDGFRB** rearrangement (ETV6::PDGFRB, etc.)",
            "M/LN-TK with **FGFR1** rearrangement (ZMYM2::FGFR1, etc.)",
            "M/LN-TK with **JAK2** rearrangement (PCM1::JAK2, BCR::JAK2, etc.)",
            "M/LN-TK with **ETV6::ABL1** fusion (NEW entity)",
            "M/LN-TK with various **FLT3** fusions (NEW entity)",
        ]
    }
}


# --- APP LAYOUT ---
st.title("HemePath Reporter Pro & Classification Guide")
st.markdown("---")

# --- SIDEBAR: DEMOGRAPHICS & CBC ---
with st.sidebar:
    st.header("Patient & CBC Data")
    accession = st.text_input("Accession Number", key="accession_input")
    age = st.number_input("Patient Age", min_value=0, max_value=120, value=60, key="age_input", on_change=update_bx_text)
    
    st.subheader("Peripheral Blood")
    wbc = st.text_input("WBC (x10^9/L)", "Normal", key="wbc")
    hb = st.text_input("Hemoglobin (g/L)", "Normal", key="hb")
    plt = st.text_input("Platelets (x10^9/L)", "Normal", key="plt")
    
    cbc_summary = f"CBC shows WBC {wbc}, Hb {hb}, and Platelets {plt}."
    if st.checkbox("Pancytopenia present?"):
        cbc_summary = "CBC shows pancytopenia."

# --- TABBED INTERFACE ---
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "1. PB (Blood Film)", 
    "2. Aspirate", 
    "3. Biopsy & IHC", 
    "4. Ancillary", 
    "5. FINAL REPORT",
    "6. My Notes",
    "7. Heme Classification Refs"
])

# ==========================================
# TAB 1: PERIPHERAL BLOOD
# ==========================================
with tab1:
    st.header("Peripheral Blood Morphology")
    
    col_pb1, col_pb2 = st.columns(2)
    
    with col_pb1:
        st.subheader("Red Blood Cells")
        st.multiselect("RBC Morphology", 
            ["unremarkable morphology", "non-specific morphology", 
             "normochromic", "normocytic", 
             "dimorphic population", "mild anisopoikilocytosis", "moderate anisopoikilocytosis", 
             "severe anisopoikilocytosis", "hypochromia", "polychromasia", "spherocytes", 
             "schistocytes", "dacrocytes (teardrops)", "elliptocytes", "target cells", 
             "basophilic stippling", "Howell-Jolly bodies", "Rouleaux formation"],
            key='rbc_morph', on_change=update_pb_text)
        
        st.divider()
        
        st.subheader("Platelets")
        st.multiselect("Platelet Morphology", 
            ["small and well granulated", "unremarkable", "variable in size with occasional large forms",
             "hypogranular", "large/giant forms present", "platelet clumps/aggregates seen"],
            key='plt_morph', on_change=update_pb_text)

    with col_pb2:
        st.subheader("Neutrophils")
        st.multiselect("Neutrophil Morphology", 
            ["normal morphology with appropriate granulation and segmentation", "unremarkable",
             "left-shifted", "toxic granulation", "hypogranular", 
             "Pseudo-Pelger-Huet anomalies", "abnormal chromatin clumping", "hypersegmented"],
            key='neut_morph', on_change=update_pb_text)
             
        st.divider()

        st.subheader("Lymphocytes") # NEW
        st.multiselect("Lymphocyte Morphology", 
            ["appear small and mature", "appear monomorphic", 
             "CLL-like cells", "cells with prominent nucleoli (prolymphocytes)",
             "cells with hairy-like projections with monocytoid morphology",
             "large granular lymphocytes", "reactive lymphocytes"],
            key='lymph_morph', on_change=update_pb_text)

        st.divider()
             
        st.subheader("Blasts (PB)")
        st.number_input("PB Blast % (Enter 0 for 'No blasts identified')", 0, 100, key="pb_blast_pct", on_change=update_pb_text)
        
        st.multiselect("PB Blast Description (Select features if >0%)", 
            ["high N:C ratio", "dispersed chromatin", "prominent nucleoli", 
             "agranular cytoplasm", "monoblastic features", "circulating micromegakaryocytes"],
            key="pb_blast_desc", on_change=update_pb_text)
        
        if st.session_state.pb_blast_pct > 0:
            st.radio("Auer Rods (PB)", ["No Auer rods seen", "Auer rods present"], key="pb_auer", on_change=update_pb_text)
        else:
            st.caption("Auer Rod status is included only if Blasts % > 0.")

    st.divider()
    st.subheader("📝 PB Report Draft (Editable)")
    st.caption("This text updates automatically as you select options above. You can also edit it manually.")
    st.text_area("Peripheral Blood Section", key="pb_report_draft", height=150)

# ==========================================
# TAB 2: ASPIRATE
# ==========================================
with tab2:
    st.header("Bone Marrow Aspirate")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Quality Assessment")
        st.selectbox("Overall Quality", ["Adequate quality for interpretation", "Excellent quality for interpretation", "Suboptimal quality for interpretation"], key="asp_status", on_change=update_asp_text)
        st.multiselect("Quality Descriptors/Limitations", 
            ["hemodiluted", "particulate", "clotted", "dry tap (punctio sicca)", "limited cellularity", "crush artifact"],
            key="asp_reasons", on_change=update_asp_text)
        
        st.text_input("M:E Ratio", key="me_ratio", on_change=update_asp_text)
        st.number_input("Marrow Blast %", 0, 100, key="bm_blast_pct", on_change=update_asp_text)
        
    with col2:
        st.subheader("Marrow Blast Morphology")
        st.multiselect("Descriptors", 
            ["high N:C ratio", "fine/dispersed chromatin", "prominent nucleoli", 
             "agranular cytoplasm", "moderate cytoplasm", "monoblastic morphology", 
             "cytoplasmic vacuolization", "cup-like nuclei"],
            key="bm_blast_desc", on_change=update_asp_text)
        if st.session_state.bm_blast_pct > 0:
            st.radio("Auer Rods (Marrow)", ["No Auer rods seen", "Auer rods identified"], key="bm_auer", on_change=update_asp_text)
        else:
            st.caption("Auer Rod status is included only if Blasts % > 0.")
    
    st.divider()
    
    # LINEAGES
    col3, col4, col5 = st.columns(3)
    
    with col3:
        st.subheader("Erythropoiesis")
        st.selectbox("Erythroid Maturation", 
            ["shows full spectrum maturation with no dysplasia", 
             "shows full spectrum maturation", 
             "is left-shifted", 
             "shows maturation arrest"],
            key="ery_maturation", on_change=update_asp_text)
        st.multiselect("Erythroid Dysplasia", 
            ["megaloblastoid change", "nuclear budding", "internuclear bridging", 
             "karyorrhexis", "poor hemoglobinization", "vacuolization", "multinucleation"],
            key="ery_dysplasia", on_change=update_asp_text)
        
    with col4:
        st.subheader("Granulopoiesis")
        st.selectbox("Granulocyte Maturation", 
            ["shows full spectrum maturation with no dysplasia",
             "shows sequential maturation to neutrophils", 
             "is left-shifted", 
             "shows maturation arrest"],
            key="gran_maturation", on_change=update_asp_text)
        st.multiselect("Granulocyte Dysplasia", 
            ["hypogranularity", "hyposegmentation (Pseudo-Pelger)", 
             "abnormal chromatin clumping", "hypersegmentation", 
             "Dohle bodies", "pseudo Chediak-Higashi granules"], # UPDATED
            key="gran_dysplasia", on_change=update_asp_text)
            
    with col5:
        st.subheader("Megakaryocytes")
        st.select_slider("Quantity", ["Absent", "Decreased", "Normal", "Increased", "Markedly Increased"], key="meg_number", on_change=update_asp_text)
        st.multiselect("Megakaryocyte Morphology", 
            ["unremarkable with no dysplastic features",
             "pleomorphic", "large/hyperlobulated", "staghorn-like nuclei", 
             "hypolobated forms", "micromegakaryocytes", "widely separated nuclear lobes", "multinuclearity"], # UPDATED
            key="meg_morph", on_change=update_asp_text)

    st.divider()
    
    # Plasma & Mast Cells (NEW)
    col_pm1, col_pm2 = st.columns(2)
    with col_pm1:
        st.subheader("Plasma Cells")
        st.multiselect("Plasma Cell Morphology", 
            ["large bizarre plasma cells", "plasma cells with binucleation", "plasma cells with multinucleation", 
             "large plasma cells", "medium sized plasma cells", "small plasma cells", "unremarkable"],
            key="asp_plasma_morph", on_change=update_asp_text)
            
    with col_pm2:
        st.subheader("Mast Cells")
        st.selectbox("Mast Cells Status", ["No increase in mast cells", "Increased mast cells", "Spindle shaped mast cells"], key="asp_mast_cells", on_change=update_asp_text)

    st.divider()
    st.select_slider("Iron Stores", ["Absent", "Decreased", "Normal", "Increased"], key="iron_stores", on_change=update_asp_text)
    st.radio("Ring Sideroblasts", ["No ring sideroblasts seen", "Rare ring sideroblasts", "Ring sideroblasts present (>15%)"], key="ring_sideroblasts", on_change=update_asp_text)

    st.divider()
    st.subheader("📝 Aspirate Report Draft (Editable)")
    st.caption("This text updates automatically as you select options above. You can also edit it manually.")
    st.text_area("Aspirate Section", key="asp_report_draft", height=200)

# ==========================================
# TAB 3: BIOPSY & IHC
# ==========================================
with tab3:
    st.header("Bone Marrow Biopsy")
    
    st.selectbox("Biopsy Quality", 
        ["adequate quality for interpretation", "Excellent quality for interpretation", "fragmented", "suboptimal due to crush artifact", "uninterpretable"],
        key="bx_quality", on_change=update_bx_text)
    
    col_b1, col_b2 = st.columns(2)
    
    with col_b1:
        st.slider("Cellularity (%)", 0, 100, step=5, key="cellularity", on_change=update_bx_text)
        # Logic for Hyper/Hypo based on age
        expected = 100 - age
        if st.session_state.cellularity > (expected + 15):
            c_status = "hypercellular"
        elif st.session_state.cellularity < (expected - 15):
            c_status = "hypocellular"
        else:
            c_status = "normocellular"
        st.info(f"Assessment: {st.session_state.cellularity}% is {c_status} for age {age}.")
    
    with col_b2:
        st.subheader("Reticulin Status")
        st.radio("Streaming Assessment", 
            ["No obvious streaming to suggest fibrosis is present", 
             "Streaming is present suggestive of fibrosis"],
            key="streaming_status", on_change=update_bx_text)

    st.subheader("Architecture & Stromal Changes (Multi-select)")
    
    st.radio("Erythroid Island Distribution",
        ["Erythroid islands are prominent and numerous",
         "Occasional erythroid islands are noted",
         "Erythroid islands are present in expected numbers",
         "Erythroid islands are reduced/absent"],
        key="erythroid_island_status", on_change=update_bx_text)

    # Granulocytes Section (NEW)
    st.text_input("Granulocytes (Biopsy)", value="Granulocytes are well represented and show full spectrum maturation", key="bx_granulocytes", on_change=update_bx_text)
         
    st.multiselect("Select Features", 
        ["Bone marrow architecture is preserved and orderly", 
         "Trilineage hematopoiesis present", 
         "Erythroid predominance", 
         "Granulocytic predominance", 
         "ALIP (Abnormal Localization of Immature Precursors)", 
         "No blast clusters are identified", 
         "Discrete blast clusters identified", 
         "No lymphoid aggregates are seen", 
         "Lymphoid aggregates are seen (usually mature)", 
         "No non-hematopoietic elements present", 
         "Dilated sinusoids", 
         "Stromal edema", 
         "Serous atrophy of fat", 
         "Granulomas"],
        key="arch_features", on_change=update_bx_text
        )
    
    st.subheader("Megakaryocyte Distribution")
    st.radio("Distribution Pattern", 
        ["Randomly distributed", "Loose clustering", "Dense clustering (>6 cells)", "Paratrabecular location"],
        key="meg_dist", on_change=update_bx_text)

    st.divider()
    st.subheader("📝 Biopsy Report Draft (Editable)")
    st.text_area("Biopsy Section", key="bx_report_draft", height=200)

    st.divider()
    st.header("Immunohistochemistry (IHC) Summary")

    st.subheader("IHC Markers Performed")
    ihc_markers_list = ["CD34", "CD3", "CD20", "CD117", "CD138", "Kappa light chain", "Lambda light chain", "CD42b", "Reticulin"]
    st.multiselect("Select Markers Used", ihc_markers_list, default=["CD34", "CD3", "CD20"], key="ihc_markers_selected")
    
    default_ihc_text = """Immunohistochemical staining for CD34 highlights blasts which account for <X>% of the cellularity.
CD3 highlights T cells in a reactive distribution pattern.
CD20 highlights interstitial B cells with no aggregates seen.
CD117 highlights occasional mast cells (non-diagnostic).
CD138 highlights scattered plasma cells (no significant increase).
Kappa light chain and Lambda light chain are polytypic in distribution."""
    st.text_area("IHC Narrative (Edit as needed for selected markers)", value=default_ihc_text, height=250, key="ihc_report_draft")


# ==========================================
# TAB 4: ANCILLARY
# ==========================================
with tab4:
    st.header("Ancillary Studies")
    st.text_area("Flow Cytometry", "No increased blasts or aberrant populations detected.", key="flow_cyto_input")
    st.text_area("Cytogenetics / FISH", "Pending.", key="cyto_input")
    st.text_area("Molecular (NGS)", "Pending.", key="ngs_input")

# ==========================================
# TAB 5: REPORT GENERATION
# ==========================================
with tab5:
    st.header("Final Generated Report")
    st.success("Copy and paste the text below into your LIS.")
    
    # --- DX TEMPLATE LOGIC ---
    # We calculate this on the fly based on current state
    dx_suggestion = "BONE MARROW, ASPIRATE AND BIOPSY:"
    if st.session_state.bm_blast_pct >= 20:
        dx_suggestion += "\n- ACUTE LEUKEMIA (See Comment)"
    elif st.session_state.bm_blast_pct >= 10:
         dx_suggestion += "\n- MDS/AML (10-19% blasts) or HIGH GRADE MDS (See Comment)"
    elif "staghorn-like nuclei" in st.session_state.meg_morph:
        dx_suggestion += "\n- MYELOPROLIFERATIVE NEOPLASM (See Comment)"
    elif len(st.session_state.ery_dysplasia) > 0 or len(st.session_state.gran_dysplasia) > 0:
        dx_suggestion += "\n- MYELODYSPLASTIC NEOPLASM (MDS) (See Comment)"
    else:
        dx_suggestion += "\n- NO DIAGNOSTIC ABNORMALITY RECOGNIZED"
    
    # Combine edits from previous tabs
    ihc_section = ""
    if st.session_state.ihc_report_draft.strip():
        ihc_section = f"\nIMMUNOHISTOCHEMISTRY (IHC):\n{st.session_state.ihc_report_draft}\n"

    full_report = f"""
{dx_suggestion}

CLINICAL HISTORY:
{age}-year-old. {cbc_summary}

PERIPHERAL BLOOD:
{st.session_state.pb_report_draft}

BONE MARROW BIOPSY:
{st.session_state.bx_report_draft}

BONE MARROW ASPIRATE:
{st.session_state.asp_report_draft}

ANCILLARY STUDIES:
{ihc_section}
Flow Cytometry: {st.session_state.flow_cyto_input}
Cytogenetics: {st.session_state.cyto_input}
Molecular (NGS): {st.session_state.ngs_input}
    """
    
    st.text_area("Final Report", value=full_report, height=800)

    # Save to Notes Button
    st.divider()
    if st.button("💾 Save Final Report to My Notes"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        report_title = f"\n\n--- SAVED REPORT (Accession: {accession if accession else 'N/A'}, {age}y, {st.session_state.bm_blast_pct}% BM Blasts) - {timestamp} ---\n"
        
        st.session_state['saved_reports'] += report_title + full_report
        st.success("Report successfully saved to 'My Notes' tab.")

# ==========================================
# TAB 6: MY NOTES / ARCHIVE
# ==========================================
with tab6:
    st.header("My Reference Notes")
    st.info("These notes are pulled from the USER_NOTES_DATABASE in the code. Use the second box for reports saved from the 'FINAL REPORT' tab.")

    for category, note_content in USER_NOTES_DATABASE.items():
        with st.expander(f"📂 {category} Notes", expanded=False):
            st.text_area(f"Edit {category} Notes:", value=note_content.strip(), height=200, key=f"note_{category}")

    st.divider()
    st.subheader("Saved Final Reports Archive")
        
    st.text_area("Archived Reports (Cleared when app is restarted)", value=st.session_state['saved_reports'], height=400)
    
    if st.button("Clear Archived Reports"):
        st.session_state['saved_reports'] = ""
        st.rerun()


# ==========================================
# TAB 7: HEME CLASSIFICATION REFS
# ==========================================
with tab7:
    st.header("Heme Classification Reference Library")
    
    search_term = st.text_input("Search Database (e.g., 'CMML', 'SF3B1', '10%')")

    # --- WHO 5th EDITION SECTION ---
    st.subheader("🧬 WHO 5th Edition: Myeloid & Histiocytic/Dendritic Neoplasms")
    
    for category, entities in WHO5_DATA.items():
        # Search filter check for category
        if search_term and search_term.lower() not in category.lower():
            entity_match = False
            for ename, edata in (entities.items() if isinstance(entities, dict) else {k: k for k in entities}.items()):
                if search_term.lower() in ename.lower() or str(edata).lower().find(search_term.lower()) != -1:
                    entity_match = True
                    break
            if not entity_match:
                continue

        with st.expander(category, expanded=True if search_term else False):
            if isinstance(entities, dict):
                for entity_name, details in entities.items():
                    if search_term and search_term.lower() not in entity_name.lower() and str(details).lower().find(search_term.lower()) == -1:
                        continue
                        
                    st.markdown(f"**{entity_name}:**")
                    if isinstance(details, list):
                        for item in details:
                            st.markdown(f"- {item}")
                    elif isinstance(details, str):
                        st.markdown(details)
                    st.markdown("---")
            elif isinstance(entities, list):
                for item in entities:
                    if search_term and search_term.lower() not in item.lower():
                        continue
                    st.markdown(f"- {item}")
                st.markdown("---")

    st.markdown("---")

    # --- ICC 2022 SECTION ---
    st.subheader("🔬 ICC 2022 Reference Library")

    for category, entities in ICC_DATA.items():
        if search_term:
            cat_match = search_term.lower() in category.lower()
            entity_match = False
            for ename, edata in entities.items():
                if search_term.lower() in ename.lower() or str(edata).lower().find(search_term.lower()) != -1:
                    entity_match = True
                    break
            if not (cat_match or entity_match):
                continue

        with st.expander(category, expanded=True if search_term else False):
            for entity_name, details in entities.items():
                if search_term and search_term.lower() not in entity_name.lower() and str(details).lower().find(search_term.lower()) == -1:
                    continue
                    
                st.markdown(f"### {entity_name}")
                if isinstance(details, dict):
                    for key, value in details.items():
                        if isinstance(value, list):
                            st.markdown(f"**{key}:**")
                            for item in value:
                                st.markdown(f"- {item}")
                        else:
                            st.markdown(f"**{key}:** {value}")
                st.markdown("---")