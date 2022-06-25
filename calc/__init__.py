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

    def __init__(self, name: str, source: str = "Unknown") -> None:
        self.name = name
        self.source = source

    def info(self) -> str:
        """Return all of the information about this item."""
        return f"Item name: {self.name}\nItem source: {self.source}"

    def key(self) -> str:
        """Return the item name and the source as a string"""
        return f"{self.name} ({self.source})"


class RecipeComponent:
    """This is the class used to represent a combination of an Item and a quantity.

    Attributes:
    item (Item): The Item object
    quantity (float): The quantity of the item. It has a float data type to allow precise
        calculations and probabilistic quantities.
    """
    def __init__(self, item: Item, quantity: float) -> None:
        self.item = item
        self.quantity = quantity

    def key(self) -> str:
        """Return a string that uniquely identifies this RecipeComponent object."""
        return self.text(include_source=True)

    def text(self, include_source: bool = False) -> str:
        """Return a string with the quantity and Item name."""
        output_text = f"{self.quantity} "

        if include_source:
            output_text += self.item.key()
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
            output_text += self.component.item.key()
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
            output_text += self.component.item.key()
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

    def is_valid(self) -> bool:
        """Return a Boolean value indicating whether this Recipe object is valid."""
        has_reactants = len(self.reactants) > 0
        has_products = len(self.products) > 0
        has_problem = not (has_reactants and has_products)

        if not has_reactants:
            logging.error("This Recipe contains no reactants!\nReactants:%s",
                          self.reactants)

        if not has_products:
            logging.error("This Recipe contains no products!\nProducts:%s",
                          self.products)

        if has_problem:
            logging.error("Invalid recipe information:\n%s", self.key())

        return has_reactants and has_products

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
        """Register a new Reactant or Product in the Recipe."""
        if isinstance(component, Reactant):
            storage_target = self.reactants
        else:
            storage_target = self.products

        if component.key() in storage_target:
            logging.info("Cannot register new %s because it already exists in this recipe:\n%s",
                         type(component), component.key())
        else:
            storage_target[component.key()] = component


