"""Recipe calculator module"""


class Item:
    """This is a class to represent items that exist in a stable form, whether it can be made or
    must be gathered from the natural world.

    Attributes:
    name (str): The name of the item
    source (str): The source of the item, to allow distinguishing between items from different
        sources
    """

    def __init__(self, name: str, source: str = "Unknown"):
        self.name = name
        self.source = source

    def info(self) -> str:
        """Return all of the information about this item."""
        return f"Item name: {self.name}\nItem source: {self.source}"

    def name_with_source(self) -> str:
        """Return the item name and the source as a string"""
        return f"{self.name} ({self.source})"


class RecipeComponent:
    """This is the parent class for Reactants and Products. It is the generic representation of a
    combination of an Item and a quantity.

    Attributes:
    item (Item): The Item object
    quantity (float): The quantity of the item. It has a float data type to allow precise
        calculations and probabilistic quantities.
    """

    def __init__(self, item: Item, quantity: float):
        self.item = item
        self.quantity = quantity

    def text(self) -> str:
        """Return a string with the quantity and item name"""
        return f"{self.quantity} {self.item.name}"


class Product(RecipeComponent):
    """This is the class for Products, which are recipe components created using one or more
    reactants.
    """
    def info(self) -> str:
        """Return the information about this product."""
        return f"Product: {self.text()}"


class Reactant(RecipeComponent):
    """This is the class for Reactants, which are recipe components used to create one or more
    products.
    """
    def info(self) -> str:
        """Return the information about this reactant."""
        return f"Reactant: {self.text()}"
