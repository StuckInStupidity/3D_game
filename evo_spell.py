from ursina import *
from enum import Enum


class RotateMeSpell(Entity):
    def __init__(self, player, r, model, scale):
        super().__init__(parent=player)
        self.asset = Entity(parent=self, position=(r, 1, 0), scale=scale, model=model)
        destroy(self, delay=2)
    def update(self):
        self.rotation_y += time.dt * 150
        self.asset.rotation_y += 150 * time.dt


class Diff_Spell(Enum): #= model I guess
    UNDEFINED = 0
    FIRE = 1
    BLADE = 2 
    TORNADO = 3 

class Spell_info(Enum):
    UNDEFINED = 0
    DAMAGE = 1
    RANGE = 2
    COOLDOWN = 3
    
class Spell:
    
    def __init__(self):
        #fire
        self.fire_d_up = [5,10,15,35]
        self.fire_r_up = [1,2,3,5]
        self.fire_c_up = [7,5,3,2]
        self.fire_damage = self.fire_d_up[0]
        self.fire_range = self.fire_r_up[0]
        self.fire_cooldown = self.fire_c_up[0]
        #blade
        self.blade_d_up = [4, 6, 12, 25]
        self.blade_r_up = [2,4,6,9]
        self.blade_c_up = [5, 4, 3, 2]
        self.blade_damage = self.blade_d_up[0]
        self.blade_range = self.blade_r_up[0]
        self.blade_cooldown = self.blade_c_up[0]
        #tornado
        self.tornado_d_up = [4, 9, 17, 30]
        self.tornado_r_up = [2,4,6,9]
        self.tornado_c_up = [9,7,5,3]
        self.tornado_damage = self.tornado_d_up[0]
        self.tornado_range = self.tornado_r_up[0]
        self.tornado_cooldown = self.tornado_c_up[0]
        #upgrades_with_skills_points
        self.upgrade_skills = [0, 1, 3, 5]
    
        
    def attack_spell(self, spell_on):
        if spell_on is Diff_Spell.FIRE:
            return (self.fire_damage, self.fire_range, self.fire_cooldown)
        elif spell_on is Diff_Spell.TORNADO:
            return (self.tornado_damage, self.tornado_range, self.tornado_cooldown)
        elif spell_on is Diff_Spell.BLADE:
            return (self.blade_damage, self.blade_range, self.blade_cooldown)
        

        

    def upgrade_spell(self, which: Diff_Spell , what: Spell_info):
        match which: 
            case Diff_Spell.FIRE:
                match what:
                    case Spell_info.RANGE:
                        i = (self.fire_r_up.index(self.fire_range)) + 1
                        if i < len(self.fire_r_up):
                            self.fire_range = self.fire_r_up[i]
                    case Spell_info.COOLDOWN:
                        i = (self.fire_c_up.index(self.fire_cooldown)) + 1
                        if i < len(self.fire_c_up):
                            self.fire_cooldown = self.fire_c_up[i]
                    case Spell_info.DAMAGE:
                        i = (self.fire_d_up.index(self.fire_damage)) + 1
                        if i < len(self.fire_d_up):
                            self.fire_damage = self.fire_d_up[i]
                    case Spell_info.UNDEFINED:
                        print('Erreur')
            case Diff_Spell.TORNADO:
                match what:
                    case Spell_info.RANGE:
                        i = (self.tornado_r_up.index(self.tornado_range)) + 1
                        if i < len(self.tornado_r_up):
                            self.tornado_range = self.tornado_r_up[i]
                    case Spell_info.COOLDOWN:
                        i = (self.tornado_c_up.index(self.tornado_cooldown)) + 1
                        if i < len(self.tornado_c_up):
                            self.tornado_cooldown = self.tornado_c_up[i]
                    case Spell_info.DAMAGE:
                        i = (self.tornado_d_up.index(self.tornado_damage)) + 1
                        if i < len(self.tornado_d_up):
                            self.tornado_damage = self.tornado_d_up[i]
                    case Spell_info.UNDEFINED:
                        print('Erreur')
            case Diff_Spell.BLADE:
                match what:
                    case Spell_info.RANGE:
                        i = (self.blade_r_up.index(self.blade_range)) + 1
                        if i < len(self.blade_r_up):
                            self.blade_range = self.blade_r_up[i]
                    case Spell_info.COOLDOWN:
                        i = (self.blade_c_up.index(self.blade_cooldown)) + 1
                        if i < len(self.blade_c_up):
                            self.blade_cooldown = self.blade_c_up[i]
                    case Spell_info.DAMAGE:
                        i = (self.blade_d_up.index(self.blade_damage)) + 1
                        if i < len(self.blade_d_up):
                            self.blade_damage = self.blade_d_up[i]
                    case Spell_info.UNDEFINED:
                        print('Erreur')
            case Diff_Spell.UNDEFINED:
                print('nonono')
            
                
                        


        
           





