# Junta os dados originais com os embeddings

import json
from pathlib import Path

# Paths de entrada e saída
ORIG_PATH    = Path('data/bulk_data_insert.ndjson')      # contém todos os campos originais
EMBED_PATH   = Path('data/bulk_co_id_co_embedded_src.ndjson')  # contém {"co_id":.., "co_embedded_src":[..]} por linha
OUTPUT_PATH  = Path('data/bulk_full_with_src_embed.ndjson')

# 1) Carrega todos os embeddings de co_src em memória
emb_map = {}
with EMBED_PATH.open('r', encoding='utf-8') as f_emb:
    for line in f_emb:
        try:
            rec = json.loads(line)
            cid = rec.get('co_id')
            emb = rec.get('co_embedded_src')
            if cid is not None and emb is not None:
                emb_map[cid] = emb
        except json.JSONDecodeError:
            continue

# 2) Processa o arquivo original, adicionando o campo co_embedded_src
count = 0
with ORIG_PATH.open('r', encoding='utf-8') as f_in, \
     OUTPUT_PATH.open('w', encoding='utf-8') as f_out:

    for raw in f_in:
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError:
            continue

        cid = obj.get('co_id')
        if cid in emb_map:
            obj['co_embedded_src'] = emb_map[cid]
            count += 1

        f_out.write(json.dumps(obj, ensure_ascii=False) + "\n")

print(f"{count} registros atualizados com 'co_embedded_src' e salvos em: {OUTPUT_PATH.resolve()}")