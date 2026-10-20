"""Web-layer tests for the simple Flask interface."""

import pytest

from app import app


@pytest.fixture()
def client():
    app.config.update(TESTING=True)
    with app.test_client() as test_client:
        yield test_client


def test_home_page_includes_search_and_staff_fallback(client):
    response = client.get("/")
    page = response.get_data(as_text=True)

    assert response.status_code == 200
    assert 'name="item"' in page
    assert "When in doubt, ask building staff." in page


def test_found_item_shows_bin_and_citation(client):
    page = client.post("/", data={"item": "plastic bottle"}).get_data(as_text=True)

    assert "Use the Recycling bin" in page
    assert "HKU Recycling Guide p.2" in page


def test_synonym_uses_the_same_bin_and_citation(client):
    page = client.post("/", data={"item": "Pop Can!"}).get_data(as_text=True)

    assert "Use the Recycling bin" in page
    assert "HKU Recycling Guide p.2" in page


def test_condition_prompt_offers_the_recorded_branches(client):
    page = client.post("/", data={"item": "pizza box"}).get_data(as_text=True)

    assert "needs a condition check" in page
    assert 'value="clean"' in page
    assert 'value="greasy"' in page
    assert "Use Compost" in page
    assert "Use Trash" in page


@pytest.mark.parametrize(
    ("choice", "expected_bin"),
    [("clean", "Compost"), ("greasy", "General waste")],
)
def test_condition_choice_returns_the_selected_bin(client, choice, expected_bin):
    page = client.post(
        "/",
        data={"item": "pizza box", "condition_option": choice},
    ).get_data(as_text=True)

    assert f"Use the {expected_bin} bin" in page
    assert "HKU Recycling Guide p.3" in page


def test_hazardous_item_is_refused_with_contact(client):
    page = client.post("/", data={"item": "battery"}).get_data(as_text=True)

    assert "Special handling required" in page
    assert "chemical@hku.hk" in page


def test_conditional_hazardous_branch_is_refused_with_contact(client):
    page = client.post(
        "/",
        data={"item": "glass bottle", "condition_option": "broken"},
    ).get_data(as_text=True)

    assert "Special handling required" in page
    assert "chemical@hku.hk" in page


def test_unknown_item_is_refused_without_a_bin(client):
    page = client.post("/", data={"item": "unknown thing"}).get_data(as_text=True)

    assert "We won’t guess this one" in page
    assert "Use the" not in page


def test_empty_json_or_empty_form_input_is_handled(client):
    page = client.post("/", data={"item": "   "}).get_data(as_text=True)

    assert "Enter an item to get started" in page
