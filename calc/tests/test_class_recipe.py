"""Tests for the Recipe class"""

import logging

import calc


def test_probabilistic_recipe_key(recipe_sand_pulverizer_secondary: calc.Recipe) -> None:
    """Test the key of a Recipe with a probabilistic component"""
    logging.debug("Recipe to produce sand as a probabilistic output using the Pulverizer:\n%s",
                  recipe_sand_pulverizer_secondary.key())
    expected_result = "1 Cobblestone (Minecraft) + 320 Minecraft Joules (BuildCraft) + "
    expected_result += "1 (nc) Pulverizer (Thermal Foundation) = 1 Gravel (Minecraft) + "
    expected_result += "0.1 (p) Sand (Minecraft)"
    assert recipe_sand_pulverizer_secondary.key() == expected_result


def test_recipe_component_deduplication(recipe_stick: calc.Recipe,
                                        component_plank_reactant: calc.Reactant) -> None:
    """Ensure that duplicate RecipeComponents can't be registered in a recipe"""
    assert len(recipe_stick.reactants) == 1
    recipe_stick.register_component(component=component_plank_reactant)
    assert len(recipe_stick.reactants) == 1


def test_recipe_creation(item_stick: calc.Item, item_plank: calc.Item) -> None:
    """Test the creation of a Recipe object"""
    plank_component = calc.Reactant(item=item_plank, quantity=2)
    stick_component = calc.Product(item=item_stick, quantity=4)
    stick_recipe = calc.Recipe()
    stick_recipe.register_component(plank_component)
    stick_recipe.register_component(stick_component)
    assert len(stick_recipe.reactants) == 1
    assert len(stick_recipe.products) == 1
    assert plank_component.key() in stick_recipe.reactants
    assert stick_component.key() in stick_recipe.products


def test_recipe_key(recipe_stick: calc.Recipe) -> None:
    """Test the key() method of the Recipe class."""
    logging.debug("Recipe for sticks: %s", recipe_stick.key())
    assert recipe_stick.key() == "2 Oak Planks (Minecraft) = 4 Sticks (Minecraft)"
