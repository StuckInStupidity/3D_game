from ursina import *


class Inventory(Entity):
    def __init__(self):
        super().__init__(
            parent=camera.ui,
            model="quad",
            scale=(0.5, 0.8),
            origin=(-0.5, 0.5),
            position=(-0.3, 0.4),
            texture="white_cube",
            texture_scale=(5, 8),
            color=color.dark_gray,
            enabled=False,
        )

        self.item_parent = Entity(
            parent=self,
            scale=(1 / 5, 1 / 8),
            origin=(-0.5, 0.5),
            position=(0, 0),
        )
        self.taken_spots = []

    def sync_taken_spots(self):
        self.taken_spots = [
            (int(round(c.x)), int(round(c.y)))
            for c in self.item_parent.children
            if isinstance(c, Draggable)
        ]

    def find_free_spot(self):
        self.sync_taken_spots()
        for y in range(8):
            for x in range(5):
                if (x, -y) not in self.taken_spots:
                    self.taken_spots.append((x, -y))
                    return (x, -y)
        return None

    def append(self, item, item_name):
        pos = self.find_free_spot()
        if not pos:
            return None
        else:
            icon = Draggable(
                parent=self.item_parent,
                model="quad",
                texture=item,
                color=color.white,
                origin=(-0.5, 0.5),
                position=pos,
                org_pos=pos,
                z=-1,
            )
            self.name = item_name
            icon.tooltip = Tooltip(self.name)
            icon.tooltip.scale *= 1.5

            def drag():
                icon.org_pos = (icon.x, icon.y)

                icon.x = max(0, min(4, icon.x))
                icon.y = max(-7, min(0, icon.y))
                icon.z = 1

            def drop():
                origin = (int(round(icon.org_pos[0])), int(round(icon.org_pos[1])))
                target = (int(round(icon.x)), int(round(icon.y)))

                if target[0] < 0 or target[0] >= 5 or target[1] > 0 or target[1] < -7:
                    icon.position = icon.org_pos
                    return

                swap_target = None
                for i in self.item_parent.children:
                    if i is icon:
                        continue
                    if (int(round(i.x)), int(round(i.y))) == target:
                        swap_target = i
                        break

                if swap_target:
                    swap_target.position = (origin[0], origin[1], -1)
                    swap_target.org_pos = origin

                    if target in self.taken_spots:
                        self.taken_spots.remove(target)
                    else:
                        self.taken_spots.append(origin)

                icon.position = (target[0], target[1], -1)
                icon.org_pos = target

                self.sync_taken_spots()

            icon.drag = drag
            icon.drop = drop
