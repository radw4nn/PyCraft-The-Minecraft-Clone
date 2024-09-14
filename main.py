from ursina import *  # Import everything from the Ursina engine
from ursina.prefabs.first_person_controller import FirstPersonController  # Import the FirstPersonController prefab for player movement

# Create an instance of the Ursina application
app = Ursina()

# Load textures for different types of blocks and other objects
grass_texture = load_texture('assets/grass_block.png')
stone_texture = load_texture('assets/stone_block.png')
brick_texture = load_texture('assets/brick_block.png')
dirt_texture  = load_texture('assets/dirt_block.png')
sky_texture   = load_texture('assets/skybox.png')
arm_texture   = load_texture('assets/arm_texture.png')

# Load sound for when the player punches (interacts with blocks)
punch_sound   = Audio('assets/punch_sound', loop=False, autoplay=False)

# Variable to keep track of the selected block type (1 for grass, 2 for stone, etc.)
block_pick = 1

# Disable the frames-per-second counter and the exit button in the window
window.fps_counter.enabled = False
window.exit_button.visible = False

# Function to update the game state every frame
def update():
    global block_pick

    # Activate hand animation if left or right mouse button is held down
    if held_keys['left mouse'] or held_keys['right mouse']:
        hand.active()
    else:
        hand.passive()

    # Change block type based on number key pressed
    if held_keys['1']: block_pick = 1
    if held_keys['2']: block_pick = 2
    if held_keys['3']: block_pick = 3
    if held_keys['4']: block_pick = 4

# Define a class for the Voxel (block) object
class Voxel(Button):
    def __init__(self, position=(0,0,0), texture=grass_texture):
        # Initialize the button (voxel) with its position, model, texture, etc.
        super().__init__(
            parent=scene,
            position=position,
            model='assets/block',
            origin_y=0.5,  # Set the origin point on the Y-axis
            texture=texture,
            color=color.color(0, 0, random.uniform(0.9, 1)),  # Randomly vary the color brightness
            scale=0.5  # Set block size
        )

    # Handle input events (mouse clicks)
    def input(self, key):
        if self.hovered:  # If the mouse is hovering over the block
            if key == 'left mouse down':  # Place a block when left mouse button is pressed
                punch_sound.play()  # Play punch sound
                # Place different blocks based on the selected block type
                if block_pick == 1: voxel = Voxel(position=self.position + mouse.normal, texture=grass_texture)
                if block_pick == 2: voxel = Voxel(position=self.position + mouse.normal, texture=stone_texture)
                if block_pick == 3: voxel = Voxel(position=self.position + mouse.normal, texture=brick_texture)
                if block_pick == 4: voxel = Voxel(position=self.position + mouse.normal, texture=dirt_texture)

            if key == 'right mouse down':  # Destroy block when right mouse button is pressed
                punch_sound.play()  # Play punch sound
                destroy(self)  # Destroy the block

# Define a class for the Sky object
class Sky(Entity):
    def __init__(self):
        # Initialize the sky with a large sphere model and a sky texture
        super().__init__(
            parent=scene,
            model='sphere',
            texture=sky_texture,
            scale=150,  # Make the sky large
            double_sided=True  # Make the sky visible from inside
        )

# Define a class for the player's Hand (seen in first-person view)
class Hand(Entity):
    def __init__(self):
        # Initialize the hand with its model, texture, and position
        super().__init__(
            parent=camera.ui,  # Attach the hand to the camera (UI layer)
            model='assets/arm',
            texture=arm_texture,
            scale=0.2,  # Size of the hand
            rotation=Vec3(150, -10, 0),  # Initial rotation of the hand
            position=Vec2(0.4, -0.6)  # Initial position of the hand
        )

    # Move hand to an active position when interacting (e.g., punching or placing blocks)
    def active(self):
        self.position = Vec2(0.3, -0.5)

    # Move hand back to a passive position when not interacting
    def passive(self):
        self.position = Vec2(0.4, -0.6)

# Generate a grid of voxels (blocks) to create the ground
for z in range(20):
    for x in range(20):
        voxel = Voxel(position=(x, 0, z))  # Create a voxel at each grid position

# Create the player using the FirstPersonController prefab
player = FirstPersonController()

# Create the sky and hand entities
sky = Sky()
hand = Hand()

# Run the Ursina application (starts the game loop)
app.run()
