# -*- coding: utf-8 -*-
"""
CHECAGEM DE PRONTIDÃO PARA UPLOAD

Compara o que o SITE pede (lido do próprio HTML) com o que existe no DRIVE.
Se algum slot do site não tiver pasta, a mídia não teria onde ser colocada —
e o dono descobriria na hora de subir.
"""
import glob
import os
import re
import sys

BASE = r"G:/.shortcut-targets-by-id/18wGiptBKUmAmmkKHgdfu05TU4y_roWC1/BBDPRINT - BACKUP/BBDPRINT/App BBDPRiNT/PROJETOS/Projeto SER Sagi/projeto_SER_Sagi - Hermes"
S = r"G:/Meu Drive/Instituto SER Sagi - PARA O SITE"
sys.path.insert(0, os.path.join(BASE, "scripts"))
from publicar import CATEGORIAS  # noqa: E402

# nome de exibição -> pasta (slug)
POR_NOME = {v: k for k, v in CATEGORIAS.items()}

slots = {}   # (categoria, caminho_no_drive, quem_pede)
for arq in sorted(glob.glob(os.path.join(BASE, "*.html"))):
    nome = os.path.basename(arq)
    txt = open(arq, encoding="utf-8").read()
    # (a) blocos e imagens comuns:  data-secao/-img  +  data-categoria  (+ data-pagina)
    for m in re.finditer(r'data-secao(?:-img)?="([^"]+)" data-categoria="([^"]+)"(?: data-pagina="([^"]+)")?', txt):
        secao, cat, pag = m.group(1), m.group(2), m.group(3)
        raiz = POR_NOME.get(cat)
        if not raiz:
            print(f"  ❌ categoria '{cat}' não está no CATEGORIAS (publicar.py) — pedida por {nome}")
            continue
        slots.setdefault((cat, f"{raiz}/{pag}/{secao}" if pag else f"{raiz}/{secao}"), set()).add(nome)
    # (b) cards com chave (home):  data-categoria  +  data-secao-img  +  data-secao-chave
    for m in re.finditer(r'data-categoria="([^"]+)" data-secao-img="([^"]+)" data-secao-chave="([^"]+)"', txt):
        cat, secao = m.group(1), m.group(2)
        raiz = POR_NOME.get(cat)
        if not raiz:
            print(f"  ❌ categoria '{cat}' (card com chave) não está no CATEGORIAS — pedida por {nome}")
            continue
        slots.setdefault((cat, f"{raiz}/{secao}"), set()).add(nome)

print(f"slots que o site pede: {len(slots)}\n")

faltando = []
for (cat, caminho), paginas in sorted(slots.items()):
    pasta = os.path.join(S, caminho.replace("/", os.sep))
    existe = os.path.isdir(pasta)
    if not existe:
        faltando.append((cat, caminho))
    marca = "✅" if existe else "❌ FALTA A PASTA"

print("--- por categoria ---")
cat_atual = None
for (cat, caminho), paginas in sorted(slots.items()):
    if cat != cat_atual:
        cat_atual = cat
        print(f"\n  [{cat}]")
    print(f"    {marca if caminho in [c for _, c in faltando] else '✅':>15} {caminho}")

print()
if faltando:
    print(f"⚠️  {len(faltando)} pasta(s) faltando:")
    for cat, caminho in faltando:
        print(f"   • {cat}/{caminho}")
else:
    print("🎉 TODAS as pastas que o site pede existem no Drive.")
print()
print("--- pastas que existem mas nenhum slot usa (folga, não é erro) ---")
usados = {c for _, c in slots}
for raiz in os.listdir(S):
    p = os.path.join(S, raiz)
    if not os.path.isdir(p) or raiz.startswith("_"):
        continue
    for dirpath, dirnames, filenames in os.walk(p):
        rel = os.path.relpath(dirpath, S).replace("\\", "/")
        if rel in usados:
            continue
        if filenames or not dirnames:
            pass
        filhos = os.listdir(dirpath)
        if not filhos:
            print(f"   (vazia) {rel}")
