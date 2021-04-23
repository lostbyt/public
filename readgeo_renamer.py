#april 23, V0.1
#This code allow the nuke user to rename all the geometry imported from a 3D software
#with the same name used in the 3D package it comes from

import nuke
import re

for node in nuke.allNodes("ReadGeo2"):
    
    #search pattern definition
    regex = re.compile(r"\/(\w+)")
    
    #geometry path extraction, return a list with one string path
    abc_path = node['scene_view'].getSelectedItems()
    
    #list creation regex
    obj_name = re.findall(regex, abc_path[0])
    
    #set readgeo label knob with original nmae used in 3d software
    node["label"].setValue(obj_name[1])
    
