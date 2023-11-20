import customread
import gsv
import shotsetup
import nukescripts
import nuke

gsv.gsvroot()
shotsetup.shotsetup()

def addShotSetupPanel():
    global ssPanel
    ssPanel = shotsetup.shotsetup()
    return ssPanel.addToPane()

paneMenu = nuke.menu('Pane')
paneMenu.addCommand('GSV Manager', addShotSetupPanel)
nukescripts.registerPanel('com.ohufx.gsvmanager', addShotSetupPanel)

toolbar = nuke.toolbar("Nodes")
m = toolbar.addMenu("André Jukebox", icon="P:/AndreJukebox/lib/logo/icon.png")

m.addCommand("aov cc", "nuke.createNode(\"AovCC\")")
m.addCommand("aov glow", "nuke.createNode(\"AovGlow\")")
m.addCommand("chromatic aberration", "nuke.createNode(\"ca\")")
m.addCommand("render stats", "nuke.createNode(\"renStats\")")
m.addCommand("render compare", "nuke.createNode(\"renCompare\")")
m.addCommand("exp blur", "nuke.createNode(\"expBlur\")")
m.addCommand("customreads", "nuke.createNode(\"customreads\")")
m.addCommand("veg", "nuke.createNode(\"veg\")")

nuke.addFormat("2048 858 andre_output")
nuke.addFormat("3840 1613 andre_output_4k")

import DeadlineNukeClient
menubar = nuke.menu("Nuke")
tbmenu = menubar.addMenu("&Thinkbox")
tbmenu.addCommand("Submit Nuke To Deadline", DeadlineNukeClient.main, "")

toolbar = nuke.toolbar("Nodes")
toolbar.addMenu("VideoCopilot", icon="VideoCopilot.png")
toolbar.addCommand( "VideoCopilot/OpticalFlares", "nuke.createNode('OpticalFlares')", icon="OpticalFlares.png")