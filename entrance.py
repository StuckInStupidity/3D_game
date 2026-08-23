from ursina import *
from end import CONGRATS, GAMEOVER
from time import time

# ********
#   TEST
# ********

class FakePlayer():
    def __init__(self):
        self.nb_killed = 14
        self.dam_inf = 1350
        self.start_time = time()


player = FakePlayer()
nb_enemies = 30

#*********************************************************
#		LES CONFIGS
#*********************************************************

app = Ursina(title="Echoes-of-Arkanum", icon="ui/icon.ico")
window.fullscreen = True
window.exit_button.enabled = True
window.exit_button.texture = load_texture("ui/X.png")
window.exit_button.text = ""
window.exit_button.scale = 0.08
window.fps_counter.enabled = False
window.entity_counter.enabled = False
window.collider_counter.enabled = False
Text.default_font = "ui/font.ttf"
# Text.size = 0.1 => not working for input fields :(


#*********************************************************
#		First menu
#*********************************************************

class BG(Entity):
    def actionOnline(self):
        self.disable()
        Logg().enable()

    def actionOffline(self):
        self.disable()
        Avatar().enable()

    def __init__(self):
        super().__init__(parent=camera.ui)
	

        self.bg = Entity(parent=self, model="quad", scale=(camera.aspect_ratio, 1), texture=load_texture("ui/table.png"), z=2)
        self.title = Text("Echoes of Arkanum", parent=self, origin=(0,0), z=1, y=0.2, color=color.white, scale=4)

        self.button1 = Button(parent=self, model='quad', texture="ui/rectangle.png", collider='box', z=1, scale=(0.32, 0.16), y=0, color=color.white, highlight_scale=1.1)
        self.text1 = Text("online", parent=self, origin=(0,0), z=0, y=0, scale=4, color=color.white)

        self.button2 = Button(parent=self, model='quad', texture="ui/rectangle.png", collider='box', z=1, scale=(0.32, 0.16), y=-0.2, color=color.white, highlight_scale=1.1)
        self.text2 = Text("offline", parent=self, origin=(0,0), z=0, y=-0.2, scale=4, color=color.white)

        self.button1.on_click = self.actionOnline
        self.button2.on_click = self.actionOffline

#******************************************************
#	Menu pour choisir entre knight et wizard
#******************************************************

class Avatar(Entity):   # class built in lobby for multi
    def choice1(self):
        pass               # start game directly with the right avatar for solo play

    def choice2(self):
        pass

    def __init__(self):
        super().__init__(parent=camera.ui)
        self.bg = Entity(parent=self, model="quad", scale=(camera.aspect_ratio, 1), texture=load_texture("ui/table.png"), z=2)
        self.title = Text("Choose your avatar", origin=(0,0), parent=self, z=1, y=0.24, color=color.white, scale=4)

        self.button1 = Button(parent=self, model='quad', texture="ui/knight.png", collider='box', z=1, scale=(0.30, 0.30), x=0.2, y=0, color=color.white, highlight_scale=1.1)
        self.text1 = Text("knight", origin=(0,0), parent=self, z=1, y=-0.2, x=0.2, color=color.white, scale=4)

        self.button2 = Button(parent=self, model='quad', texture="ui/wizard.png", collider='box', z=1, scale=(0.30, 0.30), x=-0.2, y=0, color=color.white, highlight_scale=1.1)
        self.text2 = Text("wizard", origin=(0,0), parent=self, z=1, y=-0.2, x=-0.2, color=color.white, scale=4)

        self.button1.on_click = self.choice1
        self.button2.on_click = self.choice2

#***************************************************
#		Login menu
#***************************************************

class Logg(Entity):
    def action(self):
        self.disable()
        Room().enable()

    def __init__(self):
        super().__init__(parent=camera.ui)
        self.bg = Entity(parent=self, model="quad", scale=(camera.aspect_ratio, 1), texture=load_texture("ui/table.png"), z=2)
        self.title = Text("LOG IN", parent=self, origin=(0,0), z=1, y=0.2, color=color.white, scale=4)

        self.input1 = InputField(parent=self, default_value='Username', max_lines=1, text_color=color.white, y=0.07)

        self.input2 = InputField(parent=self, default_value='Password', max_lines=1, text_color=color.white, hide_content=True, y=-0.03)

        self.button = Button(parent=self, model='quad', texture="ui/rectangle.png", collider='box', z=1, scale=(0.32, 0.16), y=-0.2, color=color.white, highlight_scale=0.8)
        self.text = Text("Login", parent=self, origin=(0,0), z=0, y=-0.2, scale=4, color=color.white)

        self.button.on_click = self.action

bg = BG()
app.run()