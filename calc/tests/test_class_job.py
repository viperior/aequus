"""Tests for the Job class"""

import calc


def test_job_bill_of_materials_calculation_complex(job_stick: calc.Job) -> None:
    """Test the calculation of a BillOfMaterials for a Job to create 16 sticks"""
    job_stick.calculate_bill_of_materials()
    assert job_stick.materials_text() == "2 Oak Wood (Minecraft)"


def test_job_bill_of_materials_calculation_simple() -> None:
    """Test the calculation of a BillOfMaterials for a Job to create 16 sticks"""
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
