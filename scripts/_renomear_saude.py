# -*- coding: utf-8 -*-
"""
1) Atualiza todas as referências de consultorio-odontologico.html -> saude.html
2) Ajusta a página saude.html: título + banner com imagem e scrim
3) Adiciona a classe .banner-scrim ao css/style.css
"""
import os
import re

BASE = r"C:/Projetos Code/Projeto SER Sagi/projeto_SER_Sagi - Hermes"

# ---------------------------------------------------------------
# 1) Referências (hrefs) em todas as páginas + main.js
# ---------------------------------------------------------------
n = 0
for nome in sorted(os.listdir(BASE)):
    if not nome.endswith(".html"):
        continue
    p = os.path.join(BASE, nome)
    txt = open(p, encoding="utf-8", newline="").read()
    novo = txt.replace("consultorio-odontologico.html", "saude.html")
    if novo != txt:
        open(p, "w", encoding="utf-8", newline="").write(novo)
        n += 1
print(f"  refs atualizadas em {n} páginas HTML")

p = os.path.join(BASE, "js", "main.js")
txt = open(p, encoding="utf-8", newline="").read()
novo = txt.replace("consultorio-odontologico.html", "saude.html")
if novo != txt:
    open(p, "w", encoding="utf-8", newline="").write(novo)
    print("  refs atualizadas em js/main.js")

# ---------------------------------------------------------------
# 2) saude.html — título + banner com imagem/scrim
# ---------------------------------------------------------------
p = os.path.join(BASE, "saude.html")
txt = open(p, encoding="utf-8", newline="").read()

txt = txt.replace(
    "<title>Consultório Odontológico | Instituto S.E.R. Sagi</title>",
    "<title>Saúde | Instituto S.E.R. Sagi</title>"
)

BANNER_NOVO = (
    '<section class="page-banner text-white relative overflow-hidden">\n'
    '      <!-- CAMADA 1 · IMAGEM de fundo (ilustrativa — trocar por foto real em img/banners/) -->\n'
    '      <img src="https://loremflickr.com/1600/600/dentist,health,care?lock=201" alt="" aria-hidden="true" class="absolute inset-0 h-full w-full object-cover">\n'
    '      <!-- CAMADA 2 · SCRIM (véu diagonal — mesmo efeito do hero da home) -->\n'
    '      <div class="banner-scrim absolute inset-0"></div>\n'
    '      <!-- CAMADA 3 · CONTEÚDO (por cima) -->\n'
    '      <div class="relative z-10 mx-auto max-w-7xl px-4 py-16 lg:px-8 lg:py-20">\n'
    '        <p class="text-sm font-semibold uppercase tracking-[0.25em] text-sun">Saúde • Nossas Ações</p>\n'
    '        <h2 class="mt-4 max-w-4xl text-4xl font-extrabold leading-tight sm:text-5xl">Saúde</h2>\n'
    '        <p class="mt-6 max-w-3xl text-lg text-white/85">Cuidado com a saúde da comunidade do Sagi — começando pelo consultório odontológico, com prevenção, tratamento e acolhimento.</p>\n'
    '      </div>\n'
    '    </section>'
)

txt, qtd = re.subn(r'<section class="page-banner text-white">.*?</section>',
                   lambda m: BANNER_NOVO, txt, count=1, flags=re.DOTALL)
print(f"  banner com imagem/scrim aplicado: {qtd}x")

open(p, "w", encoding="utf-8", newline="").write(txt)

# ---------------------------------------------------------------
# 3) CSS — classe .banner-scrim
# ---------------------------------------------------------------
p = os.path.join(BASE, "css", "style.css")
css = open(p, encoding="utf-8", newline="").read()

if ".banner-scrim" not in css:
    css = css.rstrip() + """

/* ============================================================
   BANNER INTERNO COM IMAGEM + SCRIM
   Mesmo efeito do hero da home: imagem de fundo coberta por um
   véu escuro diagonal, mantendo o texto legível à esquerda.
   Degradação graciosa: se a imagem não carregar, o gradiente
   do .page-banner aparece por baixo.
   ============================================================ */
.banner-scrim {
  background: linear-gradient(112deg,
    rgba(8, 59, 76, 0.92) 0%,
    rgba(8, 59, 76, 0.66) 40%,
    rgba(8, 59, 76, 0.30) 72%,
    rgba(8, 59, 76, 0.16) 100%);
}
"""
    open(p, "w", encoding="utf-8", newline="").write(css)
    print("  .banner-scrim adicionado ao css/style.css")
else:
    print("  .banner-scrim já existia no CSS")
