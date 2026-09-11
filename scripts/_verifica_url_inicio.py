# -*- coding: utf-8 -*-
"""Verifica a troca dos links de início (index.html -> ./)."""
import os, re, urllib.request

BASE = r"C:/Projetos Code/Projeto SER Sagi/projeto_SER_Sagi - Hermes"
URL = "http://127.0.0.1:5501"

paginas = sorted(f for f in os.listdir(BASE) if f.endswith(".html"))

print("=== 1) A RAIZ serve a home? ===")
try:
    with urllib.request.urlopen(f"{URL}/", timeout=5) as r:
        corpo = r.read().decode("utf-8", "replace")
    tem_home = "S. E. R." in corpo or "S.E.R. Sagi" in corpo
    print(f"   http://127.0.0.1:5501/  ->  HTTP {r.status}  |  é a home? {'SIM' if tem_home else 'NAO'}")
except Exception as e:
    print("   ❌", e)

print("\n=== 2) Links do menu 'Início' agora são './' ===")
total = 0
for p in paginas:
    txt = open(os.path.join(BASE, p), encoding="utf-8").read()
    n = txt.count('href="./" data-page-link')
    total += n
    if n == 0:
        print(f"   ⚠️  {p}: nenhum link de início encontrado")
print(f"   {total} links 'Início' com './' (esperado: 2 por página x 27 = 54)")

print("\n=== 3) Sobrou algum index.html nos links? ===")
resto = sum(open(os.path.join(BASE, p), encoding="utf-8").read().count('href="index.html"') for p in paginas)
print(f"   {'✅ nenhum' if resto == 0 else f'❌ {resto} restantes'}")

print("\n=== 4) Todas as páginas respondem? ===")
falhas = []
for p in paginas:
    try:
        with urllib.request.urlopen(f"{URL}/{p}", timeout=5) as r:
            if r.status != 200:
                falhas.append(p)
    except Exception as e:
        falhas.append(f"{p} ({e})")
print(f"   {len(paginas) - len(falhas)}/{len(paginas)} OK")
for f in falhas:
    print("   ❌", f)

print("\n=== 5) Links internos quebrados ===")
quebrados = set()
for p in paginas:
    txt = open(os.path.join(BASE, p), encoding="utf-8").read()
    for h in set(re.findall(r'href="([a-z0-9\-\.]+\.html)', txt)):
        if not os.path.exists(os.path.join(BASE, h)):
            quebrados.add(f"{p} -> {h}")
print("   ✅ nenhum" if not quebrados else "\n".join("   ❌ " + q for q in sorted(quebrados)))
