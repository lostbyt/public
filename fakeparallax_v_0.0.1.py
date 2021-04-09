###########################################
#fake_parallax_v007.py
#Version 0.0.1
#Last updated April 08 2021
#This module allow you to simulate fake parallax on a static image while push in into it. Separation of the fgnd, mdgnd and bkgnd
#is done by the user with rotos. Based on tutorial: https://www.youtube.com/watch?v=avtDQcZNThI
###########################################
import nuke


node_index = 1
roto_index = 1


class fake_parallax:
    def __init__(self, num):
        self._num = num

    def starter(self):
        grp = nuke.nodes.Group(name = "FAKE PARALLAX " + str(self._num), note_font= "Bahnschrift SemiLight")
        grp["tile_color"].setValue(5608959)

        #User interface construction
        title_01        = nuke.Text_Knob("par_title01", "::::: G L O B A L  T R A N S F O R M :::::")
        glb_translation = nuke.XY_Knob("par_glb_translate", "Translate")
        glb_scale       = nuke.WH_Knob("par_glb_scale", "Scale")
        glb_center      = nuke.XY_Knob("par_glb_center", "Center")
        title_02        = nuke.Text_Knob("Testi", "::::: R O T O  C R E A T I O N :::::")
        plane_crea      = nuke.PyScript_Knob("par_plane_crea", "Create new roto", "fake_parallax_v007.plane_crea()")
        divider_01      = nuke.Text_Knob("divider_01", "")

        glb_scale.setValue(1)
        glb_center.setValue([nuke.root().width() / 2, nuke.root().height() / 2])

        grp.addKnob(title_01)
        grp.addKnob(glb_scale)
        grp.addKnob(glb_translation)
        grp.addKnob(glb_center)
        grp.addKnob(title_02)
        grp.addKnob(plane_crea)
        grp.addKnob(divider_01)

        #Nodes creation
        grp.begin()
        c         = nuke.nodes.Constant(xpos = 0, ypos = 0, channels= "rgb")
        e         = nuke.nodes.Expression(inputs= [c], expr0= "(x+.5)/width", expr1= "(y+.5)/height")
        t         = nuke.nodes.Transform(name = "Global_transform", inputs= [e])

        t["scale"].setExpression("parent.par_glb_scale")
        t["translate"].setExpression("parent.par_glb_translate")
        t["center"].setExpression("parent.par_glb_center")

        d_tr      = nuke.nodes.Dot(name = "Dot glb transf", xpos = (t.screenWidth()/2)-5, ypos = 200, inputs = [t])
        d_ST      = nuke.nodes.Dot(name = "Dot STMap", xpos = (t.screenWidth()/2), ypos = 800, inputs = [d_tr])
        i         = nuke.nodes.Input(name = "Image input", xpos = 400, ypos = 50)
        s         = nuke.nodes.STMap(xpos= i.xpos(), ypos= 800 - (d_tr.screenWidth()/2), inputs = [i, d_ST], uv = "rgb")
        d_sh      = nuke.nodes.Dot(name = "Dot to alpha", label = "to alpha", xpos = s.xpos()-500, ypos = 1000, inputs = [d_ST])
        const     = nuke.nodes.Constant(name = "Constant overlay", xpos = s.xpos() - 200, ypos = 900, channels = "rgba.red -rgba.green -rgba.blue -rgba.alpha", color = 1)
        copy      = nuke.nodes.Copy(xpos = const.xpos(), ypos = 1000, inputs = [const, d_sh], from0 = "rgba.alpha", to0 = "rgba.alpha" )
        pre       = nuke.nodes.Premult(xpos = copy.xpos(), ypos = 1200, inputs =[copy])
        m_over    = nuke.nodes.Merge2(name = "Merge overlay", xpos = s.xpos(), ypos = 1200, inputs = [s, pre], mix = 0.5 )
        sw        = nuke.nodes.Switch(name = "Switch overlay", xpos = s.xpos() + 150, ypos = 1200, inputs = [s, m_over])
        o         = nuke.nodes.Output(inputs = [sw], xpos = s.xpos() + 150, ypos = 1400)
        grp.end()



