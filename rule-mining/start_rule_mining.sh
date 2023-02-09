#!/bin/bash
FILES="./../../../data/services/GraphDB/data/graphdb-import/BenchmarkLPDatasets/*"
for file_path in $FILES
do
  filename=$(basename -- "$file_path")
  extension="${filename##*.}"
  filename="${filename%.*}"
  echo "Mining rules from $file_path"
  java -jar amie/amie-dev.jar $file_path -d" " > ./../mined_rules/raw_logs/$filename.txt  
done

