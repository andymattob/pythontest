from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random
import os
import numpy as np
from PIL import Image

# --- 1. SUPER-TEXTURE GENERATOR (Skapar alla filer om de saknas) ---
def generate_all_textures():
    # Trä (Wood)
    if not os.path.exists('wood_tex.png'):
        data = np.zeros((256, 256, 3), dtype=np.uint8)
        for x in range(256):
            val = int(100 + 30 * np.sin(x / 8.0))
            data[:, x] = [val, val-30, val-50] # Brun
        Image.fromarray(data).save('wood_tex.png')

    # Sten (Stone)
    if not os.path.exists('stone_tex.png'):
        data = np.random.randint(110, 160, (256, 256, 3), dtype=np.uint8)
        # Lägg till lite sprickor
        for i in range(500):
            x, y = random.randint(0,255), random.randint(0,255)
            data[x:x+2, y:y+2] = [80, 80, 80]
        Image.fromarray(data).save('stone_tex.png')

    # Gräs (Grass)
    if not os.path.exists('grass_tex.png'):
        data = np.random.randint(40, 120, (256, 256, 3), dtype=np.uint8)
        data[:, :, 0] = 0 # Ta bort rött
        data[:, :, 2] = random.randint(0,30) # Lite blått
        Image.fromarray(data).save('grass_tex.png')

    # Björnpäls (Bear Fur)
    if not os.path.exists('bear_tex.png'):
        data = np.random.randint(80, 120, (128, 128, 3), dtype=np.uint8)
        data[:, :, 1] -= 20; data[:, :, 2] -= 40 # Mörkbrun
        Image.fromarray(data).save('bear_tex.png')

    # Sol/Himmel (Sky/Sun)
    if not os.path.exists('sky_tex.png'):
        data = np.zeros((128, 128, 3), dtype=np.uint8)
        for y in range(128):
            val = int(150 + y / 2)
            data[y, :] = [val-100, val-50, val] # Blå gradient
        # Lägg till en obelisk-liknande form i horisonten
        data[60:128, 60:68] = [200, 200, 255]
        Image.fromarray(data).save('sky_tex.png')

    # Hotbar Ikoner
    if not os.path.exists('axe_icon.png'): Image.fromarray(np.random.randint(100, 200, (64,64,3), dtype=np.uint8)).save('axe_icon.png')
    if not os.path.exists('spear_icon.png'): Image.fromarray(np.random.randint(100, 200, (64,64,3), dtype=np.uint8)).save('spear_icon.png')
    if not os.path.exists('torch_icon.png'): Image.fromarray(np.random.randint(200, 255, (64,64,3), dtype=np.uint8)).save('torch_icon.png')
    if not os.path.exists('berry_icon.png'): 
        data = np.zeros((64, 64, 3), dtype=np.uint8)
        data[:] = [0, 255, 0] # Grön
        data[20:44, 20:44] = [255, 0, 0] # Rött bär
        Image.fromarray(data).save('berry_icon.png')

generate_all_textures()

app = Ursina()

# --- 2. GLOBAL STATUS & DEFINITIONER ---
resources = {'Trä': 30, 'Sten': 20, 'Bär': 10}
health, hunger = 100, 100
inventory = {'Axe': False, 'Spear': False, 'Torch': False}
current_tool, current_tool_index = None, -1
build_mode, crafting_mode = False, False
selected_build_item = 0

build_items = [
    {'name': 'Golv', 'model': 'cube', 'cost': 15, 'tex': 'wood_tex.png', 'scale': (4, 0.2, 4)},
    {'name': 'Vägg', 'model': 'cube', 'cost': 20, 'tex': 'wood_tex.png', 'scale': (4, 3, 0.2)},
    {'name': 'Tak',  'model': 'cube', 'cost': 30, 'tex': 'wood_tex.png', 'scale': (4, 0.2, 4)}
]

# --- 3. UI (HOTBAR, STATUS, CRAFTING) ---
# Status Bars
Entity(parent=camera.ui, model='quad', color=color.black66, scale=(0.4, 0.025), position=(-0.6, -0.4))
hb = Entity(parent=camera.ui, model='quad', color=color.red, scale=(1, 1), position=(-0.6, -0.4), origin=(-0.5,0))
hb.add_script(SmoothFollow(target=hb, offset=(0,0,0), speed=5))

