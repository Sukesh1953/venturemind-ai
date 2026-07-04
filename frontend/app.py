"""
VentureMind AI — Streamlit Frontend
AI-powered Startup Due Diligence Platform
"""

import time
import requests
import streamlit as st
# =============================================================================
# Configuration
# =============================================================================
API_URL = "http://127.0.0.1:8000/analyze"
APP_TITLE = "VentureMind AI"
APP_TAGLINE = "AI-Powered Startup Due Diligence Platform"
PROGRESS_STEPS = [
    "Reading Website...",
    "Researching Company...",
    "Business Analysis...",
    "Generating Report...",
]
NOT_AVAILABLE = "Not Available"
# =============================================================================
# Page Configuration
# =============================================================================
def configure_page() -> None:
    """Set Streamlit page config and session defaults."""
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    if "analysis_result" not in st.session_state:
        st.session_state.analysis_result = None
    if "analysis_error" not in st.session_state:
        st.session_state.analysis_error = None
    if "last_company" not in st.session_state:
        st.session_state.last_company = ""
    if "last_website" not in st.session_state:
        st.session_state.last_website = ""
# =============================================================================
# Custom CSS
# =============================================================================
def inject_custom_css() -> None:
    """Inject professional SaaS styling."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }
        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 2rem;
            max-width: 1200px;
        }
        .hero-container {
            background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 50%, #0ea5e9 100%);
            border-radius: 20px;
            padding: 3rem 2.5rem;
            margin-bottom: 2rem;
            color: #ffffff;
            box-shadow: 0 20px 60px rgba(14, 165, 233, 0.15);
        }
        .hero-title {
            font-size: 2.8rem;
            font-weight: 800;
            margin-bottom: 0.5rem;
            line-height: 1.2;
        }
        .hero-subtitle {
            font-size: 1.15rem;
            opacity: 0.9;
            margin-bottom: 0;
            font-weight: 400;
        }
        .input-card {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 16px;
            padding: 2rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 24px rgba(15, 23, 42, 0.06);
        }
        .metric-card {
            background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
            border: 1px solid #e2e8f0;
            border-radius: 14px;
            padding: 1.5rem 1.25rem;
            text-align: center;
            box-shadow: 0 2px 12px rgba(15, 23, 42, 0.04);
            min-height: 120px;
        }
        .metric-label {
            font-size: 0.8rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: #64748b;
            margin-bottom: 0.5rem;
        }
        .metric-value {
            font-size: 1.6rem;
            font-weight: 700;
            color: #0f172a;
            word-break: break-word;
        }
        .metric-value.score {
            color: #0ea5e9;
        }
        .metric-value.risk-low {
            color: #16a34a;
        }
        .metric-value.risk-medium {
            color: #d97706;
        }
        .metric-value.risk-high {
            color: #dc2626;
        }
        .progress-step {
            padding: 0.75rem 1rem;
            margin: 0.4rem 0;
            border-radius: 10px;
            background: #f1f5f9;
            color: #64748b;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        .progress-step.active {
            background: linear-gradient(90deg, #0ea5e9, #38bdf8);
            color: #ffffff;
            font-weight: 600;
            box-shadow: 0 4px 14px rgba(14, 165, 233, 0.3);
        }
        .progress-step.done {
            background: #ecfdf5;
            color: #16a34a;
            font-weight: 600;
        }
        .footer-container {
            margin-top: 3rem;
            padding: 1.5rem 0;
            border-top: 1px solid #e2e8f0;
            text-align: center;
            color: #94a3b8;
            font-size: 0.85rem;
        }
        .sidebar-section {
            margin-bottom: 1.5rem;
        }
        .sidebar-heading {
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            color: #64748b;
            margin-bottom: 0.5rem;
        }
        div[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
        }
        div[data-testid="stSidebar"] * {
            color: #e2e8f0 !important;
        }
        div[data-testid="stSidebar"] .sidebar-heading {
            color: #94a3b8 !important;
        }
        .stButton > button[kind="primary"] {
            background: linear-gradient(90deg, #0ea5e9, #2563eb);
            border: none;
            border-radius: 12px;
            padding: 0.85rem 2rem;
            font-weight: 700;
            font-size: 1.05rem;
            width: 100%;
            transition: all 0.2s ease;
        }
        .stButton > button[kind="primary"]:hover {
            box-shadow: 0 8px 24px rgba(14, 165, 233, 0.35);
            transform: translateY(-1px);
        }
        .tab-content {
            padding: 1.5rem 0;
        }
        @media (max-width: 768px) {
            .hero-title {
                font-size: 2rem;
            }
            .hero-container {
                padding: 2rem 1.5rem;
            }
            .metric-value {
                font-size: 1.3rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
# =============================================================================
# Sidebar
# =============================================================================
def render_sidebar() -> None:
    """Render modern sidebar with project information."""
    with st.sidebar:
        st.markdown(
            """
            <div style="text-align:center; padding: 1rem 0 1.5rem 0;">
                <div style="font-size:2.5rem;">🧠</div>
                <div style="font-size:1.4rem; font-weight:800; color:#ffffff;">
                    VentureMind AI
                </div>
                <div style="font-size:0.85rem; opacity:0.7; margin-top:0.25rem;">
                    Startup Due Diligence
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown('<div class="sidebar-heading">AI Workflow</div>', unsafe_allow_html=True)
        st.markdown(
            """
            1. **Read** company website
            2. **Research** market & competitors
            3. **Analyze** business model
            4. **Generate** investment report
            """
        )
        st.markdown("---")
        st.markdown('<div class="sidebar-heading">Tech Stack</div>', unsafe_allow_html=True)
        st.markdown(
            """
            - **Frontend:** Streamlit
            - **Backend:** FastAPI
            - **AI:** LLM Analysis
            - **Data:** Web Research
            """
        )
        st.markdown("---")
        st.markdown('<div class="sidebar-heading">About Project</div>', unsafe_allow_html=True)
        st.markdown(
            """
            VentureMind AI automates startup due diligence by
            analyzing websites, researching companies, and
            generating comprehensive investment reports —
            powered by artificial intelligence.
            """
        )
