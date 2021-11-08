###########################################
#cycleTree.py
#Version 1.3.02

#Last updated August 08 2021
#
#
###########################################

import nuke, re




def cycle_tree(my_group, channels_to_assembly, render_choice, assembly_choice, new_index, read_file, pass_naming):
    ###################################
    #:::::::::::::::CYCLE:::::::::::::#
    #:::::::::::::::TREE::::::::::::::#
    #::::::::::CCONSTRUCTION::::::::::#
    ###################################
    main_channels = []

    for item in channels_to_assembly:
        if item == "Emit":
            main_channels.append(item)
        else:
            main_channels.append(item[0:(len(item)-3)])
    main_channels = list(set(main_channels))

    #################################
    # Cycle additive assembly
    #################################
    if assembly_choice == "Additive":

        for channel in channels_to_assembly:

            unpremult = nuke.nodes.Unpremult(name = "Unpremult "+channel, xpos = (nuke.toNode("Dot "+channel)["xpos"].value() - 34), ypos = 1300)
            unpremult["channels"].setValue("rgb")
            unpremult["alpha"].setValue("rgba.alpha")
            unpremult.setInput(0,nuke.toNode("Dot "+channel))

            grade = nuke.nodes.Grade(name = "Grade "+channel, label = channel, xpos = (nuke.toNode("Dot "+channel)["xpos"].value() - 34), ypos = 1400)
            grade.setInput(0, nuke.toNode("Unpremult "+channel))
            grade["blackpoint"].setExpression("AUTO_BEAUTY_"+str(new_index)+"_"+render_choice+"_"+assembly_choice+".par_b_point_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel)
            grade["whitepoint"].setExpression("AUTO_BEAUTY_"+str(new_index)+"_"+render_choice+"_"+assembly_choice+".par_w_point_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel)
            grade["black"].setExpression("AUTO_BEAUTY_"+str(new_index)+"_"+render_choice+"_"+assembly_choice+".par_lift_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel)
            grade["white"].setExpression("AUTO_BEAUTY_"+str(new_index)+"_"+render_choice+"_"+assembly_choice+".par_gain_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel)
            grade["multiply"].setExpression("AUTO_BEAUTY_"+str(new_index)+"_"+render_choice+"_"+assembly_choice+".par_multiply_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel)
            grade["add"].setExpression("AUTO_BEAUTY_"+str(new_index)+"_"+render_choice+"_"+assembly_choice+".par_offset_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel)
            grade["gamma"].setExpression("AUTO_BEAUTY_"+str(new_index)+"_"+render_choice+"_"+assembly_choice+".par_gamma_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel)

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
        dot4 = nuke.nodes.Dot(name = "second dot from render", xpos = -2500, ypos = 2380)
        dot5 = nuke.nodes.Dot(name = "dot from render", xpos = -2500, ypos = 15)
        copy.setInput(0, merge3)
        copy.setInput(1, nuke.toNode("second dot from render"))
        dot4.setInput(0, nuke.toNode("dot from render"))
        dot5.setInput(0, nuke.toNode("render"))
        copy["from0"].setValue("rgba.alpha")
        copy["to0"].setValue("rgba.alpha")


    #################################
    # Cycle substractive assembly
    #################################
    else:

        dot1 = nuke.nodes.Dot(name = "dot1 to assembly", xpos = nuke.toNode("Beauty ref")["xpos"].value() + 35, ypos = 1250)

        dot1.setInput(0, nuke.toNode("Beauty ref"))
        #dot2 = nuke.nodes.Dot(name = "dot2 to assembly", xpos = (nuke.toNode("Beauty ref")["xpos"].value()-90), ypos = 1250)
        #dot2.setInput(0,dot1)
        unpremult = nuke.nodes.Unpremult(name = "unpremult all channels", xpos = dot1.xpos() -34, ypos = 1300)
        unpremult.setInput(0,dot1)
        unpremult["channels"].setValue("all")

        position_Y = 1400
        i = 0
        for channel in channels_to_assembly:

            unpremult2 = nuke.nodes.Unpremult(name = "Unpremult "+channel, xpos = (nuke.toNode("Dot "+channel)["xpos"].value() - 34), ypos = 1300)
            unpremult2["channels"].setValue("rgb")
            unpremult2["alpha"].setValue("rgba.alpha")
            unpremult2.setInput(0,nuke.toNode("Dot "+channel))

            grade = nuke.nodes.Grade(name = "Grade "+channel, label = channel, xpos = (nuke.toNode("Dot "+channel)["xpos"].value() - 34), ypos = 1325)
            grade.setInput(0, nuke.toNode("Unpremult "+channel))
            grade["blackpoint"].setExpression("AUTO_BEAUTY_"+str(new_index)+"_"+render_choice+"_"+assembly_choice+".par_b_point_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel)
            grade["whitepoint"].setExpression("AUTO_BEAUTY_"+str(new_index)+"_"+render_choice+"_"+assembly_choice+".par_w_point_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel)
            grade["black"].setExpression("AUTO_BEAUTY_"+str(new_index)+"_"+render_choice+"_"+assembly_choice+".par_lift_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel)
            grade["white"].setExpression("AUTO_BEAUTY_"+str(new_index)+"_"+render_choice+"_"+assembly_choice+".par_gain_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel)
            grade["multiply"].setExpression("AUTO_BEAUTY_"+str(new_index)+"_"+render_choice+"_"+assembly_choice+".par_multiply_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel)
            grade["add"].setExpression("AUTO_BEAUTY_"+str(new_index)+"_"+render_choice+"_"+assembly_choice+".par_offset_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel)
            grade["gamma"].setExpression("AUTO_BEAUTY_"+str(new_index)+"_"+render_choice+"_"+assembly_choice+".par_gamma_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel)

            merge1 = nuke.nodes.Merge2(name = "Merge sub"+channel, xpos = nuke.toNode("unpremult all channels")["xpos"].value(), ypos = position_Y)
            merge1.setInput(1,nuke.toNode("Unpremult "+channel))
            if i == 0:
                merge1.setInput(0, nuke.toNode("unpremult all channels"))
            else:
                merge1.setInput(0, nuke.toNode("Merge plus"+ channels_to_assembly[i-1]))

            merge1["operation"].setValue("from")
            merge2 = nuke.nodes.Merge2(name = "Merge plus"+channel, xpos = nuke.toNode("unpremult all channels")["xpos"].value(), ypos = position_Y + 75 )
            merge2.setInput(1,grade)
            merge2.setInput(0, nuke.toNode("Merge sub"+channel))
            merge2["operation"].setValue("plus")

            position_Y += 100
            i += 1

        remove = nuke.nodes.Remove(name = "keep rgb", xpos = nuke.toNode("Merge plusTransInd")["xpos"].value(), ypos = 2410)
        remove.setInput(0, nuke.toNode("Merge plusTransInd"))
        remove["operation"].setValue("keep")
        remove["channels"].setValue("rgb")


        dot3 = nuke.nodes.Dot(name = "dot from assembly", xpos = (nuke.toNode("unpremult all channels")["xpos"].value()+34), ypos = 2440)
        dot3.setInput(0, nuke.toNode("keep rgb"))


        copy = nuke.nodes.Copy(name = "fresh alpha", xpos = nuke.toNode("render")["xpos"].value(), ypos = 2432)
        dot4 = nuke.nodes.Dot(name = "second dot from render", xpos = -2500, ypos = 2440)
        dot5 = nuke.nodes.Dot(name = "dot from render", xpos = -2500, ypos = 15)
        copy.setInput(0, dot3)
        copy.setInput(1, nuke.toNode("second dot from render"))
        dot4.setInput(0, nuke.toNode("dot from render"))
        dot5.setInput(0, nuke.toNode("render"))
        copy["from0"].setValue("rgba.alpha")
        copy["to0"].setValue("rgba.alpha")

        premult = nuke.nodes.Premult(name = "premult fresh alpha", xpos = copy.xpos(), ypos = 2470)
        premult.setInput(0,copy)
