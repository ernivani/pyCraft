from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import os
import noise

app = Ursina()

def load_asset(*path_parts):
    return os.path.join("Assets", *path_parts)

block_textures = {
    'grass': load_texture(load_asset('Textures', 'Blocks', 'Grass_Block.png')),
    'stone': load_texture(load_asset('Textures', 'Blocks', 'Stone_Block.png')),
    'brick': load_texture(load_asset('Textures', 'Blocks', 'Brick_Block.png')),
    'dirt': load_texture(load_asset('Textures', 'Blocks', 'Dirt_Block.png')),
    'wood': load_texture(load_asset('Textures', 'Blocks', 'Planks_Block.png')),
}

inventory_icons = {
    'grass': load_texture(load_asset('Textures', 'Inventory', 'grass.png')),
    'stone': load_texture(load_asset('Textures', 'Inventory', 'stone.png')),
    'brick': load_texture(load_asset('Textures', 'Inventory', 'brick.png')),
    'dirt': load_texture(load_asset('Textures', 'Inventory', 'dirt.png')),
    'wood': load_texture(load_asset('Textures', 'Inventory', 'planks_oak.png')),
    'empty': load_texture(load_asset('Textures', 'Inventory', 'empty.png'))
}

textures = {
    'sky': load_texture(load_asset('Textures', 'Sky', 'Skybox.png')),
    'arm': load_texture(load_asset('Textures', 'Arm', 'Arm_Texture.png'))
}

gui_textures = {
    'inventory_bg': load_texture(load_asset("Textures", 'Gui', 'inventory_bg.png')),
    'selection_indicator': load_texture(load_asset("Textures", 'Gui', 'selection_indicator.png'))
}

punch_sound = Audio(load_asset('SFX', 'Punch_Sound.wav'), loop=False, autoplay=False)
window.exit_button.visible = False

selected_block = 1

inventory = {
    1: 'grass',
    2: 'stone',
    3: 'brick',
    4: 'dirt',
    5: 'wood',
    6: 'empty',
    7: 'empty',
    8: 'empty',
    9: 'empty'
}

class InventoryUI(Entity):
    def __init__(self):
        super().__init__(parent=camera.ui)
        self.background = Entity(
            parent=self,
            model='quad',
            texture=gui_textures['inventory_bg'],
            scale=(0.9, 0.1),
            position=Vec2(0, -0.45),
            z=1
        )
        self.slots = []
        self.slot_positions = []
        slot_count = 9
        slot_size = 0.06
        initial_x = -0.4

        for i in range(slot_count):
            x = initial_x + (i * slot_size * 1.67)
            self.slot_positions.append(x)
            item = inventory.get(i + 1, 'empty')
            if item != 'empty':
                button = Button(
                    parent=self,
                    model='quad',
                    texture=inventory_icons[item],
                    position=Vec2(x, -0.45),
                    scale=slot_size,
                    color=color.white,
                    highlight_color=color.lime,
                    pressed_color=color.lime.tint(-0.2),
                    z=-1
                )
                self.slots.append(button)
            else:
                self.slots.append(None)

        self.selection_indicator = Entity(
            parent=self,
            model='quad',
            texture=gui_textures['selection_indicator'],
            scale=slot_size * 1.6,
            position=Vec2(self.slot_positions[selected_block - 1], -0.45),
            z=-2
        )

    def update(self):
        self.selection_indicator.position = Vec2(self.slot_positions[selected_block - 1], -0.45)
        for i in range(9):
            item = inventory.get(i + 1, 'empty')
            if item != 'empty' and self.slots[i]:
                self.slots[i].texture = inventory_icons[item]

inventory_ui = InventoryUI()

def update():
    global selected_block
    if held_keys['left mouse'] or held_keys['right mouse']:
        hand.active()
    else:
        hand.passive()

    for i in range(1, 10):
        if held_keys[str(i)]:
            selected_block = i
            inventory_ui.update()

class Voxel(Button):
    def __init__(self, position=(0, 0, 0), texture='grass'):
        super().__init__(
            parent=scene,
            position=position,
            model=load_asset('Models', 'Block', 'Block.obj'),
            origin_y=0.5,
            texture=block_textures[texture],
            color=color.color(0, 0, random.uniform(0.9, 1)),
            highlight_color=color.light_gray,
            scale=0.5
        )

    def input(self, key):
        if self.hovered:
            if key == 'left mouse down' and inventory.get(selected_block, 'empty') != 'empty':
                punch_sound.play()
                Voxel(position=self.position + mouse.normal, texture=inventory.get(selected_block, 'empty'))
            elif key == 'right mouse down':
                punch_sound.play()
                destroy(self)

class Sky(Entity):
    def __init__(self):
        super().__init__(
            parent=scene,
            model='sphere',
            texture=textures['sky'],
            scale=150,
            double_sided=True
        )

class Hand(Entity):
    def __init__(self):
        super().__init__(
            parent=camera.ui,
            model=load_asset('Models', 'Arm', 'Arm.obj'),
            texture=textures['arm'],
            scale=0.2,
            rotation=Vec3(150, -10, 0),
            position=Vec2(0.4, -0.6)
        )

    def active(self):
        self.position = Vec2(0.3, -0.5)

    def passive(self):
        self.position = Vec2(0.4, -0.6)

def generate_height(x, z):
    scale = 50.0
    max_height = 15
    height = noise.pnoise2(x / scale, z / scale, octaves=6, persistence=0.5, lacunarity=2.0, repeatx=1024, repeaty=1024, base=42)
    normalized = (height + 0.5) / 1.5
    return min(int(normalized * max_height), max_height)

def generate_terrain():
    for z in range(20):
        for x in range(20):
            y = generate_height(x, z)
            for dy in range(y + 1):
                if dy == y:
                    texture = 'grass'
                elif dy >= y - 3:
                    texture = 'dirt'
                else:
                    texture = 'stone'
                Voxel(position=(x, dy, z), texture=texture)

generate_terrain()

player = FirstPersonController()
player.position = Vec3(0, 10, 0)

sky = Sky()
hand = Hand()

app.run()
