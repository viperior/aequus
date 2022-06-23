# aequus

A recursive recipe calculator inspired by chemistry

## What is this for?

Aequus helps you calculate the total quantities of raw materials for recipes. The recipes can be simple or have dozens of ingredients. For ingredients that are themselves creatable, it can recurse through them until you arrive at a complete calculation of every raw material needed to create something.

"Aequus" is a Latin word that can mean "equal" or "like." This application draws inspiration from chemical equations because balancing chemical equations and complex recipes share many concepts.

You can use this program for cooking recipes in real life, crafting recipes in simulations or video games (like Minecraft), or anywhere recipes appear. It is designed in an abstract way to allow the definition of recipes of many kinds.

## How do I run it?

Calculate the total raw materials needed to create 16 sticks in Minecraft:

```bash
python -m calc product_name target_quantity [source_mod]
python -m calc stick 16
```

The source mod is only required if multiple items exist in the `ItemDatabase` sharing the same name.

```text
Product: Stick
Target quantity: 16

Bill of raw materials:
1 Log

Explanation:
1 Log = 4 Oak Planks = 16 Sticks
```

## Features

- Recursive calculation of raw materials
- Support for probabilistic ingredients (things created through a chance-based process)
- Define jobs to produce n quantity of an item and calculate the raw materials needed for the job
- Define multiple recipes per product

## Object model

| Entity | Definition | Example |
| ------ | ---------- | ------- |
| `Item` | Something that exists in a stable form, whether it can be made or gathered | Stick |
| `RecipeComponent` | A combination of an `Item` and a quantity | 2 Oak Planks |
| `Reactant` | A `RecipeComponent` that is used to create one or more `Products` | 2 Oak Planks |
| `Product` | A `RecipeComponent` that is created from one or more `Reactants` in a recipe | 4 Sticks |
| `Recipe` | A group of `Reactants` and `Products` | 2 Oak Planks = 4 Sticks |
| `Job` | A combination of a `Recipe` and a target quantity | Recipe: (2 Oak Planks = 4 Sticks), Target quantity: 12 |
| `ItemDatabase` | A collection of known `Items` | Stick, Button, Oak Planks |
| `RecipeDatabase` | A collection of `Recipes` associated with `Products` | Product: Stick, Recipe: 2 Oak Planks = 4 Sticks |
