

# The game starts here.

label start:
    
    call variables
    call functions

    scene bg room

    show vasya 

    v "Ну здарова"
    
    v "Не узнал меня?"

    label inventory_loop:
        $ inventory_string = inventory.contains()
        "У меня в инвентаре: \n[inventory_string]"

    menu:
    
        "Взять исчислимый предмет в количестве от 1 до 10 штук (число и предмет случайны)":
            $ random_amount = random.randrange(1, 10)
            $ taken_item = StackableItem("Stone", random_number, 1, "Just a stone")
            $ inventory.add_item(taken_item)
            "%(random_number)d предме[lexicon_ending] добавлено в инвентарь!"
            jump inventory_loop
        "Взять новый случайный одиночный предмет со случайными статами":
            $ taken_item = StatItem("Sword", "Solid straight sword", 10, ItemStat("Strenght", 5))
            $ inventory.add_item(taken_item)
            "Вы взяли [taken_item.name] с характеристиками [taken_item.stat.value] [taken_item.stat.name] и стоимостью [taken_item.value]"
            jump inventory_loop
        "Взять случайный уникальный предмет":
            $ taken_item = UniqueItem("Varezhka", "A powerful mitten", 100, ItemStat("Strenght", 10))
            $ is_unique_in_inventory = inventory.add_item(taken_item)
            if is_unique_in_inventory:
                "У вас уже есть уникальный предмет в инвентаре!"
            else:
                "Вы взяли уникальный предмет [taken_item.name] с характеристиками [taken_item.stat.value] [taken_item.stat.name] и стоимостью [taken_item.value]"
            jump inventory_loop
        "Отдать исчислимый предмет в количестве от 1 до 10 штук (случайно)":
            $ random_amount = random.randrange(1, 10)
            
    return



label variables:
    $ v = Character("Vasya")
    $ inventory = Inventory()
    $ random_number = random.randrange(1, 10)
    $ lexicon_ending = "т" if random_number == 1 else "та" if random_number < 5 else "тов"
    $ items_data = {
        "stackable_items": {
            "Stone": {
                "name": "Stone",
                "description": "Just a stone",
                "value": 1
            },
            "Branch": {
                "name": "Branch",
                "description": "A branch",
                "value": 5
            },
            "Arrow": {
                "name": "Arrow",
                "description": "A handy arrow",
                "value": 15
            }
        },
        "stat_items": {
            "Sword": {
                "name": "Sword",
                "description": "Solid straight sword",
                "value": 10,
                "stat": ItemStat("Strength", 5)
            },
            "Staff": {
                "name": "Staff",
                "description": "Staff which handy for a wizards, Harry",
                "value": 10,
                "stat": ItemStat("Intelligence", 5)
            },
            "Bow": {
                "name": "Bow",
                "description": "Bow",
                "value": 10,
                "stat": ItemStat("Agility", 5)
            }
        },
        "unique_items": {
            "Varezhka": {
                "name": "Varezhka",
                "description": "A powerful mitten",
                "value": 100,
                "stat": ItemStat("Strength", 10)
            },
            "Samovar": {
                "name": "Samovar",
                "description": "Fabulous teapot with ornaments",
                "value": 200,
                "stat": ItemStat("Intelligence", 20)
            },
            "Matryoshka": {
                "name": "Nested dolls that somehow make you thinner",
                "description": "",
                "value": 250,
                "stat": ItemStat("Agility", 25)
            }
        }
    }
    $ items_stat_data = {
        "Strength": {
            "name": "Strength"
        },
        "Agility": {
            "name": "Agility"
        },
        "Intelligence": {
            "name": "Intelligence"
        },
        "Luck": {
            "name": "Luck"
        }
    }

label functions:

    init python:
        
        ######
        # Inventory functions
        ######

        import random

        class ItemStat:
    
            def __init__(self, name: str, value: int):
                # if items_data.name == name:
                self.name = name
                self.value = value
                # else:
                #     return "There's no such attribute!"


        class Item:

            def __init__(self, name: str, description: str = "", value: int = 1):
                self.name = name
                self.description = description
                self.value = value

            def __str__(self):
                if hasattr(self, "amount"):
                    return f"{self.name} ({self.description}) value: {self.value}, amount: {self.amount}"
                if hasattr(self, "stat"):
                    return f"{self.name} ({self.description}) value: {self.value}, stat: {self.stat.value} {self.stat.name}"
                return f"{self.name} ({self.description}) value: {self.value}"


        class StackableItem(Item):

            def __init__(self, name: str, amount: int, value: int, description: str) :
                super().__init__(name, description, value)
                self.amount = amount


        class StatItem(Item):

            def __init__(self, name: str, description: str, value: int, stat: ItemStat):
                super().__init__(name, description, value)
                self.stat = stat


        class UniqueItem(Item):

            def __init__(self, name: str, description: str, value: int, stat: ItemStat):
                super().__init__(name, description, value)
                self.stat = stat
                self.unique = True
        
        class Inventory(object):

            def __init__(self):
                self.items = []
                # self.gold = 0

            def add_item(self, item: Item):
                if isinstance(item, UniqueItem) and item.unique and any(
                    hasattr(object, "unique") and object.unique
                    for object in inventory.items):
                    return True
                if isinstance(item, StackableItem) and any(obj.name == item.name
                                                        for obj in self.items):
                    added_item = self.get_item(item.name)
                    added_item.amount += item.amount
                    return True
                self.items.append(item)

            def remove_item(self, item: Item):
                self.items.remove(item)

            def get_item(self, item_name: str):
                for item in self.items:
                    if item.name == item_name:
                        return item

            def contains(self):
                result = "Пусто" if not self.items else ""
                for item in self.items:
                    result += (str(item) + "\n")
                return result
