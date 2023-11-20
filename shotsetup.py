import nuke
import nukescripts
import json
import customread

class shotsetup(nukescripts.PythonPanel):
    def __init__(self):
        nukescripts.PythonPanel.__init__(self,"GSV manager", 'com.ohufx.gsvmanager')
        self.jsonread()
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

        # if knob in self._knobs_callbacks:
        #         self._knobs_callbacks[knob]()

    def syncshot(self):
        self.currentshot = self.knobs()['shot'].value()
        nuke.root().knobs()['shots'].setValue(self.currentshot)

    def shotinfoupdate(self):
        currentseq = self.knobs()['seq'].value()
        currentshot = self.knobs()['shot'].value()
        shottype = self.seqsdict[currentseq][currentshot]['type']
        self.knobs()['shottypebtn'].setValue(shottype)

        shotparent = self.seqsdict[currentseq][currentshot]['parent']
        self.knobs()['parentbtn'].setValue(shotparent)

        shotchilds = self.seqsdict[currentseq][currentshot]['childs']
        shotchildslist = shotchilds.replace(","," ")
        self.knobs()['childsbtn'].setValue(shotchildslist)
    
    def shotinfo(self):
        currentseq = self.knobs()['seq'].value()
        currentshot = self.knobs()['shot'].value()
        shottype = self.seqsdict[currentseq][currentshot]['type']
        shottypebutton = nuke.Text_Knob('shottypebtn', 'Shot Type', shottype)
        self.addKnob(shottypebutton)

        shotparent = self.seqsdict[currentseq][currentshot]['parent']
        parentbutton = nuke.Text_Knob('parentbtn', 'Parent', shotparent)
        self.addKnob(parentbutton)
        
        shotchilds = self.seqsdict[currentseq][currentshot]['childs']
        shotchildslist = shotchilds.replace(","," ")
        childsbutton = nuke.Text_Knob('childsbtn', 'Child List', shotchildslist)
        self.addKnob(childsbutton)
    
    def updateshotsknobs(self):
        self.currentseq = self.knobs()['seq'].value()
        self.currentshot = self.knobs()['shot'].value()
        shot_knob = self.knobs()['shot']
        updateshot = []
        for newshots in self.seqsdict[self.currentseq]:
            updateshot.append(newshots)
        shot_knob.setValues(updateshot)
        nuke.root().knobs()['shots'].setValues(updateshot)
        shot_knob.setValue(updateshot[0])
        nuke.root().knobs()['shots'].setValue(updateshot[0])
        nuke.root().knobs()['seqs'].setValue(self.currentseq)

    def jsonread(self):
        self.seqsdictjson = open('P:/AndreJukebox/aj_seq_dict.json')
        self.seqsdict = json.load(self.seqsdictjson)

    def knobstart(self):
        addseqitem = []
        for seqs in self.seqsdict:
            addseqitem.append(seqs)
        self.seqknob = nuke.Enumeration_Knob('seq', 'seq', addseqitem)
        self.addKnob(self.seqknob)
        self.setglobalseq()

        addshotitem = []
        currentseq = self.knobs()['seq'].value()
        for shots in self.seqsdict[currentseq]:
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
        self.currentseq = self.knobs()['seq'].value()
        self.currentshot = self.knobs()['shot'].value()
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
