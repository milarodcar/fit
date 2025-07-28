from sqlalchemy.orm import Session
from db.models import Client
from typing import List, Optional

class ClientRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_client(self, client_id: int) -> Optional[Client]:
        return self.db.query(Client).filter(
            Client.id == client_id,
            Client.is_active == True
        ).first()

    def get_clients(self, skip: int = 0, limit: int = 100) -> List[Client]:
        return self.db.query(Client).filter(
            Client.is_active == True
        ).offset(skip).limit(limit).all()

    def create_client(self, client_data: dict) -> Client:
        db_client = Client(**client_data)
        self.db.add(db_client)
        self.db.commit()
        self.db.refresh(db_client)
        return db_client

    def update_client(self, client_id: int, client_data: dict) -> Optional[Client]:
        db_client = self.get_client(client_id)
        if not db_client:
            return None
        
        for key, value in client_data.items():
            setattr(db_client, key, value)
        
        self.db.commit()
        self.db.refresh(db_client)
        return db_client

    def deactivate_client(self, client_id: int) -> bool:
        db_client = self.get_client(client_id)
        if not db_client:
            return False
        
        db_client.is_active = False
        self.db.commit()
        return True