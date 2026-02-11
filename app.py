from datetime import date

import streamlit as st

from db import get_database_url, list_services
from ui import inject_global_styles, render_footer, render_header

SERVICES_FALLBACK = [
    {
        "name": "Corte de Cabelo",
        "tagline": "Corte profissional com estilo",
        "description": "Corte personalizado com os melhores profissionais da regiao.",
        "price": 50.00,
        "duration_minutes": 30,
    },
    {
        "name": "Barba & Bigode",
        "tagline": "Acabamento perfeito",
        "description": "Servico completo de barba com produtos premium.",
        "price": 35.00,
        "duration_minutes": 25,
    },
    {
        "name": "Coloracao",
        "tagline": "Cores vibrantes e duradouras",
        "description": "Coloracao profissional com tintas de qualidade.",
        "price": 80.00,
        "duration_minutes": 60,
    },
    {
        "name": "Tratamento Capilar",
        "tagline": "Hidratacao profunda",
        "description": "Tratamentos especificos para cada tipo de cabelo.",
        "price": 60.00,
        "duration_minutes": 45,
    },
    {
        "name": "Manicure & Pedicure",
        "tagline": "Unhas perfeitas",
        "description": "Cuidados completos com unhas e pele.",
        "price": 45.00,
        "duration_minutes": 40,
    },
    {
        "name": "Pacotes Especiais",
        "tagline": "Combos com desconto",
        "description": "Pacotes personalizados com precos especiais.",
        "price": 0.00,
        "duration_minutes": 0,
    },
]

st.set_page_config(
    page_title="Barber & Beauty",
    page_icon="✂️",
    layout="wide",
)

inject_global_styles()

render_header()

st.markdown(
    """
    <div class="hero">
        <div class="hero-badge">✨ Agendamento Online</div>
        <h1>Sua <span style="color:#FF6B00;">beleza</span> em primeiro lugar</h1>
        <p class="muted">
            Agende seus servicos de barbearia e beleza de forma rapida e facil. 
            Escolha o profissional, o horario e aproveite uma experiencia premium.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

if not get_database_url():
    st.warning(
        "DATABASE_URL nao configurada. Exibindo dados locais. Configure o Postgres no Railway para salvar agendamentos."
    )

services = list_services() or SERVICES_FALLBACK

st.markdown("## Nossos Servicos")
cols = st.columns(3)
for idx, service in enumerate(services):
    with cols[idx % 3]:
        price = service["price"]
        price_text = f"R$ {price:.2f}" if price > 0 else "Consulte"
        st.markdown(
            f"""
            <div class="card">
                <h3>{service['name']}</h3>
                <p class="muted">{service.get('tagline', '')}</p>
                <p class="muted">{service.get('description', '')}</p>
                <p class="price">{price_text}</p>
                <p class="muted">{service['duration_minutes']} min</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("## Por Que Nos Escolher?")
features = [
    ("Profissionais Experientes", "Equipe altamente qualificada"),
    ("Agendamento Facil", "Reserve em poucos cliques"),
    ("Qualidade Premium", "Produtos e servicos de primeira"),
    ("Flexibilidade", "Horarios convenientes"),
]
feature_cols = st.columns(4)
for idx, (title, subtitle) in enumerate(features):
    with feature_cols[idx]:
        st.markdown(
            f"""
            <div class="card">
                <h4>{title}</h4>
                <p class="muted">{subtitle}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("## Pronto para agendar?")
st.button("Entrar e Agendar", use_container_width=True)

render_footer()
