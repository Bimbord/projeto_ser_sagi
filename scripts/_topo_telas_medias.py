# -*- coding: utf-8 -*-
"""
Topo (header): faz os botões "Seja Parceiro" e "Doe Agora" caberem em telas
médias (1024–1279px), combinando as ideias A e B:

  A) botões mais compactos nessa faixa
  B) menu com menos espaçamento/fonte nessa faixa
  + logo um pouco menor nessa faixa (ganha ~40px)

Medição real (navegador): em 1024px faltavam ~153px.
"""
import glob
import os
import re

BASE = r"G:/.shortcut-targets-by-id/18wGiptBKUmAmmkKHgdfu05TU4y_roWC1/BBDPRINT - BACKUP/BBDPRINT/App BBDPRiNT/PROJETOS/Projeto SER Sagi/projeto_SER_Sagi - Hermes"
L = lambda p: os.path.join(BASE, p)  # noqa: E731

# ---------- 1. HTML: classes de gancho + botões visíveis a partir de lg ----------
paginas = sorted(glob.glob(L("*.html")))
n_logo = n_cta = n_vis = 0
for p in paginas:
    txt = open(p, encoding="utf-8", newline="").read()
    orig = txt
    # logo do topo ganha classe (para poder diminuir em telas médias)
    if 'topo-logo' not in txt and '<img src="img/logo.png" alt="Instituto S.E.R. Sagi" class="h-16 w-auto object-contain">' in txt:
        txt = txt.replace('<img src="img/logo.png" alt="Instituto S.E.R. Sagi" class="h-16 w-auto object-contain">',
                          '<img src="img/logo.png" alt="Instituto S.E.R. Sagi" class="topo-logo h-16 w-auto object-contain">', 1)
    n_logo += 1 if 'topo-logo' in txt else 0
    # container dos botões CTA
    if 'class="hidden items-center gap-3 xl:flex"' in txt:
        txt = txt.replace('class="hidden items-center gap-3 xl:flex"', 'class="topo-cta hidden items-center gap-3 lg:flex"')
        n_vis += 1
    elif 'class="hidden items-center gap-3"' in txt:
        txt = txt.replace('class="hidden items-center gap-3"', 'class="topo-cta hidden items-center gap-3 lg:flex"')
        n_vis += 1
    if txt != orig:
        open(p, "w", encoding="utf-8", newline="").write(txt)
        n_cta += 1

print(f"  ✅ logo com classe 'topo-logo': {n_logo}/{len(paginas)}")
print(f"  ✅ botões CTA a partir de lg: {n_vis}/{len(paginas)} páginas")

# ---------- 2. CSS ----------
p_css = L("css/style.css")
css = open(p_css, encoding="utf-8", newline="").read()
if "topo-logo" in css:
    print("  ⚠️  CSS já tinha o ajuste do topo")
else:
    css += """

/* ============================================================
   TOPO em telas médias (1024–1279px)
   O menu cresceu (dropdowns + Jóia da Coroa) e os botões CTA
   ficavam escondidos. Aqui tudo compacta um pouco — medido no
   navegador: em 1024px faltavam ~153px; isto devolve ~200px.
   ============================================================ */
@media (min-width: 1024px) and (max-width: 1279px) {
  nav[aria-label="Menu principal"] { gap: 0.125rem; }
  .nav-link {
    padding: 0.4rem 0.45rem;
    font-size: 0.8125rem;
    gap: 0.25rem;
  }
  .nav-link .fa-chevron-down { font-size: 0.55rem; }
  header img.topo-logo { height: 3rem; }
  header .topo-cta a {
    padding: 0.45rem 0.85rem;
    font-size: 0.8125rem;
  }
}
"""
    open(p_css, "w", encoding="utf-8", newline="").write(css)
    print("  ✅ css/style.css — faixa 1024–1279px compacta")
