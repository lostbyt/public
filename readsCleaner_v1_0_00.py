###########################################
#readsCleaner.py
#Version 1.0.00
#Last updated August 08 2021
#
#Order the read nodes selected by ascending frame_range, descending frame range or name.
#
#
###########################################
import nuke, re


#Variables declaration
reads_list =[]
regex = re.compile(r"\/(\w+)")
reads_dict = {}

def readsCleaner():
    noop = nuke.nodes.NoOp(name = "\n"+"READS"+"\nCLEANER"+"\n")
    noop["tile_color"].setValue(5608959)


    #:::::::::::::::::::::::::::::::#
    #::::::::UI construction::::::::#
    #:::::::::::::::::::::::::::::::#
    add_all_reads      = nuke.PyScript_Knob("adds_all_reads", "Add all reads", "readsCleaner.add_all_reads()")
    add_selected_reads = nuke.PyScript_Knob("add_selected_reads", "Add read(s) selected", "readsCleaner.add_selected_reads()")
    divider_01         = nuke.Text_Knob("divider_01", "")
    list_display       = nuke.Text_Knob("list_display", "List of reads selected: ")
    divider_02         = nuke.Text_Knob("divider02", "")
    clean_reads_button = nuke.PyScript_Knob("clear_reads", "Clear list of reads", "readsCleaner.clear_reads()")
    divider_03         = nuke.Text_Knob("divider03", "")
    asc_order_button   = nuke.PyScript_Knob("asc_order", "Ascending order", "readsCleaner.frame_range_order('asc')")
    desc_order_button  = nuke.PyScript_Knob("desc_order", "Descending order", "readsCleaner.frame_range_order('desc')")
    name_order_button  = nuke.PyScript_Knob("name_order", "Name order", "readsCleaner.name_order()")

    noop.addKnob(add_all_reads)
    noop.addKnob(add_selected_reads)
    noop.addKnob(divider_01)
    noop.addKnob(list_display)
    noop["list_display"].clearFlag(nuke.STARTLINE)
    noop.addKnob(divider_02)
    noop.addKnob(clean_reads_button)
    noop.addKnob(divider_03)
    noop.addKnob(asc_order_button)
    noop.addKnob(desc_order_button)
    noop.addKnob(name_order_button)
    noop["name_order"].clearFlag(nuke.STARTLINE)

def add_all_reads():
    for node in nuke.allNodes("Read"):
        if node["name"].value() not in reads_list:
            reads_list.append(node["name"].value())

    read_list_display = "\n".join(reads_list)
    nuke.thisNode()["list_display"].setValue(read_list_display)

def add_selected_reads():
    for node in nuke.allNodes("Read"):
        if node.knob("selected").getValue() == True:
            if node["name"].value() not in reads_list:
                reads_list.append(node["name"].value())

    read_list_display = "\n".join(reads_list)
    nuke.thisNode()["list_display"].setValue(read_list_display)

def clear_reads():
    global reads_list
    reads_list = []
    nuke.thisNode()["list_display"].setValue("")

def frame_range_order(order):
    nodes_dict = {}

    for node in nuke.allNodes("BackdropNode"):
        if "frames" in node["label"].value():
            nuke.delete(node)

    for name in reads_list:
        frame_range_node = int(nuke.toNode(name)["origlast"].value()) - int(nuke.toNode(name)["origfirst"].value())
        nodes_dict[name] = frame_range_node

    if order == "desc":
        x = 50
        y = 100
        while nodes_dict:
            node_name  = min(nodes_dict, key = nodes_dict.get)
            s = nuke.toNode(node_name)
            s["selected"].setValue(True)
            s.setXpos(x)
            s.setYpos(y)
            b = nuke.nodes.BackdropNode(label = str(nodes_dict[node_name]) + " frames", xpos = nuke.toNode(node_name)["xpos"].getValue()-10,\
            ypos = nuke.toNode(node_name)["ypos"].getValue()-100, bdheight = 200, bdwidth = 100)
            x += 300
            nodes_dict.pop(node_name)
        return

    elif order == "asc":
        x = 50
        y = 100
        while nodes_dict:
            node_name  = max(nodes_dict, key = nodes_dict.get)
            s = nuke.toNode(node_name)
            s["selected"].setValue(True)
            s.setXpos(x)
            s.setYpos(y)
            b = nuke.nodes.BackdropNode(label = str(nodes_dict[node_name]) + " frames", xpos = nuke.toNode(node_name)["xpos"].getValue()-10,\
            ypos = nuke.toNode(node_name)["ypos"].getValue()-100, bdheight = 200, bdwidth = 100)
            x += 300
            nodes_dict.pop(node_name)
        return

def name_order():
    nodes_dict = {}
    sorted_nodes = []

    for node in nuke.allNodes("BackdropNode"):
        if "frames" in node["label"].value():
            nuke.delete(node)

    for node in reads_list:
        path = nuke.toNode(node)["file"].value()
        name = re.findall(regex, path)
        nodes_dict[node] = name[-1]

    x = 50
    y = 100
    while nodes_dict:
        key_lowest_node_name = min(nodes_dict, key = lambda k: nodes_dict[k])
        value_lowest_node_name = nodes_dict[min(nodes_dict, key = lambda k: nodes_dict[k])]
        s = nuke.toNode(key_lowest_node_name)
        s["selected"].setValue(True)
        s.setXpos(x)
        s.setYpos(y)
        b = nuke.nodes.BackdropNode(label = str(nodes_dict[key_lowest_node_name]) + " frames", xpos = nuke.toNode(key_lowest_node_name)["xpos"].getValue()-10,\
        ypos = nuke.toNode(key_lowest_node_name)["ypos"].getValue()-100, bdheight = 200, bdwidth = 100)
        x += 300
        nodes_dict.pop(key_lowest_node_name)
    return
