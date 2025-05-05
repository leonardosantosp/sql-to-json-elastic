# Código responsável por criar o vetor de embeddings para o campo co_src para cada um dos documentos

import json
from pathlib import Path
from sentence_transformers import SentenceTransformer

# Configurações
INPUT_PATH   = Path('data/bulk_co_id_co_src.ndjson')    # arquivo de entrada: {"co_id":…, "co_src":…} por linha
OUTPUT_PATH  = Path('data/bulk_co_id_co_embedded_src.ndjson') # arquivo de saída
MODEL_NAME   = 'all-MiniLM-L12-v2'
BATCH_SIZE   = 64     # quantos itens por lote passado ao modelo
CHUNK_SIZE   = 1024   # quantos itens ler antes de chamar encode (para não estourar memória)

# Carrega o modelo
model = SentenceTransformer(MODEL_NAME)

with INPUT_PATH.open('r', encoding='utf-8') as fin, OUTPUT_PATH.open('w', encoding='utf-8') as fout:
    ids, texts = [], []
    total = 0

    for line in fin:
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue

        co_id  = rec.get('co_id')
        co_src = rec.get('co_src', '')
        if co_id is None or not co_src:
            continue

        ids.append(co_id)
        texts.append(co_src)

        # Quando acumular CHUNK_SIZE itens, gera os embeddings e escreve
        if len(texts) >= CHUNK_SIZE:
            embeddings = model.encode(texts, batch_size=BATCH_SIZE, show_progress_bar=True)
            for cid, emb in zip(ids, embeddings):
                out = {
                    "co_id": cid,
                    "co_embedded_src": emb.tolist()
                }
                fout.write(json.dumps(out, ensure_ascii=False) + "\n")
            total += len(texts)
            ids.clear()
            texts.clear()

    # Processa o restante
    if texts:
        embeddings = model.encode(texts, batch_size=BATCH_SIZE, show_progress_bar=True)
        for cid, emb in zip(ids, embeddings):
            out = {
                "co_id": cid,
                "co_embedded_src": emb.tolist()
            }
            fout.write(json.dumps(out, ensure_ascii=False) + "\n")
        total += len(texts)

print(f"Processo concluído! {total} embeddings salvos em: {OUTPUT_PATH.resolve()}")