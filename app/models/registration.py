from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, ForeignKey, String, Integer
from typing import TYPE_CHECKING

if TYPE_CHECKING: # per evitare import ciclici con User e Event
    # Importa User ed Event solo se il tipo di controllo è attivo, per evitare cicli di importazione
    from app.models.user import User
    from app.models.event import Event

class RegistrationBase(SQLModel):
    """
    Modello base per la registrazione, definisce i campi comuni.
    """
    username: str
    event_id: int

class Registration(RegistrationBase, table=True):
    """
    Modello di registrazione che estende RegistrationBase e rappresenta una tabella nel database.
    """
    username: str = Field(
        sa_column=Column(
            "username", String,
            ForeignKey(
                "user.username",
                ondelete="CASCADE" # Imposta la cancellazione a cascata
            ),
            primary_key=True
        )
    )
    event_id: int = Field(
        sa_column=Column(
            "event_id", Integer,
            ForeignKey(
                "event.id",
                ondelete="CASCADE" # Imposta la cancellazione a cascata
            ),
            primary_key=True
        )
    )

    user: "User" = Relationship(back_populates="registrations") # Relazione con il modello User
    event: "Event" = Relationship(back_populates="registrations") # Relazione con il modello Event

class RegistrationPublic(RegistrationBase):
    """
    Modello utilizzato per restituire tutti i dati delle registrazioni nelle risposte API.
    Estende RegistrationBase e include i campi necessari per la visualizzazione pubblica.
    """
    pass # Non include ulteriori campi, poiché eredita tutto da RegistrationBase

class RegistrationCreate(RegistrationBase):
    """
    Modello per la creazione di una nuova registrazione, estende RegistrationBase.
    """
    pass  # Non ha bisogno di ulteriori campi, poiché eredita tutto da RegistrationBase