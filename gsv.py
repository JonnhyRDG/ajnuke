import nuke
import json
import project_dict

class gsvroot():
    def __init__(self):
        self.group = nuke.thisNode()
        project_dict.dictread(self)
        self.populateroot()
        nuke.addKnobChanged(self.updateshots)#, nodeClass='Group', node=self.group)

    def populateroot(self):
        self.nukeroot = nuke.root()
        tab = nuke.Tab_Knob("GSV")
        self.nukeroot.addKnob(tab)
        self.buildshow()
        self.buildseqs()
        self.buildshots()
        self.shotinfo()
        # self.updateshots()

    def buildshow(self):
        ## This is an arbitrary list, should be changed eventually by database info
        addshowitem = ['assets','concept_animatic']
        showknob = nuke.Enumeration_Knob('show', 'show', addshowitem)
        self.nukeroot.addKnob(showknob)
        showknob.clearFlag(nuke.STARTLINE)

    def buildseqs(self):
        addseqitem = []
        for seqs in self.seqsdict:
            addseqitem.append(seqs)
        seqknob = nuke.Enumeration_Knob('seqs', 'seq', addseqitem)
        self.nukeroot.addKnob(seqknob)

    def shotinfo(self):
        currentseq = nuke.root().knobs()['seqs'].value()
        currentshot = nuke.root().knobs()['shots'].value()
        shottype = self.seqsdict[currentseq][currentshot]['type']
        shottypebutton = nuke.Text_Knob('shottypebtn', 'Shot Type', shottype)
        self.nukeroot.addKnob(shottypebutton)

        shotparent = self.seqsdict[currentseq][currentshot]['parent']
        parentbutton = nuke.Text_Knob('parentbtn', 'Parent', shotparent)
        self.nukeroot.addKnob(parentbutton)
        
        shotchilds = self.seqsdict[currentseq][currentshot]['childs']
        childsbutton = nuke.Text_Knob('childsbtn', 'Child List', shotchilds)
        self.nukeroot.addKnob(childsbutton)

    def shotinfoupdate(self):
        currentseq = nuke.root().knobs()['seqs'].value()
        currentshot = nuke.root().knobs()['shots'].value()
        shottype = self.seqsdict[currentseq][currentshot]['type']
        nuke.root().knobs()['shottypebtn'].setValue(shottype)

        shotparent = self.seqsdict[currentseq][currentshot]['parent']
        nuke.root().knobs()['parentbtn'].setValue(shotparent)

        shotchilds = self.seqsdict[currentseq][currentshot]['childs']
        shotschildlist = shotchilds.replace(","," ")
        nuke.root().knobs()['childsbtn'].setValue(shotschildlist)

    def buildshots(self):
        addshotitem = []
        currentseq = self.group.knobs()['seqs'].value()
        for shots in self.seqsdict[currentseq]:
            addshotitem.append(shots)
        shotknob = nuke.Enumeration_Knob('shots', 'shot', addshotitem)
        self.nukeroot.addKnob(shotknob)
        shotknob.clearFlag(nuke.STARTLINE)
    
    # callbacks!

    def updateshots(self):
        knoblfick = nuke.thisKnob()
        if knoblfick.name() in ('seqs','shots'):
            print('gsv callback!')
            self.currentseq = nuke.root().knobs()['seqs'].value()
            shot_knob = nuke.root().knobs()['shots']
            updateshot = []
            for newshots in self.seqsdict[self.currentseq]:
                updateshot.append(newshots)
            shot_knob.setValues(updateshot)
            self.shotinfoupdate()