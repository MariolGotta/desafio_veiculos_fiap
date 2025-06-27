from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate
from passlib.context import CryptContext
from typing import Optional

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UsuarioService:

    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def criar_usuario(db: Session, usuario: UsuarioCreate) -> Usuario:
        hashed_password = UsuarioService.hash_password(usuario.senha)

        db_usuario = Usuario(
            nome=usuario.nome,
            sobrenome=usuario.sobrenome,
            cpf=usuario.cpf,
            rg=usuario.rg,
            data_nascimento=usuario.data_nascimento,
            endereco=usuario.endereco,
            telefone=usuario.telefone,
            email=usuario.email,
            senha_hash=hashed_password,
            tipo_usuario=usuario.tipo_usuario,
            razao_social=usuario.razao_social,
            cnpj=usuario.cnpj,
            endereco_comercial=usuario.endereco_comercial
        )

        db.add(db_usuario)
        db.commit()
        db.refresh(db_usuario)
        return db_usuario

    @staticmethod
    def buscar_por_email(db: Session, email: str) -> Optional[Usuario]:
        return db.query(Usuario).filter(Usuario.email == email).first()

    @staticmethod
    def buscar_por_cpf(db: Session, cpf: str) -> Optional[Usuario]:
        return db.query(Usuario).filter(Usuario.cpf == cpf).first()

    @staticmethod
    def autenticar_usuario(db: Session, email: str, senha: str) -> Optional[Usuario]:
        usuario = UsuarioService.buscar_por_email(db, email)
        if not usuario:
            return None
        if not UsuarioService.verify_password(senha, usuario.senha_hash):
            return None
        return usuario