class Job:
    """A Job consists of a desired item, a target quantity of that item to produce, a Recipe to use
    to create the desired item, and a BillOfMaterials that tracks the total raw materials needed to
    complete the Job.

    Attributes:
    desired_item (Item): The desired item to create through the Job
    target_quantity (float): The desired quantity of product to produce through the Job
    recipe (Recipe): The top-level Recipe to use to create the desired product
    """
    def __init__(self, desired_item: Item, target_quantity: float, recipe: Recipe) -> None:
        self.desired_item = desired_item
        self.target_quantity = target_quantity
        assert recipe.is_valid()
        self.recipe = recipe
        self.materials = {}
        self.initialize_materials()
        self.recipe_database = {}

    def calculate_bill_of_materials(self) -> None:
        """Calculate the total raw materials required to complete this Job."""
        # Track whether any materials were converted into their raw materials in the last iteration.
        expansion_performed = False
        iteration_count = 0

        while iteration_count == 0 or expansion_performed is True:
            logging.debug("Material expansion iteration #%d", iteration_count)
            logging.debug("Material expansion performed during last loop? = %s",
                          expansion_performed)
            logging.debug("Current materials at iteration start:\n%s", self.materials_text())

            # Create a temporary dictionary to store replaced materials.
            replacement_materials = {}

            # Begin each pass through the material list with the expansion sentry set to False.
            expansion_performed = False

            for material_key, material in self.materials.items():
                # Determine whether there is a Recipe with a Product matching the current material.
                if material_key in self.recipe_database:
                    logging.debug("A Recipe was found in the database for the material, %s",
                                  material_key)
                    matching_recipe = self.recipe_database[material_key]
                    logging.debug("Matching recipe:\n%s", matching_recipe.key())

                    # Expand the material using its matching Recipe.
                    # Isolate the Product in the matching recipe that matches the desired product
                    # for this material.
                    matching_recipe_product = None

                    for product in matching_recipe.products.values():
                        if product.component.item.key() == material_key:
                            matching_recipe_product = product
                            break

                    # Ensure that a matching product is found.
                    assert matching_recipe_product is not None and\
                        isinstance(matching_recipe_product, Product)

                    # Calculate the quantity modifier based on how many runs of the matching recipe
                    # are required to produce the target quantity for this material.
                    quantity_modifier = material["quantity"] /\
                        matching_recipe_product.component.quantity

                    # Add each Reactant from the matching Recipe with adjusted quantities to the
                    # collection replacement materials.
                    for reactant in matching_recipe.reactants.values():
                        additional_quantity = reactant.component.quantity * quantity_modifier
                        reactant_item_key = reactant.component.item.key()

                        if reactant_item_key in replacement_materials:
                            # Add to existing material if the material is already present.
                            logging.debug("Existing material, %s, quantity increasing by %f",
                                          reactant_item_key, additional_quantity)
                            logging.debug("Quantity BEFORE addition from replacement: %f",
                                          replacement_materials[reactant_item_key]["quantity"])
                            replacement_materials[reactant_item_key]["quantity"] +=\
                                additional_quantity
                            logging.debug("Quantity AFTER addition from replacement: %f",
                                          replacement_materials[reactant_item_key]["quantity"])
                        else:
                            # Create new material entry for newly identified materials.
                            logging.debug("Creating new material entry for new material, %s",
                                          reactant_item_key)
                            logging.debug("Quantity of new material = %f", additional_quantity)
                            replacement_materials[reactant_item_key] = {
                                "quantity": additional_quantity
                            }

                    expansion_performed = True
                else:
                    logging.debug("A Recipe was NOT found in the database for the material, %s",
                                  material_key)

                    # Add the unmodified material to the replacement material dictionary.
                    replacement_materials[material_key] = material

            if expansion_performed:
                self.materials = replacement_materials

            logging.debug("Current materials at iteration end:\n%s", self.materials_text())
            iteration_count += 1

    def initialize_materials(self) -> None:
        """Initialize the raw materials dictionary using the top-level recipe for this Job."""
        # Isolate the Product in the top-level recipe that matches the desired product for this Job.
        matching_recipe_product = None

        for product in self.recipe.products.values():
            if product.component.item.key() == self.desired_item.key():
                matching_recipe_product = product
                break

        # Ensure that a matching product is found
        assert matching_recipe_product is not None
        assert isinstance(matching_recipe_product, Product)

        # Calculate the quantity modifier based on how many runs of the recipe are required to
        # produce the target quantity for this Job.
        quantity_modifier = self.target_quantity / matching_recipe_product.component.quantity

        for reactant_key in self.recipe.reactants:
            reactant = self.recipe.reactants[reactant_key]
            self.materials[reactant.component.item.key()] = {
                "quantity": reactant.component.quantity * quantity_modifier
            }

    def key(self) -> str():
        """Return a string that uniquely identifies this Job."""
        output_text = f"Job:\n\tDesired item: {self.desired_item.name}\n\t"
        output_text += f"Target quantity: {self.target_quantity}\n\tTop-level recipe: "
        output_text += f"{self.recipe.key()}"

        return output_text

    def materials_text(self) -> str():
        """Return a string listing all the raw materials needed to complete this Job."""
        output_text = ""

        for index, material_key in enumerate(self.materials.keys()):
            if index > 0:
                output_text += " + "

            # Apply rounding to material quantities
            raw_quantity = self.materials[material_key]['quantity']
            rounded_quantity = int(raw_quantity)

            if raw_quantity == rounded_quantity:
                display_quantity = rounded_quantity
            else:
                display_quantity = raw_quantity

            output_text += f"{display_quantity} {material_key}"

        return output_text

    def register_recipe_database(self, recipe_database: dict) -> None:
        """Register a recipe database, which is a collection of item keys and their recipes."""
        self.recipe_database = recipe_database
