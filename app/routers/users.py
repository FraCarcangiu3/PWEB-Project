from fastapi import APIRouter, Request, HTTPException, Path, Form
from app.models.user import UserCreate, User, UserPublic
from typing import Annotated
from app.data.db import SessionDep
from sqlmodel import select, delete

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/")
def get_all_users(
    session: SessionDep,
    request: Request,
    sort: bool = False
) -> list[UserPublic]:
    """
    Ottieni la lista di tutti gli utenti.
    """
    statement = select(User)
    users = session.exec(statement).all()
    if sort:
        return sorted(users, key=lambda user: user.username)
    return list(users)

@router.get("/{username}")
def get_user_by_username(
    username: Annotated[str, Path(description="Username dell'utente da recuperare")],
    session: SessionDep
) -> UserPublic:
    """
    Ottieni un utente per username dato.
    """
    statement = select(User).where(User.username == username)
    user = session.exec(statement).one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User non trovato!")
    return UserPublic.model_validate(user)

@router.post("/")
def add_user(
    request: Request,
    user: UserCreate,
    session: SessionDep
):
    """
    Aggiunge un nuovo utente.
    """
    validated_user = User.model_validate(user)
    session.add(validated_user)
    session.commit()
    return "User aggiunto con successo."

@router.delete("/")
def delete_all_users(
    session: SessionDep
):
    """
    Cancella tutti gli utenti.
    """
    # statement = delete(User) # Non funziona il cascading delete.
    # siccome singolarmente funziona, allora lo faccio uno per uno.
    statement = select(User) # Seleziona tutti gli utenti
    users = session.exec(statement).all() # Recupera tutti gli utenti
    for user in users: # Itera su ogni utente
        session.delete(user) # Elimina l'utente corrente
    # session.exec(statement)
    session.commit() # Commit delle modifiche
    return "Tutti gli utenti sono stati cancellati."

@router.delete("/{username}")
def delete_user_by_username(
    username: Annotated[str, Path(description="Username dell'utente da cancellare")],
    session: SessionDep
):
    """
    Cancella un utente per username dato.
    """
    statement = select(User).where(User.username == username)
    user = session.exec(statement).one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User non trovato!")
    session.delete(user)
    session.commit()
    return "User cancellato con successo."