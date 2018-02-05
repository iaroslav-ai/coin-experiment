import bpy
import mathutils
import random
import sys
import json

print("Reading config.json file ...")

config = json.load(open('config.json'))

print("Creating the mesh of coins ...")

n = 32
step = 20.0
sn = -n*0.5*step
pi = 3.1415926535

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
        obj.location = loc + mathutils.Vector((sn+i*step,sn+j*step,0.0))
        rot = list(random.uniform(-pi, pi) for i in range(3))
        obj.rotation_euler = rot

        # add momentum
        obj.rigid_body.kinematic = True
        obj.keyframe_insert(data_path="rotation_euler", frame=1)
        obj.keyframe_insert(data_path="location", frame=1)
        obj.keyframe_insert(data_path="rigid_body.kinematic", frame=1)

        rot = list(rot[i] + random.uniform(-pi*5.0, pi*5.0)*0.0 for i in range(3))
        obj.rotation_euler = rot
        loc = list(obj.location[i] + random.uniform(-step*0.2, step*0.2)*0.0 for i in range(3))
        obj.location = loc

        obj.rigid_body.kinematic = False
        obj.keyframe_insert(data_path="rotation_euler", frame=12)
        obj.keyframe_insert(data_path="location", frame=12)
        obj.keyframe_insert(data_path="rigid_body.kinematic", frame=12)

        idx += 1

print('Baking physics ... ')
bpy.ops.ptcache.bake_all(bake=True)

print('Counting the laying or standing coins ...')
import bpy
bpy.context.scene.frame_set(1000)

cyllinders = []

# get all cylinder names
for obj in bpy.data.objects:
    if obj.name.startswith('Cylinder'):
        cyllinders.append(obj)

print('Start count ...')
standing_count = 0.0

for c in cyllinders:
    loc, rot, scale = c.matrix_world.decompose()
    laying=any([abs(v) < 0.01 for v in (rot.x, rot.y, rot.z)])
    #print(rot, laying)
    standing_count += 0.0 if laying else 1.0

json.dump({'Standing': standing_count, 'Total': len(cyllinders)*1.0}, open('result.json', 'w'))

#sys.exit()

