"""Tests for the Product class"""

import calc


def test_product_creation() -> None:
    """Test the creation of a Product object"""
    stick_item = calc.Item(name="Sticks", source="Minecraft")
    stick_product = calc.Product(item=stick_item, quantity=4)
    assert stick_product.info() == "Product: 4 Sticks"
