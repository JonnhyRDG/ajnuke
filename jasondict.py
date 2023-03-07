import csv
import json
csvfile = open("P:/AndreJukebox/aj_seq_data.csv", "r")
reader = csv.DictReader(csvfile)

seqsdict = {}

for row in reader:
    seq = str(row['seq'])
    shot = str(row['shot'])
    if seq not in seqsdict:
        seqsdict[seq] = {}
    if shot in seqsdict[seq]:
        print(f"{self.shot} is duplicated")
        continue
    seqsdict[seq][shot] = {'start':row['start'],'end':row['end'],'assets':row['assets'],'cut':row['cut'],
                           'type':row['type'],'parent':row['parent'],'childs':row['childs']}

with open('P:/AndreJukebox/aj_seq_dict.json', 'w') as outdict:
    json.dump(seqsdict, outdict)


# import json
# seqsdictjson = open('P:/AndreJukebox/aj_seq_dict.json')
# seqsdict = json.load(seqsdictjson)
# print(seqsdict['020_MFG']['s0260']['end'])
#
# seqlist = []
# shotlist = []
#
# for seq in seqsdict:
#     seqlist.append(seq)
#
# seq = '010_NCT'
#
# for shot in seqsdict[seq]:
#         shotlist.append(shot)
#
# print(shotlist)

# for seqs in seqsdict:
#     for shots in seqsdict[seqs]:
#         check = 'type'
#         pattern = 'key'
#         if seqsdict[seqs][shots][check] == pattern:
#             print(f"{pattern}:{seqs}_{shots} --childs--> {seqsdict[seqs][shots]['childs']}")