def plane_crea():

    global roto_index
    index = check_input()

    if index == 0:
        i = nuke.nodes.Input(name = "Roto input "+ str(roto_index), xpos = -400, ypos = 0)
    else:
        i = nuke.nodes.Input(name = "Roto input "+ str(roto_index), xpos = nuke.toNode("Roto input " + str(index))["xpos"].value() -400, ypos = 0)

    e        = nuke.nodes.FilterErode(name = "Roto erode "+ str(roto_index), inputs = [i])
    b        = nuke.nodes.Blur(name = "Roto blur "+ str(roto_index), inputs = [e])
    t_global = nuke.nodes.Transform(name = "Global_transform "+ str(roto_index), inputs = [b])
    d_roto   = nuke.nodes.Dot(name = "dot roto " + str(roto_index), inputs = [t_global])
    d_image  = nuke.nodes.Dot(name = "dot image " + str(roto_index), xpos = 200, ypos = 100, inputs = [nuke.toNode("Global_transform")])
    t_roto   = nuke.nodes.Transform(name = "Roto transform" + str(roto_index), xpos = 200, ypos = 300, inputs = [d_image])


    e["size"].setExpression("parent.par_roto_erode_" + str(roto_index))
    b["size"].setExpression("parent.par_roto_blur_" + str(roto_index))
    t_global["translate"].setExpression("parent.Global_transform.translate")
    t_global["scale"].setExpression("parent.Global_transform.scale")
    t_global["center"].setExpression("parent.Global_transform.center")
    t_roto["translate"].setExpression("par_roto_translate_" +str(roto_index))
    t_roto["scale"].setExpression("par_roto_scale_" +str(roto_index))
    t_roto["center"].setExpression("par_roto_center_" +str(roto_index))


    r = check_keymix()
    if r != 0:
        k    = nuke.nodes.Keymix(name = "Keymix roto " + str(roto_index), xpos = nuke.toNode("Global_transform")["xpos"].value(),
        ypos = nuke.toNode("Keymix roto " + str(r))["ypos"].value() + 80, inputs = [nuke.toNode(("Keymix roto " + str(r))), t_roto, d_roto])
        nuke.toNode("Dot STMap").setInput(0,k)
    else:
        k    = nuke.nodes.Keymix(name = "Keymix roto " + str(roto_index), xpos = nuke.toNode("Global_transform")["xpos"].value(),
        ypos = nuke.toNode("Global_transform")["ypos"].value() + 80, inputs = [nuke.toNode("Dot glb transf"), t_roto, d_roto])
        nuke.toNode("Dot STMap").setInput(0, nuke.toNode("Keymix roto " + str(roto_index)))


    grp       = nuke.thisGroup()
    title_03  = nuke.Text_Knob("par_title03_"+ str(roto_index), "Roto " + str(roto_index) + " transform")
    overlay   = nuke.PyScript_Knob("par_overlay_" + str(roto_index), "Overlay roto " + str(roto_index), "num = " + str(roto_index) + "\nfake_parallax_v007.overlay(num)")
    plane_del = nuke.PyScript_Knob("par_plane_del_" + str(roto_index), "Delete roto " + str(roto_index), "num =" + str(roto_index)+"\nfake_parallax_v007.plane_del(num)")
    roto_erod = nuke.WH_Knob("par_roto_erode_" + str(roto_index), "Erode")
    roto_blur = nuke.WH_Knob("par_roto_blur_" + str(roto_index), "Blur")
    roto_tran = nuke.XY_Knob("par_roto_translate_" + str(roto_index), "Translate")
    roto_scal = nuke.WH_Knob("par_roto_scale_" + str(roto_index), "Scale")
    roto_cent = nuke.XY_Knob("par_roto_center_" + str(roto_index), "Center")

    roto_scal.setValue(1)
    roto_cent.setValue([nuke.root().width() / 2, nuke.root().height() / 2])

    grp.addKnob(title_03)
    grp.addKnob(overlay)
    grp.addKnob(plane_del)
    grp.addKnob(roto_erod)
    grp.addKnob(roto_blur)
    grp.addKnob(roto_tran)
    grp.addKnob(roto_scal)
    grp.addKnob(roto_cent)

    roto_index += 1

def plane_del(num):

    #Nodes to delete
    nuke.delete(nuke.toNode("Keymix roto " + str(num)))
    nuke.delete(nuke.toNode("Global_transform " + str(num)))
    nuke.delete(nuke.toNode("Roto blur " + str(num)))
    nuke.delete(nuke.toNode("Roto erode " + str(num)))
    nuke.delete(nuke.toNode("Roto input " + str(num)))
    nuke.delete(nuke.toNode("dot roto " + str(num)))
    nuke.delete(nuke.toNode("Roto transform" + str(num)))
    nuke.delete(nuke.toNode("dot image " + str(num)))

    #knobs to delete
    nuke.toNode("FAKE PARALLAX " + str(num))
    my_group = nuke.thisNode()
    knobs = my_group.knobs()
    my_group.removeKnob(knobs["par_title03_" + str(num)])
    my_group.removeKnob(knobs["par_plane_del_" + str(num)])
    my_group.removeKnob(knobs["par_roto_erode_" + str(num)])
    my_group.removeKnob(knobs["par_roto_blur_" + str(num)])
    my_group.removeKnob(knobs["par_roto_translate_" + str(num)])
    my_group.removeKnob(knobs["par_roto_scale_" + str(num)])
    my_group.removeKnob(knobs["par_roto_center_" + str(num)])
    my_group.removeKnob(knobs["par_overlay_" + str(num)])

    nuke.toNode("Dot to alpha").setInput(0, nuke.toNode("Dot STMap"))
    nuke.toNode("Switch overlay")["which"].setValue(0)

def check_input():
        index = 0

        for node in nuke.allNodes("Input"):
            if node.name()[:4] == "Roto":
                index = node.name().split(" ")
                index = int(index[2])
        return index

def check_keymix():
    r = 0

    for node in nuke.allNodes("Keymix"):
        if int(node.name().split(" ")[2]) > r:
            r = int(node.name().split(" ")[2])
    return r

def overlay(num):
    if nuke.toNode("Switch overlay")["which"].value() == 1:
        nuke.toNode("Switch overlay")["which"].setValue(0)
    else:
        nuke.toNode("Dot to alpha").setInput(0, nuke.toNode("dot roto " + str(num)))
        nuke.toNode("Switch overlay")["which"].setValue(1)

def main():
    group_fake = fake_parallax(node_index)
    group_fake.starter()
    global node_index
    node_index += 1
