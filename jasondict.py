import csv
import json


class json_exp():
    def __init__(self):
        self.readFiles()


    def readFiles(self):
        self.seqcsvfile = open("P:/AndreJukebox/aj_seq_data.csv", "r")
        self.seqreader = csv.DictReader(self.seqcsvfile)
        self.assetcsvfile = open("P:/AndreJukebox/aj_asset_data.csv", "r")
        self.assetreader = csv.DictReader(self.assetcsvfile)

        self.seqsdict = {}
        self.assetdict= {}

    def seqsdict_export(self):
        for row in self.seqreader:
            seq = str(row['seq'])
            shot = str(row['shot'])
            if seq not in self.seqsdict:
                self.seqsdict[seq] = {}
            if shot in self.seqsdict[seq]:
                # print(f"{shot} is duplicated")
                continue
            self.seqsdict[seq][shot] = {'start':row['start'],'end':row['end'],'assets':row['assets'],'cut':row['cut'],
                                'type':row['type'],'parent':row['parent'],'childs':row['childs'],'layers':row['layers'],
                                'keyframe':row['keyframe']}

        with open('P:/AndreJukebox/aj_seq_dict.json', 'w') as outdict:
            json.dump(self.seqsdict, outdict)
        print('seqs dict exported')

    def assetdict_export(self):
        # self.assetdict = {}
        for row in self.assetreader:
            type = str(row['type'])
            asset = str(row['asset'])
            if type not in self.assetdict:
                self.assetdict[type] = {}
            if asset in self.assetdict[type]:
                print(f"{asset} is duplicated")
                continue
            self.assetdict[type][asset] = {'start':row['start'],'end':row['end'],'layers':row['layers'],'file':row['file']}
        with open('P:/AndreJukebox/aj_asset_dict.json', 'w') as outdict:
            json.dump(self.assetdict, outdict)
        print('asset dict exported')