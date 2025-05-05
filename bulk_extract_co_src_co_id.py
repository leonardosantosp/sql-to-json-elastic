# Extrair os campos co_id e co_src de um arquivo .ndjson e salvar somente esses campos em um novo arquivo .ndjson.

import json
from pathlib import Path

input_path  = Path('data/bulk_data_insert.ndjson')
output_path = Path('data/bulk_co_id_co_src.ndjson')

with input_path.open('r', encoding='utf-8') as src, \
     output_path.open('w', encoding='utf-8') as dest:

    for line in src:
        line = line.strip()
        if not line:
            continue

        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue

        # only if both
        if "co_id" not in record or "co_src" not in record:
            continue

        co_id  = record["co_id"]
        co_src = record["co_src"]

        # ignore empty
        if co_id == "" and co_src == "":
            continue

        out = {
            "co_id":  co_id,
            "co_src": co_src
        }
        dest.write(json.dumps(out, ensure_ascii=False) + "\n")

print(f"Extraction done. co_id and co_src saved to: {output_path.resolve()}")