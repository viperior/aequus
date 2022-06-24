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
    """This is the class used to represent a combination of an Item and a quantity.

    Attributes:
    item (Item): The Item object
    quantity (float): The quantity of the item. It has a float data type to allow precise
        calculations and probabilistic quantities.
    """
    def __init__(self, item: Item, quantity: float):
        self.item = item
        self.quantity = quantity

    def key(self) -> str:
        """Return a string that uniquely identifies this RecipeComponent object."""
        return self.text(include_source=True)

    def text(self, include_source: bool = False) -> str:
        """Return a string with the quantity and Item name."""
        output_text = f"{self.quantity} "

        if include_source:
            output_text += self.item.name_with_source()
        else:
            output_text += self.item.name

        return output_text


class Product:
    """This class is used to represent recipe outputs.

    Attributes:
    component (RecipeComponent): The combination of Item object and quantity
    is_probabilistic (bool): A bool indicating whether the product is probabilistic (chance-based),
        such as the 10% chance of creating Sand when pulverizing Cobblestone
    """
    def __init__(self, item: Item, quantity: float, is_probabilistic: bool = False) -> None:
        self.component = RecipeComponent(item=item, quantity=quantity)
        self.is_probabilistic = is_probabilistic

    def info(self) -> str:
        """Return the information about this Product."""
        return f"Product: {self.text()}"

    def key(self) -> str:
        """Return a string that uniquely identifies this Product object."""
        return self.text(include_source=True)

    def text(self, include_source: bool = False) -> str:
        """Return a string with the quantity and Item name."""
        output_text = f"{self.component.quantity} "

        # Indicate that this Product is probabilistic when applicable.
        if self.is_probabilistic:
            output_text += "(p) "

        if include_source:
            output_text += self.component.item.name_with_source()
        else:
            output_text += self.component.item.name

        return output_text


class Reactant:
    """This class is used to represent recipe inputs.

    Attributes:
    component (RecipeComponent): The combination of Item object and quantity
    is_consumed (bool): A bool indicating whether the component is consumed upon execution of the
        recipe
    """
    def __init__(self, item: Item, quantity: float, is_consumed: bool = True) -> None:
        self.component = RecipeComponent(item=item, quantity=quantity)
        self.is_consumed = is_consumed

    def info(self) -> str:
        """Return the information about this Reactant."""
        return f"Reactant: {self.text()}"

    def key(self) -> str:
        """Return a string that uniquely identifies this Reactant object."""
        return self.text(include_source=True)

    def text(self, include_source: bool = False) -> str:
        """Return a string with the quantity and Item name."""
        output_text = f"{self.component.quantity} "

        # Indicate that this Reactant is non-consumable when applicable.
        if not self.is_consumed:
            output_text += "(nc) "

        if include_source:
            output_text += self.component.item.name_with_source()
        else:
            output_text += self.component.item.name

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

    def register_component(self, component) -> None:
        """Register a new reactant in the Recipe"""
        if isinstance(component, Reactant):
            storage_target = self.reactants
        else:
            storage_target = self.products

        if component.key() in storage_target:
            logging.info("Cannot register new %s because it already exists in this recipe:\n%s",
                         type(component), component.key())
        else:
            storage_target[component.key()] = component
