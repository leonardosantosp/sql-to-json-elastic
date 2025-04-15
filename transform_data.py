import re
import json

input_sql = "input.sql"
output_json = "dados_limpos.json"

insert_start = "INSERT INTO `tb_content` VALUES"
insert_buffer = []
inside_insert = False

def clean_text(text):
    return re.sub(r"<som\d+>(.*?)</som\d+>", r"\1", text)

def split_fields(raw_tuple):
    # Divide os campos considerando aspas e escapes corretamente
    pattern = re.compile(r"""
        '((?:[^'\\]|\\.)*)'    # Campo entre aspas simples com escapes
        | NULL                 # Ou valor NULL
        | ([^,()]+)            # Ou qualquer outro valor não delimitado por vírgula/parênteses
    """, re.VERBOSE)

    matches = pattern.findall(raw_tuple)
    fields = []
    for quoted, plain in matches:
        if quoted:
            val = quoted.replace("\\'", "'").replace('\\\\', '\\')
        elif plain.strip() == 'NULL':
            val = ''
        else:
            val = plain.strip()
        fields.append(val)
    return fields

def parse_and_store(block, seen, all_data):
    tuples = re.findall(r"\((.*?)\)", block)
    for tup in tuples:
        fields = split_fields(tup)
        if len(fields) == 6:
            try:
                co_id = int(fields[0])
                co_math = int(fields[5])
            except:
                continue

            key = (co_id, fields[1])
            if key not in seen:
                seen.add(key)
                all_data.append({
                    "co_id": co_id,
                    "co_url": fields[1],
                    "co_title": clean_text(fields[2]),
                    "co_src": clean_text(fields[3]),
                    "co_abstract": clean_text(fields[4]),
                    "co_math": co_math
                })

def main():
    all_data = []
    seen = set()
    buffer = ""

    with open(input_sql, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith(insert_start):
                buffer = line
            elif buffer:
                buffer += line
                if line.strip().endswith(";"):
                    parse_and_store(buffer[len(insert_start):], seen, all_data)
                    buffer = ""

    with open(output_json, "w", encoding="utf-8") as out:
        json.dump(all_data, out, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
