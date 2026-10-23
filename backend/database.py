import os
from pathlib import Path
from typing import Generator

from dotenv import load_dotenv
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

# Carrega as variáveis de ambiente do arquivo .env
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(env_path, override=True)

db_password = os.getenv("DB_PASSWORD")
if not db_password:
    raise RuntimeError("A variável de ambiente 'DB_PASSWORD' não foi configurada no arquivo .env.")

# Configuração da URL de conexão com o PostgreSQL
db_url = URL.create(
    drivername="postgresql+psycopg2",
    username=os.getenv("DB_USER", "postgres"),
    password=db_password,
    host=os.getenv("DB_HOST", "localhost"),
    port=int(os.getenv("DB_PORT", "5432")),
    database=os.getenv("DB_NAME", "mercearia"),
)

# Configuração do Engine e da Sessão
engine = create_engine(db_url, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    """Classe base para os modelos declarativos do SQLAlchemy."""
    pass


def get_db() -> Generator[Session, None, None]:
    """Gera uma sessão do banco de dados para uso em rotas (ex: FastAPI)."""
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()