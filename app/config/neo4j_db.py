from neo4j import GraphDatabase
import os


class Neo4jConnection:
    def __init__(self):
        # Usar variável de ambiente ou nome do serviço Docker
        neo4j_uri = os.getenv("NEO4J_URI", "bolt://neo4j:7687")
        neo4j_user = os.getenv("NEO4J_USER", "neo4j")
        neo4j_password = os.getenv("NEO4J_PASSWORD", "novasenha123")

        print(f"🔗 Conectando ao Neo4j: {neo4j_uri}")

        self.driver = GraphDatabase.driver(
            neo4j_uri,
            auth=(neo4j_user, neo4j_password)
        )

    def close(self):
        if self.driver is not None:
            self.driver.close()

    def query(self, query, parameters=None):
        with self.driver.session() as session:
            result = session.run(query, parameters)
            return [record for record in result]


# Instância global
neo4j_db = Neo4jConnection()
