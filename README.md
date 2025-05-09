# Conversor de Dump SQL para JSON

Este projeto tem como objetivo extrair dados de um arquivo `.sql` contendo blocos de `INSERT INTO` e convertê-los para um formato `.json`, útil para análises ou manipulações posteriores.

## 📁 Estrutura Esperada do Arquivo SQL

O arquivo `.sql` deve conter instruções como:

```sql
INSERT INTO `tb_content` VALUES 
(1, 'url1', 'title1', 'content1', '', 1),
(2, 'url2', 'title2', 'content2', '', 1),
...;
```
Esses dados são convertidos em objetos JSON com as seguintes chaves:

- `co_id` (ID do conteúdo)
- `co_url` (URL)
- `co_title` (título)
- `co_src` (conteúdo original)
- `co_abstract` (resumo, pode estar vazio)
- `co_math` (indicador se contém fórmulas matemáticas)

## 🚀 Como funciona o código

### script `transform_data.py`:

1. Lê o arquivo `.sql` linha a linha.
2. Detecta blocos de `INSERT INTO` (mesmo que estejam em várias linhas).
3. Extrai cada tupla de valores.
4. Converte as tuplas em dicionários.
5. Limpa os dados usando expressões regulares (remove tags indesejadas e caracteres especiais).
6. Remove duplicatas com base no campo `co_id`.
7. Exporta todos os dados para um arquivo `.json`.

###  script `bulk_transform.py`:

1. Lê o arquivo `.json` gerado pelo `transform_data.py`.
2. Converte o arquivo `.json` para o formato `.ndjson` (uma linha por comando).
     ```bash
         Rodar: jq -c '.[]' seu_arquivo.json > seu_arquivo.ndjson
      ``` 
3. Adiciona metadados de indexação para cada linha, formatando como `{"index": {"_index": "math_articles"}}`.
4. Escreve o conteúdo convertido em um novo arquivo `.ndjson` para ser usado pelo `Elasticsearch`.

###  script `bulk_extract_co_src_co_id.py`:

1. Lê o arquivo `.ndjson` gerado por `bulk_transform.py`.
2. Extrai os campos `co_id` e `co_src` de cada linha do arquivo.
3. Cria um novo arquivo `.ndjson` contendo apenas esses dois campos.
4. Esse arquivo será usado para gerar os embeddings do campo `co_src`.

###  script `embedding_code.py`:

1. Lê o arquivo `.ndjson` com os campos `co_id` e `co_src`.
2. Usa o modelo `sentence-transformers` para gerar embeddings a partir do campo `co_src`.
3. Processa os dados em lotes (para evitar sobrecarga de memória).
4. Salva os embeddings gerados em um novo arquivo `.ndjson`, associando o campo `co_id` ao seu embedding correspondente.

###  script `bulk_full.py`:

1. Lê os dados originais do arquivo `.ndjson` com os campos `co_id` e `co_src`.
2. Lê o arquivo com os embeddings gerados pelo `embedding_code.py`.
3. Associa os embeddings aos dados originais, com base no campo `co_id`.
4. Salva o resultado final em um novo arquivo `.ndjson`, contendo os campos `co_id`, `co_src` e `co_embedded_src`.

###  script `send_src.sh`:

Antes de rodar esse script você deve quebrar o arquivo `.ndjson` em partes menores com o comando

```bash
  split -l {quantos documentos por arquivo você quer} arquivo_entrada.txt arquivo_saida_prefixo_
```

1. Lê os arquivos `.ndjson` gerados pelo `bulk_full.py`.
2. Usa o comando `curl` para enviar os arquivos em partes para o `Elasticsearch` via API _bulk.
3. Divide os arquivos em partes menores, se necessário, usando a variável range para gerar os nomes dos arquivos.
4. Espera um intervalo entre os uploads (ajustado com sleep) para não sobrecarregar o servidor Elasticsearch.
5. Realiza a indexação dos dados no Elasticsearch.

###  script `sgenerate_query_embedding.py`:

1. Lê uma query de texto fornecida pelo usuário.
2. Usa o modelo `sentence-transformers` para gerar o embedding da query.
3. O embedding gerado pode ser usado para buscas vetoriais no `Elasticsearch`.


## 📄 Arquivos

- `transform_data.py`: Script principal de conversão.
- `data.sql`: (exemplo) Dump SQL contendo os dados brutos.
- `output.json`: Arquivo gerado com os dados estruturados em JSON.

## 🛠️ Como usar

1. Coloque seu arquivo `.sql` na mesma pasta.
2. Edite no topo do `transform_data.py` para indicar o nome correto do arquivo:

```bash
  input_sql = "seuarquivo.sql"
  output_json = "saida.json"
```

Execute:
```bash
  python3 transform_data.py
```

Veja o resultado em `saida.json`.

## 📊 Exemplo de saída

```bash
  [
  {
    "co_id": 1,
    "co_url": "https://mathoverflow.net/questions/13/...",
    "co_title": "Learning about Lie groups",
    "co_src": "There's also Fulton & Harris...",
    "co_abstract": "",
    "co_math": 1
  },
  ...
]
```

## ✅ Observações

- O script trata corretamente blocos grandes de `INSERT INTO` que se estendem por centenas de linhas e finalizam com `);`.
- Tuplas com `co_id` repetidos são descartadas.
- Pode ser adaptado facilmente para outras tabelas com estrutura semelhante.

Se quiser usar ou melhorar este projeto, fique à vontade para contribuir ou entrar em contato!


```
