from unittest.mock import patch, MagicMock
from requests import Session
import pytest
from jobo_scraper import JoboScraping
from tests import (
    JOBO_WEBPAGE_WITHOUT_EVENTS,
    JOBO_LOGIN,
    JOBO_WEBPAGE_WITH_EVENT,
    JOBO_WEBPAGE_BROKEN,
)


@patch.object(Session, "post")
@patch.object(Session, "get")
def test_return_available_event(mock_session_get, mock_session_post):
    login = MagicMock()
    login.content = JOBO_LOGIN
    events = MagicMock()
    events.content = JOBO_WEBPAGE_WITH_EVENT

    mock_session_get.side_effect = [login, events]

    jobo = JoboScraping("test@test.com", "testpassword")
    result = jobo.get_list_of_events()

    assert result
    event = list(result.values())[0]
    assert (
        event.get("title")
        and event.get("image")
        and event.get("place")
        and event.get("link")
        and event.get("days")
        and event.get("description")
    )
    assert mock_session_get.called
    assert mock_session_get.call_count == 2
    assert mock_session_post.called


@patch.object(Session, "post")
@patch.object(Session, "get")
def test_return_empty_list_of_events(mock_session_get, mock_session_post):
    login = MagicMock()
    login.content = JOBO_LOGIN
    events = MagicMock()
    events.content = JOBO_WEBPAGE_WITHOUT_EVENTS

    mock_session_get.side_effect = [login, events]

    jobo = JoboScraping("test@test.com", "testpassword")
    result = jobo.get_list_of_events()

    assert result == {}
    assert mock_session_get.called
    assert mock_session_get.call_count == 2
    assert mock_session_post.called


@patch.object(Session, "get")
def test_fail_login(mock_session_get):
    login = MagicMock()
    login.content = "test_to_fail"

    mock_session_get.return_value = login

    jobo = JoboScraping("test@test.com", "testpassword")
    with pytest.raises(TypeError):
        jobo.get_list_of_events()

    assert mock_session_get.called
    assert mock_session_get.call_count == 4


@patch.object(Session, "post")
@patch.object(Session, "get")
def test_bad_events_webpage(mock_session_get, mock_session_post):
    login = MagicMock()
    login.content = JOBO_LOGIN
    events = MagicMock()
    events.content = JOBO_WEBPAGE_BROKEN

    mock_session_get.side_effect = [login, events]

    jobo = JoboScraping("test@test.com", "testpassword")
    result = jobo.get_list_of_events()

    assert result
    assert result.get("scraping_error")
