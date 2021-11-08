###########################################
#commonTreeEnd.py
#Version 1.3.02

#Last updated August 08 2021
#
#
###########################################

import nuke, re

def common_tree_end(my_group, channels_to_assembly, render_choice, assembly_choice, new_index, read_file, pass_naming):

    ###########################################################################################
    #:::::::::::::::::::::::::::::::::::::END OF COMMON TREE:::::::::::::::::::::::::::::::::::
    ##########################################################################################

    #Common part between Redshift and Cycle tree.
    dot_final = nuke.nodes.Dot(name = "Dot beauty", xpos = nuke.toNode("fresh alpha")["xpos"].value() + 33, ypos = 2470)
    if assembly_choice == "Additive":
        dot_final.setInput(0, nuke.toNode("fresh alpha"))
    else:
        dot_final.setInput(0, nuke.toNode("premult fresh alpha"))


    merge_qc = nuke.nodes.Merge2(name = "Merge QC", xpos = nuke.toNode("Beauty ref")["xpos"].value()+200, ypos = nuke.toNode("Dot beauty")["ypos"].value())
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
    expression_qc_check = "AUTO_BEAUTY_"+str(new_index)+"_"+render_choice+"_"+assembly_choice+".par_qc_check_"+render_choice+"_"+assembly_choice+"_"+str(new_index)
    switch_qc["which"].setExpression(expression_qc_check)

    write_beauty = nuke.nodes.Write(name = "Write beauty_"+render_choice+"_"+assembly_choice+"_"+str(new_index), xpos = nuke.toNode("Dot beauty"), ypos = 2650 )
    write_beauty.setInput(0, nuke.toNode("Switch QC"))
    write_beauty["channels"].setValue("rgba")
    write_beauty["use_limit"].setExpression("AUTO_BEAUTY_"+str(new_index)+"_"+render_choice+"_"+assembly_choice+".par_limit_range_"+render_choice+"_"+assembly_choice+"_"+str(new_index))
    write_beauty["first"].setExpression("AUTO_BEAUTY_"+str(new_index)+"_"+render_choice+"_"+assembly_choice+".par_first_frame_"+render_choice+"_"+assembly_choice+"_"+str(new_index))
    write_beauty["last"].setExpression("AUTO_BEAUTY_"+str(new_index)+"_"+render_choice+"_"+assembly_choice+".par_last_frame_"+render_choice+"_"+assembly_choice+"_"+str(new_index))
    write_beauty["file"].setExpression("AUTO_BEAUTY_"+str(new_index)+"_"+render_choice+"_"+assembly_choice+".par_file_"+render_choice+"_"+assembly_choice+"_"+str(new_index))
    #write_beauty["datatype"].setExpression("AUTO_BEAUTY_"+str(index)+"_"+render_choice+"_"+assembly_choice+".par_data_type_"+render_choice+"_"+assembly_choice+"_"+str(index))


    out = nuke.nodes.Output(name = "Out_AUTO_BEAUTY "+render_choice+" "+assembly_choice, xpos = nuke.toNode("Write beauty_"+render_choice+"_"+assembly_choice+"_"+str(new_index))["xpos"].value(), ypos = 2750)
    out.setInput(0,nuke.toNode("Write beauty_"+render_choice+"_"+assembly_choice+"_"+str(new_index)))
