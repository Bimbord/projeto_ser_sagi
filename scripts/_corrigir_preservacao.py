# -*- coding: utf-8 -*-
"""
Corrige o typo do nome: preseravacao -> preservacao, republica e limpa o registro errado.

O arquivo já foi publicado como "preseravacao" (não casa com o card "Preservação").
Este script:
  1. traz o arquivo de volta do _publicados com o nome certo
  2. libera no manifesto
  3. republica
  4. apaga o registro errado (do banco e do R2)
  5. confere o casamento das 5 chaves
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import unicodedata
import urllib.request

BASE = r"G:/.shortcut-targets-by-id/18wGiptBKUmAmmkKHgdfu05TU4y_roWC1/BBDPRINT - BACKUP/BBDPRINT/App BBDPRiNT/PROJETOS/Projeto SER Sagi/projeto_SER_Sagi - Hermes"
S = r"G:/Meu Drive/Instituto SER Sagi - PARA O SITE"
PASTA = os.path.join(S, "home", "pilares")
PUBLICADOS = os.path.join(S, "_publicados", "home")
MANIFESTO = os.path.join(S, "_publicados", "publicados.json")

sys.path.insert(0, os.path.join(BASE, "scripts"))
from supabase_admin import SUPABASE_URL, admin_headers  # noqa: E402


def norm(t):
    t = "".join(c for c in unicodedata.normalize("NFD", (t or "").lower())
                if unicodedata.category(c) != "Mn")
    return re.sub(r"^-+|-+$", "", re.sub(r"[^a-z0-9]+", "-", t))


# ---- 1. arquivo com o nome certo ----
origem = os.path.join(PUBLICADOS, "preseravacao.jpg")
destino = os.path.join(PASTA, "preservacao.jpg")
os.makedirs(PASTA, exist_ok=True)
if os.path.isfile(origem):
    shutil.copy2(origem, destino)
    print(f"  ✅ {os.path.basename(origem)} -> home/pilares/preservacao.jpg")
elif os.path.isfile(destino):
    print("  (o arquivo já estava na pasta com o nome certo)")
else:
    sys.exit("❌ não achei o arquivo preseravacao.jpg para renomear")

# ---- 2. libera no manifesto ----
h = hashlib.sha256(open(destino, "rb").read()).hexdigest()
d = json.load(open(MANIFESTO, encoding="utf-8"))
if h in d["arquivos"]:
    antigo = d["arquivos"].pop(h)
    json.dump(d, open(MANIFESTO, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"  🔓 liberado no manifesto (era id {antigo.get('id')}, arquivo {antigo.get('arquivo')})")

# ---- 3. publica ----
print("\n--- publicando ---")
subprocess.run([sys.executable, os.path.join(BASE, "scripts", "servidor_midias.py"),
                "--publicar", "--autorizado"], cwd=BASE, check=False)

# ---- 4. apaga o registro errado (preseravacao) ----
print("\n--- removendo o registro com nome errado ---")
url = f"{SUPABASE_URL}/rest/v1/arquivo?select=id,titulo,imagem_url&categoria=eq.Home&secao=eq.pilares&deleted=eq.false"
r = urllib.request.Request(url)
for k, v in admin_headers().items():
    r.add_header(k, v)
with urllib.request.urlopen(r, timeout=30) as resp:
    linhas = json.loads(resp.read().decode())

html = open(os.path.join(BASE, "index.html"), encoding="utf-8").read()
chaves = set(re.findall(r'data-secao-img="pilares" data-secao-chave="([^"]+)"', html))

errados, chaves_vistas = [], {}
for i in linhas:
    k = norm(i["titulo"])
    chaves_vistas[k] = i["id"]
    if k not in chaves:
        errados.append(i)

if errados:
    ids = ",".join(str(i["id"]) for i in errados)
    subprocess.run([sys.executable, os.path.join(BASE, "scripts", "excluir.py"),
                    "--tabela", "arquivo", "--ids", ids], cwd=BASE, check=False)
    for i in errados:
        chave_r2 = "fotos/" + i["imagem_url"].split("/")[-1]
        subprocess.run([sys.executable, os.path.join(BASE, "scripts", "upload_r2.py"),
                        "--delete", chave_r2], cwd=BASE, check=False, stdout=subprocess.DEVNULL)
        print(f"  🗑️  id {i['id']} ({i['imagem_url'].split('/')[-1]}) removido do banco e do R2")
else:
    print("  (nenhum registro com nome errado)")

# ---- 5. conferência ----
print("\n--- casamento final das chaves dos pilares ---")
for c in sorted(chaves):
    if c in chaves_vistas:
        print(f"  ✅ {c:14} → foto id {chaves_vistas[c]}")
    else:
        print(f"  ⚪ {c:14} → sem foto")
