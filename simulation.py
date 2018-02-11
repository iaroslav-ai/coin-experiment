import bpy
import mathutils
import random
import sys
import json

# This enables necessary 'impulse.py' plugin
import os
path = os.getcwd()
impulse_path = os.path.join(path, 'impulse.py')
bpy.ops.wm.addon_install(filepath=impulse_path)
bpy.ops.wm.addon_enable(module='impulse')
bpy.ops.wm.save_userpref()

print("Reading config.json file ...")
config = json.load(open('config.json'))

scn = bpy.context.scene

# A rectangular grid of coins is created by
# copying one coin located at (0.0, 0.0, 50.0)
# point in world coordinate system.
coin_thickness = config['coin_thickness'] # in cm
coin_diameter = config['coin_diameter'] # in cm

n = config['coin_grid_size'] # size of coin grid in every dimension
grid_step = config['coin_grid_step'] # distance between every coin in a grid, cm
angular_velocity_std = config['angular_velocity_std'] # cm/s, standard deviation of normal distribution of angular speeds
linear_velocity_std = config['linear_velocity_std'] # cm/s, standard deviation of normal distribution of linear speeds
coin_density = config['coin_density'] # grams / cm^3
coin_friction = config['coin_friction'] # friction of coin
coin_restitution = config['coin_restitution'] # bounciness/restitution of coin
table_friction = config['table_friction'] # friction of coin
table_restitution = config['table_restitution'] # bounciness/restitution of coin
# Some data sources
# material densities: http://www.semicore.com/reference/density-reference
# friction coefficients: https://en.wikipedia.org/wiki/Friction#Approximate_coefficients_of_friction
# restitution coefficients: https://hypertextbook.com/facts/2006/restitution.shtml

# Configuration of simulation
exit_when_done = config['exit_when_done']

# minimum x and y coordinates of coins in a grid
min_coord = -n * 0.5 * grid_step
pi = 3.1415926535

# names of objects
coin_name = 'Coin'
table_name = 'Table'

print("Creating a grid of %s coins ..." % (n*n))

# set the thickness of a coin
bpy.data.objects[coin_name].dimensions[0] = coin_diameter
bpy.data.objects[coin_name].dimensions[1] = coin_diameter
bpy.data.objects[coin_name].dimensions[2] = coin_thickness

# deselect all the objects
for obj in bpy.data.objects:
    obj.select = False

# select the original cylinder
coin_orig = bpy.data.objects[coin_name]
table = bpy.data.objects[table_name]
coin_orig.select = True

# set the rigid body properties
coin_orig.rigid_body.friction = coin_friction
coin_orig.rigid_body.restitution = coin_restitution
# mass = volume * density; density in miligram / cm^3
coin_radius = coin_diameter / 2.0
coin_orig.rigid_body.mass = (pi * coin_thickness * coin_radius * coin_radius) * coin_density * 1000.0

table.rigid_body.friction = table_friction
table.rigid_body.restitution = table_restitution

# create n*n copies; 1 cylinder is already there
for i in range(n*n-1):
    bpy.ops.object.duplicate(linked=0,mode='TRANSLATION')

coin_orig.select = False
coins = []

def normal_v_vector(sigma=1.0, sz=3):
    return tuple(random.normalvariate(0.0, sigma) for _ in range(sz))

# code that does uniform rotation of the object
def rotate_uniform(s):
    """Apply rotation such that every orientation of
    object is equally likely. See misc/check_uniform_rotations.blend
    for verification."""
    o = normal_v_vector()
    DirectionVector = mathutils.Vector(o)
    s.rotation_mode = 'QUATERNION'
    s.rotation_quaternion = DirectionVector.to_track_quat('Z','Y')
    s.rotation_mode = 'XYZ'


# get all coins
for obj in bpy.data.objects:
    if obj.name.startswith(coin_name):
        coins.append(obj)

# move the cyllinders
idx = 0
for i in range(n):
    for j in range(n):
        obj = coins[idx]
        idx += 1

        # add initial location and orientation
        loc = obj.location
        obj.location = loc + mathutils.Vector((min_coord + i * grid_step, min_coord + j * grid_step, 0.0))

        rotate_uniform(obj)

        # add object to impulse
        bpy.context.scene.objects.active = obj
        bpy.ops.rigidbody.impulse_add_object()
        # All speeds are in cm/s; The values in Impulse plugin do not take into
        # account the scaling of blender units.
        obj.impulse_props.v = normal_v_vector(linear_velocity_std)
        obj.impulse_props.av = normal_v_vector(angular_velocity_std)

# for some reason double call to the function is needed to make it work :/
bpy.ops.rigidbody.impulse_execute()
bpy.ops.rigidbody.impulse_execute()

# calculate necessary physics
print('Simulating falling coins ...')
bpy.ops.ptcache.bake_all(bake=True)

print('Counting the coin orientation ...')
bpy.context.scene.frame_set(1000)

edge_count = 0.0
heads_count = 0.0
tails_count = 0.0

for c in coins:
    mesh = c.data
    mat = c.matrix_world

    # Coordinates of points on heads and tails edge.
    # Let coordinate system be located in the center
    # of the cylinder of height h. Then two points are
    # considered:
    # Tails=(0.0, 1.0, -0.5h), Heads=(0.0, 1.0, 0.5h)
    # Both points are converted into world coordinate
    # system, and thus represent orientation of cylinder.
    # relative to the table, which is a flat surface with
    # constant z value.
    # Tails
    tx, ty, tz = mat * mesh.vertices[0].co
    # Heads
    hx, hy, hz = mat * mesh.vertices[1].co

    # if the cylinder is laying, then bz ~ tz
    if abs(tz - hz) < 0.01:
        edge_count += 1.0

    # if the x and y coordinates coincide, the cylinder has
    # fallen either on heads or tails
    if abs(tx - hx) < 0.01 and abs(ty - hy) < 0.01:
        if hz < tz: # coin settled on tails
            tails_count += 1.0
        else:
            heads_count += 1.0

result = {
    'Edge': edge_count,
    'Tails': tails_count,
    'Heads': heads_count,
}

json.dump(
    result,
    open('result.json', 'w')
)

print(result)
print('Done!')

if exit_when_done:
    sys.exit()
