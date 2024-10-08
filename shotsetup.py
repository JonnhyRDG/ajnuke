import nuke
import nukescripts
import json
import customread
import project_dict

class shotsetup(nukescripts.PythonPanel):
    def __init__(self):
        nukescripts.PythonPanel.__init__(self,"GSV manager", 'com.ohufx.gsvmanager')
        project_dict.proj_dict().dictread()
        self.knobstart()
        self._knobs_callbacks = {'init':{''}}

    def knobChanged(self,knob):
        # elif method for button callbacks
        if knob == self.setseqshotbtn:
            self.setseqshots()
        elif knob == self.seqknob:
            self.updateshotsknobs()
            self.shotinfoupdate()
        elif knob == self.shotknob:
            self.syncshot()
            self.shotinfoupdate()
            self.setseqshots()
        elif knob == self.showknob:
            self.setseqshots()
            

        # if knob in self._knobs_callbacks:
        #         self._knobs_callbacks[knob]()

    def syncshot(self):
        self.currentshot = self.knobs()['shot'].value()
        nuke.root().knobs()['shots'].setValue(self.currentshot)

    def buildshow(self):
        ## This is an arbitrary list, should be changed eventually by database info
        addshowitem = ['assets','concept_animatic']
        self.showknob = nuke.Enumeration_Knob('show', 'show', addshowitem)
        self.addKnob(self.showknob)
        self.showknob.clearFlag(nuke.STARTLINE)
        self.setglobalshow()

    def shotinfoupdate(self):
        currentseq = self.knobs()['seq'].value()
        currentshot = self.knobs()['shot'].value()
        shottype = project_dict.proj_dict().seqsdict[currentseq][currentshot]['type']
        self.knobs()['shottypebtn'].setValue(shottype)

        shotparent = project_dict.proj_dict().seqsdict[currentseq][currentshot]['parent']
        self.knobs()['parentbtn'].setValue(shotparent)

        shotchilds = project_dict.proj_dict().seqsdict[currentseq][currentshot]['childs']
        shotchildslist = shotchilds.replace(","," ")
        self.knobs()['childsbtn'].setValue(shotchildslist)
    
    def shotinfo(self):
        currentseq = self.knobs()['seq'].value()
        currentshot = self.knobs()['shot'].value()
        shottype = project_dict.proj_dict().seqsdict[currentseq][currentshot]['type']
        shottypebutton = nuke.Text_Knob('shottypebtn', 'Shot Type', shottype)
        self.addKnob(shottypebutton)

        shotparent = project_dict.proj_dict().seqsdict[currentseq][currentshot]['parent']
        parentbutton = nuke.Text_Knob('parentbtn', 'Parent', shotparent)
        self.addKnob(parentbutton)
        
        shotchilds = project_dict.proj_dict().seqsdict[currentseq][currentshot]['childs']
        shotchildslist = shotchilds.replace(","," ")
        childsbutton = nuke.Text_Knob('childsbtn', 'Child List', shotchildslist)
        self.addKnob(childsbutton)
    
    def updateshotsknobs(self):
        self.currentseq = self.knobs()['seq'].value()
        self.currentshot = self.knobs()['shot'].value()
        shot_knob = self.knobs()['shot']
        updateshot = []
        for newshots in project_dict.proj_dict().seqsdict[self.currentseq]:
            updateshot.append(newshots)
        shot_knob.setValues(updateshot)
        nuke.root().knobs()['shots'].setValues(updateshot)
        shot_knob.setValue(updateshot[0])
        nuke.root().knobs()['shots'].setValue(updateshot[0])
        nuke.root().knobs()['seqs'].setValue(self.currentseq)

    def knobstart(self):
        self.buildshow()
        addseqitem = []
        for seqs in project_dict.proj_dict().seqsdict:
            addseqitem.append(seqs)
        self.seqknob = nuke.Enumeration_Knob('seq', 'seq', addseqitem)
        self.addKnob(self.seqknob)
        self.setglobalseq()

        addshotitem = []
        currentseq = self.knobs()['seq'].value()
        for shots in project_dict.proj_dict().seqsdict[currentseq]:
            addshotitem.append(shots)
        self.shotknob = nuke.Enumeration_Knob('shot', 'shot', addshotitem)
        self.addKnob(self.shotknob)
        self.shotknob.clearFlag(nuke.STARTLINE)
        self.setglobalshot()

        self.setseqshotbtn = nuke.PyScript_Knob('setseqshot','SET')
        # self._knobs_callbacks[self.setseqshot] =  self.setseqshots
        self.addKnob(self.setseqshotbtn)
        self.setseqshotbtn.clearFlag(nuke.STARTLINE)
        
        self.importlayer = nuke.PyScript_Knob('importlayer','IMPORT')
        # self._knobs_callbacks[self.importlayer] =  self.importlayer
        self.addKnob(self.importlayer)
        self.importlayer.clearFlag(nuke.STARTLINE)

        # dividetabline = nuke.Text_Knob(' ')
        # self.addKnob(dividetabline)
        shotinfotabline = nuke.Text_Knob('Shot info')
        self.addKnob(shotinfotabline)
        self.shotinfo()

    def setglobalshow(self):
        globalshow = nuke.root().knobs()['show'].value()
        seqknob = self.knobs()['show']
        seqknob.setValue(globalshow)

    def setglobalseq(self):
        globalseq = nuke.root().knobs()['seqs'].value()
        seqknob = self.knobs()['seq']
        seqknob.setValue(globalseq)

    def setglobalshot(self):
        globalshot = nuke.root().knobs()['shots'].value()
        shotknob = self.knobs()['shot']
        shotknob.setValue(globalshot)

    def setseqshots(self):
        allcustoms = nuke.allNodes('Group')
        self.currentshow = self.knobs()['show'].value() 
        self.currentseq = self.knobs()['seq'].value()
        self.currentshot = self.knobs()['shot'].value()
        nuke.root().knobs()['show'].setValue(self.currentshow)
        nuke.root().knobs()['seqs'].setValue(self.currentseq)
        nuke.root().knobs()['shots'].setValue(self.currentshot)
    
        
        # import ptvsd
        # ptvsd.enable_attach(address=('localhost',3000))
        # ptvsd.wait_for_attach()
        # breakpoint()
        
        for ctms in allcustoms:
            if ctms.knob('customread'):
                customreadfunc = customread.customreads(node=ctms)
                currentversion = ctms.knob("version").value()
                layervalue = ctms.knob("layer").value()
                if currentversion != "latest":
                    ctms.knob("version").setValue("latest")
                if ctms.knob('seq'):
                    ctms.knob("seq").setValue(nuke.root().knobs()['seqs'].value())
                    customreadfunc.update()
                if ctms.knob('shot'):
                    ctms.knob("shot").setValue(nuke.root().knobs()['shots'].value())
                    customreadfunc.update()
                if ctms.knob('layer'):
                    ctms.knob("layer").setValue(layervalue)
                    customreadfunc.update()
                # ctms.knob("create").execute()
                customreadfunc.createfunc()
