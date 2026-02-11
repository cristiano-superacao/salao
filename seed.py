from datetime import date, datetime, time, timedelta

from db import (
    availabilities,
    get_engine,
    init_db,
    is_seeded,
    professional_services,
    professionals,
    services,
)

SERVICE_DATA = [
    {
        "name": "Corte de Cabelo",
        "tagline": "Corte profissional com estilo",
        "description": "Corte personalizado com os melhores profissionais da região.",
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

PROFESSIONAL_DATA = [
    {"name": "Carlos Silva", "role": "Barbeiro Master", "rating": 5.0, "reviews": 127},
    {"name": "Ana Rodrigues", "role": "Cabeleireira Expert", "rating": 5.0, "reviews": 189},
    {"name": "Roberto Martins", "role": "Barbeiro Profissional", "rating": 5.0, "reviews": 94},
    {"name": "Juliana Costa", "role": "Manicure & Pedicure", "rating": 5.0, "reviews": 156},
    {"name": "Pedro Santos", "role": "Colorista Expert", "rating": 5.0, "reviews": 112},
    {"name": "Mariana Lima", "role": "Tratamentos Capilares", "rating": 5.0, "reviews": 143},
]

PROFESSIONAL_SERVICE_MAP = {
    "Carlos Silva": ["Corte de Cabelo", "Barba & Bigode", "Coloracao"],
    "Ana Rodrigues": ["Corte de Cabelo", "Coloracao", "Tratamento Capilar"],
    "Roberto Martins": ["Corte de Cabelo", "Barba & Bigode"],
    "Juliana Costa": ["Manicure & Pedicure"],
    "Pedro Santos": ["Coloracao"],
    "Mariana Lima": ["Tratamento Capilar"],
}

DEFAULT_TIMES = [time(9, 0), time(11, 0), time(14, 0), time(16, 0)]


def seed_database() -> None:
    init_db()
    engine = get_engine()
    if not engine:
        raise RuntimeError("DATABASE_URL nao configurada.")
    if is_seeded():
        return

    with engine.begin() as conn:
        conn.execute(services.insert(), SERVICE_DATA)
        conn.execute(professionals.insert(), PROFESSIONAL_DATA)

        service_rows = conn.execute(services.select()).mappings().all()
        professional_rows = conn.execute(professionals.select()).mappings().all()

        service_by_name = {row["name"]: row["id"] for row in service_rows}
        professional_by_name = {row["name"]: row["id"] for row in professional_rows}

        mapping_rows = []
        for prof_name, service_names in PROFESSIONAL_SERVICE_MAP.items():
            for service_name in service_names:
                mapping_rows.append(
                    {
                        "professional_id": professional_by_name[prof_name],
                        "service_id": service_by_name[service_name],
                    }
                )
        conn.execute(professional_services.insert(), mapping_rows)

        today = date.today()
        availability_rows = []
        for offset in range(7):
            target_date = today + timedelta(days=offset)
            for prof in professional_rows:
                for slot in DEFAULT_TIMES:
                    availability_rows.append(
                        {
                            "professional_id": prof["id"],
                            "date": target_date,
                            "time": slot,
                            "is_available": True,
                        }
                    )
        conn.execute(availabilities.insert(), availability_rows)


if __name__ == "__main__":
    seed_database()
    print("Seed concluido com sucesso.")
