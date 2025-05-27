from sqlmodel import SQLModel, Field, Relationship
from app.models.registration import Registration

class BaseUser(SQLModel):
    """
    Modelo base per gli utenti, definisce i campi comuni per tutti i modelli di utente.
    """
    username: str
    name: str
    email: str

class User(BaseUser, table=True):
    """
    Modello di utente che estende BaseUser e rappresenta una tabella nel database.
    """
    username: str = Field(primary_key=True)
    registrations: list["Registration"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs=
        {
            "cascade": "all, delete-orphan"
        }
    )

class UserPublic(BaseUser):
    """
    Modello utilizzato per restituire tutti i dati degli utenti nelle risposte API.
    """
    pass

class UserCreate(BaseUser):
    """
    Modello per la creazione di un nuovo utente
    """
    pass