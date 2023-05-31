import numpy as np
from ampligraph.datasets import load_fb15k_237, load_wn18rr, load_fb15k, load_wn18
from ampligraph.evaluation import mrr_score, hits_at_n_score
from ampligraph.utils import restore_model
from collections import defaultdict
import pandas as pd
from constants import TrainingDataset
import os

print("Performing prediction analysis on learned models...")
# Stores ranks for every dataset
ranks_for_dataset = defaultdict()
datasets = TrainingDataset.FB15k, TrainingDataset.FB15k_237, TrainingDataset.WN18, TrainingDataset.WN18RR
for dataset in datasets:
  X = None
  if dataset == TrainingDataset.FB15k:
    X = load_fb15k()
  elif dataset == TrainingDataset.FB15k_237:
    X = load_fb15k_237()
  elif dataset == TrainingDataset.WN18:
    X = load_wn18()
  elif dataset == TrainingDataset.WN18RR:
    X = load_wn18rr()

  # Retrieve trained model
  storage_path = os.getcwd() + "/experiments/data/trainedModels/{}".format(dataset)
  model = restore_model(model_name_path=storage_path)

  # Using filtered settings
  filter = {'test' : np.concatenate((X['train'], X['valid'], X['test']))}

  # Calculate ranks for both head and tail entities
  ranks = model.evaluate(X['test'],
                        use_filter=filter,
                        corrupt_side='s,o')
  ranks_for_dataset[dataset] = ranks

  # compute and print metrics:
  mrr = mrr_score(ranks)
  hits_10 = hits_at_n_score(ranks, n=10)
  print("Metrics for %s --- MRR: %f, Hits@10: %f" % (dataset, mrr, hits_10))


  base_path = os.getcwd() + "/experiments/data/biasedPatterns/{}".format(dataset)
  defaultTail_df = pd.read_csv("{}/defaultTail.csv".format(base_path))
  defaultHead_df = pd.read_csv("{}/defaultHead.csv".format(base_path))
  overrepresentedTail_df = pd.read_csv("{}/overrepresentedTail.csv".format(base_path))
  overrepresentedHead_df = pd.read_csv("{}/overrepresentedHead.csv".format(base_path))
  duplicate_df = pd.read_csv("{}/duplicateRelations.csv".format(base_path))
  inverse_df = pd.read_csv("{}/inverseRelations.csv".format(base_path))
  symmetry_df = pd.read_csv("{}/symmetricalRelations.csv".format(base_path))

  test_statements = [' '.join(x) for x in X['test']]
  ranks = ranks_for_dataset[dataset]

  defaultTailRelation = set((str, str))
  defaultHeadRelation = set((str, str))
  overrepresentedTailRelation = set((str, str))
  overrepresentedHeadRelation = set((str, str))
  duplicateRelations = set()
  inverseRelations = set()
  symmetricRelations = set()

  for i, row in defaultTail_df.iterrows():
    tail, rel = row["option"], row["relation"]
    defaultTailRelation.add((tail, rel))
  
  for i, row in defaultHead_df.iterrows():
    tail, rel = row["option"], row["relation"]
    defaultHeadRelation.add((tail, rel))

  for i, row in overrepresentedTail_df.iterrows():
    tail, rel = row["tail"], row["relation"]
    overrepresentedTailRelation.add((tail, rel))
  
  for i, row in overrepresentedHead_df.iterrows():
    tail, rel = row["head"], row["relation"]
    overrepresentedHeadRelation.add((tail, rel))

  for i, row in duplicate_df.iterrows():
    duplicateRelations.add(row["r"])

  for i, row in inverse_df.iterrows():
    inverseRelations.add(row["relation"])
  
  for i, row in symmetry_df.iterrows():
    symmetricRelations.add(row["relation"])

  
  for setting in "head", "tail":
    output_frame = pd.DataFrame(columns=["H@K","inverseAffected", 
                                         "duplicateAffected",
                                         "symmetryAffected","defaultAffected", 
                                         "overrepresentedAffected",
                                         "unknownPredictions", "correctPredictions"])
    for tolerance in [1, 3, 5, 10]:
      defaultAffected = 0
      overrepresentedAffected = 0
      inverseAffected = 0
      duplicateAffected = 0
      symmetryAffected = 0
      unknown = 0
      correct_predictions = 0
      for i in range(len(ranks)):
        if "fb" in dataset:
          head = "http://bias.org/entity" + X['test'][i][0] 
          relation = "http://bias.org/vocab" + X['test'][i][1] 
          tail = "http://bias.org/entity" + X['test'][i][2] 
        else:
          head = "http://bias.org/entity/" + X['test'][i][0] 
          relation = "http://bias.org/vocab/" + X['test'][i][1] 
          tail = "http://bias.org/entity/" + X['test'][i][2] 

        if setting == "head":
          isDefaultAffected = (head, relation) in defaultHeadRelation
          isOverrepresentedAffect = (head, relation) in overrepresentedHeadRelation
        elif setting =="tail":
          isDefaultAffected = (tail, relation) in defaultTailRelation
          isOverrepresentedAffect = (tail, relation) in overrepresentedTailRelation
        
        isInverseRelation = relation in inverseRelations
        isDuplicateRelation = relation in duplicateRelations
        isSymmetricRelation = relation in symmetricRelations
        current_rank = ranks[i][1] if setting == "tail" else ranks[i][0]

        if current_rank <= tolerance:
          correct_predictions += 1
          if isDefaultAffected:
            defaultAffected += 1
          if isOverrepresentedAffect:
            overrepresentedAffected += 1
          if isInverseRelation:
            inverseAffected += 1
          if isDuplicateRelation:
            duplicateAffected += 1
          if isSymmetricRelation:
            symmetryAffected += 1
          if (not isDefaultAffected) and (not isDuplicateRelation) and (not isInverseRelation) and (not isOverrepresentedAffect) and (not isSymmetricRelation):
            unknown += 1

      # Write results to dataframe
      new_row = {'H@K': tolerance, 
                 'inverseAffected': inverseAffected, 
                 'duplicateAffected': duplicateAffected,
                 'symmetryAffected': symmetryAffected, 
                 'defaultAffected': defaultAffected, 
                 'overrepresentedAffected': overrepresentedAffected,
                 'unknownPredictions': unknown, 
                 'correctPredictions': correct_predictions }
      output_frame.loc[len(output_frame)] = new_row
     
    output_frame.to_csv(os.getcwd() + "/analysis/data/predictionAnalysis/{}_{}.csv".format(dataset, setting), index=False)



