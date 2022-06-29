import sys, os
import json
import bpy
import mathutils
import numpy as np

RUN = True

RESULTS_PATH = 'Orig_results'

PASSES = ['Image','Normal', 'Alpha','Shadow','AO','Depth']

VIEWS = 500
RESOLUTION = 1080

DEPTH_SCALE = 100
COLOR_DEPTH = 8
FORMAT = 'PNG'




rootpath = bpy.path.abspath(f"//{RESULTS_PATH}")
print(rootpath)

outputs = {}


for p in PASSES:
    fp = os.path.join(rootpath,p)
    outputs[p] = {"base_path":fp}
    if not os.path.exists(fp):
        print(fp)
        os.makedirs(fp)


# Render Optimizations
bpy.context.scene.render.use_persistent_data = True

# Set up rendering of depth map.
bpy.context.scene.use_nodes = True
tree = bpy.context.scene.node_tree
links = tree.links

# Add passes for additionally dumping albedo and normals.
#bpy.context.scene.view_layers["RenderLayer"].use_pass_normal = True
render_layers = tree.nodes.new('CompositorNodeRLayers')
render_layers.location = 0,0


scene = bpy.context.scene
scene.render.resolution_x = RESOLUTION
scene.render.resolution_y = RESOLUTION
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'

for i,k in enumerate(outputs.keys()):
    
    output = tree.nodes.new(type="CompositorNodeOutputFile")
    output.label = k
    output.location = 600, i*100
    output.base_path = outputs[k]['base_path'] 
    links.new(render_layers.outputs[k], output.inputs[0])
    
    outputs[k].update({"output_node":output})



# Remap as other types can not represent the full range of depth.
map = tree.nodes.new(type="CompositorNodeMapRange")
map.location = (300,0) 
map.inputs[1].default_value = 0 #from min
map.inputs[2].default_value = DEPTH_SCALE #from max

links.new(render_layers.outputs['Depth'], map.inputs[0])

links.new(map.outputs[0], outputs['Depth']['output_node'].inputs[0])
    


cam = scene.objects['CameraMove']
print(cam.location)
print(scene.frame_end)




if RUN:
    bpy.ops.render.render(animation=True, write_still=True)





