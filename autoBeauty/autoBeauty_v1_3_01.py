###########################################
#autoBeauty.py
#Version 1.3.02
#Last updated August 08 2021
#
#Simplify the id count of the class.
#
#This module allow you to import multi passes render from the render engine Cycle
#and Redshift, let the user choose between an additive or a substractive assembly
#and finally reconstruct automaticaly the beauty. There are also denoise and sharpen
#options plus a preview of the selected pass.
###########################################

import nuke, re
import tabsCreation, commonTreeBegin, cycleTree, redshiftTree, commonTreeEnd

def user_choices():

    #:::definition of the variables:::#

    #Render engine choice menu
    render_list = ["Cycle", "Redshift"]
    render_list_cleaned = " ".join(render_list)
    #Assembly type choice menu
    assembly_type = ["Additive", "Substractive"]
    assembly_type_cleaned = " ".join(assembly_type)
    #List of the passes to use depending the render engine choice, to populate.
    channels_select = []
    new_index = 0



    #:::Panel for user choices creation:::#
    my_panel = nuke.Panel("AutoBeauty")
    my_panel.addEnumerationPulldown("Render engine", render_list_cleaned)
    my_panel.addEnumerationPulldown("Assembly type", assembly_type_cleaned)
    my_panel.addClipnameSearch("File path", "Choose a file")
    my_panel.show()


    #:::User inputs:::#
    path_file = my_panel.value("File path")
    render_choice = my_panel.value("Render engine")
    assembly_choice = my_panel.value("Assembly type")


    #Warning message if user didn't choose a ".exr" file
    try:
        if ".exr" not in path_file:
            raise ValueError

    except ValueError:
        nuke.message("Choose a multi layer file '.exr', please")
        return

    else:
        node_autobeauty = Autobeauty(path_file, render_choice, assembly_choice)


class Autobeauty:
    id = 0

    def __init__(self, path_file, render_choice, assembly_choice):
        Autobeauty.id += 1
        if Autobeauty.id < 10:
            self.new_index  = str(0) + str(Autobeauty.id)
        else:
            self.new_index = str(Autobeauty.id)
        self.path_file = path_file
        self.render_choice = render_choice
        self.assembly_choice = assembly_choice
        self.my_group = nuke.nodes.Group(name= "AUTO_BEAUTY_"+str(self.new_index)+"_"+str(self.render_choice)\
        +"_"+str(self.assembly_choice), note_font= "Bahnschrift SemiLight")
        self.read_file = None
        self.channels_to_assembly = None


        #definition of channels to extract on each render engine.
        if render_choice == "Cycle":
            channels_select =  ["DiffDir.red", "DiffInd.red", "DiffCol.red", "GlossDir.red"\
            , "GlossInd.red", "GlossCol.red", "TransDir.red", "TransInd.red", "TransCol.red", "Emit.red"]

        elif render_choice == "Redshift":
            channels_select = ["DiffuseFilter.red", "DiffuseLightingRaw.red", "Emission.red"\
            , "GIRaw.red","ReflectionsFilter.red", "ReflectionsRaw.red", "RefractionsFilter.red"\
            , "RefractionsRaw.red", "SpecularLighting.red"]


        #node Group opewning to work inside#
        self.my_group["tile_color"].setValue(5608959)
        self.my_group.begin()

        #ReadNode creation with render file path set up.
        self.read_file = nuke.nodes.Read(name = "render", xpos = 0, ypos = 0)
        self.read_file["file"].setValue(path_file)
        self.read_file_Ypos = nuke.toNode("render")["ypos"].value()
        self.read_file_Xpos = nuke.toNode("render")["xpos"].value()

        #:::channels extraction from the file:::#
        channels_extraction = self.read_file.channels()
        self.channels_to_assembly = list(set([chan.split(".")[0]for chan in channels_extraction if chan in channels_select]))
        self.channels_to_assembly.sort()


        #Check if render choice match with the render type of the file selected.
        if render_choice == "Cycle":
            if "DiffDir" not in self.channels_to_assembly:
                nuke.message("Your render choice doesn't match with the file you selected")
                nuke.delete(nuke.toNode("AUTO_BEAUTY_"+new_index+"_"+render_choice+"_"+assembly_choice))
                return
        elif render_choice == "Redshift":
            if "DiffuseFilter" not in self.channels_to_assembly:
                nuke.message("Your render choice doesn't match with the file you selected")
                nuke.delete(nuke.toNode("AUTO_BEAUTY_"+new_index+"_"+render_choice+"_"+assembly_choice))
                return


        #Beauty pass reference for QC.
        for channel in channels_extraction:
            if channel == "rgba.red":
                shuffle_beauty = nuke.nodes.Shuffle(name = "Beauty ref", xpos = 2000, ypos = 30)
                shuffle_beauty.setInput(0,self.read_file)
                shuffle_beauty.knob("in").setValue(channel[:4])
            else:
                pass


        #Split the read file into all the passes.
        position_shuffle = 340
        for channel in self.channels_to_assembly:

            #Passes extraction, creation of shuffles and a remove node.
            shuffle = nuke.nodes.Shuffle(name = channel, xpos = position_shuffle, ypos = 200)
            shuffle.setInput(0,self.read_file)
            nuke.toNode(channel).knob("in").setValue(channel)
            nuke.toNode(channel).knob("in2").setValue("alpha")
            nuke.toNode(channel).knob("alpha").setValue("red2")

            keep = nuke.nodes.Remove(name = "Keep "+ channel, xpos = position_shuffle, ypos = 300)
            keep.setInput(0, shuffle)
            keep["operation"].setValue("keep")
            keep["channels"].setValue("rgb")
            keep["channels2"].setValue("alpha")
            position_shuffle -= 85


        ##################################################################
        #:::::::::::::::::::BEAUTY RECONSTRUCTION TREE:::::::::::::::::::#
        ##################################################################
        if render_choice == "Cycle":
            pass_naming = ["Diffuse color", "Diffuse direct", "Diffuse indirect", "Emission", "Glossy color", "Glossy direct", "Glossy indirect", "Transmission color", "Transmission direct", "Transmission indirect"]
            tabsCreation.tabs_creation(self.my_group, self.channels_to_assembly, self.render_choice, self.assembly_choice, self.new_index, self.read_file, pass_naming)
            commonTreeBegin.common_tree_begin(self.my_group, self.channels_to_assembly, self.render_choice, self.assembly_choice, self.new_index, self.read_file, pass_naming)
            cycleTree.cycle_tree(self.my_group, self.channels_to_assembly, self.render_choice, self.assembly_choice, self.new_index, self.read_file, pass_naming)

        elif render_choice == "Redshift":
            pass_naming = ["Diffuse filter", "Diffuse lighting raw", "Emission", "GI raw", "Reflections filter", "Reflections raw", "Refractions filter", "Refractions raw", "Specular"]
            tabsCreation.tabs_creation(self.my_group, self.channels_to_assembly, self.render_choice, self.assembly_choice, self.new_index, self.read_file, pass_naming)
            commonTreeBegin.common_tree_begin(self.my_group, self.channels_to_assembly, self.render_choice, self.assembly_choice, self.new_index, self.read_file, pass_naming)
            redshiftTree.redshift_tree(self.my_group, self.channels_to_assembly, self.render_choice, self.assembly_choice, self.new_index, self.read_file, pass_naming)

        #End of common tree
        commonTreeEnd.common_tree_end(self.my_group, self.channels_to_assembly, self.render_choice, self.assembly_choice, self.new_index, self.read_file, pass_naming)

        ##################################################################
        #::::::::::::::::::::::::::KNOB CHANGED::::::::::::::::::::::::::#
        ##################################################################
        nuke.toNode("AUTO_BEAUTY_"+str(self.new_index)+"_"+render_choice+"_"+assembly_choice).knob("knobChanged").setValue("autoBeauty_v1_3_02.visibility()")

