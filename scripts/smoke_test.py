from db import get_database_url, init_db, list_professionals, list_services


def run() -> None:
    if not get_database_url():
        raise SystemExit("DATABASE_URL nao configurada.")

    init_db()
    services = list_services()
    professionals = list_professionals()

    if not services:
        raise SystemExit("Sem servicos. Execute: python seed.py")
    if not professionals:
        raise SystemExit("Sem profissionais. Execute: python seed.py")

    print(f"Servicos: {len(services)}")
    print(f"Profissionais: {len(professionals)}")
    print("Smoke test OK")


if __name__ == "__main__":
    run()
