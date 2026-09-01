from app.graph.client import neo4j_client

class GraphBuilder:
    @staticmethod
    async def ingest_customer(customer_data: dict):
        query = """
        MERGE (c:Customer {id: $id})
        SET c.name = $name, c.email = $email
        """
        await neo4j_client.execute_query(query, customer_data)

    @staticmethod
    async def ingest_invoice(invoice_data: dict):
        query = """
        MERGE (i:Invoice {id: $invoice_id})
        SET i.amount = $amount, i.status = $status
        WITH i
        MATCH (c:Customer {id: $customer_id})
        MERGE (c)-[:ISSUED]->(i)
        """
        await neo4j_client.execute_query(query, invoice_data)
        
    @staticmethod
    async def ingest_payment(payment_data: dict):
        query = """
        MERGE (p:Payment {id: $payment_id})
        SET p.amount = $amount, p.status = $status
        WITH p
        MATCH (i:Invoice {id: $invoice_id})
        MERGE (p)-[:PAYS]->(i)
        """
        await neo4j_client.execute_query(query, payment_data)
        
    @staticmethod
    async def ingest_settlement(settlement_data: dict):
        query = """
        MERGE (s:Settlement {id: $settlement_id})
        SET s.net_amount = $net_amount, s.fee = $fee
        WITH s
        MATCH (p:Payment {id: $payment_id})
        MERGE (s)-[:SETTLES]->(p)
        """
        await neo4j_client.execute_query(query, settlement_data)
