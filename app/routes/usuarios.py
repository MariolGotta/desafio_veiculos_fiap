from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.schemas.usuario import UsuarioCreate, UsuarioResponse, UsuarioLogin
from app.services.usuario_service import UsuarioService

router = APIRouter(prefix="/usuarios", tags=["usuarios"])


@router.post("/", response_model=UsuarioResponse)
def criar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):  # Removido async
    # Verificar se email já existe
    if UsuarioService.buscar_por_email(db, usuario.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado"
        )

    # Verificar se CPF já existe
    if UsuarioService.buscar_por_cpf(db, usuario.cpf):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="CPF já cadastrado"
        )

    return UsuarioService.criar_usuario(db, usuario)


@router.post("/login")
def login(dados: UsuarioLogin, db: Session = Depends(get_db)):  # Removido async
    usuario = UsuarioService.autenticar_usuario(db, dados.email, dados.senha)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos"
        )

    return {"message": "Login realizado com sucesso", "usuario_id": usuario.id}
