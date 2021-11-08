###########################################
#redshiftTree.py
#Version 1.3.02

#Last updated August 08 2021
#
#
###########################################

import nuke, re

def redshift_tree(my_group, channels_to_assembly, render_choice, assembly_choice, new_index, read_file, pass_naming):

    ###################################
    #::::::::::::REDSHIFT:::::::::::::#
    #::::::::::::::TREE:::::::::::::::#
    #::::::::::CONSTRUCTION:::::::::::#
    ###################################
    main_channels =[]

    for item in channels_to_assembly:
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


    #################################
    # Redshift additive assembly
    #################################
    if assembly_choice == "Additive":

        filters = ["DiffuseFilter", "ReflectionsFilter", "RefractionsFilter"]

        for channel in channels_to_assembly:
            if channel in filters:
                continue
            else:
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
                premult.setInput(0, grade)


        merge1 = nuke.nodes.Merge2(name = "RefractionsRaw multiply", xpos = nuke.toNode("Premult RefractionsRaw")["xpos"].value(), ypos = 1900)
        merge1.setInput(0, nuke.toNode("Premult RefractionsRaw"))
        merge1.setInput(1, nuke.toNode("Dot RefractionsFilter"))
        merge1["operation"].setValue("multiply")

        merge2 = nuke.nodes.Merge2(name = "ReflectionsRaw multiply", xpos = nuke.toNode("Premult ReflectionsRaw")["xpos"].value(), ypos = 1850)
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

        dot_spec_add = nuke.nodes.Dot(name = "dot spec_addition", xpos = nuke.toNode("Premult SpecularLighting")["xpos"].value()+35, ypos = nuke.toNode("Premult SpecularLighting")["ypos"].value()+450)
        dot_spec_add.setInput(0, nuke.toNode("Premult SpecularLighting"))

        merge8 = nuke.nodes.Merge2(name = "Specular addition", xpos = merge3["xpos"].value(), ypos = 1950)
        merge8.setInput(0, merge7)
        merge8.setInput(1, nuke.toNode("dot spec_addition"))
        merge8["operation"].setValue("plus")

        dot4 = nuke.nodes.Dot(name = "second dot from render", xpos = -2500, ypos = 2110)
        dot5 = nuke.nodes.Dot(name = "dot from render", xpos = -2500, ypos = 15)
        dot4.setInput(0, nuke.toNode("dot from render"))
        dot5.setInput(0, nuke.toNode("render"))

        copy = nuke.nodes.Copy(name = "fresh alpha", xpos =nuke.toNode("Specular addition")["xpos"].value(), ypos = 2100)
        copy.setInput(0, merge8)
        copy.setInput(1, nuke.toNode("second dot from render"))
        copy["from0"].setValue("rgba.alpha")
        copy["to0"].setValue("rgba.alpha")


    #################################
    # Redshift substractive assembly
    #################################
    else:

        for channel in channels_to_assembly:

            unpremult = nuke.nodes.Unpremult(name = "Unpremult "+channel, xpos = (nuke.toNode("Dot "+channel)["xpos"].value() - 34), ypos = 1300)
            unpremult["channels"].setValue("rgb")
            unpremult["alpha"].setValue("rgba.alpha")
            unpremult.setInput(0, nuke.toNode("Dot "+channel))


            if channel == "SpecularLighting" or channel == "Emission":
                grade = nuke.nodes.Grade(name = "Grade "+channel, label = channel, xpos = (nuke.toNode("Dot "+channel)["xpos"].value() - 34), ypos = 1600)
                grade.setInput(0, nuke.toNode("Unpremult "+channel))
                grade["blackpoint"].setExpression("AUTO_BEAUTY_"+str(new_index)+"_"+render_choice+"_"+assembly_choice+".par_b_point_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel)
                grade["whitepoint"].setExpression("AUTO_BEAUTY_"+str(new_index)+"_"+render_choice+"_"+assembly_choice+".par_w_point_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel)
                grade["black"].setExpression("AUTO_BEAUTY_"+str(new_index)+"_"+render_choice+"_"+assembly_choice+".par_lift_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel)
                grade["white"].setExpression("AUTO_BEAUTY_"+str(new_index)+"_"+render_choice+"_"+assembly_choice+".par_gain_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel)
                grade["multiply"].setExpression("AUTO_BEAUTY_"+str(new_index)+"_"+render_choice+"_"+assembly_choice+".par_multiply_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel)
                grade["add"].setExpression("AUTO_BEAUTY_"+str(new_index)+"_"+render_choice+"_"+assembly_choice+".par_offset_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel)
                grade["gamma"].setExpression("AUTO_BEAUTY_"+str(new_index)+"_"+render_choice+"_"+assembly_choice+".par_gamma_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel)


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
                grade1["blackpoint"].setExpression("AUTO_BEAUTY_"+str(new_index)+"_"+render_choice+"_"+assembly_choice+".par_b_point_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel)
                grade1["whitepoint"].setExpression("AUTO_BEAUTY_"+str(new_index)+"_"+render_choice+"_"+assembly_choice+".par_w_point_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel)
                grade1["black"].setExpression("AUTO_BEAUTY_"+str(new_index)+"_"+render_choice+"_"+assembly_choice+".par_lift_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel)
                grade1["white"].setExpression("AUTO_BEAUTY_"+str(new_index)+"_"+render_choice+"_"+assembly_choice+".par_gain_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel)
                grade1["multiply"].setExpression("AUTO_BEAUTY_"+str(new_index)+"_"+render_choice+"_"+assembly_choice+".par_multiply_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel)
                grade1["add"].setExpression("AUTO_BEAUTY_"+str(new_index)+"_"+render_choice+"_"+assembly_choice+".par_offset_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel)
                grade1["gamma"].setExpression("AUTO_BEAUTY_"+str(new_index)+"_"+render_choice+"_"+assembly_choice+".par_gamma_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel)

                merge2 = nuke.nodes.Merge2(name = channel[:-3], xpos = nuke.toNode("Unpremult "+channel)["xpos"].value(), ypos = 1600)
                merge2.setInput(0, grade1)
                merge2["operation"].setValue("multiply")
                merge2.setInput(1, nuke.toNode("Unpremult "+channel[:-3]+"Filter"))


            elif channel in list_raw_passes_2:
                merge3 = nuke.nodes.Merge2(name = channel, xpos = nuke.toNode("Unpremult "+channel)["xpos"].value(), ypos = 1500)
                merge3.setInput(0, nuke.toNode("Unpremult DiffuseFilter"))
                merge3.setInput(1, nuke.toNode("Unpremult "+channel))
                merge3["operation"].setValue("divide")

                grade2 = nuke.nodes.Grade(name = "Grade "+channel, xpos = nuke.toNode("Unpremult "+channel)["xpos"].value(), ypos = 1550 )
                grade2.setInput(0, merge3)
                grade2["blackpoint"].setExpression("AUTO_BEAUTY_"+str(new_index)+"_"+render_choice+"_"+assembly_choice+".par_b_point_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel)
                grade2["whitepoint"].setExpression("AUTO_BEAUTY_"+str(new_index)+"_"+render_choice+"_"+assembly_choice+".par_w_point_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel)
                grade2["black"].setExpression("AUTO_BEAUTY_"+str(new_index)+"_"+render_choice+"_"+assembly_choice+".par_lift_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel)
                grade2["white"].setExpression("AUTO_BEAUTY_"+str(new_index)+"_"+render_choice+"_"+assembly_choice+".par_gain_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel)
                grade2["multiply"].setExpression("AUTO_BEAUTY_"+str(new_index)+"_"+render_choice+"_"+assembly_choice+".par_multiply_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel)
                grade2["add"].setExpression("AUTO_BEAUTY_"+str(new_index)+"_"+render_choice+"_"+assembly_choice+".par_offset_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel)
                grade2["gamma"].setExpression("AUTO_BEAUTY_"+str(new_index)+"_"+render_choice+"_"+assembly_choice+".par_gamma_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel)

                merge3 = nuke.nodes.Merge2(name = channel[:-3], xpos = nuke.toNode("Unpremult "+channel)["xpos"].value(), ypos = 1600)
                merge3.setInput(0, grade2)
                merge3["operation"].setValue("multiply")
                merge3.setInput(1, nuke.toNode("Unpremult DiffuseFilter"))





        unpremult2 = nuke.nodes.Unpremult(name = "Unpremult assembly", xpos = nuke.toNode("Beauty ref")["xpos"].value(), ypos = nuke.toNode("Beauty ref")["ypos"].value()+35)
        unpremult2.setInput(0, nuke.toNode("Beauty ref"))
        unpremult2["channels"].setValue("all")

        channels_to_assembly_no_filters = ['DiffuseLightingRaw', 'Emission', 'GIRaw', 'ReflectionsRaw', 'RefractionsRaw', 'SpecularLighting']

        #Merges creation to reassembly the passes for main pipe.
        i = -1
        pos = 375
        for channel in channels_to_assembly_no_filters:

            nuke.nodes.Merge2(name = "sub "+ channel, xpos = nuke.toNode("Unpremult assembly")["xpos"].value(), ypos = nuke.toNode("Unpremult "+ channel)["ypos"].value()+ pos ).setInput(1, nuke.toNode("Unpremult "+ channel))
            nuke.toNode("sub "+ channel)["operation"].setValue("from")
            if channel != "DiffuseLightingRaw":
                nuke.toNode("sub "+ channel).setInput(0, nuke.toNode("add "+ channels_to_assembly_no_filters[i]))

            nuke.nodes.Merge2(name = "add "+ channel, xpos = nuke.toNode("Unpremult assembly")["xpos"].value(), ypos = nuke.toNode("sub "+ channel)["ypos"].value()+20).setInput(0, nuke.toNode("sub "+ channel))
            nuke.toNode("add "+ channel)["operation"].setValue("plus")

            i += 1
            pos += 75

            if channel == "Emission":
                nuke.toNode("add "+ channel).setInput(1, nuke.toNode("Grade "+ "Emission"))
            elif channel == "SpecularLighting":
                nuke.toNode("add "+ channel).setInput(1, nuke.toNode("Grade "+ "SpecularLighting"))
            else:
                nuke.toNode("add "+ channel).setInput(1, nuke.toNode(channel[:-3]))


        nuke.toNode("sub DiffuseLightingRaw").setInput(0, nuke.toNode("Unpremult assembly"))

        remove = nuke.nodes.Remove(name = "keep rgb", xpos = nuke.toNode("add SpecularLighting")["xpos"].value(), ypos = 2250)
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

        premult = nuke.nodes.Premult(name = "premult fresh alpha", xpos = copy.xpos(), ypos = 2450)
        premult.setInput(0,copy)
