from db.models import Client
from typing import List, Optional, Set
from api.schemas import ClientCreate, ClientBase
from db.repositories.client_repo import ClientRepository

class ClientService:
    def __init__(self, db):
        self.db = db
        self.repository = ClientRepository(db)

    def get_client(self, client_id: int) -> Optional[Client]:
        return self.repository.get_client(client_id)

    def get_clients(self, skip: int = 0, limit: int = 100) -> List[Client]:
        return self.repository.get_clients(skip, limit)

    def get_clients_filtered(self, name: str = None, objective: str = None) -> List[Client]:
        query = self.db.query(Client)
        if name:
            query = query.filter(Client.name.ilike(f"%{name}%"))
        if objective:
            query = query.filter(Client.objectives.ilike(f"%{objective}%"))
        return query.order_by(Client.name).all()

    def get_all_objectives(self) -> List[str]:
        objectives = set()
        clients = self.db.query(Client.objectives).all()
        for client in clients:
            if client.objectives:
                for goal in client.objectives.split(','):
                    objectives.add(goal.strip())
        return sorted(objectives)

    def create_client(self, client: ClientCreate) -> Client:
        client_data = client.model_dump()
        client_data["objectives"] = ",".join(client.objectives)
        return self.repository.create_client(client_data)

    def update_client(self, client_id: int, updated_client: ClientCreate) -> bool:
        client = self.repository.get_client(client_id)
        if not client:
            return False

        client.name = updated_client.name
        client.age = updated_client.age
        client.weight = updated_client.weight
        client.objectives = ",".join(updated_client.objectives)
        client.phone_number = updated_client.phone_number
        client.training_type = updated_client.training_type
        client.service = updated_client.service
        client.observations = updated_client.observations

        self.db.commit()
        return True

    def delete_client(self, client_id: int) -> bool:
        client = self.repository.get_client(client_id)
        if client:
            self.db.delete(client)
            self.db.commit()
            return True
        return False
