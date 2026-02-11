import streamlit as st


def inject_global_styles() -> None:
    st.markdown(
        """
        <style>
        :root {
            --primary: #FF6B00;
            --primary-dark: #E65100;
            --bg: #0A0A0A;
            --card: #1A1A1A;
            --border: #2A2A2A;
            --text-secondary: #B0B0B0;
        }

        .hero {
            padding: 2rem 1rem 3rem 1rem;
            background: radial-gradient(ellipse at top, rgba(255, 107, 0, 0.15), transparent 60%);
            border-bottom: 1px solid var(--border);
        }

        .hero h1, .hero h2 {
            font-family: 'Playfair Display', serif;
            margin-bottom: 0.5rem;
        }

        .hero-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.35rem 0.75rem;
            border-radius: 999px;
            border: 1px solid rgba(255, 107, 0, 0.4);
            color: var(--primary);
            font-size: 0.85rem;
        }

        .section-title {
            font-family: 'Playfair Display', serif;
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }

        .card {
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 1.25rem;
        }

        .price {
            color: var(--primary);
            font-weight: 700;
        }

        .muted {
            color: var(--text-secondary);
        }
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
            st.button("Entrar", use_container_width=True)


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
