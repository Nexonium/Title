

# The game starts here.

label start:
    
    call functions
    call variables

    scene bg room

    show vasya 

    v "Ну здарова"
    v "Не узнал меня?"

    label inventory_loop:

        python:
            inventory_contains = inventory.get_all_items()

            inventory_string = ""
            for i, item in enumerate(inventory_contains, start=1):
                if isinstance(item, StackableItem):
                    inventory_string += f"[{item.amount} {item.name}]"
                elif isinstance(item, StatItem) or isinstance(item, UniqueItem):
                    stats_string = "".join([f"+{stat.value} {stat.name}" if stat.value > 0 else f"{stat.value} {stat.name}" for stat in item.stat])
                    inventory_string += f"[{stats_string} {item.name}]"
                if i < len(inventory_contains):
                    inventory_string += ", "
        
        "У меня в инвентаре:\n[inventory_string]"

    menu:

        "Взять исчислимый предмет в количестве от 1 до 10 штук (число и предмет случайны)":
            
            $ random_number = renpy.random.randint(1, 10)
            $ taken_item = get_random_item("stackable_items")

            v "Я тебе отдам... [random_number] [taken_item.name]"
            
            $ inventory.add_item(taken_item, random_number)

            "[random_number] [taken_item.name] добавлено в инвентарь!"
            
            jump inventory_loop

        "Взять новый случайный одиночный предмет со случайными статами":
            
            $ taken_item = get_random_item_with_random_stats()
            $ inventory.add_item(taken_item)
            $ string = f"Вы взяли |{taken_item.name}| c характеристиками "
            $ string += "".join([f"+{stat.value} {stat.name}" if stat.value > 0 else f"{stat.value} {stat.name}" for stat in taken_item.stat])
            
            "[string]!"
            jump inventory_loop

        "Взять случайный уникальный предмет":

            if inventory.has_unique_item:
                $ string = "У вас уже есть уникальный предмет в инвентаре"
            else:
                $ taken_item = get_random_item_with_random_stats("unique_items")
                $ inventory.add_item(taken_item)
                python:
                    string = f"Вы взяли *{taken_item.name}* c характеристиками "
                    for stat in taken_item.stat:
                        string += f"{'+' if stat.value > 0 else ''}{stat.value} {stat.name} "
            
            "[string]!"
            jump inventory_loop

        "Отдать исчислимый предмет в количестве от 1 до 10 штук (случайно)":

            $ random_number = renpy.random.randint(1, 10)
            $ random_item = inventory.get_random_item("stackable_items")

            v "Ну-ка..."

            python:
                string = ""
                if random_item:
                    if random_item.amount < random_number:
                        random_number = random_item.amount
                    inventory.remove_item(random_item, random_number)
                    string = f"Опс! {random_number} {random_item.name} отдали! Так и быть!"
                else:
                    string = "А у тебя ничего такого и нету! Растяпа..."

            v "[string]"
            jump inventory_loop

        "Отдать одиночный предмет (один из)":

            $ random_item = inventory.get_random_item("stat_items")
            
            v "Оп..."
            
            python:
                string = ""
                if random_item:
                    inventory.remove_item(random_item)
                    string = f"Хоба! Был |{random_item.name}| с "
                    for stat in random_item.stat:
                        string += f"{'+' if stat.value > 0 else ''}{stat.value} {stat.name} "
                    string += "а больше-то и нету! Вот так вот!"
                else:
                    string = "А у тебя ничего такого и нету! Растяпа..."
            
            v "[string]"
            jump inventory_loop

        "Отдать уникальный предмет":

            $ random_item = inventory.get_random_item("unique_items")
            
            v "Хммм..."
            
            python:
                string = ""
                if random_item != None:
                    inventory.remove_item(random_item, random_number)
                    string = f"Опаньки! Был *{random_item.name}* с "
                    for stat in random_item.stat:
                        string += f"{'+' if stat.value > 0 else ''}{stat.value} {stat.name} "
                    string += "а больше-то его и нету! Хорошая вещь была, конечно..."
                else:
                    string = "А у тебя ничего такого и нету! Растяпа..."
            
            v "%(string)s"
            jump inventory_loop

        "Выйти":

            return
        
    return


label variables:
    $ v = Character("Vasya")
    $ inventory = Inventory()
    $ random_number = renpy.random.randint(1, 10)
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
    $ transformed_data = transform_items_data(items_data)


label functions:

    init python:

        ######
        # Inventory functions
        ######

        import random

        # ######################################################################################
        # # Class realization
        # ######################################################################################


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

            def __init__(self, name: str, description: str, value: int, stat: ItemStat or list[ItemStat]):
                super().__init__(name, description, value)
                self.stat = stat if isinstance(
                    stat, list) else [stat] if isinstance(stat, ItemStat) else []

            def add_stat(self, stat: ItemStat):
                self.stat[
                    stat.
                    name].value += stat.value if stat.name in self.stat else stat.value

            def remove_stat(self, stat: ItemStat):
                self.stat.pop(stat.name, None)
            
            def copy(self):
                return StatItem(self.name, self.description, self.value, self.stat)


        class UniqueItem(Item):

            def __init__(self, name: str, description: str, value: int, stat: ItemStat or list[ItemStat]):
                super().__init__(name, description, value)
                self.stat = stat if isinstance(
                    stat, list) else [stat] if isinstance(stat, ItemStat) else []

            def add_stat(self, stat: ItemStat):
                self.stat[
                    stat.
                    name].value += stat.value if stat.name in self.stat else stat.value

            def remove_stat(self, stat: ItemStat):
                self.stat.pop(stat.name, None)
            
            def copy(self):
                return UniqueItem(self.name, self.description, self.value, self.stat)


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
                if item.name in self.items:
                    return self.items[self.items.index(item)]
                else:
                    return None

            def get_all_items(self)->list:
                return self.items
            
            def get_random_item(self, item_type: str):
                items_of_type = [item for item in self.items if isinstance(item, self.get_item_class(item_type))]
                if items_of_type:
                    return random.choice(items_of_type)
                else:
                    return None

            def get_item_class(self, item_type: str):
                if item_type == "stackable_items":
                    return StackableItem
                elif item_type == "stat_items":
                    return StatItem
                elif item_type == "unique_items":
                    return UniqueItem
                else:
                    return None

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

        def get_random_item(item_type: str)->obj:
            items = transformed_data.get(item_type).copy()
            sorted_items = list(items.values())
            random_shuffle(sorted_items)
            random_item = renpy.random.choice(sorted_items).copy()
            return random_item

        def random_shuffle(variable: list)->list:
            renpy.random.shuffle(variable)
            return variable

        def get_suffix(number: int)->str:
            return "а" if random_number < 5 and random_number > 1 else "ов"

        def get_random_stats(number_of_stats: int = random.randint(1, 2)):
            stat = set()
            while len(stat) < number_of_stats:
                stat_name = random.choice(list(items_stat_data.keys()))
                stat_value = random.randrange(-5, 15)

                if stat_value != 0 and stat_name not in {s.name for s in stat}:
                    stat.add(ItemStat(stat_name, stat_value))

            return list(stat)

        def get_random_item_with_random_stats(item_type: str = "stat_items"):
            if item_type == "stackable_items":
                return get_random_item(item_type)
            else:
                item = get_random_item(item_type)
                stats = get_random_stats()
                item.stat = stats
                return item

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

