import json

class proj_dict():
    def __init__(self):
        self.dictread()

    def dictread(self):
        self.seqsdictjson = open('P:/AndreJukebox/aj_seq_dict.json')
        self.seqsdict = json.load(self.seqsdictjson)
        self.assetdictjson = open('P:/AndreJukebox/aj_asset_dict.json')
        self.assetdict = json.load(self.assetdictjson)

    def reload(self):
        self.seqsdict.clear()
        self.assetdict.clear()
        print("dictionary cleared")       

proj_dict()