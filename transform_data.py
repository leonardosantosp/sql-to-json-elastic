import re
import json

input_sql = "input.sql"
output_json = "dados_limpos.json"

insert_start = "INSERT INTO `tb_content` VALUES"

def clean_text(text):
    return re.sub(r"<som\d+>(.*?)</som\d+>", r"\1", text)

def split_fields_respecting_strings(raw_tuple):
    fields = []
    current = ""
    inside_string = False
    escape = False

    for char in raw_tuple:
        if escape:
            current += char
            escape = False
        elif char == "\\":
            current += char
            escape = True
        elif char == "'":
            current += char
            inside_string = not inside_string
        elif char == "," and not inside_string:
            fields.append(current.strip())
            current = ""
        else:
            current += char
    if current:
        fields.append(current.strip())
    return fields

def parse_tuples_block(block):
    block = block.strip()
    if block.endswith(";"):
        block = block[:-1]
    if block.startswith("(") and block.endswith(")"):
        block = block[1:-1]
    tuples_raw = re.split(r"\),\s*\(", block)

    tuples = []
    for tup in tuples_raw:
        if not tup.startswith("("):
            tup = "(" + tup
        if not tup.endswith(")"):
            tup = tup + ")"
        tuples.append(tup)
    return tuples

def parse_and_store(block, seen, all_data):
    tuples = parse_tuples_block(block)
    for tup in tuples:
        tup_clean = tup[1:-1]
        fields = split_fields_respecting_strings(tup_clean)

        if len(fields) == 6:
            try:
                co_id = int(fields[0])
                co_math = int(fields[5])
            except:
                continue

            def strip_quotes(val):
                if val.startswith("'") and val.endswith("'"):
                    val = val[1:-1]
                return val.replace("\\'", "'").replace('\\\\', '\\')

            key = (co_id, strip_quotes(fields[1]))
            if key not in seen:
                seen.add(key)
                all_data.append({
                    "co_id": co_id,
                    "co_url": strip_quotes(fields[1]),
                    "co_title": clean_text(strip_quotes(fields[2])),
                    "co_src": clean_text(strip_quotes(fields[3])),
                    "co_abstract": clean_text(strip_quotes(fields[4])),
                    "co_math": co_math
                })

def main():
    all_data = []
    seen = set()
    buffer = ""
    inside_insert = False

    with open(input_sql, "r", encoding="utf-8") as f:
        for line in f:
            # detecta qualquer início de INSERT, mesmo se não for no início da linha
            if not inside_insert and "INSERT INTO `tb_content` VALUES" in line:
                buffer = line
                inside_insert = True
            elif inside_insert:
                buffer += line
                # fim do bloco de insert
                if line.strip().endswith(");") or line.strip().endswith(");--") or ";" in line:
                    try:
                        raw_data = buffer.split("VALUES", 1)[1].strip()
                        parse_and_store(raw_data, seen, all_data)
                    except Exception as e:
                        print("Erro ao processar bloco:", e)
                    buffer = ""
                    inside_insert = False

    print(f"Total de tuplas processadas: {len(all_data)}")
    if all_data:
        print("co_id mínimo:", min(d["co_id"] for d in all_data))
        print("co_id máximo:", max(d["co_id"] for d in all_data))

    with open(output_json, "w", encoding="utf-8") as out:
        json.dump(all_data, out, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
