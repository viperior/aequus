"""Recipe calculator module"""

import logging


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
    is_probabilistic (bool): A bool indicating whether the product is probabilistic (chance-based),
        such as the 10% chance of creating Sand when pulverizing Cobblestone
    is_consumed (bool): A bool indicating whether the component is consumed upon execution of the
        recipe
    """
    def __init__(self, item: Item, quantity: float, component_type: str,
                 is_probabilistic: bool = False, is_consumed: bool = True):
        self.item = item
        self.quantity = quantity
        self.component_type = component_type
        assert self.component_type in ["reactant", "product"]  # Validate the component type
        self.is_probabilistic = is_probabilistic
        self.is_consumed = is_consumed

        # Only products can be probabilistic.
        if component_type == "reactant":
            assert not is_probabilistic

    def info(self) -> str:
        """Return the information about this recipe component."""
        return f"{self.component_type.capitalize()}: {self.text()}"

    def key(self) -> str:
        """Return a string that uniquely identifies this RecipeComponent object."""
        return self.text(include_source=True)

    def text(self, include_source: bool = False) -> str:
        """Return a string with the quantity and item name"""
        output_text = f"{self.quantity}"

        # Indicate that this component is probabilistic.
        if self.is_probabilistic:
            output_text += "(p)"

        output_text += " "

        if include_source:
            output_text += self.item.name_with_source()
        else:
            output_text += self.item.name

        return output_text


class Recipe:
    """A Recipe is a collection of one or more reactants and one or more products

    Attributes:
    reactants (dict): A dictionary of reactant-key-and-reactant-object pairs used to create the
        product(s)
    products (dict): A dictionary of product-key-and-product-object pairs created from the
        reactant(s)
    """
    def __init__(self) -> None:
        self.reactants = {}
        self.products = {}

    def key(self) -> None:
        """Return a string that uniquely identifies this Recipe object."""
        return f"{self.reactant_text()} = {self.product_text()}"

    def product_text(self) -> str:
        """Return a string describing the products created by this Recipe."""
        output_text = ""

        for index, component_key in enumerate(self.products):
            if index > 0:
                output_text += " + "

            output_text += self.products[component_key].key()

        return output_text

    def reactant_text(self) -> str:
        """Return a string describing the reactants used in this Recipe."""
        output_text = ""

        for index, component_key in enumerate(self.reactants):
            if index > 0:
                output_text += " + "

            output_text += self.reactants[component_key].key()

        return output_text

    def register_component(self, component: RecipeComponent) -> None:
        """Register a new reactant in the Recipe"""
        if component.component_type == "reactant":
            storage_target = self.reactants
        else:
            storage_target = self.products

        if component.key() in storage_target:
            logging.info("Cannot register new %s because it already exists in this recipe:\n\
                %s", component.component_type, component.key())
        else:
            storage_target[component.key()] = component
