class Triple:
    def __init__(self, head, predicate, tail, dataset=""):
        self.head = head
        self.predicate = predicate
        self.tail = tail
        self.dataset = dataset

    def getCSVRow(self, withDataset=True):
        if withDataset:
            return "{},{},{},{}".format(self.head, self.predicate, self.tail, self.dataset) 
        else:
            return "{},{},{}".format(self.head, self.predicate, self.tail) 
    
    def __hash__(self):
        return hash(repr(self))
    
    def __repr__(self) -> str:
        return "Triple(" + str(self) + ")"
    
    def __eq__(self, __o: object) -> bool:
        return self.head == __o.head and self.predicate == __o.predicate and self.tail == __o.tail
    
    def __str__(self) -> str:
        return "{},{},{},{}".format(self.head, self.predicate, self.tail, self.dataset)