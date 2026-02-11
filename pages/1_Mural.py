from datetime import date

import streamlit as st

from db import (
    create_appointment,
    get_database_url,
    list_availability,
    list_professional_services,
    list_professionals,
    list_services,
)
from ui import inject_global_styles, render_footer, render_header

st.set_page_config(
    page_title="Mural - Barber & Beauty",
    page_icon="✂️",
    layout="wide",
)

inject_global_styles()
render_header()

st.markdown("# Mural de Profissionais")

if not get_database_url():
    st.warning("DATABASE_URL nao configurada. Configure o Postgres para salvar agendamentos.")

services = list_services()
professionals = list_professionals()
relations = list_professional_services()

if not services or not professionals:
    st.info("Execute o seed para popular os dados: `python seed.py`.")

service_options = {"Todos": None}
for service in services:
    service_options[service["name"]] = service["id"]

selected_service_name = st.selectbox("Servico", options=list(service_options.keys()))
selected_service_id = service_options[selected_service_name]

selected_date = st.date_input("Data", value=date.today(), min_value=date.today())

time_filter = st.selectbox(
    "Horario",
    options=["Todos", "Manha (8h - 12h)", "Tarde (12h - 18h)", "Noite (18h - 22h)"],
)

availability = list_availability(selected_date)
availability_by_prof = {}
for row in availability:
    availability_by_prof.setdefault(row["professional_id"], []).append(row)

service_lookup = {service["id"]: service["name"] for service in services}
prof_services = {}
for rel in relations:
    prof_services.setdefault(rel["professional_id"], []).append(rel["service_id"])

st.markdown("---")

if not professionals:
    st.stop()

for prof in professionals:
    service_ids = prof_services.get(prof["id"], [])
    if selected_service_id and selected_service_id not in service_ids:
        continue

    st.markdown(f"## {prof['name']}")
    st.caption(f"{prof['role']} · {prof['rating']} estrelas · {prof['reviews']} avaliacoes")
    specialties = ", ".join(service_lookup.get(sid, "") for sid in service_ids)
    st.markdown(f"**Especialidades:** {specialties}")

    slots = availability_by_prof.get(prof["id"], [])
    slots = [slot for slot in slots if slot["is_available"]]

    if time_filter != "Todos":
        filtered_slots = []
        for slot in slots:
            hour = slot["time"].hour
            if time_filter.startswith("Manha") and 8 <= hour < 12:
                filtered_slots.append(slot)
            elif time_filter.startswith("Tarde") and 12 <= hour < 18:
                filtered_slots.append(slot)
            elif time_filter.startswith("Noite") and 18 <= hour < 22:
                filtered_slots.append(slot)
        slots = filtered_slots

    if not slots:
        st.info("Sem horarios disponiveis.")
        st.markdown("---")
        continue

    cols = st.columns(min(4, len(slots)))
    selected_slot = None
    for idx, slot in enumerate(slots):
        with cols[idx % len(cols)]:
            if st.button(slot["time"].strftime("%H:%M"), key=f"slot-{prof['id']}-{idx}"):
                selected_slot = slot

    if selected_slot:
        with st.form(key=f"booking-{prof['id']}"):
            st.subheader("Dados do cliente")
            customer_name = st.text_input("Nome completo")
            customer_email = st.text_input("Email")
            customer_phone = st.text_input("Telefone")

            service_names = [service_lookup[sid] for sid in service_ids]
            service_choice = st.selectbox("Servico", options=service_names)
            service_id = next(
                (sid for sid in service_ids if service_lookup[sid] == service_choice),
                service_ids[0] if service_ids else None,
            )

            submitted = st.form_submit_button("Confirmar agendamento")

            if submitted:
                if not customer_name:
                    st.error("Informe o nome do cliente.")
                elif service_id is None:
                    st.error("Selecione um servico.")
                else:
                    success = create_appointment(
                        professional_id=prof["id"],
                        service_id=service_id,
                        date_value=selected_date,
                        time_value=selected_slot["time"],
                        customer_name=customer_name,
                        customer_email=customer_email,
                        customer_phone=customer_phone,
                    )
                    if success:
                        st.success("Agendamento confirmado e salvo na nuvem.")
                    else:
                        st.error("Falha ao salvar. Verifique o DATABASE_URL.")

    st.markdown("---")

render_footer()
