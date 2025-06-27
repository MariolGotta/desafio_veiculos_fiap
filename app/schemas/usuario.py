from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime
from enum import Enum


class TipoUsuario(str, Enum):
    PESSOA_FISICA = "pessoa_fisica"
    LOJISTA = "lojista"


class UsuarioCreate(BaseModel):
    nome: str = Field(..., min_length=1, max_length=100)
    sobrenome: str = Field(..., min_length=1, max_length=100)
    cpf: str = Field(..., pattern=r'^\d{11}$')
    rg: Optional[str] = None
    data_nascimento: Optional[date] = None
    endereco: Optional[str] = None
    telefone: Optional[str] = None
    email: str = Field(..., pattern=r'^[^@]+@[^@]+\.[^@]+$')
    senha: str = Field(..., min_length=6)
    tipo_usuario: TipoUsuario = TipoUsuario.PESSOA_FISICA

    # Campos opcionais para lojistas
    razao_social: Optional[str] = None
    cnpj: Optional[str] = None
    endereco_comercial: Optional[str] = None


class UsuarioResponse(BaseModel):
    id: int
    nome: str
    sobrenome: str
    cpf: str
    email: str
    tipo_usuario: TipoUsuario
    created_at: datetime

    class Config:
        from_attributes = True


class UsuarioLogin(BaseModel):
    email: str
    senha: str
