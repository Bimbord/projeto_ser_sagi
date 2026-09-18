# -*- coding: utf-8 -*-
"""
Prepara e publica as fotos dos PILARES (home/pilares).

Faz o que o scanner não consegue sozinho:
  1. corrige o typo "preseravacao.jpg" -> "preservacao.jpg"
  2. libera no manifesto os arquivos que o scanner estava pulando por hash
     (foto repetida de outro slot) — a foto é a mesma, mas o CARD é outro
  3. publica

Sem isso, 2 dos 5 cards ficariam sem foto e 1 não casaria.
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

BASE = r"G:/.shortcut-targets-by-id/18wGiptBKUmAmmkKHgdfu05TU4y_roWC1/BBDPRINT - BACKUP/BBDPRINT/App BBDPRiNT/PROJETOS/Projeto SER Sagi/projeto_SER_Sagi - Hermes"
S = r"G:/Meu Drive/Instituto SER Sagi - PARA O SITE"
PASTA = os.path.join(S, "home", "pilares")
MANIFESTO = os.path.join(S, "_publicados", "publicados.json")

# chaves que os cards esperam (lidas do index.html)
html = open(os.path.join(BASE, "index.html"), encoding="utf-8").read()
chaves = re.findall(r'data-secao-img="pilares" data-secao-chave="([^"]+)"', html)
print(f"chaves esperadas nos pilares: {', '.join(chaves)}\n")


def norm(t):
    import unicodedata
    t = unicodedata.normalize("NFD", (t or "").lower())
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return re.sub(r"^-+|-+$", "", re.sub(r"[^a-z0-9]+", "-", t))


# ---- 1. corrige nomes que não casariam ----
print("1) conferindo os nomes dos arquivos")
for nome in sorted(os.listdir(PASTA)):
    base, ext = os.path.splitext(nome)
    k = norm(base)
    if k in chaves:
        print(f"   ✅ {nome:24} -> chave '{k}'")
        continue
    # tenta achar a chave mais próxima (typo)
    alvo = next((c for c in chaves if abs(len(c) - len(k)) <= 3 and
                 sum(1 for a, b in zip(c, k) if a != b) <= 2 and c[0] == k[0]), None)
    if alvo:
        novo = f"{alvo}{ext}"
        shutil.move(os.path.join(PASTA, nome), os.path.join(PASTA, novo))
        print(f"   🔧 {nome} renomeado para {novo}  (chave '{alvo}')")
    else:
        print(f"   ❌ {nome:24} -> chave '{k}' NÃO existe nos cards (não vai casar)")

# ---- 2. libera no manifesto ----
print("\n2) liberando no manifesto os arquivos pulados por hash")
d = json.load(open(MANIFESTO, encoding="utf-8"))
liberados = []
for nome in sorted(os.listdir(PASTA)):
    caminho = os.path.join(PASTA, nome)
    h = hashlib.sha256(open(caminho, "rb").read()).hexdigest()
    if h in d["arquivos"]:
        antigo = d["arquivos"][h]
        del d["arquivos"][h]
        liberados.append((nome, antigo.get("id"), antigo.get("categoria"), antigo.get("secao")))
if liberados:
    json.dump(d, open(MANIFESTO, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for nome, i, cat, sec in liberados:
        print(f"   🔓 {nome} (estava como id {i} em {cat}/{sec}) — liberado para publicar")
else:
    print("   (nada a liberar)")

# ---- 3. publica ----
print("\n3) publicando")
subprocess.run([sys.executable, os.path.join(BASE, "scripts", "servidor_midias.py"),
                "--publicar", "--autorizado"], cwd=BASE, check=False)
