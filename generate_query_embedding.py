import sys
import json
from sentence_transformers import SentenceTransformer

# Configurações
MODEL_NAME = 'all-MiniLM-L12-v2'

# Verifica se a query foi passada como argumento
if len(sys.argv) < 2:
    print("Uso: python generate_query_embedding.py \"sua consulta de texto aqui\"")
    sys.exit(1)

# Pega a consulta como uma string única
query_text = " ".join(sys.argv[1:])

# Carrega o modelo
model = SentenceTransformer(MODEL_NAME)

# Gera o embedding
embedding = model.encode(query_text)

# Exibe o embedding (pode ser usado diretamente na query do Elasticsearch)
print(json.dumps({
    "query": query_text,
    "embedding": embedding.tolist()
}, ensure_ascii=False, indent=2))
