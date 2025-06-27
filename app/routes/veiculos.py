from fastapi import APIRouter, HTTPException, status
from typing import List
from app.schemas.veiculo import VeiculoCreate, VeiculoResponse
from app.services.veiculo_service import VeiculoService
import uuid

router = APIRouter(prefix="/veiculos", tags=["veiculos"])


@router.post("/", response_model=VeiculoResponse)
def criar_veiculo(veiculo: VeiculoCreate, proprietario_id: str):
    veiculo_data = veiculo.dict()
    veiculo_data["id"] = str(uuid.uuid4())
    veiculo_data["proprietario_id"] = proprietario_id

    resultado = VeiculoService.criar_veiculo(veiculo_data)
    if not resultado:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro ao criar veículo"
        )

    return VeiculoResponse(**resultado)


@router.get("/", response_model=List[VeiculoResponse])
def listar_veiculos():
    veiculos = VeiculoService.buscar_todos_veiculos()
    return [VeiculoResponse(**v) for v in veiculos]


@router.get("/categoria/{categoria}", response_model=List[VeiculoResponse])
def listar_por_categoria(categoria: str):
    veiculos = VeiculoService.buscar_veiculos_por_categoria(categoria)
    return [VeiculoResponse(**v) for v in veiculos]


@router.post("/interesse/{veiculo_id}")
def demonstrar_interesse(veiculo_id: str, usuario_id: str):
    resultado = VeiculoService.criar_interesse(usuario_id, veiculo_id)
    if not resultado:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro ao registrar interesse"
        )

    return {"message": "Interesse registrado com sucesso", "veiculo_id": veiculo_id, "usuario_id": usuario_id}


@router.get("/recomendacoes/{usuario_id}", response_model=List[VeiculoResponse])
def obter_recomendacoes(usuario_id: str):
    veiculos = VeiculoService.recomendar_veiculos(usuario_id)
    return [VeiculoResponse(**v) for v in veiculos]
