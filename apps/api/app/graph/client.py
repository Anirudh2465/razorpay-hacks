from neo4j import GraphDatabase, AsyncGraphDatabase
import logging
from app.config import settings

logger = logging.getLogger(__name__)

class Neo4jClient:
    def __init__(self):
        self.uri = settings.NEO4J_URI
        self.user = settings.NEO4J_USER
        self.password = settings.NEO4J_PASSWORD
        self._driver = None

    async def connect(self):
        try:
            self._driver = AsyncGraphDatabase.driver(
                self.uri, auth=(self.user, self.password)
            )
            await self._driver.verify_connectivity()
            logger.info("Connected to Neo4j successfully.")
        except Exception as e:
            logger.error(f"Failed to connect to Neo4j: {e}")

    async def close(self):
        if self._driver is not None:
            await self._driver.close()

    async def execute_query(self, query: str, parameters=None):
        if not self._driver:
            await self.connect()
            
        async with self._driver.session() as session:
            try:
                result = await session.run(query, parameters)
                return await result.data()
            except Exception as e:
                logger.error(f"Failed to execute Cypher query: {e}")
                return None

neo4j_client = Neo4jClient()

async def create_constraints():
    # Setup initial constraints (e.g. unique IDs)
    queries = [
        "CREATE CONSTRAINT IF NOT EXISTS FOR (c:Customer) REQUIRE c.id IS UNIQUE",
        "CREATE CONSTRAINT IF NOT EXISTS FOR (i:Invoice) REQUIRE i.id IS UNIQUE",
        "CREATE CONSTRAINT IF NOT EXISTS FOR (p:Payment) REQUIRE p.id IS UNIQUE",
        "CREATE CONSTRAINT IF NOT EXISTS FOR (s:Settlement) REQUIRE s.id IS UNIQUE",
    ]
    
    for q in queries:
        await neo4j_client.execute_query(q)
