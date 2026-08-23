from ursina import *
from random import randint, uniform, choice
from enum import Enum
from scripts.inventory import Inventory
from scripts.sound_manager import play_sound

class list_items(Enum):
    HEAL = ("Heal Potion", 25, "PotionRed")  # Health Regen + instant boost
    SIZE = ("Size Potion", 25, "PotionGreen")  # Size Boost
    MANA = ("Mana Potion", 25, "PotionBlue")  # Mana Regen + instant boost
    SHIELD = ("Shield", 130, "ShieldSmallT1")  # Resistance
    SWORD = ("Sword", 100, "SwordT1")  # Base damage
    SPEED = ("Speed Gem", 80, "GemGreen")  # Speed
    BOOK = ("Book", 80, "TomeBlue")  # Maximum mana
    LIFE = ("Helmet", 80, "HelmetT1")  # Maximum health
    COOLDOWN = ("Cooldown Gem", 100, "GemBlue")  # hand and weapon cooldowns

    def __init__(self, item_name, price, item_texture):
        self.item_name = item_name
        self.price = randint(price - price // 20, price + price // 20)
        self.item_texture = item_texture


class item:
    def __init__(self, item=None):
        if item is None:
            item = choice(list(list_items))
        self.name = item.item_name
        self.price = item.price
        self.item_texture = item.item_texture


class shop(Entity):
    def __init__(self, terrain, position_x, position_y, rotation, parent=None):
        super().__init__(
            parent=parent,
            model=f"assets/Map/{terrain}/special/shop",
            position=(position_x, -140, position_y),
            scale=(600, 600, 600),
            rotation=(0, rotation, 0),
            double_sided=True,
        )
        self.field_radius = 300


class shop_ui(Entity):
    def __init__(self, player, parent=None):
        super().__init__(
            parent=camera.ui,
            model="quad",
            texture="assets/ui/shop",
            position=(0, 0),
            enabled=False,
            scale=(0.8, 0.8),
            z=3,
        )
        self.player = player
        self.market_open = False
        self.item_one = item_image(-0.3, player, parent=self)
        self.item_two = item_image(0, player, parent=self)
        self.item_three = item_image(0.31, player, parent=self)


class item_image(Entity):
    def __init__(self, position_x, player, parent=None):
        super().__init__(
            parent=parent,
            position=(position_x, 0),
        )
        self.player = player
        self.item_sell = item()
        self.printed_price = self.item_sell.price
        self.position_x_text = position_x
        if self.printed_price < 100:
            self.position_x_text = position_x + 0.03
        self.buy_button = Button(
            parent=parent,
            model="quad",
            color=color.white,
            texture=self.item_sell.item_texture,
            collider="box",
            position=(position_x, 0),
            z=-1,
            scale=(0.3, 0.3),
            on_click=lambda: buy_item(self, self.player),
        )
        self.buy_text = Text(
            self.printed_price,
            parent=parent,
            position=(self.position_x_text - 0.085, -0.2),
            z=-1,
            scale=6,
            color=color.black,
        )


def modify_stats(item_name, player):
    if item_name == "Heal Potion":
        player.regen *= 2
        player.health = player.max_health
        print(f"player regen :{player.regen}")
    elif item_name == "Size Potion":
        player.y += player.scale
        player.scale *= 2
        print(f"player weapon damages :{player.weapon.damage}")
    elif item_name == "Mana Potion":
        player.mana = player.max_mana
        print("player at max mana")
    elif item_name == "Shield":
        player.defense += 5
        print(f"player defense :{player.defense}")
    elif item_name == "Sword":
        player.upgrade("d")
        print(f"player damage: {player.weapon.damage}")
    elif item_name == "Speed Gem":
        player.speed += 15
        print(f"player speed : {player.speed}")
    elif item_name == "Book":
        player.max_mana += 50
        player.mana = player.max_mana
        print(f"player max mana :{player.max_mana}")
    elif item_name == "Helmet":
        player.max_health += 50
        player.health = player.max_health
        print(f"player max health : {player.max_health}")
    elif item_name == "Cooldown Gem":
        player.upgrade("c")
        print(
            f"player cooldowns : weapon:{player.weapon.cooldown}"
        )


def buy_item(item_image: item_image, player):
    if item_image == None:
        return
    if item_image.printed_price > player.coins:
        t = Text(
            "Not enough coins !",
            parent=camera.ui,
            position=(0, 0.1),
            origin=(0, 0),
            scale=3,
            color=color.red,
        )
        destroy(t, delay=1)
        play_sound("denied", 1)
    else:
        player.inventory.append(
            item_image.item_sell.item_texture, item_image.item_sell.name
        )
        player.coins -= item_image.printed_price
        modify_stats(item_image.item_sell.name, player)
        player.coin_text.text = str(player.coins)
        destroy(item_image.buy_button)
        destroy(item_image.buy_text)
        destroy(item_image)
        play_sound("buy", 1)
