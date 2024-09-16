import csv
import json
seqcsvfile = open("P:/AndreJukebox/aj_seq_data.csv", "r")
seqreader = csv.DictReader(seqcsvfile)
assetcsvfile = open("P:/AndreJukebox/aj_asset_data.csv", "r")
assetreader = csv.DictReader(assetcsvfile)

seqsdict = {}
assetdict= {}

def seqsdict_export():
    for row in seqreader:
        seq = str(row['seq'])
        shot = str(row['shot'])
        if seq not in seqsdict:
            seqsdict[seq] = {}
        if shot in seqsdict[seq]:
            # print(f"{shot} is duplicated")
            continue
        seqsdict[seq][shot] = {'start':row['start'],'end':row['end'],'assets':row['assets'],'cut':row['cut'],
                            'type':row['type'],'parent':row['parent'],'childs':row['childs'],'layers':row['layers'],
                            'keyframe':row['keyframe']}

    with open('P:/AndreJukebox/aj_seq_dict.json', 'w') as outdict:
        json.dump(seqsdict, outdict)
    print('seqs dict exported')

def assetdict_export():
    for row in assetreader:
        type = str(row['type'])
        asset = str(row['asset'])
        if type not in assetdict:
            assetdict[type] = {}
        if asset in assetdict[type]:
            print(f"{asset} is duplicated")
            continue
        assetdict[type][asset] = {'start':row['start'],'end':row['end'],'layers':row['layers'],'file':row['file']}
    with open('P:/AndreJukebox/aj_asset_dict.json', 'w') as outdict:
        json.dump(assetdict, outdict)
    print('asset dict exported')