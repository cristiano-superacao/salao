import os
import sys
from datetime import date
from pathlib import Path

# Permite rodar: `python scripts/smoke_test.py`
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from db import (
    create_appointment,
    get_database_url,
    init_db,
    list_availability,
    list_professionals,
    list_services,
)


def run() -> None:
    if not get_database_url():
        raise SystemExit(
            "URL do banco nao configurada. Defina DATABASE_URL (ou URL_DO_BANCO_DE_DADOS/URL_PUBLICA_DO_BANCO_DE_DADOS)."
        )

    init_db()
    services = list_services()
    professionals = list_professionals()

    if not services:
        raise SystemExit("Sem servicos. Execute: python seed.py")
    if not professionals:
        raise SystemExit("Sem profissionais. Execute: python seed.py")

    print(f"Servicos: {len(services)}")
    print(f"Profissionais: {len(professionals)}")

    # Teste opcional de escrita (cria 1 agendamento) para validar INSERT/UPDATE.
    # Para habilitar: PowerShell -> $env:SMOKE_TEST_WRITE='1'
    if os.getenv("SMOKE_TEST_WRITE") == "1":
        target_date = date.today()
        availability = list_availability(target_date)
        open_slots = [a for a in availability if a.get("is_available") is True]
        if not open_slots:
            raise SystemExit(
                "Sem horarios disponiveis para teste de escrita. Rode novamente amanha ou ajuste o seed."
            )

        slot = open_slots[0]
        ok = create_appointment(
            professional_id=int(slot["professional_id"]),
            service_id=int(services[0]["id"]),
            date_value=target_date,
            time_value=slot["time"],
            customer_name="Teste Smoke",
            customer_email="smoke@test.local",
            customer_phone=None,
        )
        if not ok:
            raise SystemExit("Falha no teste de escrita (create_appointment retornou False).")

        availability_after = list_availability(target_date)
        matched = [
            a
            for a in availability_after
            if a.get("professional_id") == slot.get("professional_id")
            and a.get("time") == slot.get("time")
        ]
        if not matched or matched[0].get("is_available") is not False:
            raise SystemExit("Teste de escrita falhou: o horario nao foi bloqueado.")

        print("Teste de escrita OK (agendamento criado e horario bloqueado)")

    print("Smoke test OK")


if __name__ == "__main__":
    run()
