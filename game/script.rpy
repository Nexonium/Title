
define v = Character("Vasya")

define inventory = []

label receive_item(received_item):
    $ inventory.append(received_item)
    return

label give_item(given_item):
    $ inventory.remove(given_item)
    return

init python:

    def add_item(item: Item):
        # Check if it's a unique item and if there's another unique items in inventory
        if hasattr(item, "unique") and item.unique and any(
            hasattr(object, "unique") and object.unique for object in inventory):
            return
        inventory.append(item)

    def remove_item(item):
        inventory.remove(item)

    class ItemStat:
 
        def __init__(self, name: str, value: int):
            self.name = name
            self.value = value


    class Item:

        def __init__(self, name: str, description: str, value: int = 1):
            self.name = name
            self.description = description
            self.value = value

        def __str__(self):
            return f"{self.name} ({self.description}): {self.value}"


    class StackableItem(Item):

        def __init__(self, name: str, description: str, value: int, count: int):
            super().__init__(name, description, value)
            self.count = count


    class StatItem(Item):

        def __init__(self, name: str, description: str, value: int, stat: ItemStat):
            super().__init__(name, description, value)
            self.stat = stat


    class UniqueItem(Item):

        def __init__(self, name: str, description: str, value: int, stat: ItemStat):
            super().__init__(name, description, value)
            self.stat = stat
            self.unique = True
    

# The game starts here.

label start:

    scene bg room

    show vasya 

    v "Ну здарова"
    
    v "Не узнал меня?"

    return