class Evolution_Spell_UI(Entity):
    def __init__(self, player, parent = None):
        super().__init__(
            parent =camera.ui,
            model = 'quad',
            texture = "assets/ui/menu_evo_ui",
            position= (0,0),
            enabled = False,
            scale = (1.3125, 0.7), #ratio 1,875
            z = 3,
        )
        self.player = player
        self.skill = self.player.exp_mana.skill_points
        #range
        
        self.evo_fire_range = button_image(-0.2, 0.23, self.player, self.player.spell.fire_range, parent = self)
        self.i_fire_r = self.player.spell.fire_r_up.index(self.player.spell.fire_range) + 1
        if self.i_fire_r > 3:
            self.evo_fire_range.upgrade_button.tooltip = Tooltip('Maximum',  scale = 0.75, font = 'assets/ui/gras.ttf')
        else:
            self.evo_fire_range.upgrade_button.tooltip = Tooltip('Upgrade: ' + str(self.player.spell.fire_r_up[self.i_fire_r])+ '\n\nCost: ' + str(self.player.spell.upgrade_skills[self.i_fire_r]) + ' skill points', font = 'assets/ui/gras.ttf', scale = 0.75)
            self.evo_fire_range.upgrade_button.on_click = lambda: self.button_clicked(Diff_Spell.FIRE, Spell_info.RANGE, 1,self.player.spell.upgrade_skills[self.i_fire_r])
        
        self.evo_tornado_range = button_image(-0.2, -0.031, self.player, self.player.spell.tornado_range, parent = self)
        self.i_tornado_r = self.player.spell.tornado_r_up.index(self.player.spell.tornado_range) + 1
        if self.i_tornado_r > 3:
            self.evo_tornado_range.upgrade_button.tooltip = Tooltip('Maximum', font = 'assets/ui/gras.ttf', scale = 0.75)
        else:
            self.evo_tornado_range.upgrade_button.tooltip = Tooltip('Upgrade: ' + str(self.player.spell.tornado_r_up[self.i_tornado_r])+ '\n\nCost: ' + str(self.player.spell.upgrade_skills[self.i_tornado_r]) + ' skill points', font = 'assets/ui/gras.ttf', scale = 0.75)
            self.evo_tornado_range.upgrade_button.on_click = lambda: self.button_clicked(Diff_Spell.TORNADO, Spell_info.RANGE, 2, self.player.spell.upgrade_skills[self.i_tornado_r])

        self.evo_blade_range = button_image(-0.2, -0.292, self.player, self.player.spell.blade_range, parent = self)
        self.i_blade_r = self.player.spell.blade_r_up.index(self.player.spell.blade_range) + 1
        if self.i_blade_r > 3:
            self.evo_blade_range.upgrade_button.tooltip = Tooltip('Maximum', font = 'assets/ui/gras.ttf', scale = 0.75)
        else:
            self.evo_blade_range.upgrade_button.tooltip = Tooltip('Upgrade:' + str(self.player.spell.blade_r_up[self.i_blade_r])+ '\n\nCost: ' + str(self.player.spell.upgrade_skills[self.i_blade_r]) + ' skill points', font = 'assets/ui/gras.ttf', scale = 0.75)
            self.evo_blade_range.upgrade_button.on_click = lambda: self.button_clicked(Diff_Spell.BLADE, Spell_info.RANGE, 3,self.player.spell.upgrade_skills[self.i_blade_r])


        #damage
        
        self.evo_fire_damage = button_image(-0.025, 0.23, self.player, self.player.spell.fire_damage, parent = self)
        self.i_fire_d = self.player.spell.fire_d_up.index(self.player.spell.fire_damage) + 1
        if self.i_fire_d > 3:
            self.evo_fire_damage.upgrade_button.tooltip = Tooltip('Maximum', font = 'assets/ui/gras.ttf', scale = 0.75)
        else:
            self.evo_fire_damage.upgrade_button.tooltip = Tooltip('Upgrade: ' + str(self.player.spell.fire_d_up[self.i_fire_d])+ '\n\nCost: ' + str(self.player.spell.upgrade_skills[self.i_fire_d]) + ' skill points', font = 'assets/ui/gras.ttf', scale = 0.75)
            self.evo_fire_damage.upgrade_button.on_click = lambda: self.button_clicked(Diff_Spell.FIRE, Spell_info.DAMAGE, 4, self.player.spell.upgrade_skills[self.i_fire_d])

        self.evo_tornado_damage = button_image(-0.025, -0.031, self.player, self.player.spell.tornado_damage, parent = self)
        self.i_tornado_d = self.player.spell.tornado_d_up.index(self.player.spell.tornado_damage) + 1
        if self.i_tornado_d > 3:
            self.evo_tornado_damage.upgrade_button.tooltip = Tooltip('Maximum', font = 'assets/ui/gras.ttf', scale = 0.75)
        else:
            self.evo_tornado_damage.upgrade_button.tooltip = Tooltip('Upgrade: ' + str(self.player.spell.tornado_d_up[self.i_tornado_d])+ '\n\nCost: ' + str(self.player.spell.upgrade_skills[self.i_tornado_d]) + ' skill points', font = 'assets/ui/gras.ttf', scale = 0.75)
            self.evo_tornado_damage.upgrade_button.on_click = lambda: self.button_clicked(Diff_Spell.TORNADO, Spell_info.DAMAGE, 5,self.player.spell.upgrade_skills[self.i_tornado_d])

        self.evo_blade_damage = button_image(-0.025, -0.292, self.player, self.player.spell.blade_damage, parent = self)
        self.i_blade_d = self.player.spell.blade_d_up.index(self.player.spell.blade_damage) + 1
        if self.i_blade_d > 3:
            self.evo_blade_damage.upgrade_button.tooltip = Tooltip('Maximum', font = 'assets/ui/gras.ttf', scale = 0.75)
        else:
            self.evo_blade_damage.upgrade_button.tooltip = Tooltip('Upgrade: ' + str(self.player.spell.blade_d_up[self.i_blade_d])+ '\n\nCost: ' + str(self.player.spell.upgrade_skills[self.i_blade_d]) + ' skill points', font = 'assets/ui/gras.ttf', scale = 0.75)
            self.evo_blade_damage.upgrade_button.on_click = lambda: self.button_clicked(Diff_Spell.BLADE, Spell_info.DAMAGE, 6, self.player.spell.upgrade_skills[self.i_blade_d])

        #cooldown
        
        self.evo_fire_cooldown = button_image(0.15, 0.23, self.player, self.player.spell.fire_cooldown, parent = self)
        self.i_fire_c = self.player.spell.fire_c_up.index(self.player.spell.fire_cooldown) + 1
        if self.i_fire_c > 3:
            self.evo_fire_cooldown.upgrade_button.tooltip = Tooltip('Maximum', font = 'assets/ui/gras.ttf', scale = 0.75)
        else:
            self.evo_fire_cooldown.upgrade_button.tooltip = Tooltip('Upgrade: ' + str(self.player.spell.fire_c_up[self.i_fire_c])+ '\n\nCost: ' + str(self.player.spell.upgrade_skills[self.i_fire_c]) + ' skill points', font = 'assets/ui/gras.ttf', scale = 0.75)
            self.evo_fire_cooldown.upgrade_button.on_click = lambda: self.button_clicked(Diff_Spell.FIRE, Spell_info.COOLDOWN, 7, self.player.spell.upgrade_skills[self.i_fire_c])

        self.evo_tornado_cooldown = button_image(0.15, -0.031, self.player, self.player.spell.tornado_cooldown, parent = self, )
        self.i_tornado_c = self.player.spell.tornado_c_up.index(self.player.spell.tornado_cooldown) + 1
        if self.i_tornado_c > 3:
            self.evo_tornado_cooldown.upgrade_button.tooltip = Tooltip('Maximum', font = 'assets/ui/gras.ttf', scale = 0.75)
        else:
            self.evo_tornado_cooldown.upgrade_button.tooltip = Tooltip('Upgrade: ' + str(self.player.spell.tornado_c_up[self.i_tornado_c])+ '\n\nCost: ' + str(self.player.spell.upgrade_skills[self.i_tornado_c]) + ' skill points', font = 'assets/ui/gras.ttf', scale = 0.75)
            self.evo_tornado_cooldown.upgrade_button.on_click = lambda: self.button_clicked(Diff_Spell.TORNADO, Spell_info.COOLDOWN, 8, self.player.spell.upgrade_skills[self.i_tornado_c])

        self.evo_blade_cooldown = button_image(0.15, -0.292, self.player, self.player.spell.blade_cooldown, parent = self)
        self.i_blade_c = self.player.spell.blade_c_up.index(self.player.spell.blade_cooldown) + 1
        if self.i_blade_c > 3:
            self.evo_blade_cooldown.upgrade_button.tooltip = Tooltip('Maximum', font = 'assets/ui/gras.ttf', scale = 0.75)
        else:
            self.evo_blade_cooldown.upgrade_button.tooltip = Tooltip('Upgrade: ' + str(self.player.spell.blade_c_up[self.i_blade_c])+ '\n\nCost: ' + str(self.player.spell.upgrade_skills[self.i_blade_c]) + ' skill points', font = 'assets/ui/gras.ttf', scale = 0.75)
            self.evo_blade_cooldown.upgrade_button.on_click = lambda: self.button_clicked(Diff_Spell.BLADE, Spell_info.COOLDOWN, 9,self.player.spell.upgrade_skills[self.i_blade_c])
        
        self.skill_info =  Text(
            str(self.skill),
            parent=self,
            position=(-0.3,-0.43),
            z=-1,
            scale=1,
            color=color.black,
            font = 'gras.ttf'
        )
        
    def update_skill_info(self, new_skill):
        destroy(self.skill_info)
        self.skill_info =  Text(
            str(new_skill),
            parent=self,
            position=(-0.3,-0.43),
            z=-1,
            scale=1,
            color=color.black,
            font = 'gras.ttf'
        ) 

    def open_close_evo(self):
        if self.enabled:
            self.enabled = False
        else:
            self.enabled = True

    def tooltip_maj(self, tool_nb):
        if tool_nb == 1:
            self.i_fire_r += 1
            destroy(self.evo_fire_range.upgrade_button.tooltip)
            if self.i_fire_r > 2:
                self.evo_fire_range.upgrade_button.tooltip = Tooltip('Maximum', font = 'assets/ui/gras.ttf', scale = 0.75)
            else:
                self.evo_fire_range.upgrade_button.tooltip = Tooltip('Upgrade: ' + str(self.player.spell.fire_r_up[self.i_fire_r])+ '\n\nCost: ' + str(self.player.spell.upgrade_skills[self.i_fire_r]) + ' skill points', font = 'assets/ui/gras.ttf', scale = 0.75)
        if tool_nb == 2:
            self.i_tornado_r += 1
            destroy(self.evo_tornado_range.upgrade_button.tooltip)
            if self.i_tornado_r > 2:
                self.evo_tornado_range.upgrade_button.tooltip = Tooltip('Maximum', font = 'assets/ui/gras.ttf', scale = 0.75)
            else:
                self.evo_tornado_range.upgrade_button.tooltip = Tooltip('Upgrade: ' + str(self.player.spell.tornado_r_up[self.i_tornado_r])+ '\n\nCost: ' + str(self.player.spell.upgrade_skills[self.i_tornado_r]) + ' skill points', font = 'assets/ui/gras.ttf', scale = 0.75)
        if tool_nb == 3:
            self.i_blade_r += 1
            destroy(self.evo_blade_range.upgrade_button.tooltip)
            if self.i_blade_r > 2:
                self.evo_blade_range.upgrade_button.tooltip = Tooltip('Maximum', font = 'assets/ui/gras.ttf', scale = 0.75)
            else:
                self.evo_blade_range.upgrade_button.tooltip = Tooltip('Upgrade:' + str(self.player.spell.blade_r_up[self.i_blade_r])+ '\n\nCost: ' + str(self.player.spell.upgrade_skills[self.i_blade_r]) + ' skill points', font = 'assets/ui/gras.ttf', scale = 0.75)
        if tool_nb == 4:
            self.i_fire_d += 1
            destroy(self.evo_fire_damage.upgrade_button.tooltip)
            if self.i_fire_d > 2:
                self.evo_fire_damage.upgrade_button.tooltip = Tooltip('Maximum', font = 'assets/ui/gras.ttf', scale = 0.75)
            else:
                self.evo_fire_damage.upgrade_button.tooltip = Tooltip('Upgrade: ' + str(self.player.spell.fire_d_up[self.i_fire_d])+ '\n\nCost: ' + str(self.player.spell.upgrade_skills[self.i_fire_d]) + ' skill points', font = 'assets/ui/gras.ttf', scale = 0.75)
        if tool_nb == 5:
            self.i_tornado_d += 1
            destroy(self.evo_tornado_damage.upgrade_button.tooltip)
            if self.i_tornado_d > 2:
                self.evo_tornado_damage.upgrade_button.tooltip = Tooltip('Maximum', font = 'assets/ui/gras.ttf', scale = 0.75)
            else:
                self.evo_tornado_damage.upgrade_button.tooltip = Tooltip('Upgrade: ' + str(self.player.spell.tornado_d_up[self.i_tornado_d])+ '\n\nCost: ' + str(self.player.spell.upgrade_skills[self.i_tornado_d]) + ' skill points', font = 'assets/ui/gras.ttf', scale = 0.75)
        if tool_nb == 6:
            self.i_blade_d += 1
            destroy(self.evo_blade_damage.upgrade_button.tooltip)
            if self.i_blade_d > 2:
                self.evo_blade_damage.upgrade_button.tooltip = Tooltip('Maximum', font = 'assets/ui/gras.ttf', scale = 0.75)
            else:
                self.evo_blade_damage.upgrade_button.tooltip = Tooltip('Upgrade: ' + str(self.player.spell.blade_d_up[self.i_blade_d])+ '\n\nCost: ' + str(self.player.spell.upgrade_skills[self.i_blade_d]) + ' skill points', font = 'assets/ui/gras.ttf', scale = 0.75)
        if tool_nb == 7:
            self.i_fire_c += 1
            destroy(self.evo_fire_cooldown.upgrade_button.tooltip)
            if self.i_fire_c > 2:
                self.evo_fire_cooldown.upgrade_button.tooltip = Tooltip('Maximum', font = 'assets/ui/gras.ttf', scale = 0.75)
            else:
                self.evo_fire_cooldown.upgrade_button.tooltip = Tooltip('Upgrade: ' + str(self.player.spell.fire_c_up[self.i_fire_c])+ '\n\nCost: ' + str(self.player.spell.upgrade_skills[self.i_fire_c]) + ' skill points', font = 'assets/ui/gras.ttf', scale = 0.75)
        if tool_nb == 8:
            self.i_tornado_c += 1
            destroy(self.evo_tornado_cooldown.upgrade_button.tooltip)
            if self.i_tornado_c > 2:
                self.evo_tornado_cooldown.upgrade_button.tooltip = Tooltip('Maximum', font = 'assets/ui/gras.ttf', scale = 0.75)
            else:
                self.evo_tornado_cooldown.upgrade_button.tooltip = Tooltip('Upgrade: ' + str(self.player.spell.tornado_c_up[self.i_tornado_c])+ '\n\nCost: ' + str(self.player.spell.upgrade_skills[self.i_tornado_c]) + ' skill points', font = 'assets/ui/gras.ttf', scale = 0.75)
        if tool_nb == 9:
            self.i_blade_c += 1
            destroy(self.evo_blade_cooldown.upgrade_button.tooltip)
            if self.i_blade_c > 2:
                self.evo_blade_cooldown.upgrade_button.tooltip = Tooltip('Maximum', font = 'assets/ui/gras.ttf', scale = 0.75)
            else:
                self.evo_blade_cooldown.upgrade_button.tooltip = Tooltip('Upgrade: ' + str(self.player.spell.blade_c_up[self.i_blade_c])+ '\n\nCost: ' + str(self.player.spell.upgrade_skills[self.i_blade_c]) + ' skill points', font = 'assets/ui/gras.ttf', scale = 0.75)
        




    def button_clicked(self, which: Diff_Spell , what: Spell_info, tool_nb, cost):
        if self.player.exp_mana.skill_points >= cost:
            self.player.exp_mana.skill_points -= cost
            self.player.spell.upgrade_spell(which, what)
            self.tooltip_maj(tool_nb)
        else:
            t1 = Text(
            "Skill issue",
            parent=camera.ui,
            position=(0, 0),
            origin=(0, 0),
            scale=6.5,
            color=color.black,
            font = 'assets/ui/gras.ttf',
            )
            t2 = Text(
            "Skill issue",
            parent=camera.ui,
            position=(0, 0),
            origin=(0, 0),
            scale=6,
            color=color.red,
            font = 'assets/ui/gras.ttf',
            )
            destroy(t1, delay=0.5)
            destroy(t2, delay = 0.5)


