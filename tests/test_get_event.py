from unittest.mock import patch

import pytest
from fastapi import HTTPException

from globoticket.api import get_event
from globoticket.models import DBEvent


# this @patch decorator will replace the get_dbevent identifier in globoticket.api
# with a mock object.
# return_value is what will be returned when the mocked function is called
# You can return a dict, a string, whatever you want.
@patch("globoticket.api.get_dbevent", return_value=DBEvent())
# mock_get_dbevent is the actual mock object that's created and assigned
# by the patch decorator
def test_get_event(mock_get_dbevent):
    """Return the event found in the database"""
    assert get_event(id=36, db="Fake db") is mock_get_dbevent.return_value
    # tests to make sure the function was called correctly
    # this does this by spying on the mock_get_dbevent object and asking it
    # how it was called
    mock_get_dbevent.assert_called_with(36, "Fake db")


@patch("globoticket.api.get_dbevent", return_value=None)
# we add an underscore in the function argument because the patch decorator
# will still try to pass the mocked object it creates to the function as an
# argument and will raise an error if we leave it empty. So putting an
# underscore there says that we do take an argument, but we'll ignore it
def test_get_event_404(_):
    """Raise HTTPException when no event is found."""
    # we want an exception to be raised when we request for an event that doesn't
    # exist in the database
    with pytest.raises(HTTPException):
        get_event(id=0, db=None)


# This is an integration test, where the function we're testing is ran in the
#   context of FastAPI which will do real DB calls to a test database
# The client points to a fixture named 'client' that we defined in conftest.py
def test_client_get_event_1(client):
    """Call get_event using the client, retrieving event 1"""
    # TestClient will send a request to FastAPI, which will call our function,
    # inject the DB, etc.
    response = client.get("/events/1")
    assert response.status_code == 200
    assert response.json() == {
        "date": "2024-05-01",
        "id": 1,
        "price": "5.5000000000",
        "product_code": "123456",
        "artist": "Two Story Zori",
        "content": "An awesome band!",
        "image": "tsz.png",
        "name": "Ready to Rock!",
    }


def test_client_get_event_404(client):
    """Call get_event with a non-existent ID"""
    response = client.get("/events/1987")
    assert response.status_code == 404
