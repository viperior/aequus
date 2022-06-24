"""Tests for the Recipe class"""

import calc


def test_recipe_creation(item_stick: calc.Item, item_plank: calc.Item) -> None:
    """Test the creation of a Recipe object"""
    plank_component = calc.RecipeComponent(item=item_plank, quantity=2, component_type="reactant")
    stick_component = calc.RecipeComponent(item=item_stick, quantity=4, component_type="product")
    stick_recipe = calc.Recipe()
    stick_recipe.register_component(plank_component)
    stick_recipe.register_component(stick_component)
    assert len(stick_recipe.reactants) == 1
    assert len(stick_recipe.products) == 1
    assert plank_component.key() in stick_recipe.reactants
    assert stick_component.key() in stick_recipe.products


def test_recipe_component_deduplication() -> None:
    """Ensure that duplicate RecipeComponents can't be registered in a recipe"""
    recipe = calc.Recipe()
    component = calc.RecipeComponent(
        item=calc.Item("Oak Planks", source="Minecraft"),
        quantity=2,
        component_type="reactant"
    )

    for _ in range(2):
        recipe.register_component(component=component)

    assert len(recipe.reactants) == 1
