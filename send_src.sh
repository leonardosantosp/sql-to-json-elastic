#!/bin/bash
# curl -u elastic:user123 -k -X POST "https://localhost:9200/_bulk" -H "Content-Type: application/x-ndjson" --data-binary @bulk_part_af
USER="elastic"
PASS="user123"
ES_URL="https://localhost:9200/_bulk"
CONTENT_TYPE="application/x-ndjson"


  first="t"
  range=({a..q})
  
  for second in "${range[@]}"; do
    
    file="bulk_part_${first}${second}"
    if [ -f "$file" ]; then
      echo "Indexando $file..."
      curl -u $USER:$PASS -k -X POST "$ES_URL" \
        -H "Content-Type: $CONTENT_TYPE" \
        --data-binary @"$file"
      echo
      sleep 13 
    else
      echo "Arquivo $file não encontrado. Pulando..."
    fi
  done

echo "Processo concluído."