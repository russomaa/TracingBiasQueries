# SPARQL queries for analyzing bias patterns and other irregularities


## Bias analysis

 Seven bias patterns are defined concerning test leakage and sample selection bias, available in the folder `sparql_queries/biasPatterns`. 

Test leakage patterns:

- Near-duplicate relations
- Near-inverse relations
- Near-symmetric relations

For sample selection bias, we reused patterns defined in the work of [Rossi et al.](https://github.com/merialdo/research.lpbias), and implemented them as SPARQL queries to be used over any RDF Graph:

- Overrepresented tail answers (referred to as Type 1 Bias by Rossi et al.)
- Overrepresented head answers
- Default tail answers (referred to as Type 2 Bias by Rossi et al.)
- Default head answers

Using these patterns, we queried the number of bias-affected triples for each split in every dataset with SPARQL. The queries can be found in the folder `sparql_queries/affectedTriples`. 
