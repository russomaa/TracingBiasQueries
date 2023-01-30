import os

class Triple:
    def __init__(self, head, predicate, tail, dataset=""):
        self.head = head
        self.predicate = predicate
        self.tail = tail
        self.dataset = dataset
    
    def __hash__(self):
        return hash(repr(self))
    
    def __repr__(self) -> str:
        return "Triple(" + str(self) + ")"
    
    def __eq__(self, __o: object) -> bool:
        return self.head == __o.head and self.predicate == __o.predicate and self.tail == __o.tail
    
    def __str__(self) -> str:
        return "{}, {}, {}, {}".format(self.head, self.predicate, self.tail, self.dataset)

# Get the current working directory
current_directory = os.getcwd() + "/data/"
# Get a list of all folders in the current directory
folders = [f for f in os.listdir(current_directory) if os.path.isdir(current_directory + f)]

def readTriplesFromFolder(folder):
    triples = set()
    for dataset in "train", "valid", "test":
        with open(current_directory + folder + "/" + dataset + ".txt", "r") as reader:
            for line in reader.readlines():
                head, predicate, tail = line.replace("\n", "").split("\t")
                triple = Triple(head, predicate, tail, dataset)
                if triple in triples:
                    print(folder)
                    #print("Duplicate triple found")
                    #print(repr(triple))
                triples.add(triple)
    
    return triples

def writeMergedTriples(folder, merged_triples):
    with open(current_directory + folder + "/merged.csv", "w") as writer:
        writer.write("head, predicate, tail, dataset\n")
        for i, triple in enumerate(merged_triples):
            if i == len(merged_triples) - 1:
                writer.write(str(triple))
            else:
                writer.write(str(triple) + "\n")
            

for folder in folders:
    if folder == "DBPedia50":
        continue
    triples = readTriplesFromFolder(folder)
    writeMergedTriples(folder, triples)