def visibility():
    ###########################################################################################################
    #Function called by the knob changed, make some parameters in the denoise and sharpen tab visible or not.
    #param: None
    #return: None
    ###########################################################################################################
    x = nuke.thisNode()

    #Get the variables to identify the node.
    if "Cycle" in x["name"].value():
        render_choice = "Cycle"
    elif "Redshift" in x["name"].value():
        render_choice = "Redshift"

    if "Additive" in x["name"].value():
        assembly_choice = "Additive"
    elif "Substractive" in x["name"].value():
        assembly_choice = "Substractive"
    pass_select = x["par_pass_select_denoise"].value()

    current_index_lst = re.findall("[0-90-9]", x["name"].value())
    index = current_index_lst[0]+current_index_lst[1]


    #Denoise options.
    if x["par_onOff_den_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+pass_select].value() == True:
        x["par_reg_analys_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+pass_select].setVisible(True)
        x["par_den_amount_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+pass_select].setVisible(True)
        x["par_analysis_den_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+pass_select].setVisible(True)
    else:
        x["par_reg_analys_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+pass_select].setVisible(False)
        x["par_den_amount_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+pass_select].setVisible(False)
        x["par_analysis_den_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+pass_select].setVisible(False)


    #Sharpen option.
    if x["par_onOff_sharp_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+pass_select].value() == True:
        x["par_min_sharp_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+pass_select].setVisible(True)
        x["par_max_sharp_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+pass_select].setVisible(True)
        x["par_sharp_amount_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+pass_select].setVisible(True)
        x["par_size_sharp_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+pass_select].setVisible(True)
    else:
        x["par_min_sharp_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+pass_select].setVisible(False)
        x["par_max_sharp_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+pass_select].setVisible(False)
        x["par_sharp_amount_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+pass_select].setVisible(False)
        x["par_size_sharp_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+pass_select].setVisible(False)

    #Render options.
    channels_export = nuke.toNode("AUTO_BEAUTY_"+str(index)+"_"+render_choice+"_"+assembly_choice)["par_channels_export_"+render_choice+"_"+assembly_choice+"_"+str(index)].value()
    nuke.toNode("Write beauty_"+render_choice+"_"+assembly_choice+"_"+str(index))["channels"].setValue(channels_export)
    path_export = nuke.toNode("AUTO_BEAUTY_"+str(index)+"_"+render_choice+"_"+assembly_choice)["par_file_"+render_choice+"_"+assembly_choice+"_"+str(index)].value()
    nuke.toNode("Write beauty_"+render_choice+"_"+assembly_choice+"_"+str(index))["file"].setValue(path_export)
    select_format_export = nuke.toNode("AUTO_BEAUTY_"+str(index)+"_"+render_choice+"_"+assembly_choice)["par_file_type_"+render_choice+"_"+assembly_choice+"_"+str(index)].value()
    nuke.toNode("Write beauty_"+render_choice+"_"+assembly_choice+"_"+str(index))["file_type"].setValue(select_format_export)

def show_pass():
    ################################################################################
    #Display the selected pass when button is press in the denoise tab.
    #param: None
    #return:None
    ###############################################################################
    y = nuke.thisNode()

    #Get the variables to identify the node.
    if "Cycle" in y["name"].value():
        render_choice = "Cycle"
    elif "Redshift" in y["name"].value():
        render_choice = "Redshift"

    if "Additive" in y["name"].value():
        assembly_choice = "Additive"
    elif "Substractive" in y["name"].value():
        assembly_choice = "Substractive"

    if render_choice == "Cycle":
        pass_naming = {"DiffCol":"Diffuse color", "DiffDir":"Diffuse direct", "DiffInd":"Diffuse indirect", "Emit":"Emission", "GlossCol":"Glossy color", "GlossDir":"Glossy direct", "GlossInd":"Glossy indirect", "TransCol":"Transmission color", "TransDir":"Transmission direct", "TransInd":"Transmission indirect"}
    elif render_choice == "Redshift":
        pass_naming = ["Diffuse filter", "Diffuse lighting raw", "Emission", "GI raw", "Reflections filter", "Reflections raw", "Refractions filter", "Refractions raw", "Specular"]

    #index = y["name"].value()[12]
    current_index_lst = re.findall("[0-90-9]", y["name"].value())
    index = current_index_lst[0]+current_index_lst[1]
    pass_select = y["par_pass_select_denoise"].value()

    #Connect the right output.
    nuke.toNode("Dot preview").setInput(0, nuke.toNode("text_channel_display "+pass_select))
    nuke.toNode("Dot preview")["hide_input"].setValue(True)
    nuke.toNode("Switch preview")["which"].setValue(1)

    #Make the denoise/sharpen options accessible when the pass button is press.
    y["par_onOff_den_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+pass_select].setVisible(True)
    y["par_onOff_sharp_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+pass_select].setVisible(True)

def show_beauty():
    ####################################################################
    #Display the beauty pass when button is press in the denoise tab.
    #param: None
    #return: None
    #####################################################################
    nuke.toNode("Switch preview")["which"].setValue(0)

def analyze_noise_execution():
    ####################################################################
    #Execute the analysis button in the denoise node.
    #param: None
    #return: None
    #####################################################################
    y = nuke.thisNode()

    #Get the variables to identify the node.
    if "Cycle" in y["name"].value():
        render_choice = "Cycle"
    elif "Redshift" in y["name"].value():
        render_choice = "Redshift"

    if "Additive" in y["name"].value():
        assembly_choice = "Additive"
    elif "Substractive" in y["name"].value():
        assembly_choice = "Substractive"

    pass_select = y["par_pass_select_denoise"].value()


    nuke.show(nuke.toNode("Denoise "+pass_select))
    n = nuke.toNode("Denoise "+pass_select)
    n.knob("analyze").execute()
    n.hideControlPanel()
    nuke.show(nuke.toNode("AUTO_BEAUTY_"+str(self.new_index)+"_"+render_choice+"_"+assembly_choice))

def render():
    ####################################################################
    #Execute the render button in the render tab.
    #param: None
    #return: None
    #####################################################################
    z = nuke.thisNode()

    if "Cycle" in z["name"].value():
        render_choice = "Cycle"
    elif "Redshift" in z["name"].value():
        render_choice = "Redshift"

    if "Additive" in z["name"].value():
        assembly_choice = "Additive"
    elif "Substractive" in z["name"].value():
        assembly_choice = "Substractive"

    current_index_lst = re.findall("[0-90-9]", z["name"].value())
    index = current_index_lst[0]+current_index_lst[1]

    nuke.execute(nuke.toNode("Write beauty_"+render_choice+"_"+assembly_choice+"_"+str(index)))
