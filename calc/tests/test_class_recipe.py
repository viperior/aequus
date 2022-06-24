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


def test_recipe_component_deduplication(recipe_stick: calc.Recipe,
                                        component_plank_reactant: calc.RecipeComponent) -> None:
    """Ensure that duplicate RecipeComponents can't be registered in a recipe"""
    assert len(recipe_stick.reactants) == 1
    recipe_stick.register_component(component=component_plank_reactant)
    assert len(recipe_stick.reactants) == 1
