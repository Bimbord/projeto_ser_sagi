# -*- coding: utf-8 -*-
"""Padroniza o logo em imagem (img/logo.png) nas páginas que ainda usam logo em texto."""
import os, re

BASE = r"C:/Projetos Code/Projeto SER Sagi/projeto_SER_Sagi - Hermes"

NOVO = ('<a href="index.html" class="flex items-center" aria-label="Instituto S.E.R. Sagi — página inicial">'
        '<img src="img/logo.png" alt="Instituto S.E.R. Sagi" class="h-16 w-auto object-contain"></a>')

PADRAO = re.compile(r'<a href="index\.html" class="flex items-center gap-3">.*?</a>', re.S)

total = 0
for nome in sorted(os.listdir(BASE)):
    if not nome.endswith(".html"):
        continue
    p = os.path.join(BASE, nome)
    t = open(p, encoding="utf-8").read()
    nt, n = PADRAO.subn(NOVO, t)
    if n:
        open(p, "w", encoding="utf-8", newline="\n").write(nt)
        print(f"  OK {nome} ({n} logo)")
        total += 1

print(f"\n[logo] {total} pagina(s) padronizadas")
print(f"[logo] ainda com fa-feather: {sum(1 for f in os.listdir(BASE) if f.endswith('.html') and 'fa-feather' in open(os.path.join(BASE, f), encoding='utf-8').read())}")
