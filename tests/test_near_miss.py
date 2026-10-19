"""Near-miss items: similar names must be refused, and must route to different contacts."""

import csv
import os

import pytest

from lookup import lookup_bin

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HAZARDS_CSV = os.path.join(BASE_DIR, "data", "hazardous_items.csv")


def load_hazard_contacts():
    with open(HAZARDS_CSV, encoding="utf-8", newline="") as f:
        return {row["item"]: row["contact"] for row in csv.DictReader(f)}


def test_near_miss_set_is_not_empty():
    contacts = load_hazard_contacts()
    for item in ("battery", "car battery", "laptop battery", "phone battery"):
        assert item in contacts, f"{item} missing from hazardous_items.csv"


def test_battery_and_car_battery_are_both_refused():
    assert lookup_bin("battery")["status"] == "refused"
    assert lookup_bin("car battery")["status"] == "refused"


def test_battery_and_car_battery_route_to_different_contacts():
    contacts = load_hazard_contacts()
    battery_result = lookup_bin("battery")
    car_battery_result = lookup_bin("car battery")

    assert contacts["battery"] != contacts["car battery"]
    assert contacts["battery"] in battery_result["message"]
    assert contacts["car battery"] in car_battery_result["message"]
    assert battery_result["message"] != car_battery_result["message"]


@pytest.mark.parametrize("item", ["battery", "car battery", "laptop battery", "phone battery", "syringe"])
def test_every_battery_family_item_is_refused_with_its_own_contact(item):
    contacts = load_hazard_contacts()
    result = lookup_bin(item)

    assert result["status"] == "refused"
    assert result["bin"] is None
    assert contacts[item] in result["message"]


def test_battery_variants_do_not_collapse_into_one_channel():
    """"battery" must not answer for "car battery" - the routing is name-exact."""
    contacts = load_hazard_contacts()
    battery_contact = contacts["battery"]
    car_battery_contact = contacts["car battery"]
    laptop_contact = contacts["laptop battery"]

    assert battery_contact != car_battery_contact
    assert battery_contact != laptop_contact
    # laptop and phone batteries legitimately share the IT e-waste channel
    assert laptop_contact == contacts["phone battery"]

    for item, expected in (
        ("battery", battery_contact),
        ("car battery", car_battery_contact),
        ("laptop battery", laptop_contact),
    ):
        assert expected in lookup_bin(item)["message"]
        assert battery_contact not in lookup_bin(item)["message"] or item == "battery"
