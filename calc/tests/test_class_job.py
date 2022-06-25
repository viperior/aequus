"""Tests for the Job class"""

import calc


def test_job_creation(item_stick: calc.Item, recipe_stick: calc.Recipe) -> None:
    """Test the creation of a Job object."""
    job_stick = calc.Job(
        desired_product=item_stick,
        target_quantity=16,
        recipe=recipe_stick
    )
    expected_text = "Job:\n\tDesired product: Sticks\n\tTarget quantity: 16\n\tTop-level recipe: "
    expected_text += "2 Oak Planks (Minecraft) = 4 Sticks (Minecraft)"
    assert job_stick.key() == expected_text