class button_image(Entity):
    def __init__(self, position_x, position_y, player, valeur, parent=None):
        super().__init__(
            parent=parent,
            position=(position_x, position_y),
        )
        self.player = player
        self.position_y_text = position_y
        self.position_x_text = position_x
        self.upgrade_button = Button(
            parent=self,
            model="quad",
            color=color.white,
            texture="assets/ui/bouton_evo",
            collider="box",
            position=(0, 0),
            z=-1,
            scale=(0.05, 0.08),
           
        )
        self.spell_info = Text(
            str(valeur),
            parent=parent,
            position=(self.position_x_text + 0.037,self.position_y_text + 0.04),
            z=-1,
            scale=2,
            color=color.black,
            font = "assets/ui/gras.ttf"
        )


class Active_Spell_UI(Entity):
    def __init__(self, player, parent = None):
        super().__init__(
            parent =camera.ui,
            model = 'quad',
            color = color.red,
            texture = "assets/ui/menu_evo_ui",
            position= (0,0),
            enabled = True,
            scale = (1.3125, 0.7), #ratio 1,875
            z = 3,
        )
        self.player = player
        self.skill = self.player.exp_mana.skill_points
        self.upgrade_button = Button(
            parent=camera.ui,
            model="quad",
            color=color.white,
            texture="assets/ui/fire_button",
            collider="box",
            position=(0, 0, -1),
            scale=(0.1, 0.1),
        )  

