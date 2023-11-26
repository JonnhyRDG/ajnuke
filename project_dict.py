import json

def dictread(self):
    self.seqsdictjson = open('P:/AndreJukebox/aj_seq_dict.json')
    self.seqsdict = json.load(self.seqsdictjson)