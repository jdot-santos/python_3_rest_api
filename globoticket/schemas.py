import datetime
import decimal

from pydantic import BaseModel


# This defines the structure of the JSON data we want our REST
#   endpoints to return.
# The Event class inherits from BaseModel, imported from pydantic
#   BaseModel is a quick way to define a class with some fields.
# Pydantic will validate that all the data has the correct types
#   and will generate documentation for us. We can also filter out
#   specific fields that we don't want the client to see in the output
class Event(BaseModel):
    id: int
    product_code: str
    date: datetime.date
    price: decimal.Decimal
    artist: str
    name: str
    content: str
    image: str
