"""Pytest fixtures"""

import pytest

import calc


@pytest.fixture(name="component_plank_reactant")
def fixture_component_plank_reactant(item_plank: calc.Item) -> calc.RecipeComponent:
    """Return a test RecipeComponent object representing the Oak Planks items used in the Sticks
    Recipe.
    """
    return calc.RecipeComponent(item=item_plank, quantity=2, component_type="reactant")


@pytest.fixture(name="component_stick_product")
def fixture_component_stick_product(item_plank: calc.Item) -> calc.RecipeComponent:
    """Return a test RecipeComponent object representing the Sticks items created by the Sticks
    Recipe.
    """
    return calc.RecipeComponent(item=item_plank, quantity=4, component_type="product")


@pytest.fixture(name="item_plank")
def fixture_item_plank() -> calc.Item:
    """Return a test Item object representing an Oak Planks Item."""
    return calc.Item(name="Oak Planks", source="Minecraft")


@pytest.fixture(name="item_stick")
def fixture_item_stick() -> calc.Item:
    """Return a test Item object representing a Sticks Item."""
    return calc.Item(name="Sticks", source="Minecraft")


@pytest.fixture(name="recipe_stick")
def fixture_recipe_stick(component_plank_reactant: calc.RecipeComponent,
                         component_stick_product: calc.RecipeComponent) -> calc.Recipe:
    """Return a test Recipe object representing the Recipe to create Sticks from Oak Planks."""
    recipe_stick = calc.Recipe()
    recipe_stick.register_component(component_plank_reactant)
    recipe_stick.register_component(component_stick_product)

    return recipe_stick
