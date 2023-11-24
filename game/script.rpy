# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.

define e = Character("Eileen")
define v = Character("Vasya")
define vi = Character("Vasilyna")


# The game starts here.

label start:

    # Show a background. This uses a placeholder by default, but you can
    # add a file (named either "bg room.png" or "bg room.jpg") to the
    # images directory to show it.

    scene bg room

    # This shows a character sprite. A placeholder is used, but you can
    # replace it by adding a file named "eileen happy.png" to the images
    # directory.

    show eileen happy
    show vasya happy
    show vasilyna happy

    v "Ну здарова"
    
    vi "Не узнал меня?"

    return


define inventory = []

label receive_item(received_item):
    $ inventory.append(received_item)
    return

label give_item(given_item):
    $ inventory.remove(given_item)
    return

init python:
    
    def add_item(item):
        pass

    def remove_item(item):
        pass


    class Stat:

        def __init__(self, name, param):
            self.name = name
            self.param = param

    class Item:

        def __init__(self, name: str, description: str, value: int):
            self.name = name
            self.description = description
            self.value = value
        
        def __str__(self):
            return f"{self.name} ({self.description}): {self.value}"
    
    class count_item(Item):

        def __init__(self, name: str, description: str, value: int, count: int):
            super().__init__(name, description, value)
            self.count = count

    class stat_item(Item):

        def __init__(self, name, description, value, stat):
            super().__init__(name, description, value)
            self.stat = stat

    class unique_item(Item):

        def __init__(self, name, description, value, stat):
            super().__init__(name, description, value)
            self.stat = stat