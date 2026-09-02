# -*- coding: utf-8 -*-
"""Padroniza o logo em imagem (img/logo.png) nas páginas que usam logo em texto."""
import os

BASE = r"D:/BBDPRINT - BACKUP/BBDPRINT/App BBDPRiNT/PROJETOS/Projetos Code/Projeto SER Sagi/projeto_SER_Sagi - Hermes"

PAGES = ["acoes.html", "como-ajudar.html", "contato.html",
         "lei-incentivo.html", "quem-somos.html", "transparencia.html"]

OLD = '<a href="index.html" class="flex items-center gap-3"><div class="flex h-12 w-12 items-center justify-center rounded-full bg-ocean text-white shadow-soft"><i class="fa-solid fa-feather text-xl"></i></div><div><p class="text-xs font-semibold uppercase tracking-[0.25em] text-ocean">Instituto</p><h1 class="text-lg font-extrabold leading-tight text-oceanDeep">S.E.R. Sagi</h1></div></a>'

NEW = '<a href="index.html" class="flex items-center" aria-label="Instituto S.E.R. Sagi - página inicial"><img src="img/logo.png" alt="Instituto S.E.R. Sagi" class="h-16 w-auto object-contain"></a>'

for p in PAGES:
    fp = os.path.join(BASE, p)
    html = open(fp, encoding="utf-8").read()
    n = html.count(OLD)
    if n == 0:
        print(f"  ⚠️ {p}: logo em texto NÃO encontrado (pode já ter sido trocado)")
        continue
    html = html.replace(OLD, NEW)
    with open(fp, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  ✅ {p}: logo trocado ({n} ocorrência(s))")

print("\n=== Verificação final ===")
for p in sorted(os.listdir(BASE)):
    if p.endswith(".html"):
        html = open(os.path.join(BASE, p), encoding="utf-8").read()
        tem_texto = "fa-feather" in html
        tem_img = "img/logo.png" in html
        status = "✅ imagem" if (tem_img and not tem_texto) else ("⚠️ ainda texto" if tem_texto else "❓ sem logo")
        print(f"  {p:38s} {status}")