# =============================================================================
# Hero Section
# =============================================================================
def render_hero() -> None:
    """Render hero section at the top of the page."""
    st.markdown(
        f"""
        <div class="hero-container">
            <div class="hero-title">{APP_TITLE}</div>
            <div class="hero-subtitle">{APP_TAGLINE}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
# =============================================================================
# Input Form
# =============================================================================
def render_input_form() -> tuple[str, str, bool]:
    """Render company inputs and analyze button. Returns (company, website, clicked)."""
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    st.markdown("### Start Your Analysis")
    st.markdown(
        "Enter a company name and website URL to generate a full due diligence report."
    )
    col1, col2 = st.columns(2)
    with col1:
        company_name = st.text_input(
            "Company Name",
            value=st.session_state.last_company,
            placeholder="e.g. Acme Corp",
            key="company_name_input",
        )
    with col2:
        website_url = st.text_input(
            "Website URL",
            value=st.session_state.last_website,
            placeholder="e.g. https://acme.com",
            key="website_url_input",
        )
    st.markdown("</div>", unsafe_allow_html=True)
    analyze_clicked = st.button(
        "🔍  Analyze Company",
        type="primary",
        use_container_width=True,
    )
    return company_name.strip(), website_url.strip(), analyze_clicked
# =============================================================================
# Validation
# =============================================================================
def validate_inputs(company_name: str, website_url: str) -> str | None:
    """Validate user inputs. Returns error message or None if valid."""
    if not company_name:
        return "Please enter a company name."
    if not website_url:
        return "Please enter a website URL."
    if not website_url.startswith(("http://", "https://")):
        return "Website URL must start with http:// or https://"
    return None
# =============================================================================
# API Call
# =============================================================================
def call_analyze_api(company_name: str, website_url: str) -> dict | None:
    """
    Call the FastAPI /analyze endpoint.
    Returns response dict on success, None on failure.
    """
    payload = {
        "website_url": website_url,
        "company_name": company_name,
    }
    try:
        response = requests.post(API_URL, json=payload, timeout=300)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        st.session_state.analysis_error = (
            "Cannot connect to the backend. "
            "Make sure the FastAPI server is running at http://127.0.0.1:8000"
        )
        return None
    except requests.exceptions.Timeout:
        st.session_state.analysis_error = (
            "The analysis timed out. The company may require more time to process."
        )
        return None
    except requests.exceptions.HTTPError:
        detail = NOT_AVAILABLE
        try:
            detail = response.json().get("detail", str(response.status_code))
        except Exception:
            detail = f"HTTP {response.status_code}"
        st.session_state.analysis_error = f"Server error: {detail}"
        return None
    except requests.exceptions.RequestException as exc:
        st.session_state.analysis_error = f"Request failed: {exc}"
        return None
    except ValueError:
        st.session_state.analysis_error = "Invalid response from server (not valid JSON)."
        return None
# =============================================================================
# Progress Display
# =============================================================================
def show_progress_steps(current_index: int) -> None:
    """Display animated progress steps during analysis."""
    progress_html = ""
    for i, step in enumerate(PROGRESS_STEPS):
        if i < current_index:
            css_class = "done"
            icon = "✅ "
        elif i == current_index:
            css_class = "active"
            icon = "⏳ "
        else:
            css_class = ""
            icon = "○ "
        progress_html += f'<div class="progress-step {css_class}">{icon}{step}</div>'
    st.markdown(progress_html, unsafe_allow_html=True)
def run_analysis_with_progress(company_name: str, website_url: str) -> dict | None:
    """
    Run analysis with visual progress steps and spinner.
    Makes the API call during the final step.
    """
    progress_placeholder = st.empty()
    result = None
    with st.spinner("VentureMind AI is analyzing..."):
        for i in range(len(PROGRESS_STEPS)):
            with progress_placeholder.container():
                show_progress_steps(i)
            if i < len(PROGRESS_STEPS) - 1:
                time.sleep(0.8)
            else:
                result = call_analyze_api(company_name, website_url)
                with progress_placeholder.container():
                    show_progress_steps(len(PROGRESS_STEPS))
                time.sleep(0.3)
    return result
# =============================================================================
# Metric Extraction (gentle, non-aggressive)
# =============================================================================
def safe_extract_pattern(text: str, labels: list[str]) -> str | None:
    """
    Gently try to extract a value from text after known labels.
    Returns None if nothing reasonable is found.
    """
    if not text or not isinstance(text, str):
        return None
    lower_text = text.lower()
    for label in labels:
        idx = lower_text.find(label.lower())
        if idx == -1:
            continue
        snippet = text[idx + len(label): idx + len(label) + 80].strip(" :#-\n\t")
        if not snippet:
            continue
        value = snippet.split("\n")[0].split(".")[0].strip()
        if value and len(value) < 80:
            return value
    return None
import re

def extract_investment_score(text: str):

    if not text:
        return "Not Available"

    match = re.search(
        r"Overall Investment Score:\s*(\d+)\s*/\s*(10|100)",
        text,
        re.IGNORECASE,
    )

    if not match:
        return "Not Available"

    score = int(match.group(1))
    scale = int(match.group(2))

    if scale == 10:
        score *= 10

    return f"{score}/100"

def extract_risk_level(report_text: str) -> str:
    """Try to extract risk level; fallback to Not Available."""
    labels = [
        "risk level:",
        "risk level",
        "overall risk:",
        "overall risk",
        "risk rating:",
        "risk rating",
    ]
    value = safe_extract_pattern(report_text, labels)
    if value is not None:
        normalized = value.lower()
        for level in ("low", "medium", "high", "moderate", "critical"):
            if level in normalized:
                return level.title()
    return NOT_AVAILABLE
def extract_market(report_text: str, research_text: str) -> str:
    """Try to extract market info; fallback to Not Available."""
    combined = f"{report_text or ''}\n{research_text or ''}"
    labels = [
        "target market:",
        "target market",
        "market size:",
        "market size",
        "market segment:",
        "market segment",
        "market opportunity:",
        "market opportunity",
    ]
    value = safe_extract_pattern(combined, labels)
    if value is not None:
        return value.strip().rstrip(",")
    return NOT_AVAILABLE
def get_risk_css_class(risk_level: str) -> str:
    """Return CSS class for risk level coloring."""
    risk_lower = risk_level.lower()
    if "low" in risk_lower:
        return "risk-low"
    if "high" in risk_lower or "critical" in risk_lower:
        return "risk-high"
    if risk_lower != NOT_AVAILABLE.lower():
        return "risk-medium"
    return ""
# =============================================================================
# Dashboard Metrics
# =============================================================================
def render_dashboard(result: dict):
    """Render top dashboard with Risk Level and Market."""

    business_text = result.get("business_analysis", "") or ""
    research_text = result.get("research", "") or ""

    risk_level = extract_risk_level(business_text)
    market = extract_market(business_text, research_text)

    risk_class = get_risk_css_class(risk_level)

    st.markdown("### Analysis Dashboard")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Risk Level</div>
                <div class="metric-value {risk_class}">{risk_level}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Market</div>
                <div class="metric-value">{market}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
# =============================================================================
# Results Tabs
# =============================================================================
def render_results_tabs(result: dict) -> None:
    """Render tabbed results with markdown content."""
    research = result.get("research", "") or NOT_AVAILABLE
    business_analysis = result.get("business_analysis", "") or NOT_AVAILABLE
    report = result.get("report", "") or NOT_AVAILABLE
    tab_research, tab_analysis, tab_report = st.tabs(
        [
            "📄 Company Research",
            "📊 Business Analysis",
            "📋 Final Report",
        ]
    )
    with tab_research:
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        if research and research != NOT_AVAILABLE:
            st.markdown(research)
        else:
            st.info("Company research data is not available.")
        st.markdown("</div>", unsafe_allow_html=True)
    with tab_analysis:
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        if business_analysis and business_analysis != NOT_AVAILABLE:
            st.markdown(business_analysis)
        else:
            st.info("Business analysis data is not available.")
        st.markdown("</div>", unsafe_allow_html=True)
    with tab_report:
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        if report and report != NOT_AVAILABLE:
            st.markdown(report)
            st.markdown("---")
            render_download_button(report)
        else:
            st.info("Final report is not available.")
        st.markdown("</div>", unsafe_allow_html=True)
# =============================================================================
# Download Button
# =============================================================================
def sanitize_filename(name: str) -> str:
    """Create a safe filename from company name without regex."""
    safe_chars = []
    for ch in name:
        if ch.isalnum() or ch in ("-", "_"):
            safe_chars.append(ch)
        elif ch.isspace():
            safe_chars.append("_")
    return "".join(safe_chars).strip("_") or "company"
def render_download_button(report_text: str) -> None:
    """Render download button for the final report."""
    company = st.session_state.get("last_company", "company")
    safe_name = sanitize_filename(company)
    filename = f"venturemind_report_{safe_name}.md"
    st.download_button(
        label="📥  Download Report",
        data=report_text,
        file_name=filename,
        mime="text/markdown",
        use_container_width=True,
    )
# =============================================================================
# Results Display
# =============================================================================
def render_results(result: dict) -> None:
    """Render full results section with dashboard and tabs."""
    st.markdown("---")
    st.success(f"Analysis complete for **{st.session_state.last_company}**")
    render_dashboard(result)
    st.markdown("")
    render_results_tabs(result)
# =============================================================================
# Footer
# =============================================================================
def render_footer() -> None:
    """Render professional footer."""
    st.markdown(
        f"""
        <div class="footer-container">
            <strong>{APP_TITLE}</strong> &nbsp;|&nbsp;
            AI-Powered Startup Due Diligence &nbsp;|&nbsp;
            © 2026 VentureMind AI. All rights reserved.
        </div>
        """,
        unsafe_allow_html=True,
    )
# =============================================================================
# Main Application
# =============================================================================
def main() -> None:
    """Main application entry point."""
    configure_page()
    inject_custom_css()
    render_sidebar()
    render_hero()
    company_name, website_url, analyze_clicked = render_input_form()
    if analyze_clicked:
        st.session_state.analysis_error = None
        st.session_state.analysis_result = None
        validation_error = validate_inputs(company_name, website_url)
        if validation_error:
            st.error(validation_error)
        else:
            st.session_state.last_company = company_name
            st.session_state.last_website = website_url
            result = run_analysis_with_progress(company_name, website_url)
            if result is not None:
                st.session_state.analysis_result = result
                st.session_state.analysis_error = None
            elif st.session_state.analysis_error:
                st.error(st.session_state.analysis_error)
    if st.session_state.analysis_error and not analyze_clicked:
        st.error(st.session_state.analysis_error)
    if st.session_state.analysis_result:
        render_results(st.session_state.analysis_result)
    render_footer()
# =============================================================================
# Entry Point
# =============================================================================
if __name__ == "__main__":
    main()