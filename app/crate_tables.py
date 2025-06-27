#!/usr/bin/env python3
"""
Script para criar tabelas no PostgreSQL
Execute: python create_tables.py
"""

import os
import sys

# Configurar encoding
os.environ["PYTHONIOENCODING"] = "utf-8"
os.environ["PYTHONUTF8"] = "1"

try:
    from app.config.database import engine, Base, test_connection
    from app.models.usuario import Usuario

    print("🔄 Testando conexão com PostgreSQL...")

    if test_connection():
        print("✅ Conexão OK!")

        print("🔄 Criando tabelas...")
        Base.metadata.create_all(bind=engine)
        print("✅ Tabelas criadas com sucesso!")

        # Verificar tabelas criadas
        with engine.connect() as conn:
            result = conn.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """)
            tables = result.fetchall()
            print(f"📋 Tabelas encontradas: {[table[0] for table in tables]}")
    else:
        print("❌ Erro de conexão")

except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()
