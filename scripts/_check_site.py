# -*- coding: utf-8 -*-
"""Verifica a integridade da reconstrução do site."""
import os, re, urllib.request

BASE = r"C:/Projetos Code/Projeto SER Sagi/projeto_SER_Sagi - Hermes"
URL = "http://127.0.0.1:5502"

paginas = sorted(f for f in os.listdir(BASE) if f.endswith(".html"))
print(f"=== {len(paginas)} páginas HTML encontradas ===")
for p in paginas:
    print("   ", p)

print("\n=== Verificações ===")

# 1) todas respondem na web?
ok = 0
for p in paginas:
    try:
        with urllib.request.urlopen(f"{URL}/{p}", timeout=5) as r:
            if r.status == 200:
                ok += 1
    except Exception as e:
        print(f"  ❌ {p}: {e}")
print(f"  1) páginas servindo HTTP 200: {ok}/{len(paginas)}")

# 2) logo em imagem em todas?
com_logo, com_texto = [], []
for p in paginas:
    t = open(os.path.join(BASE, p), encoding="utf-8").read()
    if "img/logo.png" in t:
        com_logo.append(p)
    if "fa-feather" in t:
        com_texto.append(p)
print(f"  2) logo em imagem: {len(com_logo)}/{len(paginas)} | logo em texto (deve ser 0): {len(com_texto)}")

# 3) referências antigas a arquivo.html?
antigas = []
for raiz, _, arqs in os.walk(BASE):
    if any(x in raiz for x in ("scripts", "docs", "plans", "img")):
        continue
    for a in arqs:
        if a.endswith((".html", ".js")):
            t = open(os.path.join(raiz, a), encoding="utf-8", errors="ignore").read()
            if "arquivo.html" in t or ">Arquivo<" in t:
                antigas.append(a)
print(f"  3) referências antigas a 'arquivo.html'/'>Arquivo<': {len(antigas)} {antigas if antigas else ''}")

# 4) cards do acervo
t = open(os.path.join(BASE, "acervo.html"), encoding="utf-8").read()
links_acervo = re.findall(r'href="(acervo-[a-z]+\.html)"', t)
print(f"  4) acervo.html: {len(links_acervo)} cards-categoria -> {sorted(set(links_acervo))}")

# 5) cards das ações
t = open(os.path.join(BASE, "acoes.html"), encoding="utf-8").read()
links_acoes = re.findall(r'<a href="([a-z-]+\.html)" class="block rounded-3xl bg-white', t)
print(f"  5) acoes.html: {len(links_acoes)} cards-ação -> {links_acoes}")

# 6) main.js no Supabase?
t = open(os.path.join(BASE, "js", "main.js"), encoding="utf-8").read()
print(f"  6) main.js: SUPABASE_URL={'SIM' if 'SUPABASE_URL' in t else 'NAO'} | "
      f"fetch relativo antigo={'SIM' if 'fetch(`tables/' in t else 'NAO'} | "
      f"archive-grid={'SIM' if 'archive-grid' in t else 'NAO'}")

# 7) assets
for f in ("img/logo.png", "img/logo2-hero.png", "css/style.css", "js/main.js", "js/hero.js"):
    p = os.path.join(BASE, f.replace("/", os.sep))
    print(f"  7) {f}: {'OK' if os.path.exists(p) else 'FALTANDO'}")