Entity(parent=camera.ui, model='quad', color=color.black66, scale=(0.4, 0.025), position=(-0.6, -0.44))
hgb = Entity(parent=camera.ui, model='quad', color=color.orange, scale=(1, 1), position=(-0.6, -0.44), origin=(-0.5,0))

res_text = Text(text='', position=(-0.85, 0.45), scale=1.5, color=color.yellow)

# Hotbar med Ikoner
hotbar = Entity(parent=camera.ui, model='quad', color=color.black66, scale=(0.55, 0.09), position=(0, -0.41))
slots = []
icon_texs = ['axe_icon.png', 'spear_icon.png', 'torch_icon.png', 'berry_icon.png']
for i in range(4):
    slot = Entity(parent=hotbar, model='quad', color=color.rgba(255,255,255,50), scale=(0.23, 0.9), position=(-0.345 + (i * 0.23), 0))
    # Lägg till textur-ikon
    Entity(parent=slot, model='quad', texture=icon_texs[i], scale=(0.8, 0.8), z=-0.01, color=color.white if (i==3 or inventory[['Axe','Spear','Torch'][i]]) else color.gray)
    Text(parent=slot, text=str(i+1), origin=(0.5, -0.5), scale=1.2, position=(0.45, -0.45), color=color.white)
    slots.append(slot)

# Crafting Meny
craft_panel = Entity(parent=camera.ui, model='quad', color=color.black66, scale=(0.5, 0.5), position=(0,0.1), visible=False)
Text(parent=craft_panel, text="CRAFTING (C)", origin=(0,-4), scale=2, color=color.yellow)

def update_ui():
    res_text.text = f'INV | Trä: {resources["Trä"]} | Sten: {resources["Sten"]} | Bär: {resources["Bär"]}'
    hb.scale_x = (health / 100) * 0.4
    hgb.scale_x = (hunger / 100) * 0.4
    # Uppdatera hotbar-val
    for i, s in enumerate(slots):
        s.color = color.yellow if i == current_tool_index else color.rgba(255,255,255,50)

# --- 4. VERKTYG MODELLER (Texturerade) ---
axe_m = Entity(parent=camera.ui, model='cube', texture='wood_tex.png', scale=(0.05, 0.4, 0.1), position=(0.5,-0.5,0.8), rotation=(30,-10,0), visible=False)
Entity(parent=axe_m, model='cube', texture='stone_tex.png', scale=(2, 0.3, 1.5), position=(0, 0.4, 0))

spear_m = Entity(parent=camera.ui, model='cube', texture='wood_tex.png', scale=(0.02, 0.9, 0.02), position=(0.5,-0.6,1), rotation=(-10,0,0), visible=False)
Entity(parent=spear_m, model='sphere', texture='stone_tex.png', scale=(2, 4, 2), position=(0, 0.5, 0))

torch_m = Entity(parent=camera.ui, model='cube', texture='wood_tex.png', scale=(0.05, 0.3, 0.05), position=(0.5,-0.5,0.8), visible=False)
torch_l = PointLight(parent=torch_m, color=color.orange, range=20, intensity=0, position=(0,1,0))
Entity(parent=torch_m, model='sphere', color=color.orange, scale=1.5, position=(0,0.6,0), alpha=0.8) # Eld

def switch_tool(index):
    global current_tool, current_tool_index, hunger
    if index == 3: # Äta bär
        if resources['Bär'] > 0:
            resources['Bär'] -= 1; hunger = min(100, hunger + 15); update_ui()
        return

    tools = ['Axe', 'Spear', 'Torch']
    name = tools[index]
    if inventory[name]:
        current_tool, current_tool_index = name, index
        axe_m.visible = (name == 'Axe')
        spear_m.visible = (name == 'Spear')
        torch_m.visible = (name == 'Torch')
        torch_l.intensity = 5 if name == 'Torch' else 0
        update_ui()

# --- 5. LOGIK & INPUT ---
ghost = Entity(model='cube', color=color.rgba(1, 1, 1, 0.3), visible=False)

def craft(name, w, s):
    global resources
    if resources['Trä'] >= w and resources['Sten'] >= s:
        resources['Trä'] -= w; resources['Sten'] -= s; inventory[name] = True; update_ui()

