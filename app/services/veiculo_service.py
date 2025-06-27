from app.config.neo4j_db import neo4j_db
from typing import List, Dict, Optional


class VeiculoService:

    @staticmethod
    def criar_veiculo(veiculo_data: Dict) -> Dict:
        # Garantir que campos opcionais tenham valores padrão
        veiculo_data["cor"] = veiculo_data.get("cor") or None
        veiculo_data["combustivel"] = veiculo_data.get("combustivel") or None
        veiculo_data["descricao"] = veiculo_data.get("descricao") or None

        query = """
        CREATE (v:Veiculo {
            id: $id,
            marca: $marca,
            modelo: $modelo,
            ano: $ano,
            quilometragem: $quilometragem,
            preco: $preco,
            categoria: $categoria,
            condicao: $condicao,
            cor: $cor,
            combustivel: $combustivel,
            proprietario_id: $proprietario_id,
            status: 'disponivel',
            data_anuncio: datetime(),
            descricao: $descricao
        })
        RETURN v
        """

        result = neo4j_db.query(query, veiculo_data)
        if result:
            return dict(result[0]['v'])
        return None

    @staticmethod
    def buscar_veiculos_por_categoria(categoria: str) -> List[Dict]:
        query = """
        MATCH (v:Veiculo {categoria: $categoria, status: 'disponivel'})
        RETURN v
        ORDER BY v.data_anuncio DESC
        """

        result = neo4j_db.query(query, {"categoria": categoria})
        return [dict(record['v']) for record in result]

    @staticmethod
    def buscar_todos_veiculos() -> List[Dict]:
        query = """
        MATCH (v:Veiculo {status: 'disponivel'})
        RETURN v
        ORDER BY v.data_anuncio DESC
        LIMIT 50
        """

        result = neo4j_db.query(query)
        return [dict(record['v']) for record in result]

    @staticmethod
    def criar_interesse(usuario_id: str, veiculo_id: str):
        """Criar relacionamento de interesse entre usuário e veículo"""
        query = """
        MATCH (v:Veiculo {id: $veiculo_id})
        MERGE (u:Usuario {id: $usuario_id})
        MERGE (u)-[r:INTERESSADO_EM]->(v)
        SET r.data_interesse = datetime()
        RETURN r
        """

        try:
            result = neo4j_db.query(query, {
                "usuario_id": usuario_id,
                "veiculo_id": veiculo_id
            })
            return result
        except Exception as e:
            print(f"❌ Erro ao criar interesse: {e}")
            return None

    @staticmethod
    def recomendar_veiculos(usuario_id: str) -> List[Dict]:
        """Recomendar veículos baseado nos interesses"""
        query = """
        MATCH (u:Usuario {id: $usuario_id})-[:INTERESSADO_EM]->(v1:Veiculo)
        MATCH (outros:Usuario)-[:INTERESSADO_EM]->(v1)
        MATCH (outros)-[:INTERESSADO_EM]->(v2:Veiculo)
        WHERE v2.status = 'disponivel' 
        AND NOT (u)-[:INTERESSADO_EM]->(v2)
        AND v2.id <> v1.id
        RETURN DISTINCT v2 as veiculo, count(*) as score
        ORDER BY score DESC
        LIMIT 10
        """

        try:
            result = neo4j_db.query(query, {"usuario_id": usuario_id})
            return [dict(record['veiculo']) for record in result]
        except Exception as e:
            print(f"❌ Erro ao buscar recomendações: {e}")
            return []
