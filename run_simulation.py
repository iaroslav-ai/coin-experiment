import bpy
import mathutils
import random
import sys
import json

print("Reading config.json file ...")
config = json.load(open('config.json'))

# A rectangular grid of coins is created by
# copying one coin located at (0.0, 0.0, 50.0)
# pint in world coordinate system.

# size of coin grid in every dimension
n = 32

# distance between every coin in a grid
step = 20.0

# minimum x and y coordinates of coins in a grid
min_coord = -n * 0.5 * step
pi = 3.1415926535

print("Creating the grid of %s coins ..." % (n*n))

# set the z dimension of coin
bpy.data.objects['Cylinder'].dimensions[2] = config['cyllinder_height']

# deselect all the objects
for obj in bpy.data.objects:
    obj.select = False

# select the original cylinder
bpy.data.objects['Cylinder'].select = True

# create n*n copies; 1 cylinder is already there
for i in range(n*n-1):
    bpy.ops.object.duplicate(linked=0,mode='TRANSLATION')

cyllinders = []

# get all cylinder names
for obj in bpy.data.objects:
    if obj.name.startswith('Cylinder'):
        cyllinders.append(obj)

# move the cyllinders
idx = 0
for i in range(n):
    for j in range(n):

        obj = cyllinders[idx]

        # add initial location and orientation
        loc = obj.location
        obj.location = loc + mathutils.Vector((min_coord + i * step, min_coord + j * step, 0.0))

        rot = list(random.uniform(-pi, pi) for i in range(3))
        obj.rotation_euler = rot

        # add momentum
        obj.rigid_body.kinematic = True
        obj.keyframe_insert(data_path="rotation_euler", frame=1)
        obj.keyframe_insert(data_path="location", frame=1)
        obj.keyframe_insert(data_path="rigid_body.kinematic", frame=1)

        # make rotating motion for coin
        rot = list(rot[i] + random.uniform(-pi*5.0, pi*5.0)*0.0 for i in range(3))
        obj.rotation_euler = rot

        # make linear motion for coin
        loc = list(obj.location[i] + random.uniform(-step*0.2, step*0.2)*0.0 for i in range(3))
        obj.location = loc

        obj.rigid_body.kinematic = False
        obj.keyframe_insert(data_path="rotation_euler", frame=12)
        obj.keyframe_insert(data_path="location", frame=12)
        obj.keyframe_insert(data_path="rigid_body.kinematic", frame=12)

        idx += 1

print('Calculating the physics of falling coin ...')
bpy.ops.ptcache.bake_all(bake=True)

print('Counting the coin orientation ...')
import bpy
bpy.context.scene.frame_set(1000)

cyllinders = []

# get all cylinder names
for obj in bpy.data.objects:
    if obj.name.startswith('Cylinder'):
        cyllinders.append(obj)

edge_count = 0.0
heads_count = 0.0
tails_count = 0.0

for c in cyllinders:
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
sys.exit()

