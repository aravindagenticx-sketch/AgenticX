import streamlit as st
from streamlit_quill import st_quill
from fpdf import FPDF
from bs4 import BeautifulSoup
from groq import Groq

# -- Page config
st.set_page_config(page_title="AgenticX Resume", layout="wide", page_icon="✦")

# -- Groq client (key loaded from .streamlit/secrets.toml)
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# -- Global styles
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=Instrument+Serif:ital@0;1&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, .stApp {
    background-color: #09090b !important;
    color: #e4e4e7 !important;
    font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stSidebar"] {
    background-color: #0f0f11 !important;
    border-right: 1px solid #1c1c1f !important;
    min-width: 380px !important;
    max-width: 380px !important;
    padding: 2rem 1.4rem !important;
}
[data-testid="stSidebar"] * { color: #a1a1aa !important; }
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { color: #e4e4e7 !important; }

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #27272a; border-radius: 99px; }

h1, h2, h3 { font-family: 'DM Sans', sans-serif !important; font-weight: 600; }

.stTextInput>div>div>input,
.stTextArea>div>div>textarea,
.stSelectbox>div>div {
    background-color: #111113 !important;
    border: 1px solid #27272a !important;
    border-radius: 8px !important;
    color: #e4e4e7 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.875rem !important;
}
.stTextInput>div>div>input::placeholder,
.stTextArea>div>div>textarea::placeholder {
    color: #3f3f46 !important;
    font-style: italic;
}
.stTextInput>div>div>input:focus,
.stTextArea>div>div>textarea:focus {
    border-color: #52525b !important;
    box-shadow: 0 0 0 2px rgba(161,161,170,0.08) !important;
    outline: none !important;
}

label, .stTextInput label, .stTextArea label, .stSelectbox label {
    color: #52525b !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.09em !important;
    text-transform: uppercase !important;
    font-weight: 500 !important;
}

.stTextInput > div > div > div[data-testid="InputInstructions"],
small.st-emotion-cache-zt5igj,
[data-testid="InputInstructions"] { display: none !important; }

.stButton>button {
    background: #18181b !important;
    color: #e4e4e7 !important;
    border: 1px solid #27272a !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    padding: 0.5rem 1.1rem !important;
    transition: all 0.18s ease !important;
    letter-spacing: 0.02em;
    width: 100%;
}
.stButton>button:hover {
    background: #27272a !important;
    border-color: #3f3f46 !important;
    color: #fff !important;
}

.ai-btn .stButton>button {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%) !important;
    border-color: #3b82f6 !important;
    color: #93c5fd !important;
    margin-top: 0.5rem;
}
.ai-btn .stButton>button:hover {
    background: linear-gradient(135deg, #1e3a5f 0%, #1a2f4a 100%) !important;
    color: #bfdbfe !important;
}

.dl-btn .stDownloadButton>button {
    background: linear-gradient(135deg, #052e16 0%, #064e3b 100%) !important;
    border-color: #16a34a !important;
    color: #86efac !important;
    width: 100% !important;
    padding: 0.75rem !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
}

hr { border-color: #1c1c1f !important; margin: 1.5rem 0 !important; }

.ai-output textarea {
    background-color: #0d1117 !important;
    border: 1px solid #1c1c1f !important;
    color: #86efac !important;
    font-size: 0.78rem !important;
    border-radius: 8px !important;
    line-height: 1.7 !important;
}

.section-label {
    font-family: 'Instrument Serif', serif;
    font-style: italic;
    font-size: 1.05rem;
    color: #71717a;
    margin-bottom: 0.4rem;
    letter-spacing: 0.01em;
}

.hero-wrap {
    display: flex;
    align-items: baseline;
    gap: 0.5rem;
    margin-bottom: 0.2rem;
    flex-wrap: wrap;
}
.hero-brand {
    font-family: 'Instrument Serif', serif;
    font-size: 3rem;
    letter-spacing: -0.03em;
    line-height: 1;
    background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 50%, #f472b6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-suffix {
    font-family: 'Instrument Serif', serif;
    font-size: 2.4rem;
    color: #3f3f46;
    letter-spacing: -0.02em;
    line-height: 1;
}
.hero-sub {
    font-size: 0.72rem;
    color: #27272a;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-bottom: 2rem;
    margin-top: 0.25rem;
}

.card {
    background: #0f0f11;
    border: 1px solid #1c1c1f;
    border-radius: 12px;
    padding: 1.25rem 1.4rem 1.4rem;
    margin-bottom: 1.25rem;
}

.ql-toolbar { background: #111113 !important; border-color: #27272a !important; border-radius: 8px 8px 0 0 !important; }
.ql-container { background: #0f0f11 !important; border-color: #27272a !important; border-radius: 0 0 8px 8px !important; min-height: 130px; }
.ql-editor { color: #d4d4d8 !important; font-size: 0.875rem !important; line-height: 1.7 !important; }
.ql-editor.ql-blank::before { color: #3f3f46 !important; font-style: italic !important; }
.ql-stroke { stroke: #71717a !important; }
.ql-fill   { fill:   #71717a !important; }
.ql-picker  { color:  #71717a !important; }

.stSpinner > div { border-top-color: #3b82f6 !important; }

#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# -- AI helper
def get_ai_suggestion(section_name: str, user_text: str) -> str:
    try:
        prompt = (
            f"You are an elite resume writer. Rewrite the following '{section_name}' content "
            f"into 5-8 tight, high-impact bullet points suitable for a professional resume. "
            f"Each bullet must start with a strong action verb (e.g. Built, Led, Designed, Reduced). "
            f"Use numbers or metrics wherever you can reasonably infer them. "
            f"Format each point on its own line starting with '• '. "
            f"Return ONLY the bullet points, nothing else, no intro, no commentary.\n\n"
            f"Raw content:\n{user_text}"
        )
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=700,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"


# -- PDF builder
def safe(text: str) -> str:
    return text.encode("latin-1", "ignore").decode("latin-1")


def render_bullet(pdf, text: str, font_style: str = "",
                  left_margin: float = 15, line_height: float = 5.2,
                  font_size: int = 9):
    BULLET        = safe("• ")
    TEXT_INDENT   = left_margin + 5
    PAGE_WIDTH    = 210
    RIGHT_MARGIN  = 15
    usable_width  = PAGE_WIDTH - RIGHT_MARGIN - TEXT_INDENT

    pdf.set_font("Helvetica", font_style, font_size)
    pdf.set_text_color(40, 40, 40)

    words  = safe(text).split()
    lines  = []
    cur    = ""
    for word in words:
        test = (cur + " " + word).strip()
        if pdf.get_string_width(test) <= usable_width:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)

    if not lines:
        return

    pdf.set_x(left_margin)
    pdf.cell(5, line_height, BULLET, ln=0)
    pdf.set_x(TEXT_INDENT)
    pdf.cell(usable_width, line_height, lines[0], ln=True)

    for line in lines[1:]:
        pdf.set_x(left_margin)
        pdf.cell(5, line_height, "", ln=0)
        pdf.set_x(TEXT_INDENT)
        pdf.cell(usable_width, line_height, line, ln=True)


def render_paragraph(pdf, text: str, font_style: str = "",
                     left_margin: float = 15, line_height: float = 5.2,
                     font_size: int = 9):
    PAGE_WIDTH   = 210
    RIGHT_MARGIN = 15
    usable_width = PAGE_WIDTH - RIGHT_MARGIN - left_margin

    pdf.set_font("Helvetica", font_style, font_size)
    pdf.set_text_color(40, 40, 40)
    pdf.set_x(left_margin)

    words = safe(text).split()
    lines, cur = [], ""
    for word in words:
        test = (cur + " " + word).strip()
        if pdf.get_string_width(test) <= usable_width:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)

    for line in lines:
        pdf.set_x(left_margin)
        pdf.cell(usable_width, line_height, line, ln=True)


def create_pdf(name, email, phone, linkedin, sk, wk, pr, ed):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_margins(15, 15, 15)
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.set_font("Helvetica", "B", 22)
    pdf.set_text_color(20, 20, 20)
    pdf.cell(0, 12, safe(name or ""), ln=True, align="C")

    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(100, 100, 100)
    parts = [x for x in [email, phone, linkedin] if x and x.strip()]
    if parts:
        pdf.cell(0, 5, safe("  ·  ".join(parts)), ln=True, align="C")
    pdf.set_text_color(0, 0, 0)

    pdf.ln(4)
    pdf.set_draw_color(200, 200, 200)
    pdf.line(15, pdf.get_y(), 195, pdf.get_y())
    pdf.ln(5)

    sections = [("SKILLS", sk), ("EXPERIENCE", wk), ("PROJECTS", pr), ("EDUCATION", ed)]
    for title, html in sections:
        if not html or len(html) < 15:
            continue

        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(20, 20, 20)
        pdf.set_x(15)
        pdf.cell(0, 6, title, ln=True)
        pdf.set_draw_color(180, 180, 180)
        pdf.line(15, pdf.get_y(), 195, pdf.get_y())
        pdf.ln(3)

        soup = BeautifulSoup(html, "html.parser")

        for tag in soup.find_all(["p", "li"]):
            text = tag.get_text().strip()
            if not text:
                continue
            is_bold = bool(tag.find(["strong", "b"]))
            style   = "B" if is_bold else ""

            if tag.name == "li":
                render_bullet(pdf, text, font_style=style)
            else:
                render_paragraph(pdf, text, font_style=style)

        pdf.ln(4)

    return pdf.output(dest="S")


# ══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
        <div style='margin-bottom:0.4rem'>
            <span style='font-size:1.1rem;color:#3b82f6'>✦</span>
            <strong style='color:#e4e4e7;font-size:1rem;letter-spacing:0.05em;margin-left:6px'>AI WRITER</strong>
        </div>
        <p style='font-size:0.78rem;color:#3f3f46;line-height:1.6;margin-bottom:1.2rem'>
            Describe what you did in plain language.<br>Get polished resume bullets instantly.
        </p>
    """, unsafe_allow_html=True)
    st.markdown("---")

    target = st.selectbox("Section to improve", ["Work Experience", "Projects", "Skills", "Education"])
    notes = st.text_area(
        "Your rough notes",
        placeholder="e.g. I built a sales dashboard in React. Fixed slow loading. Manager was happy. Used Python for the backend APIs.",
        height=200,
        key="notes_input"
    )

    st.markdown('<div class="ai-btn">', unsafe_allow_html=True)
    generate_clicked = st.button("✦ Generate bullet points", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    if generate_clicked:
        if notes and notes.strip():
            with st.spinner("Writing…"):
                result = get_ai_suggestion(target, notes)
                st.session_state["ai_result"] = result
                st.session_state["ai_target"] = target
        else:
            st.warning("Add some notes first.")

    if "ai_result" in st.session_state:
        st.markdown(f"""
            <p style='font-size:0.68rem;color:#3b82f6;margin-top:1.2rem;
                      letter-spacing:0.12em;text-transform:uppercase'>
                down bullets for {st.session_state.get('ai_target','your section')}
            </p>
        """, unsafe_allow_html=True)

        st.markdown('<div class="ai-output">', unsafe_allow_html=True)
        st.text_area(
            "Copy these",
            value=st.session_state["ai_result"],
            height=300,
            key="ai_output_box",
            label_visibility="collapsed"
        )
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
            <p style='font-size:0.68rem;color:#27272a;margin-top:0.4rem;line-height:1.5'>
                Select all, copy, paste into the editor on the right.
            </p>
        """, unsafe_allow_html=True)

        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Redo", use_container_width=True):
                if notes and notes.strip():
                    with st.spinner("Rewriting…"):
                        st.session_state["ai_result"] = get_ai_suggestion(target, notes)
                        st.rerun()
        with col_b:
            if st.button("Clear", use_container_width=True):
                del st.session_state["ai_result"]
                st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN LAYOUT
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
    <div class='hero-wrap'>
        <span class='hero-brand'>Agenticx</span>
        <span class='hero-suffix'>Resume Builder</span>
    </div>
    <div class='hero-sub'>ai-powered · free · professional</div>
""", unsafe_allow_html=True)

TBAR = [["bold"], [{"list": "bullet"}]]

# -- Contact info
st.markdown("<div class='card'>", unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)
with c1:
    name_v = st.text_input("Full name", value="", placeholder="Jane Smith")
with c2:
    email_v = st.text_input("Email", value="", placeholder="jane@email.com")
with c3:
    phone_v = st.text_input("Phone", value="", placeholder="+91 98765 43210")
with c4:
    link_v = st.text_input("LinkedIn", value="", placeholder="linkedin.com/in/jane")
st.markdown("</div>", unsafe_allow_html=True)

# -- Two-column editors
col_l, col_r = st.columns([1, 1], gap="large")

with col_l:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<p class='section-label'>Skills</p>", unsafe_allow_html=True)
    sk_h = st_quill(toolbar=TBAR, key="sk_editor", html=True,
                    placeholder="e.g. Python, React, SQL, Figma, Docker…")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<p class='section-label'>Education</p>", unsafe_allow_html=True)
    ed_h = st_quill(toolbar=TBAR, key="ed_editor", html=True,
                    placeholder="e.g. B.Tech Computer Science · VIT · 2020-2024")
    st.markdown("</div>", unsafe_allow_html=True)

with col_r:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<p class='section-label'>Work Experience</p>", unsafe_allow_html=True)
    wk_h = st_quill(toolbar=TBAR, key="wk_editor", html=True,
                    placeholder="Paste AI bullet points here, or type directly…")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<p class='section-label'>Projects</p>", unsafe_allow_html=True)
    pr_h = st_quill(toolbar=TBAR, key="pr_editor", html=True,
                    placeholder="Paste AI bullet points here, or type directly…")
    st.markdown("</div>", unsafe_allow_html=True)

# -- Download
st.markdown("---")
_, mid, _ = st.columns([2, 1, 2])
with mid:
    if st.button("Build & Download PDF", use_container_width=True):
        try:
            raw = create_pdf(name_v, email_v, phone_v, link_v, sk_h, wk_h, pr_h, ed_h)
            pdf_bytes = bytes(raw) if not isinstance(raw, str) else raw.encode("latin-1")
            filename = f"{(name_v or 'Resume').replace(' ', '_')}_Resume.pdf"
            st.markdown('<div class="dl-btn">', unsafe_allow_html=True)
            st.download_button(
                "Save PDF",
                data=pdf_bytes,
                file_name=filename,
                mime="application/pdf",
                use_container_width=True,
            )
            st.markdown("</div>", unsafe_allow_html=True)
        except Exception as ex:
            st.error(f"PDF error: {ex}")
