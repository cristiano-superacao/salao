import streamlit as st


def inject_global_styles() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Inter:wght@300;400;500;600;700&display=swap');

        :root {
            --primary: #FF6B00;
            --primary-hover: #FF7F1F;
            --primary-dark: #E65100;
            --bg: #0A0A0A;
            --card: #1A1A1A;
            --card-hover: #222222;
            --border: #2A2A2A;
            --text: #FFFFFF;
            --text-secondary: #B0B0B0;
            --text-muted: #707070;
            --shadow: rgba(0, 0, 0, 0.5);
            --radius-sm: 0.5rem;
            --radius-md: 0.75rem;
            --radius-lg: 1rem;
            --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }

        html, body {
            background: var(--bg) !important;
        }

        .stApp {
            background: var(--bg);
            color: var(--text);
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        }

        /* Hide Streamlit chrome for a more website-like layout */
        #MainMenu { visibility: hidden; }
        header[data-testid="stHeader"] { display: none; }
        div[data-testid="stToolbar"] { visibility: hidden; height: 0; }
        footer { visibility: hidden; }

        /* Layout container */
        .block-container {
            max-width: 1280px;
            padding-top: 1.25rem;
            padding-bottom: 3rem;
        }

        @media (max-width: 640px) {
            .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
            }
        }

        /* Text helpers */
        .muted { color: var(--text-secondary); }
        .highlight { color: var(--primary); }

        /* Hero */
        .hero {
            padding: 2.25rem 0 2.75rem;
            background: radial-gradient(ellipse at top, rgba(255, 107, 0, 0.15), transparent 60%);
            border-bottom: 1px solid var(--border);
        }

        .hero-grid {
            display: grid;
            grid-template-columns: 1.15fr 0.85fr;
            gap: 2rem;
            align-items: center;
        }

        @media (max-width: 900px) {
            .hero-grid {
                grid-template-columns: 1fr;
            }
        }

        .hero-title {
            font-family: 'Playfair Display', serif;
            font-size: clamp(2.25rem, 6vw, 4rem);
            line-height: 1.1;
            margin: 0.25rem 0 0.75rem;
        }

        .hero-description {
            color: var(--text-secondary);
            font-size: 1.05rem;
            max-width: 38rem;
            margin-bottom: 1.25rem;
        }

        .hero-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem 1rem;
            background: rgba(255, 107, 0, 0.10);
            border: 1px solid rgba(255, 107, 0, 0.30);
            border-radius: 2rem;
            color: var(--primary);
            font-size: 0.875rem;
            font-weight: 500;
        }

        .hero-buttons {
            display: flex;
            gap: 0.75rem;
            flex-wrap: wrap;
            margin: 1.25rem 0 1.5rem;
        }

        .stats {
            display: flex;
            gap: 1.5rem;
            flex-wrap: wrap;
        }

        .stat-number {
            font-size: 1.75rem;
            font-weight: 700;
            color: var(--primary);
            margin-bottom: 0.15rem;
        }

        .stat-label {
            color: var(--text-secondary);
            font-size: 0.875rem;
        }

        .image-placeholder {
            background: linear-gradient(180deg, rgba(255, 107, 0, 0.08), rgba(255, 107, 0, 0.02));
            border: 1px solid rgba(255, 107, 0, 0.25);
            border-radius: 1.25rem;
            min-height: 260px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--text-secondary);
            text-align: center;
            padding: 2rem;
        }

        /* Section */
        .section-header { text-align: center; margin: 2.25rem 0 1.5rem; }
        .section-title {
            font-family: 'Playfair Display', serif;
            font-size: clamp(1.75rem, 4vw, 3rem);
            margin-bottom: 0.5rem;
        }
        .section-subtitle {
            color: var(--text-secondary);
            font-size: 1.05rem;
            max-width: 42rem;
            margin: 0 auto;
        }

        /* Cards */
        .card {
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 1rem;
            padding: 1.25rem;
            transition: var(--transition);
        }

        .card:hover {
            border-color: var(--primary);
            transform: translateY(-4px);
            box-shadow: 0 20px 40px var(--shadow);
        }

        .price { color: var(--primary); font-weight: 700; }

        /* Streamlit widgets */
        .stSelectbox > div, .stDateInput > div, .stTextInput > div {
            border-radius: var(--radius-md);
        }

        /* Buttons: use `type="primary"` for CTAs and `type="secondary"` for slots */
        .stButton > button[kind="primary"], .stFormSubmitButton > button[kind="primary"] {
            background: linear-gradient(135deg, var(--primary), var(--primary-dark)) !important;
            color: var(--text) !important;
            border: none !important;
            border-radius: var(--radius-md) !important;
            font-weight: 600 !important;
            transition: var(--transition) !important;
        }

        .stButton > button[kind="primary"]:hover, .stFormSubmitButton > button[kind="primary"]:hover {
            background: linear-gradient(135deg, var(--primary-hover), var(--primary)) !important;
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(255, 107, 0, 0.30);
        }

        .stButton > button[kind="secondary"], .stFormSubmitButton > button[kind="secondary"] {
            background: transparent !important;
            color: var(--text) !important;
            border: 2px solid var(--border) !important;
            border-radius: var(--radius-md) !important;
            font-weight: 600 !important;
            transition: var(--transition) !important;
        }

        .stButton > button[kind="secondary"]:hover, .stFormSubmitButton > button[kind="secondary"]:hover {
            border-color: var(--primary) !important;
            background: rgba(255, 107, 0, 0.10) !important;
        }

        /* Footer */
        hr { border-color: var(--border); }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header() -> None:
    with st.container():
        cols = st.columns([1, 1])
        with cols[0]:
            st.markdown("## Barber & Beauty")
        with cols[1]:
            st.write("")
            st.button("Entrar", type="primary", use_container_width=True)


def render_footer() -> None:
    st.markdown(
        """
        <hr />
        <div class="muted" style="display:flex; justify-content:space-between;">
            <span>© 2026 Barber & Beauty. Todos os direitos reservados.</span>
            <span>Instagram · Facebook · WhatsApp</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
