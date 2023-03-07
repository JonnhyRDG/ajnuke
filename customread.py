import nuke
import os
import re
import glob
import subprocess
import json

class customreads():
    def __init__(self, node=None):
        super(customreads, self).__init__()
        self.group = nuke.thisNode() if node is None else node
        self.project = self.group.knob('project').value()
        self.structure = self.group.knob('structure').value()
        self.customfile = os.path.abspath(self.group.knob('Filepath').value())
        self.aovfolder = []
        self.framenr = "%04d"
        self.colorspace = "linear"
        self.extension = "exr"
        self.depthaov = 'depth'
        self.userbuttons = ["episode", "seq", "shot", "layer", "version", " ", "create", "populate",]
        self.buttontype = ('shader', 'data', 'crypto', 'lightgroups', 'custom')
        self.shaderaov = ['diffuse', 'coat', 'specular', 'sss', 'emission','sheen','check_user_albedo']
        self.dataaov = ['check_user_P','N',self.depthaov,'motionvector','background','cputime']
        self.cryptoaov = ['crypto_asset','crypto_object','crypto_material']
        self.lightgroupsaov = []
        self.customaov = []
        self.dictread()
        self.customtypehidden()
        # self.knobstart() probar con un if para que no se ejecute cada vez que abro un script.
        nuke.addKnobChanged(self.read, nodeClass='Group', node=self.group)

    def customtypehidden(self):
        customknobs = self.group.allKnobs()
        for knobs in customknobs:
            if "customreadclass" in knobs.name():
                self.group.removeKnob(knobs)
        customtype = nuke.Text_Knob('customreadclass', 'customreadclass')
        self.group.addKnob(customtype)
        customtype.setVisible(False)

    def dictread(self):
        self.seqsdictjson = open('P:/AndreJukebox/aj_seq_dict.json')
        self.seqsdict = json.load(self.seqsdictjson)

    def knobstart(self):
        self.createreadtabs()
        epsearchexp = f"{self.project}/*"
        self.epsearchpath = os.path.abspath(epsearchexp)
        epfolder = glob.glob(self.epsearchpath)
        self.episode = epfolder[0]
        seqsearchexp = f"{self.episode}/*"
        self.seqsearchpath = os.path.abspath(seqsearchexp)
        seqfolder = glob.glob(self.seqsearchpath)
        if seqfolder:
            self.seq = seqfolder[0]
        else:
            self.seq = ['']

        shotsearchexp = f"{self.seq}/*"
        self.shotsearchpath = os.path.abspath(shotsearchexp)
        shotfolder = glob.glob(self.shotsearchpath)
        if shotfolder:
            self.shot = shotfolder[0]
        else:
            self.shot = ['']

        layersearchexp = f"{self.shot}/{self.structure}/*"
        self.layersearchpath = os.path.abspath(layersearchexp)
        layerfolder = glob.glob(self.layersearchpath)
        if layerfolder:
            self.layer = layerfolder[0]
        else:
            self.layer = ['']

        versionsearchexp = f"{self.layer}/*"
        self.versionsearchpath = os.path.abspath(versionsearchexp)
        versionfolder = glob.glob(self.versionsearchpath)
        if versionfolder:
            self.version = versionfolder[0]
        else:
            self.version = ['']

        buttondict = {
            "episode": self.epsearchpath,
            "seq": self.seqsearchpath,
            "shot": self.shotsearchpath,
            "layer": self.layersearchpath,
            "version": self.versionsearchpath
        }

        for buttons in buttondict:
            searchpath = buttondict[buttons]
            self.buttongenerate(button=buttons,searchpath=searchpath)
        self.usergui()
        self.group.knobs()['seq'].setValue(nuke.root().knobs()['seqs'].value())
        self.group.knobs()['shot'].setValue(nuke.root().knobs()['shots'].value())

    def cleanui(self):
        all_knobs = self.group.allKnobs()
        for b in all_knobs:
            if b.name() in self.userbuttons:
                self.group.removeKnob(b)
            if "check_user" in b.name():
                self.group.removeKnob(b)
        self.group.knob('Filepath').setValue("")
        self.group.knob('Start').setValue(int(0))
        self.group.knob('End').setValue(int(0))
        self.group.knob('label').setValue('')
        self.cleantabs()
        self.cleanreadtabs()

    # Clears the user tab, deletes all nodes inside the self.group (except for "Ouput") and resets all labels and
    def cleannodes(self):
        all_nodes = self.group.nodes()
        for delnodes in all_nodes:
            if not "Output" in delnodes.name():
                nuke.delete(delnodes)

    def createreadtabs(self):
        tab_name = 'reads'
        readtab = nuke.Tab_Knob(tab_name)
        if not "reads" in self.group.knobs():
            self.group.addKnob(readtab)

    def cleanreadtabs(self):
        tab_knobs = self.group.allKnobs()
        tab_name = 'reads'
        for tabs in tab_knobs:
            if tab_name in tabs.name():
                self.group.removeKnob(tabs)

    def createtabs(self):
        self.cleantabs()
        aovtab = nuke.Tab_Knob("aov_tab")
        self.group.addKnob(aovtab)

        createallbutton = nuke.PyScript_Knob('all', 'all')
        self.group.addKnob(createallbutton)
        nuke.knobTooltip('Group.create', ('Enable all aov components'))
        enableallcode = """import customread
customread.customreads().enableallaovs()"""
        self.group.knob('all').setValue(enableallcode)

        createnonebutton = nuke.PyScript_Knob('none', 'none')
        self.group.addKnob(createnonebutton)
        nuke.knobTooltip('Group.create', ('Enable all aov components'))
        disableallcode = """import customread
customread.customreads().disableallaovs()"""

        for aovbutton in self.buttontype:
            createshaderbutton = nuke.PyScript_Knob(aovbutton, aovbutton)
            self.group.addKnob(createshaderbutton)
            nuke.knobTooltip('Group.create', ('Enable and disable aov components'))
            enablecode = """import customread
customread.customreads().""" + aovbutton + 'aovbutton()'
            self.group.knob(aovbutton).setValue(enablecode)
        self.group.knob('none').setValue(disableallcode)
        lgtstring = nuke.String_Knob('lgt', 'Lightgroups pattern', 'lgroup')
        self.group.addKnob(lgtstring)
        ctmstring = nuke.String_Knob('ctm', 'Custom pattern', '')
        self.group.addKnob(ctmstring)

    def cleantabs(self):
        tab_knobs = self.group.allKnobs()
        for tabs in tab_knobs:
                if tabs.name() in self.buttontype:
                    self.group.removeKnob(tabs)
                if tabs.name() in ("aov_tab","all","none","lgt","ctm"):
                    self.group.removeKnob(tabs)

    def shaderaovbutton(self):
        self.enableaovs(self.shaderaov)

    def dataaovbutton(self):
        self.enableaovs(self.dataaov)

    def cryptoaovbutton(self):
        self.enableaovs(self.cryptoaov)

    def lightgroupsaovbutton(self):
        knobchecks = self.group.allKnobs()
        lgrouppattern = self.group.knob('lgt').value()
        for i in knobchecks:
            if lgrouppattern in i.name():
                if self.group.knob(i.name()).getValue() == 1:
                    self.group.knob(i.name()).setValue(0)
                else:
                    if self.group.knob(i.name()).getValue() == 0:
                        self.group.knob(i.name()).setValue(1)
            else:
                pass

    def customaovbutton(self):
        knobchecks = self.group.allKnobs()
        ctmpattern = self.group.knob('ctm').value()
        for i in knobchecks:
            if ctmpattern in i.name():
                if self.group.knob(i.name()).getValue() == 1:
                    self.group.knob(i.name()).setValue(0)
                else:
                    if self.group.knob(i.name()).getValue() == 0:
                        self.group.knob(i.name()).setValue(1)
            else:
                pass

    def enableallaovs(self):
        knobchecks = self.group.allKnobs()
        for i in knobchecks:
            if "check_user" in i.name():
                self.group.knob(i.name()).setValue(1)
            else:
                pass

    def disableallaovs(self):
        knobchecks = self.group.allKnobs()
        for i in knobchecks:
            if "check_user" in i.name():
                self.group.knob(i.name()).setValue(0)
            else:
                pass

    def enableaovs(self,checkaovlist):
        knobchecks = self.group.allKnobs()
        for i in knobchecks:
            for t in checkaovlist:
                if t in i.name():
                    if self.group.knob(i.name()).getValue() == 1:
                        self.group.knob(i.name()).setValue(0)
                    else:
                        if self.group.knob(i.name()).getValue() == 0:
                            self.group.knob(i.name()).setValue(1)
                else:
                    pass

    def buttongenerate(self,button,searchpath):
        pathitem = os.path.abspath(searchpath)
        item = glob.glob(pathitem)
        additem = []
        for i in item:
            p = i.rsplit("\\")
            if not ".db" in p[-1]:
                additem.append(str(p[-1]))
        if button not in self.group.knobs():
            newknob = nuke.Enumeration_Knob(button, button, additem)
            self.group.addKnob(newknob)
        else:
            itemknob = self.group.knobs()[button]
            itemknob.setValues(additem)

    def checkclean(self):
        allchecks = self.group.allKnobs()
        for checks in allchecks:
            if "check_user" in checks.name():
                self.group.removeKnob(checks)

    def checkbox(self,checkbox):
        if not checkbox in ("rgba","beauty"):
            checkname = "check_user_" + checkbox
            checks = self.group.knobs()
            checkstate = 0
            if checkname in checks:
                checkstate = self.group.knobs()[checkname].getValue()
                print(f'This one {checkname} already existed')
                removecheck = self.group.knobs()[checkname]
                self.group.removeKnob(removecheck)
            else:
                print(f'creating new {checkname}')
            knobcheck = nuke.Boolean_Knob(checkname, checkbox, 0)
            self.group.addKnob(knobcheck)
            # knobcheck.setValue(1)
            knobcheck.setValue(checkstate)
            self.group[checkname].setFlag(nuke.STARTLINE)

    def connectchecks(self):
        selectreads = nuke.allNodes("Read")
        for t in selectreads:
            if not "beauty" in t.name():
                t.knob("disable").setExpression('parent.check_user_' + t.name() + ' == 1 ? 0 : 1')
                shufflenames = t.name() + '_shf'
                shuffles = nuke.toNode(shufflenames)
                if not "crypto" in t.name():
                    shuffles.knob("disable").setExpression('parent.check_user_' + t.name() + ' == 1 ? 0 : 1')

    def currentknobs(self):
        self.episode = self.group.knob('episode').value()
        self.seq = self.group.knob('seq').value()
        self.shot = self.group.knob('shot').value()
        self.layer = self.group.knob('layer').value()

    def update(self):
        self.currentknobs()
        buttoncurrent = ['episode','seq','shot','layer','version']
        for buttons in buttoncurrent:
            episode = self.group.knob('episode').value()
            seq = self.group.knob('seq').value()
            shot = self.group.knob('shot').value()
            layer = self.group.knob('layer').value()
            # Dictionary with current knob values
            buttonupdate = {
                "episode": f"{self.project}/*",
                "seq": f"{self.project}/{episode}/*",
                "shot": f"{self.project}/{episode}/{seq}/*",
                "layer": f"{self.project}/{episode}/{seq}/{shot}/{self.structure}/*",
                "version": f"{self.project}/{episode}/{seq}/{shot}/{self.structure}/{layer}/*"
            }
            for butup in buttonupdate:
                searchpath = buttonupdate[butup]
                currentvalue = self.group.knob(butup).value()
                self.buttongenerate(button=butup,searchpath=searchpath)

    def nodeconnect(self):
        # reads connect for reformat
        reads = nuke.allNodes("Read")
        self.zconnect()
        readnodes = []

        for r in reads:
            refin = nuke.toNode(r.name() + '_ref')
            shfin = nuke.toNode(r.name() + '_shf')
            readin = nuke.toNode(r.name())
            readnodes.append(shfin)
            if r.name() == "Z":
                zmergeshuffle = nuke.toNode('Z_shf')
                readnodes.append(zmergeshuffle)

            if not r.name() == "Z":
                nuke.Layer(r.name(),[r.name()+'.red',r.name()+'.green',r.name()+'.blue',r.name()+'.alpha'])

            if r.name() not in ('crypto_asset','crypto_object','crypto_material',self.depthaov):
                refin.setInput(0, r)
                shfin.knob('out1').setValue(r.name())
                if r.name() == "beauty":
                    shfin.knob('out1').setValue('rgba')
                shfin.knob('fromInput1').setValue("{1} B A")
                shfin.setInput(1, refin)
            if "crypto" in r.name():
                refin.setInput(0, readin)
        createMerge = nuke.nodes.Merge2(name="aovmerge", A="none", also_merge="all", metainput="All")
        reformatnodes = nuke.allNodes(filter='Reformat')
        nro = 0
        for plugs in readnodes:
            nro = nro + 1
            if nro == 2:
                nro = nro + 1
            createMerge.setInput(nro, plugs)
        for refplugs in reformatnodes:
            if "beauty" in refplugs.name():
                createMerge.setInput(0, refplugs)
                
        cryptoreads = nuke.allNodes(filter='Reformat')
        for plugs in cryptoreads:
            nro = nro + 1
            if nro == 2:
                nro = nro + 1
            if "crypto" in plugs.name():
                createMerge.setInput(nro, plugs)
        nuke.toNode("Output1").setInput(0, nuke.toNode('aovmerge'))

    def aovharvest(self):
        # with self.group:
        # Define where to read from the items of the path
        project = self.group.knob('project').value()
        structure = self.group.knob('structure').value()
        episode = self.group.knob('episode').value()
        seq = self.group.knob('seq').value()
        shot = self.group.knob('shot').value()
        layer = self.group.knob('layer').value()
        version = self.group.knob('version').value()

        # STRING EXTRACTION
        # Sequence path
        framepath = f"{project}/{episode}/{seq}/{shot}/{structure}/{layer}/{version}/"
        # Converting all / to system defaults
        searchaovs = os.path.abspath(framepath + "*")

        # listing aov folders
        aovfolders = glob.glob(searchaovs)
        aovsplit = aovfolders[0].rsplit("\\")
        aovfolder = aovsplit[-1]
        searchpaths = os.path.abspath(framepath + aovfolder + "/*" + "." + self.extension)
        files = glob.glob(searchpaths)
        if files:

            # Storing the clean numbers in a variable
            setframestart = self.seqsdict[self.group.knob('seq').value()][self.group.knob('shot').value()]['start']
            setframeend = self.seqsdict[self.group.knob('seq').value()][self.group.knob('shot').value()]['end']

            #Create aov tab
            self.createtabs()
            # forming the full paths for found aovs
            singleaov = []
            for aovcomp in aovfolders:
                singleaov = aovcomp.rsplit("\\", -1)[-1]

                aovfullpath = f"{framepath}{singleaov}/{layer}_{singleaov}.{self.framenr}.{self.colorspace}.{self.extension}"
                self.checkbox(singleaov)

            #set paths strings and frame range
                if "beauty" in singleaov:
                    self.group.knob('Filepath').setValue(aovfullpath)
                    self.group.knob('Start').setValue(int(setframestart))
                    self.group.knob('End').setValue(int(setframeend))

                # create the reads
                if not "rgba" in singleaov:
                    nukepaths = re.sub(r"\\", "/", aovfullpath)
                    nuke.nodes.Read(file=nukepaths, first=setframestart, last=setframeend, name=singleaov,
                                    on_error="nearest frame")

                    # Create reformats and shuffles
                    if singleaov not in ('crypto_asset','crypto_object','crypto_material','depth','P','N','AA_inv_density','Pref'):# self.depthaov):
                        nuke.nodes.Reformat(name=singleaov + '_ref', filter='Lanczos4')
                        nuke.nodes.Shuffle2(name=singleaov + '_shf')
                    elif singleaov not in self.depthaov:
                        nuke.nodes.Reformat(name=singleaov + '_ref', filter='impulse')
                        nuke.nodes.Shuffle2(name=singleaov + '_shf')


        else:
            print('No proper structure found for f´{layer}')

    def customaovharvest(self):
        # Clean self.group
        self.cleannodes()
        # STRING EXTRACTION
        # Sequence path
        aovseparator = 'beauty'
        beautysearch = os.path.abspath(self.customfile.rsplit(aovseparator)[-3]+aovseparator+'\*')
        aovsearch = self.customfile.split("beauty")[0] + '*'

        seqlist = glob.glob(beautysearch)
        # Storing digits between . and a .
        framestart = re.search("\.\d{4}(?:\.*)*", os.path.abspath(seqlist[0]))
        frameend = re.search("\.\d{4}(?:\.*)*", os.path.abspath(seqlist[-1]))

        # Matching the digits only
        framestartnumber = re.search("\d{4}", framestart.group(0))
        frameendnumber = re.search("\d{4}", frameend.group(0))

        # Storing the clean numbers in a variable
        setframestart = self.seqsdict[self.group.knob('seq').value()][self.group.knob('shot').value()]['start']#framestartnumber.group(0)
        setframeend = self.seqsdict[self.group.knob('seq').value()][self.group.knob('shot').value()]['end']#frameendnumber.group(0)

        #create tabs
        self.createtabs()

        # create the reads and the reformats
        aovpaths = glob.glob(aovsearch)
        
        for aovitem in aovpaths:
            singleaov = aovitem.rsplit('\\')[-1]
            self.checkbox(singleaov)
            if "beauty" in aovitem:
                self.group.knob('Start').setValue(int(setframestart))
                self.group.knob('End').setValue(int(setframeend))
            if not "rgba" in aovitem:
                setpath = re.sub("beauty", singleaov, self.customfile)
                nuke.nodes.Read(file=re.sub(r'\\','/',setpath), first=setframestart, last=setframeend, name=singleaov,
                                on_error="nearest frame")
                if singleaov not in ('crypto_asset','crypto_object','crypto_material','depth','P','N','AA_inv_density','Pref'):
                    nuke.nodes.Reformat(name=singleaov + '_ref', filter='Lanczos4')
                    nuke.nodes.Shuffle2(name=singleaov + '_shf')
                elif singleaov not in self.depthaov:
                    nuke.nodes.Reformat(name=singleaov + '_ref', filter='impulse')
                    nuke.nodes.Shuffle2(name=singleaov + '_shf')
        self.nodeconnect()
        self.connectchecks()
        self.customlabel()
        self.setrootframes()

    def usergui(self):
        # if divide line exist, it deletes it and re creates it
        if not ' ' in self.group.knobs():
            divideline = nuke.Text_Knob(' ')
            self.group.addKnob(divideline)

        # if create button exist, it deletes it and re creates it
        if not "create" in self.group.knobs():
            # self.group.removeKnob(n)
            createbutton = nuke.PyScript_Knob("create", "Create")
            self.group.addKnob(createbutton)
            nuke.knobTooltip('Group.create', ('Creates all the reads for the found aovs'))
            createcode = """import customread
customread.customreads().createfunc()
"""
            self.group.knob("create").setValue(createcode)

        # if populate button exist, it deletes it and re creates it
        allthepopulates = self.group.allKnobs()

        if not "populate" in self.group.knobs():
            populatebutton = nuke.PyScript_Knob("populate", "Re-populate")
            self.group.addKnob(populatebutton)
            nuke.knobTooltip('Group.populate', 'Updates all pulldown items')
            populatecode = """import customread
customread.customreads().realoadfunc"""
            self.group.knob("populate").setValue(populatecode)
    # For the callback, condition that this knobs show change execute the update() func.

    def read(self):
        knobflick = nuke.thisKnob()
        if knobflick.name() in ("episode","seq","shot","layer","version"):
            self.update()

    # This function will execute the reload from every read node inside the self.group

    def reloadreads(self):
        allreads = nuke.allNodes(filter='Read')
        for node in allreads:
            node['reload'].execute()

    # This function will override the frames from the GUI into all read nodes inside the self.group
    def overrideframes(self):
        all_nodes = nuke.allNodes(filter="Read")
        overridestart = self.group.knob('Start').value()
        overrideend = self.group.knob('End').value()
        for readnodes in all_nodes:
            readnodes.knob('first').setValue(int(overridestart))
            readnodes.knob('last').setValue(int(overrideend))

    def labelset(self):
        seq = self.group.knob('seq').value()
        shot = self.group.knob('shot').value()
        layer = self.group.knob('layer').value()
        version = self.group.knob('version').value()
        self.grouplabel = f'{seq}_{shot}\n{layer}\n{version}'
        self.group.knob('label').setValue(self.grouplabel)

    def customlabel(self):
        seq = self.customfile.split('\\')[4]
        shot = self.customfile.split('\\')[5]
        file = self.customfile.split('\\')[10]
        layer = file.split('_')[0] + '_' + file.split('_')[1]
        ststart = self.group.knob('Start').value()
        stend = self.group.knob('End').value()
        version = self.customfile.split('\\')[8]
        self.grouplabel = f'{seq}_{shot}\n{layer}\n{version}'
        self.group.knob('label').setValue(self.grouplabel)

    def openexplorer(self):
        finalpath = self.group.knob('Filepath').value()
        pathsplit = os.path.abspath(finalpath.rsplit('/',2)[0])
        subprocess.call(f'explorer {pathsplit}', shell=True)

    def openseqrv(self):
        finalpath = self.group.knob('Filepath').value()
        pathsplit = os.path.abspath(finalpath.rsplit('/', 2)[0]) + '\\' + 'rgba'
        rv = "rv.exe"
        cmline = f'{rv} {pathsplit}'
        os.system(f'start cmd /c {cmline}')

    def setrootframes(self):
        rootframestart = self.seqsdict[self.group.knob('seq').value()][self.group.knob('shot').value()]['start']
        rootframeend = self.seqsdict[self.group.knob('seq').value()][self.group.knob('shot').value()]['end']
        nuke.root().knobs()['first_frame'].setValue(int(rootframestart))
        nuke.root().knobs()['last_frame'].setValue(int(rootframeend))

    def zconnect(self):
        allreads = nuke.allNodes("Read")
        for zread in allreads:
            if zread.name() in self.depthaov:
                zread = nuke.toNode(self.depthaov)
                createZref = nuke.nodes.Reformat(name=self.depthaov + '_ref', filter='impulse')
                createZmerge = nuke.nodes.Merge2(name=self.depthaov + "_shf", A="none", output = self.depthaov )
                createZref.setInput(0, zread)
                createZmerge.setInput(0, createZref)

    # Funtions for the buttons
    def createfunc(self):
        with self.group:
            self.cleannodes()
            # self.checkclean()
            self.aovharvest()
            self.nodeconnect()
            self.connectchecks()
            self.labelset()
            self.setrootframes()

    def realoadfunc(self):
        self.update()
