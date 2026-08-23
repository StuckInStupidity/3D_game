from ursina import *
from scripts.map_generation import Map
import time
from math import inf
from scripts.inventory import Inventory
from enum import Enum
from scenes.avatar_selection_menu import AvatarSelectorEnum
from scenes.end import GAMEOVER, CONGRATS
from scripts.shop import shop_ui, shop
from ui.ui import GameUI
from scripts.evo_spell import Evolution_Spell_UI, Spell, Diff_Spell, Spell_info, RotateMeSpell

from scripts.sound_manager import play_music,stop_music,play_sound

class Player(Entity):
    def __init__(
        self,
        avatar: AvatarSelectorEnum,
        pseudo: str,
        is_simulated: bool,
        inputs_dict: dict[str, int],
        debug: bool,
        shop_instance: shop,
        enemies_list,
        GameUI_instance: GameUI,
        is_image = False
    ):
        super().__init__(scale=4, model=avatar.value, position=(0, 0, 0))

        self.weapon = None
        self.targeted_position = None
        self.avatar = avatar
        if avatar is AvatarSelectorEnum.KNIGHT:
            self.weapon = Sword()
        elif avatar is AvatarSelectorEnum.WIZARD:
            self.weapon = Wand()
        self.is_image = is_image
        self.enemies_list = enemies_list
        self.is_simulated = is_simulated
        self.debug = debug
        self.enemies_list = []
        self.pseudo = pseudo
        self.speed = 15
        self.defense = 0
        self.max_mana = 100
        self.mana = self.max_mana
        self.max_health = 100
        self.health = self.max_health
        self.xp = 0
        self.dead = False
        self.regen_cooldown = 0
        self.can_attack = True
        self.coins = 0
        self.is_equipped = False
        self.exp_mana = EXPERIENCE(self)
        self.spell = Spell()
        self.spell_on = None
        self.dico_spell = {'0': None, '1': Diff_Spell.FIRE, '2':  Diff_Spell.TORNADO, '3': Diff_Spell.BLADE, }
        self.spell_cooldown = 0
        self.mana_cooldown = 0
        self.cooldown_start_spell = 0
        self.cooldown_start_weapon = 0
        self.can_spell = True
        self.inventory = Inventory()
        self.inputs = inputs_dict
        self.shop_ui = shop_ui(self)
        self.shop_instance = shop_instance
        self.game_ui = GameUI_instance
        self.evo_spell = Evolution_Spell_UI(self)
        self.coin_text=Text(
            str(self.coins),
            parent=self.game_ui.PlayerBoard,
            z= -1,
            y = self.y + 0.3,
            scale=6,
            color=color.black,
        )
        stop_music()
        self.music = play_music("game", 4)
        self.nb_killed = 0
        self.dam_inf = 0
        self.ok = True
        self.nb_touched = 0
        

    def attack(self):
        if self.spell_on is not None:
            (d,r,c) = self.spell.attack_spell(self.spell_on)
            time_check = time.time() - self.cooldown_start_spell
            if (time_check) >= c:
                self.can_spell = True
            if self.can_spell and self.mana >= 5:
                self.mana -= 5
                if self.spell_on == Diff_Spell.FIRE:
                    RotateMeSpell(self, r, 'assets/models/fireball.glb', 2)
                if self.spell_on == Diff_Spell.TORNADO:
                    RotateMeSpell(self, r, 'assets/models/tornado.glb', 3)
                if self.spell_on == Diff_Spell.BLADE:
                    RotateMeSpell(self, r, 'assets/models/trail.glb', 1)
                enemies_target = self.Enemies_target_spell(r)
                for enemy in enemies_target:
                    enemy.TakeDamageE(d, self)
                    self.dam_inf += d
                    self.nb_touched += 1
                self.can_spell = False
                self.cooldown_start_spell = time.time()
        else:
            time_check = time.time() - self.cooldown_start_weapon
            if time_check >= self.weapon.cooldown:
                self.can_attack = True
            if self.can_attack:
                target = self.Enemy_target(self.weapon.range)
                play_sound(self.weapon.sound,1)
                if target:
                    target.TakeDamageE(self.weapon.damage, self)
                    self.dam_inf += self.weapon.damage
                    self.nb_touched += 1
                self.cooldown_start_weapon = time.time()
                self.can_attack = False

    def upgrade(self, what):
        if what == "d":
            i = (self.weapon.upgrade_damage.index(self.weapon.damage)) + 1
            if i < len(self.weapon.upgrade_damage):
                self.weapon.damage = self.weapon.upgrade_damage[i]
        if what == "c":
            i = (self.weapon.upgrade_cooldown.index(self.weapon.cooldown)) + 1
            if i < len(self.weapon.upgrade_cooldown):
                self.weapon.cooldown = self.weapon.upgrade_cooldown[i]

    def level_up(self):
        self.health += 10
        if self.exp_mana.level %5 == 0:
            self.max_health += 5
            self.exp_mana.mult =  self.exp_mana.mult * 1.05


    def TakeDamage(self, x, defense):
        if x > 0:
            x -= defense
            if x <= 0:
                x = 1
        self.health -= x
        self.game_ui.set_health(self.health, self.max_health)
        if self.health <= 0:
            play_sound("death", 1)
            self.dead = True
        else:
            play_sound("ouch", 1)

    def Enemy_killed(self, coins, xp,e):
        self.coins += coins
        self.coin_text.text = str(self.coins)
        self.exp_mana.gain_xp(xp, self)
        self.enemies_list.remove(e)
        self.nb_killed += 1


    def OpenCloseInventory(self):
        if self.inventory.enabled :
            self.inventory.enabled = False
            play_sound("inventory_close", 1)
        else:
            self.inventory.enabled = True
            play_sound("inventory_open", 1)

    def use_market(self, market, market_open):
        if self.shop_instance is None:
            print("no shop")
            t = Text(
            "Not near a shop",
            parent=camera.ui,
            position=(0, 0.1),
            origin=(0, 0),
            scale=3,
            color=color.red,
            )
            destroy(t, delay=1)            
            play_sound("denied", 1)
            return
        elif market_open:
            print("close market")
            market.enabled = False
            market.market_open = False
        else:
            if (
                distance(self.position, self.shop_instance.position)
                < self.shop_instance.field_radius
            ):
                print("open market")
                market.enabled = True
                market.market_open = True
            else:
                t = Text(
                "Not near a shop",
                parent=camera.ui,
                position=(0, 0.1),
                origin=(0, 0),
                scale=3,
                color=color.red,
                )
                destroy(t, delay=1)
                play_sound("denied", 1)
                print(distance(self.position, self.shop_instance.position))


    def player_keep(self):
        fr = self.spell.fire_range
        fc = self.spell.fire_cooldown
        fd = self.spell.fire_damage
        br = self.spell.blade_range
        bc = self.spell.blade_cooldown
        bd = self.spell.blade_damage
        tr = self.spell.tornado_range
        tc = self.spell.tornado_cooldown
        td = self.spell.tornado_damage
        ml = self.exp_mana.level
        ms = self.exp_mana.skill_points
        mh = self.max_health
        mm = self.exp_mana.mult
        kf = {'r': fr, 'c': fc, 'd': fd}
        kb = {'r': br, 'c': bc, 'd': bd}
        kt = {'r': tr, 'c': tc, 'd': td}
        ks = {'f': kf, 'b': kb, 't': kt}
        k_a = {'l': ml, 's': ms, 'e': ks, 'h': mh, 'm': mm}
        return k_a


    def player_recover(self, dico_keep_all):
        self.max_health = dico_keep_all['h']
        self.exp_mana.level = dico_keep_all['l']
        self.exp_mana.skill_points = dico_keep_all['s']
        self.exp_mana.mult = dico_keep_all['m']
        dico_spell = dico_keep_all['e']
        #tornado
        dico_tornado = dico_spell['t']
        self.spell.tornado_cooldown = dico_tornado['c']
        self.spell.tornado_range = dico_tornado['r']
        self.spell.tornado_damage = dico_tornado['d']
        #blade
        dico_blade = dico_spell['b']
        self.spell.blade_cooldown = dico_blade['c']
        self.spell.blade_range = dico_blade['r']
        self.spell.blade_damage = dico_blade['d']
        #fire
        dico_fire = dico_spell['f']
        self.spell.fire_cooldown = dico_fire['c']
        self.spell.fire_range = dico_fire['r']
        self.spell.fire_damage = dico_fire['d']




    def Enemies_target_spell(self, range):
        r_sq = range ** 2
        return [e for e in self.enemies_list if (e.x - self.x)**2 + (e.z - self.z)**2 <= r_sq]
      
    def Enemy_target(self, range):
        target = None
        lowest_dist = inf
        for enemy in self.enemies_list:
            dist =  distance(self.position, enemy.position)
            if dist < range and dist < lowest_dist:
                target = enemy
                lowest_dist = dist
        return target
    

    def update(self):
        move_speed = self.speed * time.dt

        if self.is_simulated:

            move_dir = Vec3(0, 0, 0)

            if self.inputs.get("w"):
                move_dir[2] += 1

            if self.inputs.get("s"):
                move_dir[2] -= 1

            if self.inputs.get("a"):
                move_dir[0] -= 1

            if self.inputs.get("d"):
                move_dir[0] += 1            

            
            if self.inputs.get('0'):
                self.spell_on = None
            if self.inputs.get('1'):
                self.spell_on = Diff_Spell.FIRE
            if self.inputs.get('2'):
                self.spell_on = Diff_Spell.TORNADO
            if self.inputs.get('3'):
                self.spell_on = Diff_Spell.BLADE
               
    
               
            
            if move_dir.length() > 0:
                move_dir = move_dir.normalized()
                self.x += move_dir[0] * move_speed
                self.z += move_dir[2] * move_speed


            p_used = None
            b_used = None
            i_used = None
            n_used = None
            
            if not self.is_image:
                p_used = self.inputs.get("p")
                b_used = self.inputs.get("b")
                i_used = self.inputs.get("i")
                n_used = self.inputs.get("n")

            if p_used and not self.p_pressed:
                self.attack()
            self.p_pressed = p_used

            if n_used and not self.n_pressed:
                if not self.is_image:
                    self.evo_spell.open_close_evo()
            self.n_pressed = n_used
            o_used = self.inputs.get("o")

            if b_used and not self.b_pressed:
                self.use_market(self.shop_ui, self.shop_ui.market_open)
            self.b_pressed = b_used

            if i_used and not self.i_pressed:
                self.OpenCloseInventory()
            self.i_pressed = i_used

            if o_used and not self.o_pressed:
                if self.music is None:
                    print("play")
                    self.music = play_music("game", 4)
                else:
                    print("stop")
                    stop_music()
                    self.music = None                
            self.o_pressed = o_used

        if not self.dead :
            if self.health < self.max_health:
                if time.time() - self.regen_cooldown >= 10:
                    self.health += 1
                    self.regen_cooldown = time.time()
            if self.health > self.max_health:
                self.health = self.max_health
            if self.mana < self.max_mana:
                if time.time() - self.mana_cooldown >= 2:
                    self.mana += 1
                    self.mana_cooldown = time.time()
            if self.mana > self.max_mana:
                self.mana = self.max_mana
        else:
            if self.ok:
                GAMEOVER(self)
                self.ok = False
