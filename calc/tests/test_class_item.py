"""Tests for the Item class"""

import calc


def test_item_creation(item_stick: calc.Item) -> None:
    """Test the creation of an Item object"""
    assert item_stick.name_with_source() == "Sticks (Minecraft)"


def test_item_info(item_stick: calc.Item) -> None:
    """Test the info method of an Item object"""
    assert item_stick.info() == "Item name: Sticks\nItem source: Minecraft"
