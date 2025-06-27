from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import usuarios, veiculos

app = FastAPI(
    title="Sistema de Veículos",
    description="API para compra e venda de veículos",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(usuarios.router)
app.include_router(veiculos.router)


@app.get("/")
def root():  # Removido async
    return {"message": "Sistema de Veículos API"}


@app.get("/test-db")
def test_database():  # Removido async
    """Endpoint para testar conexão com banco"""
    try:
        from app.config.database import test_connection
        if test_connection():
            return {"status": "success", "message": "Conectado ao PostgreSQL"}
        else:
            return {"status": "error", "message": "Erro de conexão"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.post("/create-tables")
def create_tables():  # Removido async
    """Endpoint manual para criar tabelas"""
    try:
        from app.config.database import engine, Base
        print("🔄 Criando tabelas...")
        Base.metadata.create_all(bind=engine)
        return {"status": "success", "message": "Tabelas criadas com sucesso!"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
