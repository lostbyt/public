###########################################
#commonTreeBegin.py
#Version 1.3.02

#Last updated August 08 2021
#
#
###########################################

import nuke, re

##################################################################
#::::::::::::::::::::::::TREE CONSTRUCTION:::::::::::::::::::::::#
##################################################################

def common_tree_begin(my_group, channels_to_assembly, render_choice, assembly_choice, new_index, read_file, pass_naming):

    position_denoiser, position_colorSpace1, position_sharpen = 340, 340, 340
    position_splitShuffle = 1490

    #Creation of denoisers/sharpen on each passes.
    for channel in channels_to_assembly:
        denoiser_pass = nuke.nodes.Denoise2(name = "Denoise "+channel, xpos = position_denoiser, ypos = 400)
        denoiser_pass.setInput(0,nuke.toNode("Keep "+channel))

        expression_denoise_onOff = "AUTO_BEAUTY_"+str(new_index)+"_"+render_choice+"_"+assembly_choice+".par_onOff_den_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel+"-1"
        denoiser_pass["disable"].setExpression(expression_denoise_onOff)
        expression_denoise_analysis = "AUTO_BEAUTY_"+str(new_index)+"_"+render_choice+"_"+assembly_choice+".par_reg_analys_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel
        denoiser_pass["analysisRegion"].setExpression(expression_denoise_analysis)
        expression_denoise_amount = "AUTO_BEAUTY_"+str(new_index)+"_"+render_choice+"_"+assembly_choice+".par_den_amount_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel
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
                expression_sharpen_onOff = "AUTO_BEAUTY_"+str(new_index)+"_"+render_choice+"_"+assembly_choice+".par_onOff_sharp_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel+"-1"
                sharpen["disable"].setExpression(expression_sharpen_onOff)
                expression_sharpen_min = "AUTO_BEAUTY_"+str(new_index)+"_"+render_choice+"_"+assembly_choice+".par_min_sharp_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel
                sharpen["minimum"].setExpression(expression_sharpen_min)
                expression_sharpen_max = "AUTO_BEAUTY_"+str(new_index)+"_"+render_choice+"_"+assembly_choice+".par_max_sharp_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel
                sharpen["maximum"].setExpression(expression_sharpen_max)
                expression_sharpen_amount = "AUTO_BEAUTY_"+str(new_index)+"_"+render_choice+"_"+assembly_choice+".par_sharp_amount_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel
                sharpen["amount"].setExpression(expression_sharpen_amount)
                expression_sharpen_size = "AUTO_BEAUTY_"+str(new_index)+"_"+render_choice+"_"+assembly_choice+".par_size_sharp_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel
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
