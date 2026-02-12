import os
from datetime import date

from dotenv import load_dotenv
from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    MetaData,
    Numeric,
    String,
    Table,
    Time,
    create_engine,
    func,
    select,
    text,
)
from sqlalchemy.engine import Engine

load_dotenv()

metadata = MetaData()

services = Table(
    "services",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(120), nullable=False, unique=True),
    Column("tagline", String(200), nullable=True),
    Column("description", String(400), nullable=True),
    Column("price", Numeric(10, 2), nullable=False),
    Column("duration_minutes", Integer, nullable=False),
)

professionals = Table(
    "professionals",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(120), nullable=False, unique=True),
    Column("role", String(120), nullable=False),
    Column("rating", Numeric(2, 1), nullable=False, server_default="5.0"),
    Column("reviews", Integer, nullable=False, server_default="0"),
)

professional_services = Table(
    "professional_services",
    metadata,
    Column("professional_id", Integer, ForeignKey("professionals.id"), primary_key=True),
    Column("service_id", Integer, ForeignKey("services.id"), primary_key=True),
)

availabilities = Table(
    "availabilities",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("professional_id", Integer, ForeignKey("professionals.id"), nullable=False),
    Column("date", Date, nullable=False),
    Column("time", Time, nullable=False),
    Column("is_available", Boolean, nullable=False, server_default=text("true")),
)

appointments = Table(
    "appointments",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("professional_id", Integer, ForeignKey("professionals.id"), nullable=False),
    Column("service_id", Integer, ForeignKey("services.id"), nullable=False),
    Column("date", Date, nullable=False),
    Column("time", Time, nullable=False),
    Column("customer_name", String(120), nullable=False),
    Column("customer_email", String(200), nullable=True),
    Column("customer_phone", String(50), nullable=True),
    Column("status", String(40), nullable=False, server_default="confirmed"),
    Column("created_at", DateTime, nullable=False, server_default=func.now()),
)


def get_database_url() -> str | None:
    url = (
        os.getenv("DATABASE_URL")
        or os.getenv("URL_DO_BANCO_DE_DADOS")
        or os.getenv("URL_PUBLICA_DO_BANCO_DE_DADOS")
    )
    if not url:
        return None
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    if "sslmode=" not in url:
        joiner = "&" if "?" in url else "?"
        url = f"{url}{joiner}sslmode=require"
    return url


def get_engine() -> Engine | None:
    url = get_database_url()
    if not url:
        return None
    return create_engine(url, pool_pre_ping=True)


def init_db() -> None:
    engine = get_engine()
    if not engine:
        return
    metadata.create_all(engine)


def list_services() -> list[dict]:
    engine = get_engine()
    if not engine:
        return []
    with engine.connect() as conn:
        rows = conn.execute(select(services).order_by(services.c.id)).mappings().all()
        return [dict(row) for row in rows]


def list_professionals() -> list[dict]:
    engine = get_engine()
    if not engine:
        return []
    with engine.connect() as conn:
        rows = conn.execute(select(professionals).order_by(professionals.c.id)).mappings().all()
        return [dict(row) for row in rows]


def list_professional_services() -> list[dict]:
    engine = get_engine()
    if not engine:
        return []
    with engine.connect() as conn:
        rows = conn.execute(select(professional_services)).mappings().all()
        return [dict(row) for row in rows]


def list_availability(target_date: date) -> list[dict]:
    engine = get_engine()
    if not engine:
        return []
    with engine.connect() as conn:
        rows = conn.execute(
            select(availabilities)
            .where(availabilities.c.date == target_date)
            .order_by(availabilities.c.time)
        ).mappings().all()
        return [dict(row) for row in rows]


def create_appointment(
    professional_id: int,
    service_id: int,
    date_value: date,
    time_value,
    customer_name: str,
    customer_email: str | None,
    customer_phone: str | None,
) -> bool:
    engine = get_engine()
    if not engine:
        return False
    with engine.begin() as conn:
        conn.execute(
            appointments.insert().values(
                professional_id=professional_id,
                service_id=service_id,
                date=date_value,
                time=time_value,
                customer_name=customer_name,
                customer_email=customer_email,
                customer_phone=customer_phone,
                status="confirmed",
            )
        )
        conn.execute(
            availabilities.update()
            .where(
                (availabilities.c.professional_id == professional_id)
                & (availabilities.c.date == date_value)
                & (availabilities.c.time == time_value)
            )
            .values(is_available=False)
        )
    return True


def is_seeded() -> bool:
    engine = get_engine()
    if not engine:
        return False
    with engine.connect() as conn:
        result = conn.execute(select(func.count()).select_from(services)).scalar_one()
        return result > 0
