# -*- coding: utf-8 -*-
"""Verifica a aplicação do rodapé em todas as páginas."""
import os, re, urllib.request

BASE = r"C:/Projetos Code/Projeto SER Sagi/projeto_SER_Sagi - Hermes"
URL = "http://127.0.0.1:5501"

paginas = sorted(f for f in os.listdir(BASE) if f.endswith(".html"))

def ler(n):
    return open(os.path.join(BASE, n), encoding="utf-8").read()

print(f"=== {len(paginas)} páginas ===")

print("\n=== 1) Rodapé aplicado (1 por página, com copyright) ===")
sem = []
for p in paginas:
    t = ler(p)
    if t.count("<footer") != 1:
        sem.append(f"{p}: {t.count('<footer')} <footer>")
    if "© 2026 Instituto S.E.R. Sagi" not in t:
        sem.append(f"{p}: sem copyright")
print(f"   {'✅ todas OK' if not sem else chr(10).join('   ❌ ' + s for s in sem)}")

print("\n=== 2) Colunas do rodapé presentes ===")
colunas = {"Navegação": 0, "Institucional": 0, "Contato": 0, "Receba novidades": 0, "Instagram": 0}
for p in paginas:
    t = ler(p)
    for c in colunas:
        if c in t:
            colunas[c] += 1
for c, n in colunas.items():
    print(f"   {'OK ' if n == len(paginas) else '❌ '} '{c}': {n}/{len(paginas)}")

print("\n=== 3) Newsletter (form) presente ===")
faltando = [p for p in paginas if 'data-form-type="newsletter"' not in ler(p)]
print(f"   {'✅ em todas' if not faltando else '❌ faltando em: ' + ', '.join(faltando)}")

print("\n=== 4) Balanço de tags (por página) ===")
prob = []
for p in paginas:
    t = ler(p)
    for tag in ("footer", "section", "a", "form"):
        a = len(re.findall(rf"<{tag}[\s>]", t))
        f = len(re.findall(rf"</{tag}>", t))
        if a != f:
            prob.append(f"{p}: <{tag}> {a}/{f}")
print(f"   {'✅ todas balanceadas' if not prob else chr(10).join('   ❌ ' + x for x in prob)}")

print("\n=== 5) Páginas no ar ===")
falhas = []
for p in paginas:
    try:
        with urllib.request.urlopen(f"{URL}/{p}", timeout=5) as r:
            if r.status != 200:
                falhas.append(p)
    except Exception as e:
        falhas.append(f"{p} ({e})")
print(f"   {len(paginas)-len(falhas)}/{len(paginas)} HTTP 200")
for f in falhas:
    print("   ❌", f)
