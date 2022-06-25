"""Tests for the Job class"""

import logging

import calc


def test_job_bill_of_materials_calculation_complex(job_stick: calc.Job) -> None:
    """Test the calculation of a bill of materials for a Job to create 16 Sticks"""
    recipe_oak_planks = calc.Recipe()
    recipe_oak_planks.register_component(
        calc.Reactant(
            item=calc.Item(
                name="Oak Wood",
                source="Minecraft"
            ),
            quantity=1
        )
    )
    recipe_oak_planks.register_component(
        calc.Product(
            item=calc.Item(
                name="Oak Planks",
                source="Minecraft"
            ),
            quantity=4
        )
    )
    job_stick.register_recipe_database(
        {
            "Oak Planks (Minecraft)": recipe_oak_planks
        }
    )
    job_stick.calculate_bill_of_materials()
    assert job_stick.materials_text() == "2 Oak Wood (Minecraft)"


def test_job_bill_of_materials_calculation_simple() -> None:
    """Test the calculation of a bill of materials for a Job to create 1 Button"""
    recipe_button = calc.Recipe()
    recipe_button.register_component(
        calc.Reactant(
            item=calc.Item(
                name="Cobblestone",
                source="Minecraft"
            ),
            quantity=1
        )
    )
    recipe_button.register_component(
        calc.Product(
            item=calc.Item(
                name="Button",
                source="Minecraft"
            ),
            quantity=1
        )
    )
    job_button = calc.Job(
        desired_item=calc.Item(
            name="Button",
            source="Minecraft"
        ),
        target_quantity=1,
        recipe=recipe_button
    )
    job_button.calculate_bill_of_materials()
    assert job_button.materials_text() == "1 Cobblestone (Minecraft)"


def test_job_creation(item_stick: calc.Item, recipe_stick: calc.Recipe) -> None:
    """Test the creation of a Job object."""
    job_stick = calc.Job(
        desired_item=item_stick,
        target_quantity=16,
        recipe=recipe_stick
    )
    expected_text = "Job:\n\tDesired item: Sticks\n\tTarget quantity: 16\n\tTop-level recipe: "
    expected_text += "2 Oak Planks (Minecraft) = 4 Sticks (Minecraft)"
    assert job_stick.key() == expected_text


def test_job_repeating_material() -> None:
    """Test a Job that uses the same material at multiple levels of the recipe hierarchy to ensure
    test coverage of the material combination logic defined in the Job class.
    """
    item_tin_item_casing = calc.Item(
        name="Tin Item Casing",
        source="IndustrialCraft 2"
    )
    item_coil = calc.Item(
        name="Coil",
        source="IndustrialCraft 2"
    )
    item_iron_ingot = calc.Item(
        name="Iron Ingot",
        source="Minecraft"
    )
    item_electric_motor = calc.Item(
        name="Electric Motor",
        source="IndustrialCraft 2"
    )
    recipe_electric_motor = calc.Recipe()
    recipe_electric_motor.register_component(
        calc.Reactant(
            item=item_tin_item_casing,
            quantity=2
        )
    )
    recipe_electric_motor.register_component(
        calc.Reactant(
            item=item_coil,
            quantity=2
        )
    )
    recipe_electric_motor.register_component(
        calc.Reactant(
            item=item_iron_ingot,
            quantity=1
        )
    )
    recipe_electric_motor.register_component(
        calc.Product(
            item=item_electric_motor,
            quantity=1
        )
    )
    job_electric_motor = calc.Job(
        desired_item=item_electric_motor,
        target_quantity=1,
        recipe=recipe_electric_motor
    )
    job_electric_motor.calculate_bill_of_materials()
    assert "Iron Ore (Minecraft)" in job_electric_motor.materials
    assert "Tin Ore (Thermal Foundation)" in job_electric_motor.materials
    assert "Copper Ore (Thermal Foundation)" in job_electric_motor.materials
    assert job_electric_motor.materials["Iron Ore (Minecraft)"]["quantity"] == 3
    assert job_electric_motor.materials["Tin Ore (Thermal Foundation)"]["quantity"] == 1
    assert job_electric_motor.materials["Copper Ore (Thermal Foundation)"]["quantity"] == 5.333


def test_job_recipe_database_registration(recipe_sand_pulverizer_secondary: calc.Recipe) -> None:
    """Test the registration of a recipe database for a Job object."""
    item_glass = calc.Item(
        name="Glass",
        source="Minecraft"
    )
    recipe_glass = calc.Recipe()
    recipe_glass.register_component(
        calc.Reactant(
            item=calc.Item(
                name="Sand",
                source="Minecraft"
            ),
            quantity=1
        )
    )
    recipe_glass.register_component(
        calc.Reactant(
            item=calc.Item(
                name="Furnace",
                source="Minecraft"
            ),
            quantity=1,
            is_consumed=False
        )
    )
    recipe_glass.register_component(
        calc.Reactant(
            item=calc.Item(
                name="Coal",
                source="Minecraft"
            ),
            quantity=0.125
        )
    )
    recipe_glass.register_component(
        calc.Product(
            item=item_glass,
            quantity=1
        )
    )
    job_glass = calc.Job(
        desired_item=item_glass,
        target_quantity=1,
        recipe=recipe_glass
    )
    item_sand = calc.Item(
        name="Sand",
        source="Minecraft"
    )
    recipe_database = {item_sand.key(): recipe_sand_pulverizer_secondary}
    logging.debug("Glass job information:\n%s", job_glass.materials_text())
    job_glass.register_recipe_database(recipe_database=recipe_database)
    logging.debug("Recipe database for Sand recipe:\n%s", job_glass.recipe_database)
    item_key_sand = "Sand (Minecraft)"
    assert item_key_sand in job_glass.recipe_database.keys()
    assert isinstance(job_glass.recipe_database[item_key_sand], calc.Recipe)