"""
            if self.targeted_position:
                if self.targeted_position:
                    dist = distance(self.position, self.targeted_position)

                    if dist > 0.05:
                        self.position = lerp(
                            self.position, self.targeted_position, time.dt * 7
                        )

                    else:
                        self.position = self.targeted_position
"""







class EXPERIENCE():
    def __init__(self, player: Player):
        self.player = player
        self.xp = 0
        self.level = 0
        self.xp_levelup = 10
        self.skill_points = 0
        self.mult = 1

    def gain_xp(self, xp, player):
        self.xp += xp
        if self.xp == self.xp_levelup:
                self.level += 1
                self.xp_levelup += self.xp_levelup * self.mult
                self.xp = 0
                self.skill_points+= 1
                player.level_up()
                player.evo_spell.update_skill_info(self.skill_points)
        
    



class Wand:
    def __init__(self):
        self.upgrade_damage = [7, 14, 25, 37, 60]
        self.upgrade_cooldown = [5,4,3,2,1]
        self.damage = self.upgrade_damage[0]
        self.range = 5
        self.cooldown = self.upgrade_cooldown[0]
        self.sound = "magic_hit"


class Sword:
    def __init__(self):
        self.upgrade_damage = [5, 10, 20, 30, 50]
        self.upgrade_cooldown = [6,5,4,3,2,1]
        self.damage = self.upgrade_damage[0]
        self.range = 1.5
        self.cooldown = self.upgrade_cooldown[0]
        self.sound = "sword_hit"





       
