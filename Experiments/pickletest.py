import pickle

table1 = {
    "clip1":[["Jason", "Daniel"],["Jason"]],
    "clip2":[["Jason"],["Jason"]],
    "clip3":[["Jason"],[]],
    "clip4":[[],["Daniel"]],
    "clip5":[[],[]]
}

#write a table to a new pickle file
pickle_filename = pickletest_table1
with open(pickle_filename, 'w+b') as pfile:
    pickle.dump(table1, pfile)

input("continue")

#add entries to an existing pickle file
newEntry = {"clip420":[["Daniel"],["Daniel"]]}

pfile = open(pickle_filename, 'r+b')
db = pickle.load(pfile)
pfile.close()

for k,v in newEntry.items():
    db[k] = v
    
with open(pickle_filename, 'w+b') as pfile:
    pickle.dump(db, pfile)