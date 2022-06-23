"""Tests for the RecipeComponent class"""

import pytest

import calc


def test_component_type_validation() -> None:
    """Test the data validation logic of the RecipeComponent.component_type attribute"""
    with pytest.raises(AssertionError):
        stick_item = calc.Item(name="Sticks", source="Minecraft")
        calc.RecipeComponent(item=stick_item, quantity=4, component_type="sneaky")


def test_product_creation() -> None:
    """Test the creation of a Product object"""
    stick_item = calc.Item(name="Sticks", source="Minecraft")
    stick_product = calc.RecipeComponent(item=stick_item, quantity=4, component_type="product")
    assert stick_product.info() == "Product: 4 Sticks"


def test_reactant_creation() -> None:
    """Test the creation of a Reactant object"""
    plank_item = calc.Item(name="Oak Planks", source="Minecraft")
    plank_reactant = calc.RecipeComponent(item=plank_item, quantity=2, component_type="reactant")
    assert plank_reactant.info() == "Reactant: 2 Oak Planks"
