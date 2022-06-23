"""Tests for the Item class"""

import calc


def test_item_creation() -> None:
    """Test the creation of an Item object"""
    stick_item = calc.Item(name="Stick", source="Minecraft")
    assert stick_item.name_with_source() == "Stick (Minecraft)"

def test_item_info() -> None:
    """Test the info method of an Item object"""
    stick_item = calc.Item(name="Stick", source="Minecraft")
    stick_info = stick_item.info()
    assert "Item name: Stick" in stick_info
    assert "Item source: Minecraft" in stick_info
