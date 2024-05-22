"""
api.py
---

The REST Api for the Globoticket events database.
"""

from pathlib import Path
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from starlette.staticfiles import StaticFiles

from globoticket.crud import get_all_dbevents, get_dbevent
from globoticket.database import SessionLocal
from globoticket.models import DBEvent
from globoticket.schemas import Event

# the app object represents the REST API application that we'll be creating
# This is what's being referred to when we start the uvicorn server in runserver.py
app = FastAPI()

PROJECT_ROOT = Path(__file__).parent.parent


def get_session() -> Session:
    session = SessionLocal()
    try:
        # yield is a generator function that more or less pauses the get_session
        # function at this line
        yield session
    finally:
        # this gets called after FastAPI is done calling get_event() or any call
        # that's depending on this function
        session.close()


# the app.get decorator turns this function into an API call, or what FASTAPI
# calls it an operation.
# Annotated - allows us to annotate a function argument with more than just its type
#   In this case, 'db' uses two arguments:
#     - Session: This is regular type hint, saying db is supposed to be of type Session
#     - Depends: This is Python's dependency injection specific to FastAPI. This means
#           FastAPI should create this DB object by calling get_session()
# id - path param that will be used for the id argument of our function
# Event - response schema that will also be shown in the FASTAPI docs, see /docs
#   It's specified in the response_model because it's an instruction for FastAPI about
#   the data to send back to the client. FastAPI will use the model from DBEvent and
#   create a JSON object that conforms to the Event schema.
# This api is also mentioned in details.html
@app.get("/events/{id}", response_model=Event)
def get_event(id: int, db: Annotated[Session, Depends(get_session)]) -> DBEvent:
    """
    Retrieve a single event
    """
    event = get_dbevent(id, db)
    if event is None:
        raise HTTPException(status_code=404, detail=f"No product found with id {id}")
    return event


# Order matters here. If we put this above get_event() then
# this will always get called even if the client passes in an ID
# this API is also mentioned in catalog.html
@app.get("/events", response_model=list[Event])
def get_events(db: Annotated[Session, Depends(get_session)]) -> list[DBEvent]:
    """
    Retrieve a list of events
    """
    events = get_all_dbevents(db)
    return events


# We want to serve static files from the file system directly and mount the
# folder at URL "/"
# This should come LAST after all the endpoints have been defined in this class,
# since this is a catchall. If we put this first, then any incoming requests
# will always match this, preventing any other endpoints from working
app.mount("/", StaticFiles(directory=PROJECT_ROOT / "static", html=True))
