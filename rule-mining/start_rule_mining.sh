#!/bin/bash
FILES="./../BenchmarkLPDatasets/*"
for file_path in $FILES
do
  filename=$(basename -- "$file_path")
  extension="${filename##*.}"
  filename="${filename%.*}"
  echo "Mining rules from $file_path"
  mkdir mined_rules
  mkdir mined_rules/raw_logs
  java -jar amie-dev.jar $file_path -d" " > mined_rules/raw_logs/$filename.txt
done

