class Dataset:
    FB15k = "FB15k"
    FB15k_237 = "FB15k-237"
    WN18 = "WN18"
    WN18RR = "WN18RR"
    YAGO3_10 = "YAGO3-10"
    Wikidata5M = "Wikidata5M"
    DBpedia50 = "DBpedia50k"

DATASETS = [Dataset.FB15k, Dataset.FB15k_237, Dataset.WN18, 
            Dataset.WN18RR, Dataset.YAGO3_10, Dataset.YAGO3_10, 
            Dataset.DBpedia50]
DATASETS = ["FB15k", "FB15k-237", "WN18", "WN18RR", "YAGO3-10", "Wikidata5M", "DBpedia50k"]
SPLITS = ["combined", "test", "validation", "train"]
BIAS_PATTERNS = ["duplicateRelations","inverseRelations", 
                 "symmetricalRelations", "defaultTailAnswers", 
                 "defaultHeadAnswers",  "overrepresentedTail","overrepresentedHead"]