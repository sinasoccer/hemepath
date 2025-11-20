import streamlit as st
from datetime import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="HemePath Reporter Pro", layout="wide")

# ==========================================
# 0. SAFETY INITIALIZATION & DEFAULTS
# ==========================================
if 'saved_reports' not in st.session_state:
    st.session_state['saved_reports'] = ""

# Set default values for all report variables
rbc_morph = []
plt_morph = []
neut_morph = []
pb_blast_pct = 0
pb_blast_desc = []
pb_auer = "No Auer rods seen"
asp_status = "Adequate quality for interpretation"
asp_reasons = []
me_ratio = "2:1"
blast_pct = 1
blast_desc = []
auer_rods = "No Auer rods seen"
ery_maturation = "shows full spectrum maturation with no dysplasia"
ery_dysplasia = []
gran_maturation = "shows full spectrum maturation with no dysplasia"
gran_dysplasia = []
meg_number = "Normal"
meg_morph = []
iron_stores = "Normal"
ring_sideroblasts = "No ring sideroblasts seen"
bx_quality = "adequate quality for interpretation"
cellularity = 40
age = 60 # Default age needed for cellularity calculation
cell_status = "normocellular" # Default for initialization
streaming_status = "No obvious streaming to suggest fibrosis is present" 
erythroid_island_status = "Erythroid islands are present in expected numbers"
arch_features = []
meg_dist = "Randomly distributed"
ihc_report_text = ""
ihc_markers_selected = []


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

# --- ICC 2022 DATA (UPDATED as requested, comprehensive) ---
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


# --- WHO 5th EDITION DATA (NEW, EXPANDED, AND COMPREHENSIVE - Unchanged from previous step) ---
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
    age = st.number_input("Patient Age", min_value=0, max_value=120, value=60, key="age_input")
    
    st.subheader("Peripheral Blood")
    wbc = st.text_input("WBC (x10^9/L)", "Normal")
    hb = st.text_input("Hemoglobin (g/L)", "Normal")
    plt = st.text_input("Platelets (x10^9/L)", "Normal")
    
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
# (No changes here, keeping code concise for display)
# ==========================================
with tab1:
    st.header("Peripheral Blood Morphology")
    
    col_pb1, col_pb2 = st.columns(2)
    
    with col_pb1:
        st.subheader("Red Blood Cells")
        rbc_morph = st.multiselect("RBC Morphology", 
            ["unremarkable morphology", "non-specific morphology", 
             "normochromic", "normocytic", 
             "dimorphic population", "mild anisopoikilocytosis", "moderate anisopoikilocytosis", 
             "severe anisopoikilocytosis", "hypochromia", "polychromasia", "spherocytes", 
             "schistocytes", "dacrocytes (teardrops)", "elliptocytes", "target cells", 
             "basophilic stippling", "Rouleaux formation"],
            default=["unremarkable morphology"])
        
        st.divider()
        
        st.subheader("Platelets")
        plt_morph = st.multiselect("Platelet Morphology", 
            ["small and well granulated", "unremarkable", "variable in size with occasional large forms",
             "hypogranular", "large/giant forms present", "platelet clumps/aggregates seen"],
            default=["small and well granulated"])

    with col_pb2:
        st.subheader("Neutrophils")
        neut_morph = st.multiselect("Neutrophil Morphology", 
            ["normal morphology with appropriate granulation and segmentation", "unremarkable",
             "left-shifted", "toxic granulation", "hypogranular", 
             "Pseudo-Pelger-Huet anomalies", "abnormal chromatin clumping", "hypersegmented"],
            default=["normal morphology with appropriate granulation and segmentation"])
             
        st.divider()
             
        st.subheader("Blasts (PB)")
        pb_blast_pct = st.number_input("PB Blast % (Enter 0 for 'No blasts identified')", 0, 100, 0, key="pb_blast_pct_input")
        
        pb_blast_desc = st.multiselect("PB Blast Description (Select features if >0%)", 
            ["high N:C ratio", "dispersed chromatin", "prominent nucleoli", 
             "agranular cytoplasm", "monoblastic features", "circulating micromegakaryocytes"])
        
        if pb_blast_pct > 0:
            pb_auer = st.radio("Auer Rods (PB)", ["No Auer rods seen", "Auer rods present"], key="pb_auer_input")
        else:
            pb_auer = "No Auer rods seen"
            st.caption("Auer Rod status is included only if Blasts % > 0.")

