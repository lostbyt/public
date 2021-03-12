###########################################
#autoBeauty.py
#Version 1.0.8
#Last updated March 11 2021
#This module allow you to import multi passes render from the render engine Cycle
#and Redshift, let the user choose between an additive or a substractive assembly
#and finally reconstruct automaticaly the beauty. There are also denoise and sharpen
#options plus a preview of the selected pass.
###########################################

import nuke

index = 0
ids = ["node_autobeauty_" + str(i) for i in range(50)]


def Render_assembly_choice():
    ##################################################
    #::::::::::::::::User choices menu:::::::::::::::#
    ##################################################

    #Maximum of AutoBeauty nodes determined by number of inner class in the class Autobeauty (line 71)
    global index
    if index == 9:
        nuke.message("You reached the maximum number of AutoBeauty nodes")
        return

    #Render engine choice menu
    render_list = ["Cycle", "Redshift"]
    render_list_cleaned = " ".join(render_list)

    #Assembly type choice menu
    assembly_type = ["Additive", "Substractive"]
    assembly_type_cleaned = " ".join(assembly_type)

    #List of the passes to use depending the render engine choice, to populate.
    channels_select = []

    #Panel creation.
    my_panel = nuke.Panel("AutoBeauty")
    my_panel.addEnumerationPulldown("Render engine", render_list_cleaned)
    my_panel.addEnumerationPulldown("Assembly type", assembly_type_cleaned)
    my_panel.addClipnameSearch("File path", "Choose a file")
    my_panel.show()


    #variables user input
    path_file = my_panel.value("File path")
    render_choice = my_panel.value("Render engine")
    assembly_choice = my_panel.value("Assembly type")

    #Warning msg if user didn't specifiy a file to import.
    if path_file == "Choose a file" :
        nuke.message("Choose a file please")
        return


    #Check if there's already auro beauty nodes in the script.
    global index
    for node in nuke.allNodes():
        if "AUTO_BEAUTY_" in node["name"].value():
            if int(node["name"].value()[12]) >= index:
                index = int(node["name"].value()[12]) + 1


    #Main instance creation to call the construct method.
    director = Constructor()
    director.construct(ids[index], path_file, render_choice, assembly_choice, index)
    return director

class Autobeauty:
    #Pre-made instances for the call of Construct method.
    class node_autobeauty_0:
        pass
    class node_autobeauty_1:
        pass
    class node_autobeauty_2:
        pass
    class node_autobeauty_3:
        pass
    class node_autobeauty_4:
        pass
    class node_autobeauty_5:
        pass
    class node_autobeauty_6:
        pass
    class node_autobeauty_7:
        pass
    class node_autobeauty_8:
        pass
    class node_autobeauty_9:
        pass

