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