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

O script `transform_data.py`:

1. Lê o arquivo `.sql` linha a linha.
2. Detecta blocos de `INSERT INTO` (mesmo que estejam em várias linhas).
3. Extrai cada tupla de valores.
4. Converte as tuplas em dicionários.
5. Remove duplicatas com base no campo `co_id`.
6. Exporta todos os dados para um arquivo `.json`.

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

## ✅ Observações

- O script trata corretamente blocos grandes de `INSERT INTO` que se estendem por centenas de linhas e finalizam com `);`.
- Tuplas com `co_id` repetidos são descartadas.
- Pode ser adaptado facilmente para outras tabelas com estrutura semelhante.

Se quiser usar ou melhorar este projeto, fique à vontade para contribuir ou entrar em contato!


```
