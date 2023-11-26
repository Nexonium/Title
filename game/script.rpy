

# The game starts here.

label start:
    
    call functions
    call variables

    scene bg room

    show vasya 

    v "Ну здарова"
    
    v "Не узнал меня?"

    label inventory_loop:
        $ inventory_string = inventory.get_all_items()
        "У меня в инвентаре: \n[inventory_string]"

    menu:
    
        "Взять исчислимый предмет в количестве от 1 до 10 штук (число и предмет случайны)":
            $ random_number = renpy.random.randint(1, 10)
            $ lexicon = lexicon_ending(random_number)
            # $ sorted = get_sorted_items(items_data)
            # $ shuffled = get_random_shuffled(sorted)
            # $ random_item = get_random_item_from_list(shuffled)
            $ taken_item = get_random_item("stackable_items").copy()
            $ taken_item2 = get_random_item("stackable_items")
            $ taken_item3 = get_random_item("stackable_items")
            "А сейчас я тебе дам... [taken_item.name]"
            $ inventory.add_item(taken_item, random_number)
            "%(random_number)d предме[lexicon] добавлено в инвентарь!"
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
    $ renpy.store.random_number = renpy.random.randint(1, 10)
    $ items_data = renpy.store.dict()
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
    $ transformed_data = renpy.store.dict()
    $ transformed_data = transform_items_data(items_data)

