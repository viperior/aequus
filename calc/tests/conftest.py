"""Pytest fixtures"""

import pytest

import calc


@pytest.fixture(name="component_plank")
def fixture_component_plank(item_plank: calc.Item) -> calc.RecipeComponent:
    """Return a test RecipeComponent object representing the Oak Planks items used in the Sticks
    Recipe.
    """
    return calc.RecipeComponent(item=item_plank, quantity=2, component_type="reactants")


@pytest.fixture(name="component_stick")
def fixture_component_stick(item_plank: calc.Item) -> calc.RecipeComponent:
    """Return a test RecipeComponent object representing the Sticks items created by the Sticks
    Recipe.
    """
    return calc.RecipeComponent(item=item_plank, quantity=4, component_type="products")


@pytest.fixture(name="item_plank")
def fixture_item_plank() -> calc.Item:
    """Return a test Item object representing an Oak Planks Item."""
    return calc.Item(name="Oak Planks", source="Minecraft")


@pytest.fixture(name="item_stick")
def fixture_item_stick() -> calc.Item:
    """Return a test Item object representing a Sticks Item."""
    return calc.Item(name="Sticks", source="Minecraft")
