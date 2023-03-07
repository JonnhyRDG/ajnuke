import nuke

class varenable():
    def __init__(self):
        super(varenable, self).__init__()
        self.group = nuke.thisNode()
        self.disableexp()
        self.availablevars()

    def disableexp(self):
        disexpression = '[python {0 if (nuke.root().knobs()[nuke.thisNode().knobs()["variable"].value()].value()) in nuke.thisNode().knob("pattern").value() else 1}]'
        self.group.knob("disable").setExpression(disexpression)

    def availablevars(self):
        variables = 'seqs shots'
        varbutton = nuke.Text_Knob('varbtn', 'Available variables (gsv)', f'{variables}')
        varexist = self.group.knobs()
        if not 'varbtn' in varexist:
            self.group.addKnob(varbutton)