from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Nova URL com credenciais mais simples
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://postgres:admin123@postgres:5432/veiculos_db")

print(f"📡 Conectando em: {DATABASE_URL}")

engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print(f"✅ PostgreSQL: {version}")
            return True
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False