label functions:

    init python:
        
        ######
        # Inventory functions
        ######

        import random

        ######################################################################################
        # Class realization
        ######################################################################################


        class ItemStat:

            def __init__(self, name: str, value: int):
                self.name = name
                self.value = value


        class Item:

            def __init__(self, name: str, description: str, value: int):
                self.name = name
                self.description = description
                self.value = value


        class StackableItem(Item):

            def __init__(self, name: str, description: str, value: int, amount: int = 1):
                super().__init__(name, description, value)
                self.amount = amount
            
            def copy(self):
                return StackableItem(self.name, self.description, self.value, self.amount)


        class StatItem(Item):

            def __init__(self, name: str, description: str, value: int, stat: ItemStat):
                super().__init__(name, description, value)
                self.stat = stat


        class UniqueItem(Item):

            def __init__(self, name: str, description: str, value: int, stat: ItemStat):
                super().__init__(name, description, value)
                self.stat = stat


        class Inventory:

            def __init__(self):
                self.items = []
                self.has_unique_item = False

            def add_item(self, item: Item, amount: int = 1):
                if isinstance(item, UniqueItem):
                    if not self.has_unique_item:
                        self.has_unique_item = True
                        self.items.append(item)
                    else:
                        return "You can't have more than one unique item"
                elif isinstance(item, StackableItem):
                    existing_item = next((i for i in self.items if i.name == item.name), None)
                    if existing_item:
                        existing_item.amount += amount
                    else:
                        item.amount = amount
                        self.items.append(item)
                else:
                    self.items.extend([item] * amount)

            def remove_item(self, item: Item, amount: int = 1):
                if isinstance(item, UniqueItem) and self.has_unique_item:
                    self.has_unique_item = False
                    self.items.remove(item)
                elif isinstance(item, StackableItem) and item in self.items:
                    item.amount -= amount
                    if item.amount <= 0:
                        self.items.remove(item)
                else:
                    for num in range(0, amount):
                        if item in self.items:
                            self.items.remove(item)

            def get_item(self, item: Item):
                if item in self.items:
                    return self.items[self.items.index(item)]
                else:
                    return None

            def get_all_items(self)->list:
                return self.items

            def sort_items(self, sort_by: str, reverse: bool = False):
                key_functions = {
                    "name": lambda x: x.name,
                    "value": lambda x: x.value,
                    "stat": lambda x: x.stat.value,
                    "type": lambda x: x.__class__.__name__
                }

                if sort_by in key_functions:
                    self.items.sort(key=key_functions[sort_by], reverse=reverse)
                
                return self.items
        

        ########
        # Let's assume our items data is packed in dictionary
        # We need to transform it to our Item class
        ########

        def transform_items_data(items_data):
            stackable_items = {}
            stat_items = {}
            unique_items = {}
            for item_type in items_data:
                for item_name in items_data[item_type]:
                    item_data = items_data[item_type][item_name]
                if item_type == "stackable_items":
                    stackable_items[item_name] = StackableItem(item_name,
                                                            item_data["description"],
                                                            item_data["value"])
                    continue
                if item_type == "stat_items":
                    stat_data = item_data["stat"]
                    stat_items[item_name] = StatItem(
                        item_name, item_data["description"], item_data["value"],
                        ItemStat(stat_data.name, stat_data.value))
                    continue
                if item_type == "unique_items":
                    stat_data = item_data["stat"]
                    unique_items[item_name] = UniqueItem(
                        item_name, item_data["description"], item_data["value"],
                        ItemStat(stat_data.name, stat_data.value))
                    continue
            return {
                "stackable_items": stackable_items,
                "stat_items": stat_items,
                "unique_items": unique_items
            }

        def get_transfromed_data_by_name(name):
            if name in transformed_data["stackable_items"]:
                return transformed_data["stackable_items"][name]
            if name in transformed_data["stat_items"]:
                return transformed_data["stat_items"][name]
            if name in transformed_data["unique_items"]:
                return transformed_data["unique_items"][name]
            return None

        def get_random_item(item_type: str):
            items = transformed_data.get(item_type).copy()
            sorted_items = list(items.values())
            random_shuffle(sorted_items)
            random_item = random.choice(sorted_items)
            return random_item

        def get_sorted_items(item_type:list):
            items = transformed_data.get(item_type).copy()
            sorted_items = list(items.values())
            return sorted_items

        def get_random_shuffled(item_list:list):
            random_list = item_list.copy()
            random_shuffle(random_list)
            return random_list

        def get_random_item_from_list(item_list:list):
            return random.choice(item_list)

        def random_shuffle(variable: list):
            renpy.random.shuffle(variable)
            return variable

        def lexicon_ending(number: int):
            return "т" if random_number == 1 else "та" if random_number < 5 else "тов"

        ####
        # Bonus:
        ####

        ######################################################################################
        # Dict realization
        ######################################################################################


        class InventoryDict:

            def __init__(self):
                self.items = []
                self.has_unique_item = False

            def add_item(self, item: dict, amount: int = 1):
                if item.get('unique'):
                    if not self.has_unique_item:
                        self.has_unique_item = True
                        self.items.append(item)
                    else:
                        print("You can't have more than one unique item")
                elif item.get('amount'):
                    if item not in self.items:
                        item['amount'] = amount
                        self.items.append(item)
                    else:
                        self.items[self.items.index(item)]['amount'] += amount
                else:
                    self.items.extend([item] * amount)

            def remove_item(self, item: dict, amount: int = 1):
                deleted_item = self.get_item(item)
                if deleted_item:
                    if deleted_item.get('unique'):
                        self.has_unique_item = False
                        self.items.remove(deleted_item)
                    if deleted_item.get('amount'):
                        deleted_item['amount'] -= amount
                        if deleted_item['amount'] <= 0:
                            self.items.remove(deleted_item)
                    else:
                        self.items.remove(deleted_item)

            def get_item(self, item: dict):
                item_name = item.get('name') if item else None
                return next((i for i in self.items
                            if i.get('name') == item_name), None) if item_name else None

            def get_all_items(self):
                return self.items
            
            def sort_items(self, sort_by="type", reverse=False):
                key_functions = {
                    "name": lambda x: x.get('name', ''),
                    "value": lambda x: x.get('value', 0),
                    "stat": lambda x: x.get('stat', {}).get('value', 0),
                    "type": lambda x: (1 if 'unique' in x else 0, 2 if 'stat' in x else 0, 3 if 'amount' in x else 0)
                }

                if sort_by in key_functions:
                    self.items.sort(key=key_functions[sort_by], reverse=reverse)

                return self.items


        # Oldy:
        #
        # class ItemStat:
    
        #     def __init__(self, name: str, value: int):
        #         # if items_data.name == name:
        #         self.name = name
        #         self.value = value
        #         # else:
        #         #     return "There's no such attribute!"


        # class Item:

        #     def __init__(self, name: str, description: str = "", value: int = 1):
        #         self.name = name
        #         self.description = description
        #         self.value = value

        #     def __str__(self):
        #         if hasattr(self, "amount"):
        #             return f"{self.name} ({self.description}) value: {self.value}, amount: {self.amount}"
        #         if hasattr(self, "stat"):
        #             return f"{self.name} ({self.description}) value: {self.value}, stat: {self.stat.value} {self.stat.name}"
        #         return f"{self.name} ({self.description}) value: {self.value}"


        # class StackableItem(Item):

        #     def __init__(self, name: str, amount: int, value: int, description: str) :
        #         super().__init__(name, description, value)
        #         self.amount = amount


        # class StatItem(Item):

        #     def __init__(self, name: str, description: str, value: int, stat: ItemStat):
        #         super().__init__(name, description, value)
        #         self.stat = stat


        # class UniqueItem(Item):

        #     def __init__(self, name: str, description: str, value: int, stat: ItemStat):
        #         super().__init__(name, description, value)
        #         self.stat = stat
        #         self.unique = True
        
        # class Inventory(object):

        #     def __init__(self):
        #         self.items = []
        #         # self.gold = 0

        #     def add_item(self, item: Item):
        #         if isinstance(item, UniqueItem) and item.unique and any(
        #             hasattr(object, "unique") and object.unique
        #             for object in inventory.items):
        #             return True
        #         if isinstance(item, StackableItem) and any(obj.name == item.name
        #                                                 for obj in self.items):
        #             added_item = self.get_item(item.name)
        #             added_item.amount += item.amount
        #             return True
        #         self.items.append(item)

        #     def remove_item(self, item: Item):
        #         self.items.remove(item)

        #     def get_item(self, item_name: str):
        #         for item in self.items:
        #             if item.name == item_name:
        #                 return item

        #     def contains(self):
        #         result = "Пусто" if not self.items else ""
        #         for item in self.items:
        #             result += (str(item) + "\n")
        #         return result
