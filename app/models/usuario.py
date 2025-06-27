from sqlalchemy import Column, Integer, String, Date, DateTime, Text, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import Enum as SQLEnum
from app.config.database import Base
import enum


class TipoUsuario(enum.Enum):
    PESSOA_FISICA = "pessoa_fisica"
    LOJISTA = "lojista"


# Tabela de associação para seguidores
seguidores_table = Table(
    'seguidores',
    Base.metadata,
    Column('seguidor_id', Integer, ForeignKey(
        'usuarios.id'), primary_key=True),
    Column('seguido_id', Integer, ForeignKey('usuarios.id'), primary_key=True),
    Column('data_seguimento', DateTime, default=func.now())
)


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    sobrenome = Column(String(100), nullable=False)
    cpf = Column(String(11), unique=True, nullable=False, index=True)
    rg = Column(String(20))
    data_nascimento = Column(Date)
    endereco = Column(Text)
    telefone = Column(String(15))
    email = Column(String(100), unique=True, nullable=False, index=True)
    senha_hash = Column(String(255), nullable=False)

    # Usar String em vez de Enum para evitar problemas
    tipo_usuario = Column(String(20), default="pessoa_fisica")

    # Campos específicos para lojistas
    razao_social = Column(String(200))
    cnpj = Column(String(14), unique=True)
    endereco_comercial = Column(Text)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relacionamentos
    seguindo = relationship(
        "Usuario",
        secondary=seguidores_table,
        primaryjoin=id == seguidores_table.c.seguidor_id,
        secondaryjoin=id == seguidores_table.c.seguido_id,
        back_populates="seguidores"
    )

    seguidores = relationship(
        "Usuario",
        secondary=seguidores_table,
        primaryjoin=id == seguidores_table.c.seguido_id,
        secondaryjoin=id == seguidores_table.c.seguidor_id,
        back_populates="seguindo"
    )
