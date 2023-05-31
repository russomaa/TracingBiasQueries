from execute_query import execute_SPARQL_query
from reproducibility.constants import DATASETS, SPLITS, BIAS_PATTERNS, Dataset
import pandas as pd
from io import StringIO
import os


"""
Get dataset statistics (entities, relations and triples)
"""
print("Collecing dataset statistics...")
statistics_folder = "analysis/data/split_statistics"
if not os.path.exists(statistics_folder):
    os.makedirs(statistics_folder)
for overview_type in "entities", "relations", "triples":
    data_statistics = pd.DataFrame()
    query_path = "sparql_queries/dataset_overview/{}.rq".format(overview_type)
    for dataset in DATASETS:
            data_row = {}
            result = execute_SPARQL_query(query_path, dataset)
            result = pd.read_csv(StringIO(result))
            data_row["dataset"] = dataset
            for key in result:
                 data_row[key] = result[key].values[0]
            data_statistics = pd.concat([data_statistics, pd.DataFrame([data_row])], ignore_index=True)
    data_statistics.to_csv("{}/{}.csv".format(statistics_folder, overview_type), index=False)


"""
Get distribution of relations in percent
"""
print("Collecing relation frequency...")
distribution_folder = "analysis/data/relation_distribution"
if not os.path.exists(distribution_folder):
    os.makedirs(distribution_folder)
for split in SPLITS:
    for dataset in DATASETS:
        query_path = "sparql_queries/distribution_analysis/relationFrequencyInPercent.rq"
        result = execute_SPARQL_query(query_path, dataset)
        result = pd.read_csv(StringIO(result))
        result.to_csv("{}/{}_{}.csv".format(distribution_folder, dataset, split), index=False)
            

"""
Get number of bias-affected triples for each split and dataset
"""
print("Collecing number of bias-affected triples...")
bias_data_folder = "analysis/data/bias_affected_triples"
if not os.path.exists(bias_data_folder):
    os.makedirs(bias_data_folder)
for split in SPLITS:
    bias_affected_triples = pd.DataFrame(columns=["dataset"] + BIAS_PATTERNS)
    for dataset in DATASETS:
        bias_patterns_row = {}
        bias_patterns_row["dataset"] = dataset
        for pattern in BIAS_PATTERNS:
            query_base_path = "sparql_queries/affectedTriples/{}/".format(split)
            result = execute_SPARQL_query(query_base_path + pattern + ".rq", dataset)
            result = pd.read_csv(StringIO(result))
            bias_patterns_row[pattern] = result[result.columns[0]].values[0]        
        bias_affected_triples = pd.concat([bias_affected_triples, pd.DataFrame([bias_patterns_row])], ignore_index=True)
    bias_affected_triples.to_csv("{}/{}.csv".format(bias_data_folder, split), index=False)
            

"""
Collect biased relations/entities for later usage in prediction analysis
--> For datasets FB15k, FB15k-237, WN18 and WN18RR
"""
print("Collecing biased patterns...")
for dataset in Dataset.FB15k, Dataset.FB15k_237, Dataset.WN18, Dataset.WN18RR:
    output_folder = "experiments/data/biasedPatterns/{}".format(dataset)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    for pattern in BIAS_PATTERNS:
        query_path = "sparql_queries/biasPatterns/{}.rq".format(pattern)
        result = execute_SPARQL_query(query_path, dataset)
        result = pd.read_csv(StringIO(result))
        result.to_csv("{}/{}.csv".format(output_folder, pattern), index=False)        