# ==========================================
# TAB 2: ASPIRATE
# (No changes here, keeping code concise for display)
# ==========================================
with tab2:
    st.header("Bone Marrow Aspirate")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Quality Assessment")
        asp_status = st.radio("Overall Quality", ["Adequate quality for interpretation", "Suboptimal quality for interpretation"])
        asp_reasons = st.multiselect("Quality Descriptors/Limitations", 
            ["hemodiluted", "particulate", "clotted", "dry tap (punctio sicca)", "limited cellularity", "crush artifact"])
        
        me_ratio = st.text_input("M:E Ratio", "2:1")
        blast_pct = st.number_input("Marrow Blast %", 0, 100, 1, key="bm_blast_pct_input")
        
    with col2:
        st.subheader("Marrow Blast Morphology")
        blast_desc = st.multiselect("Descriptors", 
            ["high N:C ratio", "fine/dispersed chromatin", "prominent nucleoli", 
             "agranular cytoplasm", "moderate cytoplasm", "monoblastic morphology", 
             "cytoplasmic vacuolization", "cup-like nuclei"])
        if blast_pct > 0:
            auer_rods = st.radio("Auer Rods (Marrow)", ["No Auer rods seen", "Auer rods identified"], key="bm_auer_input")
        else:
            auer_rods = "No Auer rods seen"
            st.caption("Auer Rod status is included only if Blasts % > 0.")
    
    st.divider()
    
    # LINEAGES
    col3, col4, col5 = st.columns(3)
    
    with col3:
        st.subheader("Erythropoiesis")
        ery_maturation = st.selectbox("Erythroid Maturation", 
            ["shows full spectrum maturation with no dysplasia", 
             "shows full spectrum maturation", 
             "is left-shifted", 
             "shows maturation arrest"])
        ery_dysplasia = st.multiselect("Erythroid Dysplasia", 
            ["megaloblastoid change", "nuclear budding", "internuclear bridging", 
             "karyorrhexis", "poor hemoglobinization", "vacuolization", "multinucleation"])
        
    with col4:
        st.subheader("Granulopoiesis")
        gran_maturation = st.selectbox("Granulocyte Maturation", 
            ["shows full spectrum maturation with no dysplasia",
             "shows sequential maturation to neutrophils", 
             "is left-shifted", 
             "shows maturation arrest"])
        gran_dysplasia = st.multiselect("Granulocyte Dysplasia", 
            ["hypogranularity", "hyposegmentation (Pseudo-Pelger)", 
             "abnormal chromatin clumping", "hypersegmentation", "nuclear projections", "giant bands"])
            
    with col5:
        st.subheader("Megakaryocytes")
        meg_number = st.select_slider("Quantity", ["Absent", "Decreased", "Normal", "Increased", "Markedly Increased"])
        meg_morph = st.multiselect("Megakaryocyte Morphology", 
            ["unremarkable with no dysplastic features",
             "pleomorphic", "large/hyperlobulated", "staghorn-like nuclei", 
             "hypolobated forms", "micromegakaryocytes", "widely separated nuclear lobes"])

    st.divider()
    iron_stores = st.select_slider("Iron Stores", ["Absent", "Decreased", "Normal", "Increased"])
    ring_sideroblasts = st.radio("Ring Sideroblasts", ["No ring sideroblasts seen", "Rare ring sideroblasts", "Ring sideroblasts present (>15%)"])

