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


def main() -> None:
    """The main function to execute when the calc module is called"""
    print("Hello world! I'm calc. Nice to meet you.")


if __name__ == "__main__":
    main()
