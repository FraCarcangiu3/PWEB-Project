from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from datetime import datetime
from app.models.registration import Registration

class EventBase(SQLModel):
    """
    Classe base che definisce i campi comuni per tutti i modelli di evento.
    """
    title: str
    description: str
    date: datetime
    location: str

class Event(EventBase, table=True):
    """
    Modello di evento che estende EventBase e rappresenta una tabella nel database.
    """
    id: int = Field(default=None, primary_key=True) # Campo ID che funge da chiave primaria, con valore predefinito None
    registrations: list["Registration"] = Relationship(
        back_populates="event",
        sa_relationship_kwargs=
        {
            "cascade": "all,delete,delete-orphan"
        }
    )

class EventCreate(EventBase): # Modello per la creazione di un nuovo evento
    """
    Modello per la creazione di un nuovo evento, estende EventBase senza ID.
    """
    pass  # Non ha bisogno di ulteriori campi, poiché eredita tutto da EventBase

class EventPublic(EventBase): # Modello per la visualizzazione pubblica degli eventi  (ovvero per le risposte API)
    """
    Modello utilizzato per restituire tutti i dati degli eventi nelle risposte API.
    Estende EventBase e include l'ID dell'evento.
    """
    id :int