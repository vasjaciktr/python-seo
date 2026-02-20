import csv, os, math, sys, zipfile

INPUT = "never-ordered.csv"             # ← назва твого файлу
OUT_DIR = "never-ordered-splits"              # ← куди класти частини
ROWS_PER_FILE = 1500             # загалом у файлі, включно з заголовком
DATA_PER_FILE = ROWS_PER_FILE - 1  # 499 даних + 1 заголовок

os.makedirs(OUT_DIR, exist_ok=True)

# підрахунок рядків (не обов’язково, але корисно)
with open(INPUT, "r", newline="", encoding="utf-8") as f:
    total_lines = sum(1 for _ in f)
total_data = total_lines - 1
chunks = math.ceil(total_data / DATA_PER_FILE)

with open(INPUT, "r", newline="", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)

    part = 1
    written = 0
    out = None
    writer = None

    def new_writer(idx):
        path = os.path.join(OUT_DIR, f"part_{idx:02d}.csv")
        g = open(path, "w", newline="", encoding="utf-8")
        w = csv.writer(g)
        w.writerow(header)
        return g, w

    out, writer = new_writer(part)

    for row in reader:
        writer.writerow(row)
        written += 1
        if written == DATA_PER_FILE:
            out.close()
            part += 1
            if part <= chunks:
                out, writer = new_writer(part)
            written = 0

    if out and not out.closed:
        out.close()

# опціонально — запакувати в ZIP
zip_path = "never-ordered.zip"
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
    for name in sorted(os.listdir(OUT_DIR)):
        z.write(os.path.join(OUT_DIR, name), arcname=name)

print(f"Готово: {chunks} файлів у '{OUT_DIR}', ZIP: {zip_path}")
