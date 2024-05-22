import decimal
from datetime import date
from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declarative_base,
    mapped_column,
    reconstructor,
    relationship,
)

from globoticket.frontmatter import get_frontmatter

Base: DeclarativeBase = declarative_base()


class DBCategory(Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

    # this is a many-to-one relation, meaning several events
    # could be pointing to one category
    events: Mapped[List["DBEvent"]] = relationship(back_populates="category")


class DBEvent(Base):
    __tablename__ = "event"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_code: Mapped[str] = mapped_column(unique=True)
    date: Mapped[date]

    # this means that the row and category table that the foreign key points to
    # is represented not just in the foreign key, category_id, but also as an
    # actual DBCategory object in the category fields
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"))

    # By adding the lazy=joined option, this is ensuring that only one call is
    # being made to get the data if we don't add this, then SQL Alchemy
    # will do the default which is a lazy load.
    # They only get loaded when necessary, which in this case is when we
    # call to get category info in the string method
    # category: Mapped[DBCategory] = relationship(lazy="joined")

    # explicitly telling SQLAlchemy that the events field are represented
    # by the same foreign key in the database
    category: Mapped["DBCategory"] = relationship(back_populates="events")

    # chose decimal because:
    #   1. floating points might have rounding errors when performing calculations
    #   2. with ints, you cannot represent anything behind the comma
    #   3. decimals in python have infinite precision
    price: Mapped[decimal.Decimal]

    def __str__(self):
        return (
            f"{self.id}: {self.product_code: 10} "
            f"{self.category.name: 10} {self.date} ${self.price}"
        )

    # tells sqlalchemy to run this function whenever it reads an object
    #   from the database
    @reconstructor
    def _get_frontmatter(self):
        # get the dict with data from the corresponding frontmatter file
        frontmatter = get_frontmatter(self.product_code)
        for k, v in frontmatter.items():
            # if the db entry does not have an attribute with that name yet
            # this does NOT override any entry currently in the DB, like price
            if not hasattr(self, k):
                # set an attribute
                setattr(self, k, v)


# # temporary, for testing
# session = SessionLocal()
#
# # scalars turn the sqlalchemy results from the sql query into actual
# # dbcategory python objects
# results = session.execute(select(DBCategory)).scalars()
# print("\n".join(category.name for category in results))

# results_categories = session.execute(select(DBCategory)).scalars()
# print("\n".join(f"{category.name}: {len(category.events)} events"
#                 for category in results_categories))

# results_events = session.execute(select(DBEvent)).scalars()
# print("\n".join(str(event) for event in results_events))
