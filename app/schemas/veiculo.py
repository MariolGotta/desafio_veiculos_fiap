from pydantic import BaseModel, Field
from typing import Optional

class VeiculoCreate(BaseModel):
    marca: str = Field(..., min_length=1, max_length=50)
    modelo: str = Field(..., min_length=1, max_length=50)
    ano: int = Field(..., ge=1950, le=2025)
    quilometragem: int = Field(..., ge=0)
    preco: float = Field(..., gt=0)
    categoria: str = Field(..., pattern="^(carro|moto|caminhao|barco|utilitario)$")
    condicao: str = Field(..., pattern="^(novo|usado)$")
    cor: Optional[str] = None
    combustivel: Optional[str] = None
    descricao: Optional[str] = None

class VeiculoResponse(BaseModel):
    id: str
    marca: str
    modelo: str
    ano: int
    quilometragem: int
    preco: float
    categoria: str
    condicao: str
    cor: Optional[str] = None  # ✅ Mudança aqui - era obrigatório
    combustivel: Optional[str] = None  # ✅ Mudança aqui - era obrigatório
    proprietario_id: str
    status: str
    descricao: Optional[str] = None

class VeiculoFiltros(BaseModel):
    marca: Optional[str] = None
    preco_min: Optional[float] = None
    preco_max: Optional[float] = None
    categoria: Optional[str] = None
    condicao: Optional[str] = None