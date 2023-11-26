
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