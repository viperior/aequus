"""Tests for the RecipeComponent class"""

import calc


def test_product_creation() -> None:
    """Test the creation of a Product object"""
    stick_item = calc.Item(name="Sticks", source="Minecraft")
    stick_product = calc.Product(item=stick_item, quantity=4)
    assert stick_product.info() == "Product: 4 Sticks"


def test_reactant_creation() -> None:
    """Test the creation of a Reactant object"""
    plank_item = calc.Item(name="Oak Planks", source="Minecraft")
    plank_reactant = calc.Reactant(item=plank_item, quantity=2)
    assert plank_reactant.info() == "Reactant: 2 Oak Planks"
