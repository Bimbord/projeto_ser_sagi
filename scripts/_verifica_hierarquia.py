# -*- coding: utf-8 -*-
"""Verifica a hierarquia: home -> pilar -> pagina -> sub-pagina."""
import os, re, urllib.request

BASE = r"C:/Projetos Code/Projeto SER Sagi/projeto_SER_Sagi - Hermes"
URL = "http://127.0.0.1:5501"

paginas = sorted(f for f in os.listdir(BASE) if f.endswith(".html"))
print(f"=== {len(paginas)} páginas HTML ===")

# 1) todas respondem?
print("\n=== 1) Live Server (5501) ===")
falhas = []
for p in paginas:
    try:
        with urllib.request.urlopen(f"{URL}/{p}", timeout=5) as r:
            if r.status != 200:
                falhas.append(p)
    except Exception as e:
        falhas.append(f"{p} ({e})")
print(f"   {len(paginas) - len(falhas)}/{len(paginas)} respondendo HTTP 200")
for f in falhas:
    print("   ❌", f)

# 2) links dos pilares da home
print("\n=== 2) Pilares da home -> destino ===")
home = open(os.path.join(BASE, "index.html"), encoding="utf-8").read()
cards = re.findall(r'<a href="([^"]+)" class="home-card home-pillar">(.*?)</a>', home, re.S)
for href, conteudo in cards:
    t = re.search(r'home-card__title">([^<]*)<', conteudo)
    nome = t.group(1) if t else "?"
    existe = os.path.exists(os.path.join(BASE, href))
    print(f"   {nome:<14} -> {href:<32} {'OK' if existe else '❌ NAO EXISTE'}")

# 3) cards do hub Esporte
print("\n=== 3) Hub Esporte -> modalidades ===")
esp = open(os.path.join(BASE, "esporte.html"), encoding="utf-8").read()
mods = re.findall(r'<a href="([^"]+)" class="block h-full rounded-3xl', esp)
print(f"   {len(mods)} cards")
for h in mods:
    existe = os.path.exists(os.path.join(BASE, h))
    print(f"   {'OK ' if existe else '❌ '} {h}")

# 4) links quebrados em TODO o site
print("\n=== 4) Links internos quebrados (todo o site) ===")
quebrados = []
for p in paginas:
    txt = open(os.path.join(BASE, p), encoding="utf-8").read()
    for h in set(re.findall(r'href="([a-z0-9\-\.]+\.html)', txt)):
        if not os.path.exists(os.path.join(BASE, h)):
            quebrados.append(f"{p} -> {h}")
if quebrados:
    for q in sorted(set(quebrados)):
        print("   ❌", q)
else:
    print("   ✅ nenhum link quebrado")

# 5) resumo da hierarquia
print("\n=== 5) Hierarquia ===")
print("""   Home (index)
   ├── Saúde        -> consultorio-odontologico.html
   ├── Esporte      -> esporte.html (hub)
   │      ├── Jiu-Jitsu   -> escola-jiu-jitsu.html
   │      ├── Vôlei       -> volei.html
   │      ├── Futevôlei   -> futevolei.html
   │      ├── Musculação  -> estudio-musculacao.html
   │      ├── Natação     -> natacao.html
   │      └── Dança       -> danca.html
   ├── Educação     -> educacao.html
   ├── Cultura      -> cultura.html
   └── Preservação  -> preservacao-ambiental.html""")
