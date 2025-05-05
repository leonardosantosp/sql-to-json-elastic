# Rodar: jq -c '.[]' seu_arquivo.json > seu_arquivo.ndjson 
# Esse código basicamente insere um indice em cada linha do json para que seja inserido corretamente no elastic

import json

arquivo_entrada = 'bulk_data.ndjson'
arquivo_saida = 'bulk_data_insert.ndjson'
indice = 'math_articles'

with open(arquivo_entrada, 'r', encoding='utf-8') as f_in, open(arquivo_saida, 'w', encoding='utf-8') as f_out:
    for line in f_in:
        try:
            doc = json.loads(line.strip())
            f_out.write(json.dumps({"index": {"_index": indice}}) + '\n')
            f_out.write(json.dumps(doc) + '\n')
        except Exception as e:
            print("Erro ao processar linha:", e)

print(f"Arquivo '{arquivo_saida}' gerado com sucesso!")
