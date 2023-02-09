#!/bin/bash
FILES="./../mappings/output/*"
for file_path in $FILES
do
  filename=$(basename -- "$file_path")
  extension="${filename##*.}"
  filename="${filename%.*}"
  echo $filename
  echo "Mining rules for $filename"
  java -jar amie-dev.jar $file_path -d" " > $filename.txt  
done


