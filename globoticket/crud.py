from sqlalchemy import select
from sqlalchemy.orm import Session

from globoticket.models import DBEvent


# we're isolating these db calls to its own file so that unit testing will be easier
# via mocking
def get_dbevent(id: int, db: Session) -> DBEvent | None:
    return db.get(DBEvent, id)


def get_all_dbevents(db: Session) -> list[DBEvent]:
    return db.execute(select(DBEvent)).scalars()
