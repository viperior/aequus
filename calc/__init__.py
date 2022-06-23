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
    """This is the class used to represent Reactants and Products. It is the generic representation
    of a combination of an Item and a quantity. Whether something is a Product or Reactant depends
    on whether it is one of the inputs or outputs of a recipe. This can change based on context.

    Attributes:
    item (Item): The Item object
    quantity (float): The quantity of the item. It has a float data type to allow precise
        calculations and probabilistic quantities.
    component_type (str): The category of component (reactant or product)
    """

    def __init__(self, item: Item, quantity: float, component_type: str):
        self.item = item
        self.quantity = quantity
        self.component_type = component_type
        assert self.component_type in ["reactant", "product"] # Validate the component type

    def info(self) -> str:
        """Return the information about this recipe component."""
        return f"{self.component_type.capitalize()}: {self.text()}"

    def text(self) -> str:
        """Return a string with the quantity and item name"""
        return f"{self.quantity} {self.item.name}"
