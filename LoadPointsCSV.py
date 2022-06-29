import bpy
import csv
import numpy
from mathutils import Vector
import os
from collections import defaultdict

root = "E:\Daniel\OLA_RESEARCH\DFWORKSHOP2022\sampledata\data (2)"

filename = "umap_3d_allsounds.csv"

fullpath = os.path.join(root,filename)

csvfile = open(fullpath, 'r', newline='')
ofile = csv.reader(csvfile, delimiter=',')
verts = []
s = []
namecheck = []

pointclouds = defaultdict(list)

def create_obj(name,verts):
    obj_name = name
    mesh_data = bpy.data.meshes.new(obj_name + "data")
    obj = bpy.data.objects.new(obj_name, mesh_data)
    bpy.context.scene.collection.objects.link(obj)
    mesh_data.from_pydata(verts, [], [])

    obj.data.attributes.new(name='scaleVec', type='FLOAT', domain='POINT')

for i,row in enumerate(ofile):
    if i==0:
        print(row)
    if i!= 0:
        name = str(row[5])
            
        x,y,z = float(row[1]), float(row[2]), float(row[3])
        print(i,x,y,z)
        verts.append(Vector([x,y,z]))
        
        pointclouds[name].append(Vector([x,y,z]))     

    #print(row)

csvfile.close()

def  createclouds(pointclouds):

    for k,v in pointclouds.items():
        print(k)
        print(len(v))
        create_obj(k, v)

run = True
    
if run:
    createclouds(pointclouds)