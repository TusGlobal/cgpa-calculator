import streamlit as st
import math

# ──────────────────────────────────────────────────────────────────────────────
# Page config
# ──────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CGPA to Percentage | TUS International Admissions",
    page_icon="https://upload.wikimedia.org/wikipedia/en/b/bc/TUS_Midlands_Midwest_Logo.svg",
    layout="centered",
)

# ──────────────────────────────────────────────────────────────────────────────
# Custom CSS — TUS brand colours: navy #002147, teal #009EB3
# ──────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    html, body, [class*="css"] { font-family: 'Segoe UI', sans-serif; }

    .tus-header {
        background: #002147;
        padding: 18px 28px 14px 28px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        gap: 20px;
        margin-bottom: 24px;
    }
    .tus-header img { height: 56px; }
    .tus-header-text h1 {
        color: #ffffff;
        font-size: 1.35rem;
        margin: 0;
        font-weight: 700;
        letter-spacing: 0.3px;
    }
    .tus-header-text p {
        color: #a8c4d4;
        font-size: 0.82rem;
        margin: 2px 0 0 0;
    }

    .teal-rule { border: none; border-top: 3px solid #009EB3; margin: 0 0 22px 0; }

    .ugc-notice {
        background: #f0f8ff;
        border-left: 5px solid #009EB3;
        padding: 14px 18px;
        border-radius: 4px;
        font-size: 0.88rem;
        color: #002147;
        margin-bottom: 20px;
    }

    .result-card {
        background: #002147;
        color: white;
        padding: 20px 24px;
        border-radius: 8px;
        margin-top: 18px;
    }
    .result-card .pct { font-size: 2.4rem; font-weight: 800; color: #009EB3; }
    .result-card .formula { font-size: 0.82rem; color: #a8c4d4; margin-top: 4px; }

    .schol-card {
        padding: 14px 18px;
        border-radius: 8px;
        margin-top: 14px;
        font-weight: 600;
        font-size: 0.95rem;
    }
    .schol-none  { background:#fdecea; color:#b71c1c; border-left:5px solid #ef5350; }
    .schol-1000  { background:#fff3e0; color:#e65100; border-left:5px solid #ffa726; }
    .schol-2000  { background:#fff8e1; color:#f57f17; border-left:5px solid #ffca28; }
    .schol-3000  { background:#e8f5e9; color:#1b5e20; border-left:5px solid #66bb6a; }
    .schol-4000  { background:#e3f2fd; color:#0d47a1; border-left:5px solid #42a5f5; }

    .source-pill {
        display: inline-block;
        background: #eaf4f7;
        color: #007a99;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.78rem;
        text-decoration: none;
        margin-top: 10px;
    }

    .tus-footer {
        margin-top: 40px;
        padding-top: 14px;
        border-top: 1px solid #dde;
        font-size: 0.78rem;
        color: #666;
        text-align: center;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# Header
# ──────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="tus-header">
    <img src="https://upload.wikimedia.org/wikipedia/en/b/bc/TUS_Midlands_Midwest_Logo.svg"
         alt="TUS Logo" onerror="this.style.display='none'">
    <div class="tus-header-text">
        <h1>CGPA to Percentage Calculator</h1>
        <p>Technological University of the Shannon &nbsp;|&nbsp; International Admissions &amp; Scholarships</p>
    </div>
</div>
<hr class="teal-rule">
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# UGC Policy Note
# ──────────────────────────────────────────────────────────────────────────────
with st.expander("UGC Policy Note — Why formulas differ across Indian universities", expanded=False):
    st.markdown("""
**Background**

In 2015 the University Grants Commission (UGC) of India introduced the **Choice Based Credit System
(CBCS)**, standardising a 10-point grading scale across all Higher Education Institutions (HEIs).
Under CBCS, letter grades map to grade points as: O = 10, A+ = 9, A = 8, B+ = 7, B = 6, C = 5,
P = 4, F = 0.

**On percentage conversion**, the UGC CBCS guidelines note an indicative equivalence suggesting
**CGPA × 9.5** for institutions on the 10-point CBCS scale. This formula is mandated for centrally
affiliated universities (JNU, BHU, AMU, HCU, EFLU) per the 2012 UGC circular, and is followed by
IITs, NITs, and most Delhi-University affiliated colleges.

However, **the UGC has not issued a single nationally binding formula**. Universities that adopted
CBCS partially, or that follow AICTE engineering norms, or that pre-date CBCS, use their own
officially notified formulas.

**Fallback for unlisted universities:** Where no university-specific formula exists, the
**(CGPA − 0.5) × 10** formula is applied. This corresponds to the lower bound of each grade
interval on the UGC 10-point scale, and is the approach most commonly cited in government
recruitment notifications that state *"CGPA will be converted as per the formula given by the
respective university"*.

**Key sources**
- [UGC — Guidelines on Adoption of CBCS (2015)](https://www.ugc.gov.in/pdfnews/5713988_UGC-CBCS.pdf)
- UGC Circular (2012) — 9.5× multiplier for centrally affiliated universities
- AICTE norms for Engineering & Technology programmes

> For TUS scholarship assessment, the formula specific to each university is used where documented.
> For any Indian university not listed, the fallback **(CGPA − 0.5) × 10** is applied.
""")

# ──────────────────────────────────────────────────────────────────────────────
# Scholarship Bands
# ──────────────────────────────────────────────────────────────────────────────
with st.expander("TUS Scholarship Bands", expanded=False):
    st.markdown("""
| Percentage Range | Scholarship Award |
|---|---|
| Below 60% | Not eligible |
| 60% – 64.99% | €1,000 |
| 65% – 69.99% | €2,000 |
| 70% – 79.99% | €3,000 |
| 80% and above | €4,000 *(if programme fee ≥ €16,500)* |

*Awards are indicative. Final eligibility is subject to TUS Admissions Office confirmation.*
""")

st.markdown("---")

# ──────────────────────────────────────────────────────────────────────────────
# University data
# ──────────────────────────────────────────────────────────────────────────────
def f_deduct75(c): return (c - 0.75) * 10
def f_times10(c):  return c * 10
def f_deduct05(c): return (c - 0.5) * 10

UNIVERSITIES = {
    "— Select your university —": None,
    "Savitribai Pule Pune University  (Engineering / Architecture / Pharmacy)": {
        "formula_label": "(CGPA − 0.75) × 10",
        "fn": f_deduct75,
        "source_url": "https://drive.google.com/file/d/1GRwdUiPDCJSWLcWd2j1vx3HlxfElVHbP/view",
        "source_label": "Evaluation Criterions for CBCS — SPPU (01-07-2022)",
        "note": "Applicable for Engineering, Architecture and Pharmacy courses under AICTE/CBCS. "
                "For Humanities, Science and Commerce programmes under SPPU, grade-specific formulas apply — "
                "please contact your examination section.",
        "special": None,
    },
    "Visvesvaraya Technological University (VTU), Belgavi": {
        "formula_label": "(CGPA − 0.75) × 10",
        "fn": f_deduct75,
        "source_url": "https://vtu.ac.in/en/cgpa-standard-formula/",
        "source_label": "VTU — CGPA Standard Formula (Official Page)",
        "note": "Standard formula for 2015, 2017 and 2018 scheme students.",
        "special": None,
    },
    "Anna University": {
        "formula_label": "CGPA × 10",
        "fn": f_times10,
        "source_url": "https://www.annauniv.edu/",
        "source_label": "Anna University — ACOE Letter No.001/ACOE(UDs)/2021 (15-07-2021)",
        "note": "Applicable to all UG and PG programmes under Regulations R-2015, R-2018 and R-2019.",
        "special": None,
    },
    "Jawaharlal Nehru Technological University (JNTU)": {
        "formula_label": "(CGPA − 0.5) × 10  [UGC fallback]",
        "fn": f_deduct05,
        "source_url": "https://jntuh.ac.in/",
        "source_label": "JNTUH — R16 B.Tech Academic Regulations",
        "note": "JNTUH has issued multiple notifications with different formulas over the years, "
                "creating significant confusion. The UGC general fallback (CGPA − 0.5) × 10 is "
                "applied here for consistency. Students should attach their university's official "
                "conversion certificate when applying.",
        "special": None,
    },
    "Mahatma Gandhi University": {
        "formula_label": "CGPA × 10",
        "fn": f_times10,
        "source_url": "https://www.mgu.ac.in/",
        "source_label": "Mahatma Gandhi University — Official Regulations",
        "note": None,
        "special": None,
    },
    "Rashtrasant Tukadoji Maharaj Nagpur University": {
        "formula_label": "(CGPA − 0.75) × 10",
        "fn": f_deduct75,
        "source_url": "https://www.nagpuruniversity.ac.in/",
        "source_label": "RTMNU — Official Conversion Guidelines",
        "note": None,
        "special": None,
    },
    "Dr. APJ Abdul Kalam Technical University (AKTU), Lucknow": {
        "formula_label": "CGPA × 10",
        "fn": f_times10,
        "source_url": "https://aktu.ac.in/",
        "source_label": "AKTU — Academic Regulations",
        "note": None,
        "special": None,
    },
    "APJ Abdul Kalam Technological University (KTU), Kerala": {
        "formula_label": "CGPA × 10",
        "fn": f_times10,
        "source_url": "https://ktu.edu.in/",
        "source_label": "KTU — Notification 1584-2023 R.6.21",
        "note": None,
        "special": None,
    },
    "University of Mumbai": {
        "formula_label": "Special — select CGPI or CGPA",
        "fn": None,
        "source_url": "https://mu.ac.in/",
        "source_label": "Mumbai University — CGPI/CGPA to Percentage (Official Formula)",
        "note": None,
        "special": "mumbai",
    },
    "Rajiv Gandhi Proudyogiki Vishwavidyalaya (RGPV)": {
        "formula_label": "CPA × 10",
        "fn": f_times10,
        "source_url": "https://www.rgpv.ac.in/",
        "source_label": "RGPV — Ord. 32 Dual Degree Master of Applied Management",
        "note": None,
        "special": None,
    },
    "University of Calicut": {
        "formula_label": "CGPA × 10",
        "fn": f_times10,
        "source_url": "https://uoc.ac.in/",
        "source_label": "University of Calicut — Academic Regulations (2024)",
        "note": None,
        "special": None,
    },
    "Other Indian University  (UGC general fallback)": {
        "formula_label": "(CGPA − 0.5) × 10",
        "fn": f_deduct05,
        "source_url": "https://www.ugc.gov.in/pdfnews/5713988_UGC-CBCS.pdf",
        "source_label": "UGC — Guidelines on Adoption of CBCS (2015)",
        "note": "Your university is not listed. As per UGC guidelines, where no specific formula "
                "has been notified, the conversion (CGPA − 0.5) × 10 is applied. This corresponds "
                "to the lower bound of each grade interval on the UGC 10-point scale.",
        "special": None,
    },
}

# ──────────────────────────────────────────────────────────────────────────────
# Scholarship helper
# ──────────────────────────────────────────────────────────────────────────────
def scholarship_band(pct, prog_fee=None):
    if pct < 60:
        return "schol-none", "Not eligible for a merit scholarship (below 60%)"
    elif pct < 65:
        return "schol-1000", "Eligible for €1,000 scholarship  (60% – 64.99%)"
    elif pct < 70:
        return "schol-2000", "Eligible for €2,000 scholarship  (65% – 69.99%)"
    elif pct < 80:
        return "schol-3000", "Eligible for €3,000 scholarship  (70% – 79.99%)"
    else:
        if prog_fee and prog_fee >= 16500:
            return "schol-4000", "Eligible for €4,000 scholarship  (80%+, programme fee ≥ €16,500)"
        return "schol-3000", "Eligible for €3,000 scholarship  (80%+, but programme fee not confirmed ≥ €16,500 — verify for €4,000 band)"

def render_result(pct, formula_str, prog_fee):
    css, msg = scholarship_band(pct, prog_fee)
    st.markdown(f"""
<div class="result-card">
  <div class="pct">{pct:.2f}%</div>
  <div class="formula">{formula_str}</div>
</div>
<div class="schol-card {css}">{msg}</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# University selector
# ──────────────────────────────────────────────────────────────────────────────
university = st.selectbox("Select University", list(UNIVERSITIES.keys()))

if university == "— Select your university —":
    st.info("Select your Indian university from the dropdown above to begin.")
    st.stop()

info = UNIVERSITIES[university]

if info.get("note"):
    st.markdown(f'<div class="ugc-notice">{info["note"]}</div>', unsafe_allow_html=True)

with st.expander("Optional: Enter programme fee for accurate scholarship band"):
    prog_fee = st.number_input(
        "Annual programme fee (€)", min_value=0, max_value=50000, value=0, step=500,
        help="Only relevant for the €4,000 band which requires fee ≥ €16,500."
    )
    prog_fee = prog_fee if prog_fee > 0 else None

st.markdown("---")

# ──────────────────────────────────────────────────────────────────────────────
# Mumbai University special handling
# ──────────────────────────────────────────────────────────────────────────────
if info["special"] == "mumbai":
    st.markdown("**University of Mumbai**")
    score_type = st.radio(
        "Which score is on your transcript?",
        [
            "CGPI  (Engineering — Faculty of Technology, 10-point scale)",
            "CGPA  (Arts / Science / Commerce — CBCS, 10-point scale)",
        ],
    )

    if "CGPI" in score_type:
        st.markdown(
            "**Formulas (Engineering Faculty — CGPI):**  \n"
            "- CGPI < 7 → `Percentage = 7.1 × CGPI + 12` *(rounded up)*  \n"
            "- CGPI ≥ 7 → `Percentage = 7.4 × CGPI + 12` *(rounded up)*"
        )
        score = st.number_input("Enter CGPI", min_value=0.0, max_value=10.0, step=0.01, format="%.2f")
        if st.button("Calculate Percentage"):
            if score < 7:
                raw = 7.1 * score + 12
                formula_str = f"7.1 × {score} + 12 = {raw:.4f} → rounded up"
            else:
                raw = 7.4 * score + 12
                formula_str = f"7.4 × {score} + 12 = {raw:.4f} → rounded up"
            pct = float(math.ceil(raw))
            render_result(pct, formula_str, prog_fee)
    else:
        st.markdown("**Formula (Arts / Science / Commerce CBCS):** `Percentage = 7.1 × CGPA + 11`")
        score = st.number_input("Enter CGPA", min_value=0.0, max_value=10.0, step=0.01, format="%.2f")
        if st.button("Calculate Percentage"):
            pct = 7.1 * score + 11
            render_result(pct, f"7.1 × {score} + 11 = {pct:.2f}%", prog_fee)

# ──────────────────────────────────────────────────────────────────────────────
# All other universities
# ──────────────────────────────────────────────────────────────────────────────
else:
    st.markdown(f"**Formula:** `{info['formula_label']}`")
    score = st.number_input("Enter CGPA", min_value=0.0, max_value=10.0, step=0.01, format="%.2f")
    if st.button("Calculate Percentage"):
        pct = info["fn"](score)
        formula_str = f"{info['formula_label']} where CGPA = {score} → {pct:.2f}%"
        render_result(pct, formula_str, prog_fee)

# Source link
st.markdown(
    f'<a class="source-pill" href="{info["source_url"]}" target="_blank">'
    f'Source: {info["source_label"]}</a>',
    unsafe_allow_html=True,
)

# ──────────────────────────────────────────────────────────────────────────────
# Footer
# ──────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="tus-footer">
    Technological University of the Shannon &nbsp;|&nbsp; International Admissions Office<br>
    Formulas sourced from official university documents and UGC CBCS guidelines (2015).<br>
    This tool is for indicative purposes only. Always verify with the student's official transcript
    and their university's examination office before making a final scholarship decision.
</div>
""", unsafe_allow_html=True)
