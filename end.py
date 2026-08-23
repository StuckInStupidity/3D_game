from ursina import *
from panda3d.core import MovieTexture
from time import time

class CONGRATS(Entity):
    def option(self):
        pass

    def __init__(self, player, nb_enemies):
        super().__init__(parent=camera.ui)

        total_time = int(time()-player.start_time)
        minutes = total_time // 60
        seconds = total_time % 60

        self.movie = MovieTexture("congrats")
        self.movie.read("ui/CONGRATS.mp4")
        self.movie.loop = False
        self.video = Entity(parent=self, model="quad", texture=self.movie, scale=(camera.aspect_ratio, 1), z=0)
        self.movie.play()
        self.sound = Audio("ui/CONGRATS.mp4", autoplay=False)
        invoke(self.sound.play, delay=0.68)
        self.time = Text(parent=self, text=f"Time : {minutes:02}:{seconds:02}", origin=(0,0), z=-1, y=0.10, scale = 3, visible=False)
        self.kill = Text(parent=self, text=f"Killed : {player.nb_killed}/{nb_enemies}", origin=(0,0), z=-1, y=0, scale = 3, visible=False)
        self.damage = Text(parent=self, text=f"Damage : {player.dam_inf}", origin=(0,0), z=-1, y=-0.10, scale = 3, visible=False)
        invoke(setattr, self.time, 'visible', True, delay=8)
        invoke(setattr, self.kill, 'visible', True, delay=9)
        invoke(setattr, self.damage, 'visible', True, delay=10)

        self.button = Button(parent=self, model='quad', texture="ui/rectangle.png", collider='box', y=-0.3, z=-1, scale=(0.26, 0.13), x=0, color=color.white, highlight_scale=1.1, visible=False)
        self.text = Text("Back to Home", parent=self, origin=(0,0), y=-0.3, z=-2, x=0, scale=2, color=color.white, visible=False)

        invoke(setattr, self.button, 'visible', True, delay=11)
        invoke(setattr, self.text, 'visible', True, delay=11)

        self.button.on_click = self.option


class GAMEOVER(Entity):
    def option(self):
        pass

    def __init__(self, player, nb_enemies):
        super().__init__(parent=camera.ui)

        total_time = int(time()-player.start_time)
        minutes = total_time // 60
        seconds = total_time % 60

        self.movie = MovieTexture("gameover")
        self.movie.read("ui/GAMEOVER.mp4")
        self.movie.loop = False
        self.video = Entity(parent=self, model="quad", texture=self.movie, scale=(camera.aspect_ratio, 1), z=0)
        self.movie.play()
        self.sound = Audio("ui/GAMEOVER.mp4", autoplay=False)
        invoke(self.sound.play, delay=0.88)
        self.time = Text(parent=self, text=f"Time : {minutes:02}:{seconds:02}", origin=(0,0), z=-1, y=0.10, scale = 3, visible=False)
        self.kill = Text(parent=self, text=f"Killed : {player.nb_killed}/{nb_enemies}", origin=(0,0), z=-1, y=0, scale = 3, visible=False)
        self.damage = Text(parent=self, text=f"Damage : {player.dam_inf}", origin=(0,0), z=-1, y=-0.10, scale = 3, visible=False)
        invoke(setattr, self.time, 'visible', True, delay=8)
        invoke(setattr, self.kill, 'visible', True, delay=9)
        invoke(setattr, self.damage, 'visible', True, delay=10)

        self.button = Button(parent=self, model='quad', texture="ui/rectangle.png", collider='box', y=-0.3, z=-1, scale=(0.26, 0.13), x=0, color=color.white, highlight_scale=1.1, visible=False)
        self.text = Text("Back to Home", parent=self, origin=(0,0), y=-0.3, z=-2, x=0, scale=2, color=color.white, visible=False)

        invoke(setattr, self.button, 'visible', True, delay=11)
        invoke(setattr, self.text, 'visible', True, delay=11)

        self.button.on_click = self.option
