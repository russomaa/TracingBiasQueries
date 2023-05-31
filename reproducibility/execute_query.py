import argparse
from SPARQLWrapper import SPARQLWrapper, CSV
import os


def execute_SPARQL_query(file_path, dataset, output_dir=None):
    sparql = SPARQLWrapper(
        "https://labs.tib.eu/sdm/graphdb_dev/repositories/{}".format(dataset)
    )
    sparql.setCredentials("sammy","weT4Ca65DD35DNX")
    sparql.setReturnFormat(CSV)

    query = ""
    with open(os.getcwd() + "/" + file_path) as reader:
        query = reader.read()

    sparql.setQuery(query)
    ret = sparql.queryAndConvert()
    if output_dir:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        with open(output_dir + "/" + file_path.split("/")[-1] + ".csv", "w") as writer:
            writer.write(ret.decode('utf-8'))
    
    return ret.decode('utf-8')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Read query file.')
    parser.add_argument('query', metavar='q', type=str,
                    help='Specify the path to the .rq SPARQL query file that should be run')
    parser.add_argument('dataset', metavar='d', type=str,
                    help='Specify the dataset ("FB15k", "FB15k-237", "WN18", "WN18RR", "YAGO3-10", "Wikidata5M" or "DBpedia50k")')
    parser.add_argument('--output', metavar='-o', type=str,
                    help='Specify what folder the results of the query should be written to')

    args = parser.parse_args()
    query_file_path = args.query
        
    try:
        execute_SPARQL_query(query_file_path, args.dataset, args.output)
    except Exception as e:
        print(e)