# ==========================================
# TAB 3: BIOPSY & IHC
# (No changes here, keeping code concise for display)
# ==========================================
with tab3:
    st.header("Bone Marrow Biopsy")
    
    bx_quality = st.selectbox("Biopsy Quality", 
        ["adequate quality for interpretation", "fragmented", "suboptimal due to crush artifact", "uninterpretable"])
    
    col_b1, col_b2 = st.columns(2)
    
    with col_b1:
        cellularity = st.slider("Cellularity (%)", 0, 100, 40, step=5)
        
        # Logic for Hyper/Hypo based on age
        expected = 100 - age
        if cellularity > (expected + 15):
            cell_status = "hypercellular"
        elif cellularity < (expected - 15):
            cell_status = "hypocellular"
        else:
            cell_status = "normocellular"
            
        st.info(f"Assessment: {cellularity}% is {cell_status} for age {age}.")
    
    with col_b2:
        # NEW Fibrosis/Streaming Section (Replaces WHO Grade)
        st.subheader("Reticulin Status")
        streaming_status = st.radio("Streaming Assessment", 
            ["No obvious streaming to suggest fibrosis is present", 
             "Streaming is present suggestive of fibrosis"])

    st.subheader("Architecture & Stromal Changes (Multi-select)")
    
    # NEW Erythroid Island Section (moved before megakaryocyte dist)
    erythroid_island_status = st.radio("Erythroid Island Distribution",
        ["Erythroid islands are prominent and numerous",
         "Occasional erythroid islands are noted",
         "Erythroid islands are present in expected numbers",
         "Erythroid islands are reduced/absent"])
         
    arch_features = st.multiselect("Select Features", 
        ["Bone marrow architecture is preserved and orderly", 
         "Trilineage hematopoiesis present", 
         "Erythroid predominance", 
         "Granulocytic predominance", 
         "ALIP (Abnormal Localization of Immature Precursors)", 
         "No blast clusters are identified", 
         "Discrete blast clusters identified", 
         "No lymphoid aggregates are seen", 
         "Lymphoid aggregates are seen (usually mature)", 
         "No non-hematopoietic elements present", # NEW
         "Dilated sinusoids", 
         "Stromal edema", 
         "Serous atrophy of fat", 
         "Granulomas"],
        default=["Bone marrow architecture is preserved and orderly", "Trilineage hematopoiesis present", "No blast clusters are identified", "No lymphoid aggregates are seen", "No non-hematopoietic elements present"]
        )
    
    st.subheader("Megakaryocyte Distribution")
    meg_dist = st.radio("Distribution Pattern", 
        ["Randomly distributed", "Loose clustering", "Dense clustering (>6 cells)", "Paratrabecular location"])

    st.divider()
    st.header("Immunohistochemistry (IHC) Summary")

    st.subheader("IHC Markers Performed")
    ihc_markers_list = ["CD34", "CD3", "CD20", "CD117", "CD138", "Kappa light chain", "Lambda light chain", "CD42b", "Reticulin"]
    ihc_markers_selected = st.multiselect("Select Markers Used", ihc_markers_list, default=["CD34", "CD3", "CD20"])
    
    default_ihc_text = """
Immunohistochemical staining for CD34 highlights blasts which account for <X>% of the cellularity.
CD3 highlights T cells in a reactive distribution pattern.
CD20 highlights interstitial B cells with no aggregates seen.
CD117 highlights occasional mast cells (non-diagnostic).
CD138 highlights scattered plasma cells (no significant increase).
Kappa light chain and Lambda light chain are polytypic in distribution.
"""
    ihc_report_text = st.text_area("IHC Narrative (Edit as needed for selected markers)", default_ihc_text.strip(), height=250, key="ihc_report_text_input")


# ==========================================
# TAB 4: ANCILLARY
# (No changes here, keeping code concise for display)
# ==========================================
with tab4:
    st.header("Ancillary Studies")
    flow_cyto_input = st.text_area("Flow Cytometry", "No increased blasts or aberrant populations detected.", key="flow_cyto_input")
    cyto_input = st.text_area("Cytogenetics / FISH", "Pending.", key="cyto_input")
    ngs_input = st.text_area("Molecular (NGS)", "Pending.", key="ngs_input")