class Constructor:
    def __init__(self):
        self.allids = []



    def construct(self, buildername, path_file, render_choice, assembly_choice, index):
        targetId = getattr(Autobeauty, buildername)
        instance = targetId
        self.allids.append(instance)
        setattr(instance, "path_file", path_file)
        setattr(instance, "render", render_choice)
        setattr(instance, "assembly", assembly_choice)
        setattr(instance, "index", index)

        self.my_group = nuke.nodes.Group(name= "AUTO_BEAUTY_"+str(index)+"_"+render_choice+"_"+assembly_choice, note_font= "Bahnschrift SemiLight")
        self.read_files = None
        self.channels_to_assembly = None
        self.name = "node_"+str(index)


        #definition of channels to extract on each render engine.
        if render_choice == "Cycle":
            channels_select =  ["DiffDir.red", "DiffInd.red", "DiffCol.red", "GlossDir.red", "GlossInd.red", "GlossCol.red", "TransDir.red", "TransInd.red", "TransCol.red", "Emit.red"]
        elif render_choice == "Redshift":
            channels_select = ["DiffuseFilter.red", "DiffuseLightingRaw.red", "Emission.red", "GIRaw.red","ReflectionsFilter.red", "ReflectionsRaw.red", "RefractionsFilter.red", "RefractionsRaw.red", "SpecularLighting.red" ]


        #Group creation.
        self.my_group["tile_color"].setValue(5608959)
        self.my_group.begin()

        #ReadNode creation with render file path set up.
        self.readFile= nuke.nodes.Read(name = "render", xpos = 0, ypos = 0)
        self.readFile["file"].setValue(path_file)
        self.readFile_Ypos = nuke.toNode("render")["ypos"].value()
        self.readFile_Xpos = nuke.toNode("render")["xpos"].value()

        #channels extraction from the file.
        channels_extraction = self.readFile.channels()
        self.channels_to_assembly = list(set([chan.split(".")[0]for chan in channels_extraction if chan in channels_select]))
        self.channels_to_assembly.sort()

        #Check if render choice match with the render type of the file selected.
        if render_choice == "Cycle":
            if "DiffDir" not in self.channels_to_assembly:
                nuke.message("Your render choice doesn't match with the file you selected")
                nuke.delete(nuke.toNode("AUTO_BEAUTY_"+str(index)+"_"+render_choice+"_"+assembly_choice))
                return
        elif render_choice == "Redshift":
            if "DiffuseFilter" not in self.channels_to_assembly:
                nuke.message("Your render choice doesn't match with the file you selected")
                nuke.delete(nuke.toNode("AUTO_BEAUTY_"+str(index)+"_"+render_choice+"_"+assembly_choice))
                return



        #Beauty pass reference for QC.
        for channel in channels_extraction:
            if channel == "rgba.red":
                shuffle_beauty = nuke.nodes.Shuffle(name = "Beauty ref", xpos = 2000, ypos = 0)
                shuffle_beauty.setInput(0,self.readFile)
                shuffle_beauty.knob("in").setValue(channel[:4])



        #Split the read file into all the passes.
        position_shuffle = 340
        for channel in self.channels_to_assembly:


            #Passes extraction, creation of shuffles and a remove node.
            shuffle = nuke.nodes.Shuffle(name = channel, xpos = position_shuffle, ypos = 200)
            shuffle.setInput(0,self.readFile)
            nuke.toNode(channel).knob("in").setValue(channel)
            nuke.toNode(channel).knob("in2").setValue("alpha")
            nuke.toNode(channel).knob("alpha").setValue("red2")

            keep = nuke.nodes.Remove(name = "Keep "+ channel, xpos = position_shuffle, ypos = 300)
            keep.setInput(0, shuffle)
            keep["operation"].setValue("keep")
            keep["channels"].setValue("rgb")
            keep["channels2"].setValue("alpha")
            position_shuffle -= 85


        if render_choice == "Cycle":
            pass_naming = ["Diffuse color", "Diffuse direct", "Diffuse indirect", "Emission", "Glossy color", "Glossy direct", "Glossy indirect", "Transmission color", "Transmission direct", "Transmission indirect"]
        elif render_choice == "Redshift":
            pass_naming = ["Diffuse filter", "Diffuse lighting raw", "Emission", "GI raw", "Reflections filter", "Reflections raw", "Refractions filter", "Refractions raw", "Specular"]



        ##################################################################
        #::::::::::::::::Tabs with knobs creation on group:::::::::::::::#
        ##################################################################
        #INFOS TAB
        #Messages to the user with the name of the passes supported for each render engine.
        tab_warning = nuke.Tab_Knob("Infos")
        self.my_group.addKnob(tab_warning)
        message1 = "V1.0.7 emmanuel moulun"
        warning_message1 = nuke.Text_Knob(message1)
        self.my_group.addKnob(warning_message1)

        message2 = ""
        warning_message2 = nuke.Text_Knob(message2)
        self.my_group.addKnob(warning_message2)

        message3 = "CYCLE PASSES EXPECTED:"
        warning_message3 = nuke.Text_Knob(message3)
        self.my_group.addKnob(warning_message3)

        message4 = "RGBA, Diffuse, Glossy, Transmission, Emission"
        warning_message4 = nuke.Text_Knob(message4)
        self.my_group.addKnob(warning_message4)

        message5 = ""
        warning_message5 = nuke.Text_Knob(message5)
        self.my_group.addKnob(warning_message5)

        message6 = "REDSHIFT PASSES EXPECTED:"
        warning_message6 = nuke.Text_Knob(message6)
        self.my_group.addKnob(warning_message6)

        message7 = "RGBA, DiffuseLighting Raw, Emission, GI raw"
        warning_message7 = nuke.Text_Knob(message7)
        self.my_group.addKnob(warning_message7)

        message8 = "Reflections Raw, Refractions Raw, SpecularLighting"
        warning_message8 = nuke.Text_Knob(message8)
        self.my_group.addKnob(warning_message8)



        #DENOISE/SHARPEN TAB.
        #Tabs creations, instructions messages.
        tab_denoise = nuke.Tab_Knob("Denoise/ Sharpen")

        self.my_group.addKnob(tab_denoise)
        pass_selection = nuke.Enumeration_Knob("par_pass_select_denoise", "Pass to preview", self.channels_to_assembly)
        self.my_group.addKnob(pass_selection)

        show_pass_denoise = nuke.PyScript_Knob("par_show_pass_den", "Preview pass", "autoBeauty_v207.show_pass()")
        self.my_group.addKnob(show_pass_denoise)
        show_beauty_reconstructed = nuke.PyScript_Knob("par_show_beauty_recon", "Back to beauty", "autoBeauty_v207.show_beauty()")
        self.my_group.addKnob(show_beauty_reconstructed)
        self.my_group["par_show_pass_den"].setFlag(nuke.STARTLINE)

        message9 = ""
        warning_message9 = nuke.Text_Knob(message9)
        self.my_group.addKnob(warning_message9)

        message10 = "To access the denoise/sharpen options"
        warning_message10 = nuke.Text_Knob(message10)
        self.my_group.addKnob(warning_message10)

        message11 = "select the desired pass in the \"preview pass\" menu"
        warning_message11 = nuke.Text_Knob(message11)
        self.my_group.addKnob(warning_message11)

        message12 = "then, tick the denoise/sharpen boxes"
        warning_message12 = nuke.Text_Knob(message12)
        self.my_group.addKnob(warning_message12)

        message13 = ""
        warning_message13 = nuke.Text_Knob(message13)
        self.my_group.addKnob(warning_message13)



        #Denoise options.
        iterator_pass_naming = 0
        for channel in self.channels_to_assembly:
            divider_channels = nuke.Text_Knob((pass_naming[iterator_pass_naming]).upper())
            self.my_group.addKnob(divider_channels)
            on_off = nuke.Boolean_Knob("par_onOff_den_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel, "Enable denoise", False)
            self.my_group.addKnob(on_off)
            self.my_group["par_onOff_den_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel].setFlag(nuke.STARTLINE)
            region = nuke.BBox_Knob("par_reg_analys_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel, "Region analysis")
            self.my_group.addKnob(region)
            self.my_group["par_reg_analys_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel].setVisible(False)
            render_file_width = self.readFile.format().width()
            render_file_height = self.readFile.format().height()
            region_analysis_left = int(render_file_width * 0.3)
            region_analysis_bottom = int(render_file_height * 0.4)
            region_analysis_right = int(render_file_width * 0.5)
            region_analysis_top = int(render_file_height * 0.6)
            self.my_group["par_reg_analys_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel].setValue((region_analysis_left, region_analysis_bottom, region_analysis_right, region_analysis_top))
            self.my_group["par_reg_analys_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel].setVisible(False)
            analysis_noise = nuke.PyScript_Knob("par_analysis_den_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel, "Analyze noise", "autoBeauty_v207.analyze_noise_execution()")
            self.my_group.addKnob(analysis_noise)
            self.my_group["par_analysis_den_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel].setVisible(False)
            denoise_amount = nuke.Double_Knob("par_den_amount_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel, "Amount")
            self.my_group.addKnob(denoise_amount)
            self.my_group["par_den_amount_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel].setValue(1)
            self.my_group["par_den_amount_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel].setVisible(False)

            #Sharpen options.
            on_off_sharpen = nuke.Boolean_Knob("par_onOff_sharp_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel, "Enable sharpen", False)
            self.my_group.addKnob(on_off_sharpen)
            self.my_group["par_onOff_sharp_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel].setFlag(nuke.STARTLINE)
            minimum_amount = nuke.Double_Knob("par_min_sharp_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel, "Minimum")
            self.my_group.addKnob(minimum_amount)
            self.my_group["par_min_sharp_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel].setVisible(False)
            maximum_amount = nuke.Double_Knob("par_max_sharp_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel, "Maximum")
            self.my_group.addKnob(maximum_amount)
            self.my_group["par_max_sharp_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel].setValue(1)
            self.my_group["par_max_sharp_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel].setVisible(False)
            sharpen_amount = nuke.Double_Knob("par_sharp_amount_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel, "Amount")
            self.my_group.addKnob(sharpen_amount)
            self.my_group["par_sharp_amount_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel].setValue(1)
            self.my_group["par_sharp_amount_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel].setVisible(False)
            size_amount = nuke.Double_Knob("par_size_sharp_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel, "Size")
            self.my_group.addKnob(size_amount)
            self.my_group["par_size_sharp_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel].setValue(3)
            self.my_group["par_size_sharp_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel].setVisible(False)
            iterator_pass_naming += 1





        #QC TAB.
        #to compare the beauty reconstructed with the original one.
        tab_qc = nuke.Tab_Knob("QC")
        self.my_group.addKnob(tab_qc)
        divider_qc = nuke.Text_Knob("If checked, this will difference the original beauty with the reconstruted one")
        self.my_group.addKnob(divider_qc)
        qc_checker = nuke.Boolean_Knob("par_qc_check_"+render_choice+"_"+assembly_choice+"_"+str(index), "QC", False)
        self.my_group.addKnob(qc_checker)
        self.my_group["par_qc_check_"+render_choice+"_"+assembly_choice+"_"+str(index)].setFlag(nuke.STARTLINE)





        #GRADING TAB.
        #to grade each pass.
        tab_grade = nuke.Tab_Knob("Grading")
        self.my_group.addKnob(tab_grade)

        iterator_pass_naming = 0
        filters = ["DiffuseFilter", "ReflectionsFilter", "RefractionsFilter"]
        for channel in self.channels_to_assembly:
            if channel in filters:
                iterator_pass_naming += 1
                continue
            else:
                divider = nuke.Text_Knob((pass_naming[iterator_pass_naming]).upper())
                self.my_group.addKnob(divider)
                black_point = nuke.Color_Knob("par_b_point_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel, "Blackpoint")
                black_point.setRange(-1,1)
                self.my_group.addKnob(black_point)
                self.my_group["par_b_point_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel].setValue(0)
                white_point = nuke.Color_Knob("par_w_point_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel, "Whitepoint")
                white_point.setRange(-1,4)
                self.my_group.addKnob(white_point)
                self.my_group["par_w_point_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel].setValue(1)
                lift = nuke.Color_Knob("par_lift_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel, "Lift")
                lift.setRange(-1,1)
                self.my_group.addKnob(lift)
                self.my_group["par_lift_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel].setValue(0)
                gain = nuke.Color_Knob("par_gain_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel, "Gain")
                gain.setRange(0,4)
                self.my_group.addKnob(gain)
                self.my_group["par_gain_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel].setValue(1)
                multiply = nuke.Color_Knob("par_multiply_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel, "Multiply")
                multiply.setRange(0,4)
                self.my_group.addKnob(multiply)
                self.my_group["par_multiply_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel].setValue(1)
                offset = nuke.Color_Knob("par_offset_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel, "Offset")
                offset.setRange(-1,1)
                self.my_group.addKnob(offset)
                self.my_group["par_offset_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel].setValue(0)
                gamma = nuke.Color_Knob("par_gamma_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel, "Gamma")
                gamma.setRange(0,5)
                self.my_group.addKnob(gamma)
                self.my_group["par_gamma_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel].setValue(1)
                iterator_pass_naming += 1



        #WRITE TAB
        my_list_format = ["exr", "png", "jpeg", "mov"]
        my_list_channels_export = ["rgba", "rgb", "alpha"]
        my_data_type = ["16bits", "32bits"]

        tab_write = nuke.Tab_Knob("Render")
        self.my_group.addKnob(tab_write)

        channels_selection = nuke.Enumeration_Knob("par_channels_export_"+render_choice+"_"+assembly_choice+"_"+str(index), "Channels", my_list_channels_export)
        self.my_group.addKnob(channels_selection)

        file_prerender = nuke.File_Knob("par_file_"+render_choice+"_"+assembly_choice+"_"+str(index), "File path")
        self.my_group.addKnob(file_prerender)

        file_type = nuke.Enumeration_Knob("par_file_type_"+render_choice+"_"+assembly_choice+"_"+str(index), "File type", my_list_format)
        self.my_group.addKnob(file_type)

        limit_frame_range = nuke.Boolean_Knob("par_limit_range_"+render_choice+"_"+assembly_choice+"_"+str(index), "Limit to range", False)
        self.my_group.addKnob(limit_frame_range)

        first_frame = nuke.Int_Knob("par_first_frame_"+render_choice+"_"+assembly_choice+"_"+str(index), "First frame")
        self.my_group.addKnob(first_frame)

        last_frame = nuke.Int_Knob("par_last_frame_"+render_choice+"_"+assembly_choice+"_"+str(index), "Last frame")
        self.my_group.addKnob(last_frame)

        prerender_button = nuke.PyScript_Knob("par_render_"+render_choice+"_"+assembly_choice+"_"+str(index), "Render", "autoBeauty_v207.render()")
        self.my_group.addKnob(prerender_button)
        self.my_group["par_render_"+render_choice+"_"+assembly_choice+"_"+str(index)].setFlag(nuke.STARTLINE)


        ##################################################################
        #::::::::::::::::::::::::::KNOB CHANGED::::::::::::::::::::::::::#
        ##################################################################
        nuke.toNode("AUTO_BEAUTY_"+str(index)+"_"+render_choice+"_"+assembly_choice).knob("knobChanged").setValue("autoBeauty_v207.visibility()")


        ##################################################################
        #::::::::::::::::::::::::TREE CONSTRUCTION:::::::::::::::::::::::#
        ##################################################################
        position_denoiser, position_colorSpace1, position_sharpen = 340, 340, 340
        position_splitShuffle = 1490

        #Creation of denoisers on each passes.
        for channel in self.channels_to_assembly:
            denoiser_pass = nuke.nodes.Denoise2(name = "Denoise "+channel, xpos = position_denoiser, ypos = 400)
            denoiser_pass.setInput(0,nuke.toNode("Keep "+channel))

            expression_denoise_onOff = "AUTO_BEAUTY_"+str(index)+"_"+render_choice+"_"+assembly_choice+".par_onOff_den_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel+"-1"
            denoiser_pass["disable"].setExpression(expression_denoise_onOff)
            expression_denoise_analysis = "AUTO_BEAUTY_"+str(index)+"_"+render_choice+"_"+assembly_choice+".par_reg_analys_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel
            denoiser_pass["analysisRegion"].setExpression(expression_denoise_analysis)
            expression_denoise_amount = "AUTO_BEAUTY_"+str(index)+"_"+render_choice+"_"+assembly_choice+".par_den_amount_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel
            denoiser_pass["amount"].setExpression(expression_denoise_amount)
            position_denoiser -= 85


            #Colorspace change, linear to YCbCr.
            colorSpace1 = nuke.nodes.Colorspace(name = channel+"\ncolorspace in", xpos = position_colorSpace1, ypos = 600)
            colorSpace1.setInput(0,denoiser_pass)
            colorSpace1["colorspace_out"].setValue("YCbCr")
            colorSpace1["label"].setValue("[value colorspace_in]"+"\nto"+"\n[value colorspace_out]")
            position_colorSpace1 -= 85


            #Definition of naming for incoming shuffles.
            x = ["Y", "Cb", "Cr"]
            y = ["red", "green", "blue", "alpha"]
            z = {"red": ["red", "black", "black", "black"], "green" : ["black", "green", "black", "black"], "blue": ["black", "black", "blue", "black"]}
            a = 0
            b = 0
            for i in range(3):
                #Creation of shuffles. They split each pass in Y, Cb and Cr respectively on the channels Red,Green and Blue.
                splitShuffle = nuke.nodes.Shuffle(name = channel +" "+x[i], xpos = position_splitShuffle, ypos = 800)
                splitShuffle.setInput(0,nuke.toNode(channel+"\ncolorspace in"))
                splitShuffle[y[b]].setValue(z[y[i]][a])
                splitShuffle[y[b+1]].setValue(z[y[i]][a+1])
                splitShuffle[y[b+2]].setValue(z[y[i]][a+2])
                splitShuffle["in2"].setValue("alpha")
                splitShuffle[y[b+3]].setValue("red2")
                position_splitShuffle -= 115


                if i == 0:
                    #Creation of sharpen node only on the Y channel.
                    sharpen = nuke.nodes.Sharpen(name = channel+" Y_Sharpen", xpos = (splitShuffle.knob("xpos").value()), ypos = 850)
                    sharpen.setInput(0,splitShuffle)
                    sharpen["disable"].setValue(True)
                    expression_sharpen_onOff = "AUTO_BEAUTY_"+str(index)+"_"+render_choice+"_"+assembly_choice+".par_onOff_sharp_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel+"-1"
                    sharpen["disable"].setExpression(expression_sharpen_onOff)
                    expression_sharpen_min = "AUTO_BEAUTY_"+str(index)+"_"+render_choice+"_"+assembly_choice+".par_min_sharp_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel
                    sharpen["minimum"].setExpression(expression_sharpen_min)
                    expression_sharpen_max = "AUTO_BEAUTY_"+str(index)+"_"+render_choice+"_"+assembly_choice+".par_max_sharp_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel
                    sharpen["maximum"].setExpression(expression_sharpen_max)
                    expression_sharpen_amount = "AUTO_BEAUTY_"+str(index)+"_"+render_choice+"_"+assembly_choice+".par_sharp_amount_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel
                    sharpen["amount"].setExpression(expression_sharpen_amount)
                    expression_sharpen_size = "AUTO_BEAUTY_"+str(index)+"_"+render_choice+"_"+assembly_choice+".par_size_sharp_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel
                    sharpen["size"].setExpression(expression_sharpen_size)


            #Reassembly Luma and chroma with merge creation.
            merge = nuke.nodes.Merge2(label = channel, xpos = (sharpen.knob("xpos").value()), ypos = +950)
            merge["operation"].setValue("plus")
            merge.setInput(0,sharpen)
            merge.setInput(1,nuke.toNode(channel +" "+x[1]))
            merge.setInput(3,nuke.toNode(channel +" "+x[2]))

            #Creation of a clamp for the alpha.
            clamp = nuke.nodes.Clamp(name = "clamp alpha"+channel, xpos = (sharpen.knob("xpos").value()), ypos = +1000)
            clamp["channels"].setValue("alpha")
            clamp.setInput(0, merge)

            #move back to linear from YCbCr.
            colorSpace2 = nuke.nodes.Colorspace(name = channel+"\ncolorspace out", label = "[value colorspace_in]"+"\nto"+"\n[value colorspace_out]", xpos = (merge.knob("xpos").value()), ypos = 1100)
            colorSpace2["colorspace_in"].setValue("YCbCr")
            colorSpace2.setInput(0,clamp)

            #Dot with name of each pass creation.
            dot = nuke.nodes.Dot(name = "Dot "+channel, label = channel, xpos = (colorSpace2.knob("xpos").value()+34), ypos = 1250)
            dot.setInput(0,colorSpace2)

            #Text node for pass visualization.
            txt = nuke.nodes.Text2( name = "text_channel_display "+channel, xpos = (dot.knob("xpos").value()+65), ypos = 1270)
            txt.setInput(0, dot)
            txt["box"].setValue((20, 40, 1000, 130))
            txt["font"].setValue("Bahnschrift", "Regular")
            txt["global_font_scale"].setValue(0.2)
            txt["message"].setValue(channel.upper())






        ###########################################################################################
        #::::::::::::::::::::::::::::::::BEGINNING OF RENDER SPECIFIC TREE::::::::::::::::::::::::::::::
        ##########################################################################################
        ##################
        #Render Cycle.
        ##################
        if render_choice == "Cycle":
            #nuke.nodes.StickyNote(label = "The channels extracted are "+str(self.channels_to_assembly))
            #nuke.nodes.StickyNote(label = "Name of the object: "+str(self.name))


            main_channels = []

            for item in self.channels_to_assembly:
                if item == "Emit":
                    main_channels.append(item)
                else:
                    main_channels.append(item[0:(len(item)-3)])
            main_channels = list(set(main_channels))


            if assembly_choice == "Additive":

                for channel in self.channels_to_assembly:

                    unpremult = nuke.nodes.Unpremult(name = "Unpremult "+channel, xpos = (nuke.toNode("Dot "+channel)["xpos"].value() - 34), ypos = 1300)
                    unpremult["channels"].setValue("rgb")
                    unpremult["alpha"].setValue("rgba.alpha")
                    unpremult.setInput(0,nuke.toNode("Dot "+channel))

                    grade = nuke.nodes.Grade(name = "Grade "+channel, label = channel, xpos = (nuke.toNode("Dot "+channel)["xpos"].value() - 34), ypos = 1400)
                    grade.setInput(0, nuke.toNode("Unpremult "+channel))
                    grade["blackpoint"].setExpression("AUTO_BEAUTY_"+str(index)+"_"+render_choice+"_"+assembly_choice+".par_b_point_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel)
                    grade["whitepoint"].setExpression("AUTO_BEAUTY_"+str(index)+"_"+render_choice+"_"+assembly_choice+".par_w_point_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel)
                    grade["black"].setExpression("AUTO_BEAUTY_"+str(index)+"_"+render_choice+"_"+assembly_choice+".par_lift_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel)
                    grade["white"].setExpression("AUTO_BEAUTY_"+str(index)+"_"+render_choice+"_"+assembly_choice+".par_gain_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel)
                    grade["multiply"].setExpression("AUTO_BEAUTY_"+str(index)+"_"+render_choice+"_"+assembly_choice+".par_multiply_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel)
                    grade["add"].setExpression("AUTO_BEAUTY_"+str(index)+"_"+render_choice+"_"+assembly_choice+".par_offset_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel)
                    grade["gamma"].setExpression("AUTO_BEAUTY_"+str(index)+"_"+render_choice+"_"+assembly_choice+".par_gamma_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel)

                    premult = nuke.nodes.Premult(name = "Premult "+channel, xpos = (nuke.toNode("Dot "+channel)["xpos"].value() - 34), ypos = 1500)
                    premult["channels"].setValue("rgb")
                    premult["alpha"].setValue("rgba.alpha")
                    premult.setInput(0,grade)


                for channel in main_channels:

                    if channel != "Emit":
                        merge = nuke.nodes.Merge2( name = channel+" addition", xpos = nuke.toNode("Grade "+channel+"Ind")["xpos"].value(), ypos = 1800)
                        merge.setInput(0, nuke.toNode("Premult "+channel+"Ind"))
                        merge.setInput(1, nuke.toNode("Premult "+channel+"Dir"))
                        merge["operation"].setValue("plus")

                        merge2 = nuke.nodes.Merge2( name = channel+" multiplication", xpos = nuke.toNode(channel+" addition")["xpos"].value(), ypos = 2000)
                        merge2.setInput(0, nuke.toNode(channel+" addition"))
                        merge2.setInput(1, nuke.toNode("Premult "+channel+"Col"))
                        merge2["operation"].setValue("multiply")
                    else:
                        continue

                merge3 = nuke.nodes.Merge2(name = "Merge_output", xpos = nuke.toNode("Diff multiplication")["xpos"].value(), ypos = 2300)
                merge3["operation"].setValue("plus")
                i = 0
                for channel in main_channels:
                    if i == 2:
                        merge3.setInput(3,nuke.toNode(channel+" multiplication"))
                        i += 1
                    elif i == 3:
                        merge3.setInput(4,nuke.toNode("Premult Emit"))
                    else:
                        merge3.setInput(i,nuke.toNode(channel+" multiplication"))
                        i += 1

                copy = nuke.nodes.Copy(name = "fresh alpha", xpos = merge3.xpos(), ypos = 2380)
                copy.setInput(0, merge3)
                copy.setInput(1, nuke.toNode("render"))
                copy["from0"].setValue("rgba.alpha")
                copy["to0"].setValue("rgba.alpha")



            else:

                dot1 = nuke.nodes.Dot(name = "dot1 to assembly", xpos = nuke.toNode("Beauty ref")["xpos"].value(), ypos = 1250)
                dot1.setInput(0, nuke.toNode("Beauty ref"))
                dot2 = nuke.nodes.Dot(name = "dot2 to assembly", xpos = (nuke.toNode("Beauty ref")["xpos"].value()-90), ypos = 1250)
                dot2.setInput(0,dot1)
                unpremult = nuke.nodes.Unpremult(name = "unpremult all channels", xpos = dot2.xpos(), ypos = 1300)
                unpremult.setInput(0,dot2)
                unpremult["channels"].setValue("all")

                position_Y = 1400
                i = 0
                for channel in self.channels_to_assembly:

                    unpremult2 = nuke.nodes.Unpremult(name = "Unpremult "+channel, xpos = (nuke.toNode("Dot "+channel)["xpos"].value() - 34), ypos = 1300)
                    unpremult2["channels"].setValue("rgb")
                    unpremult2["alpha"].setValue("rgba.alpha")
                    unpremult2.setInput(0,nuke.toNode("Dot "+channel))

                    grade = nuke.nodes.Grade(name = "Grade "+channel, label = channel, xpos = (nuke.toNode("Dot "+channel)["xpos"].value() - 34), ypos = 1400)
                    grade.setInput(0, nuke.toNode("Unpremult "+channel))
                    grade["blackpoint"].setExpression("AUTO_BEAUTY_"+str(index)+"_"+render_choice+"_"+assembly_choice+".par_b_point_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel)
                    grade["whitepoint"].setExpression("AUTO_BEAUTY_"+str(index)+"_"+render_choice+"_"+assembly_choice+".par_w_point_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel)
                    grade["black"].setExpression("AUTO_BEAUTY_"+str(index)+"_"+render_choice+"_"+assembly_choice+".par_lift_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel)
                    grade["white"].setExpression("AUTO_BEAUTY_"+str(index)+"_"+render_choice+"_"+assembly_choice+".par_gain_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel)
                    grade["multiply"].setExpression("AUTO_BEAUTY_"+str(index)+"_"+render_choice+"_"+assembly_choice+".par_multiply_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel)
                    grade["add"].setExpression("AUTO_BEAUTY_"+str(index)+"_"+render_choice+"_"+assembly_choice+".par_offset_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel)
                    grade["gamma"].setExpression("AUTO_BEAUTY_"+str(index)+"_"+render_choice+"_"+assembly_choice+".par_gamma_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel)

                    merge1 = nuke.nodes.Merge2(name = "Merge sub"+channel, xpos = nuke.toNode("unpremult all channels")["xpos"].value(), ypos = position_Y)
                    merge1.setInput(1,nuke.toNode("Unpremult "+channel))
                    if i == 0:
                        merge1.setInput(0, nuke.toNode("unpremult all channels"))
                    else:
                        merge1.setInput(0, nuke.toNode("Merge plus"+self.channels_to_assembly[i-1]))

                    merge1["operation"].setValue("from")
                    merge2 = nuke.nodes.Merge2(name = "Merge plus"+channel, xpos = nuke.toNode("unpremult all channels")["xpos"].value(), ypos = position_Y + 80 )
                    merge2.setInput(1,grade)
                    merge2.setInput(0, nuke.toNode("Merge sub"+channel))
                    merge2["operation"].setValue("plus")

                    position_Y += 100
                    i += 1

                remove = nuke.nodes.Remove(name = "keep rgb", xpos = nuke.toNode("Merge plusTransInd")["xpos"].value(), ypos = 2380)
                remove.setInput(0, nuke.toNode("Merge plusTransInd"))
                remove["operation"].setValue("keep")
                remove["channels"].setValue("rgb")


                dot3 = nuke.nodes.Dot(name = "dot from assembly", xpos = (nuke.toNode("unpremult all channels")["xpos"].value()+34), ypos = 2400)
                dot3.setInput(0, nuke.toNode("keep rgb"))


                copy = nuke.nodes.Copy(name = "fresh alpha", xpos = nuke.toNode("render")["xpos"].value(), ypos = 2400)
                copy.setInput(0, dot3)
                copy.setInput(1, nuke.toNode("render"))
                copy["from0"].setValue("rgba.alpha")
                copy["to0"].setValue("rgba.alpha")

                premult = nuke.nodes.Premult(name = "premult fresh alpha", xpos = copy.xpos(), ypos = 2420)
                premult.setInput(0,copy)

        ##################
        #Render Redshift:
        ##################
        elif render_choice == "Redshift":
            nuke.nodes.StickyNote(label = "The channels extracted are "+str(self.channels_to_assembly))

            main_channels =[]
            for item in self.channels_to_assembly:
                if "Raw" in item:
                    main_channels.append(item[0:(len(item)-3)])
                elif "Filter" in item:
                    main_channels.append(item[0:(len(item)-6)])
                elif "Lighting" in item:
                    main_channels.append(item[0:(len(item)-8)])
                else:
                    main_channels.append(item)

            main_channels = list(set(main_channels))
            main_channels.remove("GI")
            main_channels.remove("DiffuseLighting")



            if assembly_choice == "Additive":
                filters = ["DiffuseFilter", "ReflectionsFilter", "RefractionsFilter"]
                for channel in self.channels_to_assembly:
                    if channel in filters:
                        continue
                    else:
                        unpremult = nuke.nodes.Unpremult(name = "Unpremult "+channel, xpos = (nuke.toNode("Dot "+channel)["xpos"].value() - 34), ypos = 1300)
                        unpremult["channels"].setValue("rgb")
                        unpremult["alpha"].setValue("rgba.alpha")
                        unpremult.setInput(0,nuke.toNode("Dot "+channel))

                        grade = nuke.nodes.Grade(name = "Grade "+channel, label = channel, xpos = (nuke.toNode("Dot "+channel)["xpos"].value() - 34), ypos = 1400)
                        grade.setInput(0, nuke.toNode("Unpremult "+channel))
                        grade["blackpoint"].setExpression("AUTO_BEAUTY_"+str(index)+"_"+render_choice+"_"+assembly_choice+".par_b_point_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel)
                        grade["whitepoint"].setExpression("AUTO_BEAUTY_"+str(index)+"_"+render_choice+"_"+assembly_choice+".par_w_point_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel)
                        grade["black"].setExpression("AUTO_BEAUTY_"+str(index)+"_"+render_choice+"_"+assembly_choice+".par_lift_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel)
                        grade["white"].setExpression("AUTO_BEAUTY_"+str(index)+"_"+render_choice+"_"+assembly_choice+".par_gain_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel)
                        grade["multiply"].setExpression("AUTO_BEAUTY_"+str(index)+"_"+render_choice+"_"+assembly_choice+".par_multiply_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel)
                        grade["add"].setExpression("AUTO_BEAUTY_"+str(index)+"_"+render_choice+"_"+assembly_choice+".par_offset_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel)
                        grade["gamma"].setExpression("AUTO_BEAUTY_"+str(index)+"_"+render_choice+"_"+assembly_choice+".par_gamma_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel)


                        premult = nuke.nodes.Premult(name = "Premult "+channel, xpos = (nuke.toNode("Dot "+channel)["xpos"].value() - 34), ypos = 1500)
                        premult["channels"].setValue("rgb")
                        premult["alpha"].setValue("rgba.alpha")
                        premult.setInput(0, grade)


                merge1 = nuke.nodes.Merge2(name = "RefractionsRaw multiply", xpos = nuke.toNode("Premult RefractionsRaw")["xpos"].value(), ypos = 1700)
                merge1.setInput(0, nuke.toNode("Premult RefractionsRaw"))
                merge1.setInput(1, nuke.toNode("Dot RefractionsFilter"))
                merge1["operation"].setValue("multiply")

                merge2 = nuke.nodes.Merge2(name = "ReflectionsRaw multiply", xpos = nuke.toNode("Premult ReflectionsRaw")["xpos"].value(), ypos = 1700)
                merge2.setInput(0, nuke.toNode("Premult ReflectionsRaw"))
                merge2.setInput(1, nuke.toNode("Dot ReflectionsFilter"))
                merge2["operation"].setValue("multiply")

                merge3 = nuke.nodes.Merge2(name = "DiffuseLightingRaw addition", xpos = nuke.toNode("Premult DiffuseLightingRaw")["xpos"].value(), ypos = 1700)
                merge3.setInput(0, nuke.toNode("Premult DiffuseLightingRaw"))
                merge3.setInput(1,  nuke.toNode("Premult GIRaw"))
                merge3["operation"].setValue("plus")

                merge4 = nuke.nodes.Merge2(name = "DiffuseFilter multiply", xpos = merge3["xpos"].value(), ypos = 1750)
                merge4.setInput(0, merge3)
                merge4.setInput(1, nuke.toNode("Dot DiffuseFilter"))
                merge4["operation"].setValue("multiply")

                merge5 = nuke.nodes.Merge2(name = "Emission addition", xpos = merge3["xpos"].value(), ypos = 1800)
                merge5.setInput(0, merge4)
                merge5.setInput(1, nuke.toNode("Premult Emission"))
                merge5["operation"].setValue("plus")

                merge6 = nuke.nodes.Merge2(name = "Reflections addition", xpos = merge3["xpos"].value(), ypos = 1850)
                merge6.setInput(0, merge5)
                merge6.setInput(1, merge2)
                merge6["operation"].setValue("plus")

                merge7 = nuke.nodes.Merge2(name = "Refractions addition", xpos = merge3["xpos"].value(), ypos = 1900)
                merge7.setInput(0, merge6)
                merge7.setInput(1, merge1)
                merge7["operation"].setValue("plus")

                merge8 = nuke.nodes.Merge2(name = "Specular addition", xpos = merge3["xpos"].value(), ypos = 1950)
                merge8.setInput(0, merge7)
                merge8.setInput(1, nuke.toNode("Premult SpecularLighting"))
                merge8["operation"].setValue("plus")

                copy = nuke.nodes.Copy(name = "fresh alpha", xpos =nuke.toNode("Premult DiffuseFilter"), ypos = 2100)
                copy.setInput(0, merge8)
                copy.setInput(1, nuke.toNode("render"))
                copy["from0"].setValue("rgba.alpha")
                copy["to0"].setValue("rgba.alpha")


            else:

                for channel in self.channels_to_assembly:

                    unpremult = nuke.nodes.Unpremult(name = "Unpremult "+channel, xpos = (nuke.toNode("Dot "+channel)["xpos"].value() - 34), ypos = 1300)
                    unpremult["channels"].setValue("rgb")
                    unpremult["alpha"].setValue("rgba.alpha")
                    unpremult.setInput(0, nuke.toNode("Dot "+channel))


                    if channel == "SpecularLighting" or channel == "Emission":
                        grade = nuke.nodes.Grade(name = channel, label = channel, xpos = (nuke.toNode("Dot "+channel)["xpos"].value() - 34), ypos = 1600)
                        grade.setInput(0, nuke.toNode("Unpremult "+channel))
                        grade["blackpoint"].setExpression("AUTO_BEAUTY_"+str(index)+"_"+render_choice+"_"+assembly_choice+".par_b_point_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel)
                        grade["whitepoint"].setExpression("AUTO_BEAUTY_"+str(index)+"_"+render_choice+"_"+assembly_choice+".par_w_point_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel)
                        grade["black"].setExpression("AUTO_BEAUTY_"+str(index)+"_"+render_choice+"_"+assembly_choice+".par_lift_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel)
                        grade["white"].setExpression("AUTO_BEAUTY_"+str(index)+"_"+render_choice+"_"+assembly_choice+".par_gain_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel)
                        grade["multiply"].setExpression("AUTO_BEAUTY_"+str(index)+"_"+render_choice+"_"+assembly_choice+".par_multiply_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel)
                        grade["add"].setExpression("AUTO_BEAUTY_"+str(index)+"_"+render_choice+"_"+assembly_choice+".par_offset_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel)
                        grade["gamma"].setExpression("AUTO_BEAUTY_"+str(index)+"_"+render_choice+"_"+assembly_choice+".par_gamma_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel)


                    list_raw_passes = ["RefractionsRaw", "ReflectionsRaw"]
                    list_raw_passes_2 = ["GIRaw", "DiffuseLightingRaw"]
                    main_channels = ['Emission', 'Refractions', 'Specular', 'Reflections', 'Diffuse']
                    filters = ["RefractionsFilter", "ReflectionsFilter", "DiffuseFilter"]

                    if channel in list_raw_passes:
                        merge1 = nuke.nodes.Merge2(name = channel, xpos = nuke.toNode("Unpremult "+channel)["xpos"].value(), ypos = 1500)
                        merge1.setInput(0, nuke.toNode("Unpremult "+channel[:-3]+"Filter"))
                        merge1.setInput(1, nuke.toNode("Unpremult "+channel))
                        merge1["operation"].setValue("divide")
                        grade1 = nuke.nodes.Grade(name = "Grade "+channel, xpos = nuke.toNode("Unpremult "+channel)["xpos"].value(), ypos = 1550 )
                        grade1.setInput(0, merge1)
                        grade1["blackpoint"].setExpression("AUTO_BEAUTY_"+str(index)+"_"+render_choice+"_"+assembly_choice+".par_b_point_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel)
                        grade1["whitepoint"].setExpression("AUTO_BEAUTY_"+str(index)+"_"+render_choice+"_"+assembly_choice+".par_w_point_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel)
                        grade1["black"].setExpression("AUTO_BEAUTY_"+str(index)+"_"+render_choice+"_"+assembly_choice+".par_lift_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel)
                        grade1["white"].setExpression("AUTO_BEAUTY_"+str(index)+"_"+render_choice+"_"+assembly_choice+".par_gain_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel)
                        grade1["multiply"].setExpression("AUTO_BEAUTY_"+str(index)+"_"+render_choice+"_"+assembly_choice+".par_multiply_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel)
                        grade1["add"].setExpression("AUTO_BEAUTY_"+str(index)+"_"+render_choice+"_"+assembly_choice+".par_offset_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel)
                        grade1["gamma"].setExpression("AUTO_BEAUTY_"+str(index)+"_"+render_choice+"_"+assembly_choice+".par_gamma_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel)

                        merge2 = nuke.nodes.Merge2(name = channel[:-3], xpos = nuke.toNode("Unpremult "+channel)["xpos"].value(), ypos = 1600)
                        merge2.setInput(0, grade1)
                        merge2["operation"].setValue("multiply")
                        merge2.setInput(1, nuke.toNode("Unpremult "+channel[:-3]+"Filter"))


                    if channel in list_raw_passes_2:
                        merge3 = nuke.nodes.Merge2(name = channel, xpos = nuke.toNode("Unpremult "+channel)["xpos"].value(), ypos = 1500)
                        merge3.setInput(0, nuke.toNode("Unpremult DiffuseFilter"))
                        merge3.setInput(1, nuke.toNode("Unpremult "+channel))
                        merge3["operation"].setValue("divide")
                        grade2 = nuke.nodes.Grade(name = "Grade "+channel, xpos = nuke.toNode("Unpremult "+channel)["xpos"].value(), ypos = 1550 )
                        grade2.setInput(0, merge3)
                        grade2["blackpoint"].setExpression("AUTO_BEAUTY_"+str(index)+"_"+render_choice+"_"+assembly_choice+".par_b_point_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel)
                        grade2["whitepoint"].setExpression("AUTO_BEAUTY_"+str(index)+"_"+render_choice+"_"+assembly_choice+".par_w_point_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel)
                        grade2["black"].setExpression("AUTO_BEAUTY_"+str(index)+"_"+render_choice+"_"+assembly_choice+".par_lift_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel)
                        grade2["white"].setExpression("AUTO_BEAUTY_"+str(index)+"_"+render_choice+"_"+assembly_choice+".par_gain_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel)
                        grade2["multiply"].setExpression("AUTO_BEAUTY_"+str(index)+"_"+render_choice+"_"+assembly_choice+".par_multiply_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel)
                        grade2["add"].setExpression("AUTO_BEAUTY_"+str(index)+"_"+render_choice+"_"+assembly_choice+".par_offset_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel)
                        grade2["gamma"].setExpression("AUTO_BEAUTY_"+str(index)+"_"+render_choice+"_"+assembly_choice+".par_gamma_"+render_choice+"_"+assembly_choice+"_"+str(index)+"_"+channel)

                        merge3 = nuke.nodes.Merge2(name = channel[:-3], xpos = nuke.toNode("Unpremult "+channel)["xpos"].value(), ypos = 1600)
                        merge3.setInput(0, grade2)
                        merge3["operation"].setValue("multiply")
                        merge3.setInput(1, nuke.toNode("Unpremult DiffuseFilter"))




                unpremult2 = nuke.nodes.Unpremult(name = "Unpremult assembly", xpos = nuke.toNode("Beauty ref")["xpos"].value()-80, ypos = nuke.toNode("Unpremult DiffuseFilter")["xpos"].value())
                unpremult2.setInput(0, nuke.toNode("Beauty ref"))
                unpremult2["channels"].setValue("all")

                channels_to_assembly_no_filters = ['DiffuseLightingRaw', 'Emission', 'GIRaw', 'ReflectionsRaw', 'RefractionsRaw', 'SpecularLighting']

                #Merges creation for main pipe.
                nuke.toNode("Unpremult assembly").setSelected(True)
                i = 0
                for channel in channels_to_assembly_no_filters:
                    #Merge substarctives
                    nuke.createNode("Merge2")['name'].setValue("sub "+channel)
                    nuke.toNode("sub "+channel)["operation"].setValue("from")
                    nuke.toNode("sub "+channel).setInput(1, nuke.toNode("Unpremult "+channel))
                    if channel == "DiffuseLightingRaw":
                        nuke.toNode("sub "+channel).setInput(0, nuke.toNode("Unpremult assembly"))
                    else:
                        nuke.toNode("sub "+channel).setInput(0, nuke.toNode("sub "+channels_to_assembly_no_filters[i]))
                        i += 1

                    #Merges additives.
                    nuke.createNode("Merge2")['name'].setValue("add "+channel)
                    nuke.toNode("add "+channel)["operation"].setValue("plus")
                    if "Raw" in channel:
                        nuke.toNode("add "+channel).setInput(1, nuke.toNode(channel[:-3]))
                    else:
                        nuke.toNode("add "+channel).setInput(1, nuke.toNode(channel))

                i = 0
                for channel in channels_to_assembly_no_filters:
                    if channel == "DiffuseLightingRaw":
                        nuke.toNode("add "+channel).setInput(0, nuke.toNode("sub SpecularLighting"))
                    else:
                        nuke.toNode("add "+channel).setInput(0, nuke.toNode("add "+channels_to_assembly_no_filters[i]))
                        i += 1





                remove = nuke.nodes.Remove(name = "keep rgb", xpos = nuke.toNode("add SpecularLighting")["xpos"].value(), ypos = 2380)
                remove.setInput(0,nuke.toNode("add SpecularLighting"))
                remove["operation"].setValue("keep")
                remove["channels"].setValue("rgb")


                dot3 = nuke.nodes.Dot(name = "dot from assembly", xpos = (nuke.toNode("keep rgb")["xpos"].value()+34), ypos = 2400)
                dot3.setInput(0,nuke.toNode("keep rgb"))


                copy = nuke.nodes.Copy(name = "fresh alpha", xpos = nuke.toNode("render")["xpos"].value(), ypos = 2400)
                copy.setInput(0, nuke.toNode("dot from assembly"))
                copy.setInput(1,nuke.toNode("render"))
                copy["from0"].setValue("rgba.alpha")
                copy["to0"].setValue("rgba.alpha")

                premult = nuke.nodes.Premult(name = "premult fresh alpha", xpos = copy.xpos(), ypos = 2420)
                premult.setInput(0,copy)


        ###########################################################################################
        #::::::::::::::::::::::::::::::::END OF RENDER SPECIFIC TREE::::::::::::::::::::::::::::::
        ##########################################################################################

        #Common part between Redshift and Cycle tree.
        dot_final = nuke.nodes.Dot(name = "Dot beauty", xpos = nuke.toNode("fresh alpha")["xpos"].value() + 33, ypos = 2470)
        if assembly_choice == "Additive":
            dot_final.setInput(0, nuke.toNode("fresh alpha"))
        else:
            dot_final.setInput(0, nuke.toNode("premult fresh alpha"))


        merge_qc = nuke.nodes.Merge2(name = "Merge QC", xpos = nuke.toNode("Beauty ref")["xpos"].value(), ypos = nuke.toNode("Dot beauty")["ypos"].value())
        merge_qc["operation"].setValue("difference")
        merge_qc.setInput(1,nuke.toNode("Dot beauty"))
        merge_qc.setInput(0,nuke.toNode("Beauty ref"))

        txt_qc = nuke.nodes.Text2( name = "text_qc", xpos = merge_qc.knob("xpos").value(), ypos = 2550)
        txt_qc.setInput(0, merge_qc)
        txt_qc["box"].setValue((20, 40, 1000, 130))
        txt_qc["font"].setValue("Bahnschrift", "Regular")
        txt_qc["global_font_scale"].setValue(0.2)
        txt_qc["message"].setValue("QC (difference between original beauty and beauty reconstructed)")

        dot_preview = nuke.nodes.Dot(name = "Dot preview", xpos = (nuke.toNode("Dot beauty")["xpos"].value() - 200), ypos = 2500  )

        switch_preview = nuke.nodes.Switch(name = "Switch preview", xpos = nuke.toNode("Dot beauty")["xpos"].value() - 34, ypos = 2500 )
        switch_preview.setInput(0,nuke.toNode("Dot beauty"))
        switch_preview.setInput(1,dot_preview)

        switch_qc = nuke.nodes.Switch(name = "Switch QC", xpos = nuke.toNode("Dot beauty")["xpos"].value() - 34, ypos = 2550 )
        switch_qc.setInput(0, nuke.toNode("Switch preview"))
        switch_qc.setInput(1, nuke.toNode("text_qc"))
        expression_qc_check = "AUTO_BEAUTY_"+str(index)+"_"+render_choice+"_"+assembly_choice+".par_qc_check_"+render_choice+"_"+assembly_choice+"_"+str(index)
        switch_qc["which"].setExpression(expression_qc_check)

        write_beauty = nuke.nodes.Write(name = "Write beauty_"+render_choice+"_"+assembly_choice+"_"+str(index), xpos = nuke.toNode("Dot beauty"), ypos = 2650 )
        write_beauty.setInput(0, nuke.toNode("Switch QC"))
        write_beauty["channels"].setValue("rgba")
        write_beauty["use_limit"].setExpression("AUTO_BEAUTY_"+str(index)+"_"+render_choice+"_"+assembly_choice+".par_limit_range_"+render_choice+"_"+assembly_choice+"_"+str(index))
        write_beauty["first"].setExpression("AUTO_BEAUTY_"+str(index)+"_"+render_choice+"_"+assembly_choice+".par_first_frame_"+render_choice+"_"+assembly_choice+"_"+str(index))
        write_beauty["last"].setExpression("AUTO_BEAUTY_"+str(index)+"_"+render_choice+"_"+assembly_choice+".par_last_frame_"+render_choice+"_"+assembly_choice+"_"+str(index))
        write_beauty["file"].setExpression("AUTO_BEAUTY_"+str(index)+"_"+render_choice+"_"+assembly_choice+".par_file_"+render_choice+"_"+assembly_choice+"_"+str(index))
        #write_beauty["datatype"].setExpression("AUTO_BEAUTY_"+str(index)+"_"+render_choice+"_"+assembly_choice+".par_data_type_"+render_choice+"_"+assembly_choice+"_"+str(index))


        out = nuke.nodes.Output(name = "Out_AUTO_BEAUTY "+render_choice+" "+assembly_choice, xpos = nuke.toNode("Write beauty_"+render_choice+"_"+assembly_choice+"_"+str(index))["xpos"].value(), ypos = 2750)
        out.setInput(0,nuke.toNode("Write beauty_"+render_choice+"_"+assembly_choice+"_"+str(index)))

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
    index = x["name"].value()[12]

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

    index = y["name"].value()[12]
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
    nuke.show(nuke.toNode("AUTO_BEAUTY_"+render_choice+"_"+assembly_choice))

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

    index = z["name"].value()[12]

    nuke.execute(nuke.toNode("Write beauty_"+render_choice+"_"+assembly_choice+"_"+str(index)))

