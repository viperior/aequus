"""Tests for the Item class"""

import calc


def test_item_creation() -> None:
    """Test the creation of an Item object"""
    stick_item = calc.Item(name="Stick", source="Minecraft")
    assert stick_item.name_with_source() == "Stick (Minecraft)"