# Knappar i Crafting
Button(parent=craft_panel, text="Yxa (15 Trä, 10 Sten)", scale=(0.8,0.12), position=(0,0.1), on_click=lambda: craft('Axe', 15, 10))
Button(parent=craft_panel, text="Spjut (10 Trä, 20 Sten)", scale=(0.8,0.12), position=(0,-0.05), on_click=lambda: craft('Spear', 10, 20))
Button(parent=craft_panel, text="Fackla (10 Trä)", scale=(0.8,0.12), position=(0,-0.2), on_click=lambda: craft('Torch', 10, 0))

def input(key):
    global build_mode, crafting_mode, selected_build_item
    if key == 'c':
        crafting_mode = not crafting_mode
        craft_panel.visible, mouse.locked = crafting_mode, not crafting_mode
    
    if not crafting_mode:
        if key in '1234': switch_tool(int(key)-1)
        if key == 'b': build_mode = not build_mode; ghost.visible = build_mode

    if key == 'left mouse down' and not crafting_mode:
        # Attack/Gather
        if current_tool == 'Axe': axe_m.animate_rotation((0,-30,0), duration=0.1); axe_m.animate_rotation((30,-10,0), duration=0.1, delay=0.1)
        
        if build_mode:
            item = build_items[selected_build_item]
            if resources['Trä'] >= item['cost']:
                resources['Trä'] -= item['cost']
                Entity(model='cube', texture=item['tex'], position=ghost.position, rotation=ghost.rotation, scale=item['scale'], collider='box')
                update_ui()
        else:
            if mouse.hovered_entity:
                t = mouse.hovered_entity
                if hasattr(t, 'type'):
                    t.shake()
                    if t.type == 'tree': 
                        resources['Trä'] += 8 if current_tool == 'Axe' else 1
                        if random.random() > 0.7: resources['Bär'] += 1
                    if t.type == 'rock': resources['Sten'] += 8 if current_tool == 'Axe' else 1
                    if t.type == 'bear' and current_tool == 'Spear': t.health -= 25; t.animate_color(color.red, duration=0.1); t.animate_color(color.white, duration=0.1, delay=0.1)
                    if hasattr(t, 'health') and t.health <= 0: destroy(t)
                    update_ui()

def update():
    global hunger, health
    hunger -= time.dt * 0.1
    if hunger <= 0: health -= time.dt * 2
    if health <= 0: res_text.text = "YOU DIED"; res_text.color = color.red
    update_ui()
    if build_mode:
        item = build_items[selected_build_item]
        ghost.position = player.position + camera.forward * 5
        ghost.y = 0.1 if item['name'] == 'Golv' else 1.5
        ghost.rotation_y = player.rotation_y

# --- 6. VÄRLDSGENERERING (Texturerade objekt) ---
Sky(texture='sky_tex.png')
DirectionalLight(rotation=(45, 45, 45))
ground = Entity(model='plane', scale=200, texture='grass_tex.png', collider='box', tile_count=(20,20))

# Träd med stam-textur
for i in range(30):
    p = (random.uniform(-80,80), 0, random.uniform(-80,80))
    t = Entity(model='cube', texture='wood_tex.png', position=(p[0], 2.5, p[2]), scale=(0.8, 5, 0.8), collider='box', type='tree')
    Entity(parent=t, model='sphere', color=color.green, y=0.5, scale=3, texture='white_cube', alpha=0.9)

# Stenar med sten-textur
for i in range(20):
    p = (random.uniform(-80,80), 0.5, random.uniform(-80,80))
    Entity(model='cube', texture='stone_tex.png', position=p, scale=(random.uniform(2,4), 2, 2), collider='box', type='rock')

# Björnar med päls-textur
class Bear(Entity):
    def __init__(self, **kwargs):
        super().__init__(model='cube', texture='bear_tex.png', scale=(2, 1.5, 3), collider='box', type='bear', **kwargs)
        self.health = 100
    def update(self):
        dist = distance(self, player)
        if dist < 15:
            self.look_at(player); self.rotation_x = 0
            self.position += self.forward * time.dt * 3
            if dist < 2:
                global health; health -= time.dt * 15

for i in range(3): Bear(position=(random.uniform(-40, 40), 1, random.uniform(-40, 40)))

player = FirstPersonController()
update_ui()
app.run()