# ==========================================
# TAB 5: REPORT GENERATION
# (Report assembly logic is here, but the code structure for assembly is omitted for conciseness)
# ==========================================
with tab5:
    st.header("Final Generated Report")
    st.success("Copy and paste the text below into your LIS.")
    
    # --- PB CONSTRUCTION ---
    neut_str = ", ".join(neut_morph) if neut_morph else "unremarkable"
    plt_str = ", ".join(plt_morph) if plt_morph else "unremarkable"
    
    # NEW RBC Logic:
    rbc_phrase = ""
    if "unremarkable morphology" in rbc_morph and len(rbc_morph) <= 2 and ("normochromic" in rbc_morph or "normocytic" in rbc_morph or len(rbc_morph) == 1):
        rbc_phrase = "have unremarkable morphology"
    elif "non-specific morphology" in rbc_morph:
        rbc_phrase = "show non-specific morphology"
    elif rbc_morph:
        filtered_morph = [m for m in rbc_morph if m not in ["unremarkable morphology", "non-specific morphology"]]
        if filtered_morph:
            rbc_phrase = f"are {', '.join(filtered_morph)}"
        else:
            rbc_phrase = "have unremarkable morphology"
    else:
        rbc_phrase = "have unremarkable morphology"
        
    if pb_blast_pct > 0:
        pb_desc_str = ", ".join(pb_blast_desc) if pb_blast_desc else "unremarkable morphology"
        pb_blast_text = f"Blasts account for {pb_blast_pct}% of leukocytes. They exhibit {pb_desc_str}. {pb_auer}."
    else:
        pb_blast_text = "No blasts are identified."

    pb_report = f"""
PERIPHERAL BLOOD:
Red blood cells {rbc_phrase}.
Neutrophils are {neut_str}.
Platelets are {plt_str}.
{pb_blast_text}
    """
    
    # --- BIOPSY CONSTRUCTION ---
    arch_text_statements = [f"{item}." for item in arch_features] if arch_features else ["Bone marrow architecture is preserved."]
    arch_text = "\n".join(arch_text_statements)
    
    biopsy_text = f"""
BONE MARROW BIOPSY:
The bone marrow biopsy is of {bx_quality}.
The cellularity is approximately {cellularity}%, which is {cell_status} for age.
{arch_text}
{erythroid_island_status}.
{streaming_status}.
Megakaryocytes are {meg_dist.lower()}.
Trabecular bone is unremarkable.
    """

    # --- ASPIRATE CONSTRUCTION ---
    if asp_reasons:
        quality_str = f"{asp_status}, {', '.join(asp_reasons)}"
    else:
        quality_str = asp_status

    blast_full_str = f"Blasts account for {blast_pct}% of the differential count."
    if blast_pct > 0:
        blast_desc_text = ", ".join(blast_desc) if blast_desc else "unremarkable morphology"
        blast_full_str += f" The blasts exhibit {blast_desc_text}. {auer_rods}."
    else:
        blast_full_str = "No blasts are identified."

    ery_dys_text = f" Dysplastic features include {', '.join(ery_dysplasia)}." if ery_dysplasia else ""
    gran_dys_text = f" Dysplastic features include {', '.join(gran_dysplasia)}." if gran_dysplasia else ""
    meg_morph_str = ", ".join(meg_morph) if meg_morph else "unremarkable morphology"

    aspirate_text = f"""
BONE MARROW ASPIRATE:
The bone marrow aspirate is of {quality_str}.
The myeloid-to-erythroid (M:E) ratio is {me_ratio}.
{blast_full_str}
Erythropoiesis {ery_maturation}.{ery_dys_text}
Granulopoiesis {gran_maturation}.{gran_dys_text}
Megakaryocytes are {meg_number.lower()} and display {meg_morph_str}.
Iron staining shows {iron_stores.lower()} iron stores.
{ring_sideroblasts}.
    """
    
    # --- IHC CONSTRUCTION ---
    ihc_section = ""
    if ihc_report_text.strip():
        ihc_section = f"""
IMMUNOHISTOCHEMISTRY (IHC):
{ihc_report_text}
"""

    # --- DX TEMPLATE ---
    dx_suggestion = "BONE MARROW, ASPIRATE AND BIOPSY:"
    if blast_pct >= 20:
        dx_suggestion += "\n- ACUTE LEUKEMIA (See Comment)"
    elif blast_pct >= 10:
         dx_suggestion += "\n- MDS/AML (10-19% blasts) or HIGH GRADE MDS (See Comment)"
    elif "staghorn-like nuclei" in meg_morph:
        dx_suggestion += "\n- MYELOPROLIFERATIVE NEOPLASM (See Comment)"
    elif len(ery_dysplasia) > 0 or len(gran_dysplasia) > 0:
        dx_suggestion += "\n- MYELODYSPLASTIC NEOPLASM (MDS) (See Comment)"
    else:
        dx_suggestion += "\n- NO DIAGNOSTIC ABNORMALITY RECOGNIZED"

    # --- FULL ASSEMBLY ---
    full_report = f"""
{dx_suggestion}

CLINICAL HISTORY:
{age}-year-old. {cbc_summary}
{pb_report}
{biopsy_text}
{aspirate_text}

ANCILLARY STUDIES:
{ihc_section}
Flow Cytometry: {flow_cyto_input}
Cytogenetics: {cyto_input}
Molecular (NGS): {ngs_input}
    """
    
    st.text_area("Final Report", value=full_report, height=800)

    # Save to Notes Button
    st.divider()
    if st.button("💾 Save Final Report to My Notes"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        report_title = f"\n\n--- SAVED REPORT (Accession: {accession if accession else 'N/A'}, {age}y, {blast_pct}% BM Blasts) - {timestamp} ---\n"
        
        st.session_state['saved_reports'] += report_title + full_report
        st.success("Report successfully saved to 'My Notes' tab.")

# ==========================================
# TAB 6: MY NOTES / ARCHIVE
# (No changes here, keeping code concise for display)
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
        st.experimental_rerun()


# ==========================================
# TAB 7: HEME CLASSIFICATION REFS (UPDATED)
# ==========================================
with tab7:
    st.header("Heme Classification Reference Library")
    
    search_term = st.text_input("Search Database (e.g., 'CMML', 'SF3B1', '10%')")

    # --- WHO 5th EDITION SECTION (NEW & COMPREHENSIVE) ---
    st.subheader("🧬 WHO 5th Edition: Myeloid & Histiocytic/Dendritic Neoplasms (Comprehensive)")
    st.markdown("*A non-summarized, exhaustive listing of diagnostic categories and entities.*")
    
    for category, entities in WHO5_DATA.items():
        # Search filter check for category
        if search_term and search_term.lower() not in category.lower():
            entity_match = False
            # Handles both dict and list values in WHO5_DATA
            for ename, edata in (entities.items() if isinstance(entities, dict) else {k: k for k in entities}.items()):
                if search_term.lower() in ename.lower() or str(edata).lower().find(search_term.lower()) != -1:
                    entity_match = True
                    break
            if not entity_match:
                continue

        with st.expander(category, expanded=True if search_term else False):
            # Handles both dict and list values in WHO5_DATA
            if isinstance(entities, dict):
                for entity_name, details in entities.items():
                    # Search filter check for entity
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
                    # Search filter check for list item
                    if search_term and search_term.lower() not in item.lower():
                        continue
                    st.markdown(f"- {item}")
                st.markdown("---")

    st.markdown("---")

    # --- ICC 2022 SECTION (UPDATED) ---
    st.subheader("🔬 ICC 2022 Reference Library (Myeloid/MDS/MPN/Plasma Cell)")
    st.markdown("*The revised, detailed International Consensus Classification criteria.*")

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