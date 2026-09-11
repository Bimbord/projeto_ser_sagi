# -*- coding: utf-8 -*-
"""Verifica a implementação de Instalações (hub + seção no Quem Somos + links cruzados)."""
import os, re, urllib.request

BASE = r"C:/Projetos Code/Projeto SER Sagi/projeto_SER_Sagi - Hermes"
URL = "http://127.0.0.1:5501"


def ler(nome):
    return open(os.path.join(BASE, nome), encoding="utf-8").read()


paginas = sorted(f for f in os.listdir(BASE) if f.endswith(".html"))
print(f"=== {len(paginas)} páginas ===")

print("\n=== 1) instalacoes.html ===")
if os.path.exists(os.path.join(BASE, "instalacoes.html")):
    inst = ler("instalacoes.html")
    cards = re.findall(r'<a href="([^"]+)" class="block h-full rounded-3xl', inst)
    print(f"   {len(cards)} cards:")
    for c in cards:
        ok = os.path.exists(os.path.join(BASE, c))
        print(f"     {'OK ' if ok else '❌ '} {c}")
else:
    print("   ❌ não existe")

print("\n=== 2) Seção 'Nossas instalações' no Quem Somos ===")
qs = ler("quem-somos.html")
print("   título presente:", "Nossas instalações" in qs)
links_qs = re.findall(r'<a href="([^"]+)" class="flex items-start gap-4', qs)
print(f"   {len(links_qs)} cards compactos: {links_qs}")

print("\n=== 3) Links cruzados (Onde acontece) ===")
for p in ("volei.html", "futevolei.html"):
    txt = ler(p)
    tem = 'Onde acontece' in txt and 'arena-futevolei-volei.html' in txt
    print(f"   {'OK ' if tem else '❌ '} {p}")

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

print("\n=== 5) Links internos quebrados (site inteiro) ===")
quebrados = set()
for p in paginas:
    for h in set(re.findall(r'href="([a-z0-9\-\.]+\.html)', ler(p))):
        if not os.path.exists(os.path.join(BASE, h)):
            quebrados.add(f"{p} -> {h}")
print("   ✅ nenhum" if not quebrados else "\n".join("   ❌ " + q for q in sorted(quebrados)))

print("\n=== 6) Navegação por instalações ===")
print("""   Quem Somos (seção "Nossas instalações")
   ├── Arena de Futevôlei e Vôlei   -> arena-futevolei-volei.html
   ├── Consultório Odontológico     -> consultorio-odontologico.html
   ├── Estúdio de Musculação        -> estudio-musculacao.html
   └── Tatame (Jiu-Jitsu)           -> escola-jiu-jitsu.html
   └── botão -> instalacoes.html (hub completo)
   Vôlei e Futevôlei -> link cruzado "Onde acontece: Arena" """)
