#!/usr/bin/env python3
"""
Teste de conexão PostgreSQL isolado
"""

import os
import sys

# Forçar UTF-8
os.environ["PYTHONIOENCODING"] = "utf-8"
os.environ["PYTHONUTF8"] = "1"
os.environ["PGCLIENTENCODING"] = "UTF8"

try:
    import psycopg2

    # Testar conexão direta
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="veiculos_db",
        user="user_admin",
        password="senha123",
        client_encoding="UTF8"
    )

    cursor = conn.cursor()
    cursor.execute("SELECT version()")
    version = cursor.fetchone()[0]

    print(f"✅ Conexão direta funcionou!")
    print(f"📋 Versão: {version}")

    cursor.close()
    conn.close()

except Exception as e:
    print(f"❌ Erro na conexão direta: {e}")
    import traceback
    traceback.print_exc()

# Agora testar com SQLAlchemy
try:
    from sqlalchemy import create_engine

    DATABASE_URL = "postgresql://user_admin:senha123@localhost:5432/veiculos_db"

    engine = create_engine(
        DATABASE_URL,
        echo=True,
        connect_args={
            "client_encoding": "UTF8"
        }
    )

    with engine.connect() as connection:
        result = connection.execute("SELECT version()")
        version = result.fetchone()[0]
        print(f"✅ SQLAlchemy funcionou!")
        print(f"📋 Versão: {version}")

except Exception as e:
    print(f"❌ Erro SQLAlchemy: {e}")
    import traceback
    traceback.print_exc()
