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
        loc = obj.location
        obj.location = loc + mathutils.Vector((sn+i*step,sn+j*step,0.0))
        rot = list(random.uniform(0.0, 3.1415926535) for i in range(3))
        obj.rotation_euler = rot
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

sys.exit()

