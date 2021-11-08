###########################################
#tabsCreation.py
#Version 1.3.02

#Last updated August 08 2021
#
#
###########################################


import nuke, re

##################################################################
#::::::::::::::::Tabs with knobs creation on group:::::::::::::::#
##################################################################
def tabs_creation(my_group, channels_to_assembly, render_choice, assembly_choice, new_index, read_file, pass_naming):

    #INFOS TAB
    #Messages to the user with the name of the passes supported for each render engine.

    tab_warning = nuke.Tab_Knob("Infos")
    my_group.addKnob(tab_warning)
    message1 = "V1.3.01 emmanuel moulun"
    warning_message1 = nuke.Text_Knob(message1)
    my_group.addKnob(warning_message1)

    message2 = ""
    warning_message2 = nuke.Text_Knob(message2)
    my_group.addKnob(warning_message2)

    message3 = "CYCLE PASSES EXPECTED:"
    warning_message3 = nuke.Text_Knob(message3)
    my_group.addKnob(warning_message3)

    message4 = "RGBA, Diffuse, Glossy, Transmission, Emission"
    warning_message4 = nuke.Text_Knob(message4)
    my_group.addKnob(warning_message4)

    message5 = ""
    warning_message5 = nuke.Text_Knob(message5)
    my_group.addKnob(warning_message5)

    message6 = "REDSHIFT PASSES EXPECTED:"
    warning_message6 = nuke.Text_Knob(message6)
    my_group.addKnob(warning_message6)

    message7 = "RGBA, DiffuseLighting Raw, Emission, GI raw"
    warning_message7 = nuke.Text_Knob(message7)
    my_group.addKnob(warning_message7)

    message8 = "Reflections Raw, Refractions Raw, SpecularLighting"
    warning_message8 = nuke.Text_Knob(message8)
    my_group.addKnob(warning_message8)



    #DENOISE/SHARPEN TAB.
    #Tabs creations, instructions messages.
    tab_denoise = nuke.Tab_Knob("Denoise/ Sharpen")

    my_group.addKnob(tab_denoise)
    pass_selection = nuke.Enumeration_Knob("par_pass_select_denoise", "Pass to preview", channels_to_assembly)
    my_group.addKnob(pass_selection)

    show_pass_denoise = nuke.PyScript_Knob("par_show_pass_den", "Preview pass", "autoBeauty_v1_3_02.show_pass()")
    my_group.addKnob(show_pass_denoise)
    show_beauty_reconstructed = nuke.PyScript_Knob("par_show_beauty_recon", "Back to beauty", "autoBeauty_v1_3_02.show_beauty()")
    my_group.addKnob(show_beauty_reconstructed)
    my_group["par_show_pass_den"].setFlag(nuke.STARTLINE)

    message9 = ""
    warning_message9 = nuke.Text_Knob(message9)
    my_group.addKnob(warning_message9)

    message10 = "WARNING: To access the denoise/sharpen options"
    warning_message10 = nuke.Text_Knob(message10)
    my_group.addKnob(warning_message10)

    message11 = "select the desired pass in the \"preview pass\" menu"
    warning_message11 = nuke.Text_Knob(message11)
    my_group.addKnob(warning_message11)

    message12 = "then, tick the denoise/sharpen boxes"
    warning_message12 = nuke.Text_Knob(message12)
    my_group.addKnob(warning_message12)

    message13 = ""
    warning_message13 = nuke.Text_Knob(message13)
    my_group.addKnob(warning_message13)


    #Denoise controls.
    iterator_pass_naming = 0
    for channel in channels_to_assembly:

        divider_channels = nuke.Text_Knob((pass_naming[iterator_pass_naming]).upper())
        my_group.addKnob(divider_channels)

        on_off = nuke.Boolean_Knob("par_onOff_den_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel, "Enable denoise", False)
        my_group.addKnob(on_off)
        my_group["par_onOff_den_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel].setFlag(nuke.STARTLINE)

        region = nuke.BBox_Knob("par_reg_analys_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel, "Region analysis")
        my_group.addKnob(region)
        my_group["par_reg_analys_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel].setVisible(False)

        render_file_width = read_file.format().width()
        render_file_height = read_file.format().height()
        region_analysis_left = int(render_file_width * 0.3)
        region_analysis_bottom = int(render_file_height * 0.4)
        region_analysis_right = int(render_file_width * 0.5)
        region_analysis_top = int(render_file_height * 0.6)
        my_group["par_reg_analys_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel].setValue((region_analysis_left, region_analysis_bottom, region_analysis_right, region_analysis_top))
        my_group["par_reg_analys_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel].setVisible(False)
        analysis_noise = nuke.PyScript_Knob("par_analysis_den_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel, "Analyze noise", "autoBeauty_v1_3_02.analyze_noise_execution()")
        my_group.addKnob(analysis_noise)
        my_group["par_analysis_den_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel].setVisible(False)

        denoise_amount = nuke.Double_Knob("par_den_amount_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel, "Amount")
        my_group.addKnob(denoise_amount)
        my_group["par_den_amount_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel].setValue(1)
        my_group["par_den_amount_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel].setVisible(False)

        #Sharpen options.
        on_off_sharpen = nuke.Boolean_Knob("par_onOff_sharp_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel, "Enable sharpen", False)
        my_group.addKnob(on_off_sharpen)
        my_group["par_onOff_sharp_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel].setFlag(nuke.STARTLINE)

        minimum_amount = nuke.Double_Knob("par_min_sharp_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel, "Minimum")
        my_group.addKnob(minimum_amount)
        my_group["par_min_sharp_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel].setVisible(False)

        maximum_amount = nuke.Double_Knob("par_max_sharp_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel, "Maximum")
        my_group.addKnob(maximum_amount)
        my_group["par_max_sharp_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel].setValue(1)
        my_group["par_max_sharp_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel].setVisible(False)

        sharpen_amount = nuke.Double_Knob("par_sharp_amount_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel, "Amount")
        my_group.addKnob(sharpen_amount)
        my_group["par_sharp_amount_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel].setValue(1)
        my_group["par_sharp_amount_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel].setVisible(False)

        size_amount = nuke.Double_Knob("par_size_sharp_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel, "Size")
        my_group.addKnob(size_amount)
        my_group["par_size_sharp_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel].setValue(3)
        my_group["par_size_sharp_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel].setVisible(False)

        iterator_pass_naming += 1

    #QC TAB.
    #to compare the beauty reconstructed with the original one.
    tab_qc = nuke.Tab_Knob("QC")
    my_group.addKnob(tab_qc)
    divider_qc = nuke.Text_Knob("If checked, this will difference the original beauty with the reconstruted one")
    my_group.addKnob(divider_qc)
    qc_checker = nuke.Boolean_Knob("par_qc_check_"+render_choice+"_"+assembly_choice+"_"+str(new_index), "QC", False)
    my_group.addKnob(qc_checker)
    my_group["par_qc_check_"+render_choice+"_"+assembly_choice+"_"+str(new_index)].setFlag(nuke.STARTLINE)


    #GRADING TAB.
    #to grade each pass.
    tab_grade = nuke.Tab_Knob("Grading")
    my_group.addKnob(tab_grade)

    iterator_pass_naming = 0
    filters = ["DiffuseFilter", "ReflectionsFilter", "RefractionsFilter"]

    for channel in channels_to_assembly:
        if channel in filters:
            iterator_pass_naming += 1
            continue
        else:
            divider = nuke.Text_Knob((pass_naming[iterator_pass_naming]).upper())
            my_group.addKnob(divider)

            black_point = nuke.Color_Knob("par_b_point_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel, "Blackpoint")
            black_point.setRange(-1,1)
            my_group.addKnob(black_point)
            my_group["par_b_point_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel].setValue(0)

            white_point = nuke.Color_Knob("par_w_point_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel, "Whitepoint")
            white_point.setRange(-1,4)
            my_group.addKnob(white_point)
            my_group["par_w_point_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel].setValue(1)

            lift = nuke.Color_Knob("par_lift_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel, "Lift")
            lift.setRange(-1,1)
            my_group.addKnob(lift)
            my_group["par_lift_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel].setValue(0)

            gain = nuke.Color_Knob("par_gain_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel, "Gain")
            gain.setRange(0,4)
            my_group.addKnob(gain)
            my_group["par_gain_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel].setValue(1)

            multiply = nuke.Color_Knob("par_multiply_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel, "Multiply")
            multiply.setRange(0,4)
            my_group.addKnob(multiply)
            my_group["par_multiply_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel].setValue(1)

            offset = nuke.Color_Knob("par_offset_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel, "Offset")
            offset.setRange(-1,1)
            my_group.addKnob(offset)
            my_group["par_offset_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel].setValue(0)

            gamma = nuke.Color_Knob("par_gamma_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel, "Gamma")
            gamma.setRange(0,5)
            my_group.addKnob(gamma)
            my_group["par_gamma_"+render_choice+"_"+assembly_choice+"_"+str(new_index)+"_"+channel].setValue(1)

            iterator_pass_naming += 1

    #WRITE TAB
    my_list_format = ["exr", "png", "jpeg", "mov"]
    my_list_channels_export = ["rgba", "rgb", "alpha"]
    my_data_type = ["16bits", "32bits"]

    tab_write = nuke.Tab_Knob("Render")
    my_group.addKnob(tab_write)

    channels_selection = nuke.Enumeration_Knob("par_channels_export_"+render_choice+"_"+assembly_choice+"_"+str(new_index), "Channels", my_list_channels_export)
    my_group.addKnob(channels_selection)

    file_prerender = nuke.File_Knob("par_file_"+render_choice+"_"+assembly_choice+"_"+str(new_index), "File path")
    my_group.addKnob(file_prerender)

    file_type = nuke.Enumeration_Knob("par_file_type_"+render_choice+"_"+assembly_choice+"_"+str(new_index), "File type", my_list_format)
    my_group.addKnob(file_type)

    limit_frame_range = nuke.Boolean_Knob("par_limit_range_"+render_choice+"_"+assembly_choice+"_"+str(new_index), "Limit to range", False)
    my_group.addKnob(limit_frame_range)

    first_frame = nuke.Int_Knob("par_first_frame_"+render_choice+"_"+assembly_choice+"_"+str(new_index), "First frame")
    my_group.addKnob(first_frame)

    last_frame = nuke.Int_Knob("par_last_frame_"+render_choice+"_"+assembly_choice+"_"+str(new_index), "Last frame")
    my_group.addKnob(last_frame)

    prerender_button = nuke.PyScript_Knob("par_render_"+render_choice+"_"+assembly_choice+"_"+str(new_index), "Render", "autoBeauty_v1_3_02.render()")
    my_group.addKnob(prerender_button)
    my_group["par_render_"+render_choice+"_"+assembly_choice+"_"+str(new_index)].setFlag(nuke.STARTLINE)
