"""Tests for the Reactant class"""

import calc


def test_reactant_creation() -> None:
    """Test the creation of a Reactant object"""
    plank_item = calc.Item(name="Oak Planks", source="Minecraft")
    plank_reactant = calc.Reactant(item=plank_item, quantity=2)
    assert plank_reactant.info() == "Reactant: 2 Oak Planks"
