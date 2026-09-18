# -*- coding: utf-8 -*-
"""
Liga os cards de "Impacto em números" (home) às páginas correspondentes.

O card vira <a> inteiro (como os cards de pilares). Para manter HTML VÁLIDO,
a lista <dl> vira <div> e <dt>/<dd> viram <span> com display:block no CSS
(um <a> não é filho válido de <dl>).

Destinos conferidos contra as páginas que existem no site.
"""
import os
import re

BASE = r"G:/.shortcut-targets-by-id/18wGiptBKUmAmmkKHgdfu05TU4y_roWC1/BBDPRINT - BACKUP/BBDPRINT/App BBDPRiNT/PROJETOS/Projeto SER Sagi/projeto_SER_Sagi - Hermes"
L = lambda p: os.path.join(BASE, p)  # noqa: E731

# rótulo do card -> página de destino
DESTINOS = {
    "Projeto principal": "acoes.html",            # a Jóia da Coroa reúne todas as frentes
    "Saúde": "saude.html",
    "Consultório": "saude.html",
    "Esporte": "esporte.html",
    "Jiu-jitsu": "escola-jiu-jitsu.html",
    "Musculação": "estudio-musculacao.html",
}

# ---------- 1. HTML ----------
p_idx = L("index.html")
html = open(p_idx, encoding="utf-8", newline="").read()
antes = html

if 'class="home-stat" href=' in html or "<a class=\"home-stat\"" in html:
    print("  ⚠️  os cards já estavam linkados — pulando")
else:
    # dl -> div
    html = html.replace('<dl class="home-stats__grid">', '<div class="home-stats__grid">', 1)
    # fecha o grid (o </dl> do bloco de números)
    html = html.replace("</dl>", "</div>", 1)

    feitos = []
    for rotulo, destino in DESTINOS.items():
        # <div class="home-stat"> ... <dt class="home-stat__label">RÓTULO</dt>
        padrao = re.compile(
            r'<div class="home-stat">(\s*<img[^>]*>\s*)<dt class="home-stat__label">'
            + re.escape(rotulo) + r'</dt>\s*<dd class="home-stat__value">(.*?)</dd>',
            re.DOTALL)
        novo = (f'<a class="home-stat" href="{destino}">\\1'
                f'<span class="home-stat__label">{rotulo}</span>\n'
                f'            <span class="home-stat__value">\\2</span>')
        html, n = padrao.subn(novo, html, count=1)
        feitos.append((rotulo, destino, n))

    # fecha os cards (</div> logo após o <p class="home-stat__desc">...</p>)
    html = re.sub(r'(<p class="home-stat__desc">[^<]*</p>)\s*</div>', r'\1\n          </a>', html)
    # fecha o <dl> que sobrou, se houver
    html = html.replace("</dl>", "</div>")

    open(p_idx, "w", encoding="utf-8", newline="").write(html)

    print("  ✅ index.html:")
    for rotulo, destino, n in feitos:
        print(f"     {'✅' if n else '❌'} {rotulo:20} -> {destino}")
    print('     <a class="home-stat"> no arquivo: ' + str(html.count('<a class="home-stat"')))
    print('     </a> de fechamento:            ' + str(html.count('</a>')) + ' (total de links da página)')

# ---------- 2. CSS ----------
p_css = L("css/style.css")
css = open(p_css, encoding="utf-8", newline="").read()
if ".home-stat__label," in css or "a.home-stat" in css:
    print("\n  ⚠️  CSS já tratado — pulando")
else:
    css += """

/* ============================================================
   CARDS DE IMPACTO EM NÚMEROS — clicáveis
   (viraram <a>; <dt>/<dd> viraram <span>, precisam de display:block)
   ============================================================ */
.home-stat__label,
.home-stat__value { display: block; }
a.home-stat {
  text-decoration: none;
  color: inherit;
  display: block;
  transition: background .25s ease;
}
a.home-stat:hover { background: var(--mist); }
a.home-stat:focus-visible { outline: 2px solid var(--ocean); outline-offset: -2px; }
a.home-stat:hover .home-stat__value { color: var(--ocean); }
"""
    open(p_css, "w", encoding="utf-8", newline="").write(css)
    print("\n  ✅ css/style.css — display:block + hover + foco visível")

# ---------- 3. confere se os destinos existem ----------
print("\n  --- destinos ---")
for rotulo, destino in DESTINOS.items():
    existe = os.path.isfile(L(destino))
    print(f"     {'✅' if existe else '❌ NÃO EXISTE'} {rotulo:20} -> {destino}")
