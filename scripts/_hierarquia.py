# -*- coding: utf-8 -*-
"""
Hierarquia: ACOES > CATEGORIA > SUB > PAGINA

ETAPA 1 — acoes.html passa a mostrar as 5 CATEGORIAS
          (Saude, Esporte, Educacao, Cultura, Preservacao)

ETAPA 2 — saude.html vira HUB da categoria Saude
          e o conteudo do consultorio vira consultorio-odontologico.html
"""
import os
import re

BASE = r"G:/.shortcut-targets-by-id/18wGiptBKUmAmmkKHgdfu05TU4y_roWC1/BBDPRINT - BACKUP/BBDPRINT/App BBDPRiNT/PROJETOS/Projeto SER Sagi/projeto_SER_Sagi - Hermes"

BADGE = ('<span class="mt-3 inline-flex items-center gap-1.5 rounded-full bg-sand px-2.5 py-1 text-[10px] '
         'font-semibold uppercase tracking-[0.15em] text-slate-500" title="Conteúdo ilustrativo — será substituído por imagem real">'
         '<i class="fa-solid fa-wand-magic-sparkles text-[9px]"></i>Imagem ilustrativa</span>')

CARD = ('<a href="{href}" class="block rounded-3xl bg-white p-6 shadow-soft transition hover:-translate-y-1 hover:ring-2 hover:ring-ocean/30">'
        '<div class="relative -mx-1 overflow-hidden rounded-2xl"><img src="{img}" alt="Imagem ilustrativa — {nome}" class="h-40 w-full object-cover" loading="lazy" /></div>'
        + BADGE +
        '<i class="fa-solid {icone} mt-3 block text-2xl text-ocean"></i>'
        '<h3 class="mt-4 text-xl font-bold text-oceanDeep">{nome}</h3>'
        '<p class="mt-3 text-sm leading-7 text-slate-600">{texto}</p>'
        '<ul class="mt-4 space-y-2 text-sm text-slate-700">{itens}</ul>'
        '<span class="mt-4 inline-flex items-center gap-2 text-sm font-semibold text-ocean">Ver categoria <i class="fa-solid fa-arrow-right text-xs"></i></span>'
        '</a>')

CATEGORIAS = [
    dict(href="saude.html", nome="Saúde", icone="fa-heart-pulse",
         img="https://loremflickr.com/800/500/dentist,health,clinic?lock=101",
         texto="Cuidado com a saúde da comunidade do Sagi, começando pelo consultório odontológico.",
         itens=["Consultório odontológico"]),
    dict(href="esporte.html", nome="Esporte", icone="fa-futbol",
         img="https://loremflickr.com/800/500/sports,kids,team?lock=102",
         texto="Esporte como ferramenta de disciplina, saúde e convivência para crianças e adolescentes.",
         itens=["Jiu-jitsu", "Vôlei e futevôlei", "Musculação e natação", "Dança"]),
    dict(href="educacao.html", nome="Educação", icone="fa-book-open",
         img="https://loremflickr.com/800/500/classroom,education,kids?lock=103",
         texto="Aulas que ampliam horizontes e abrem portas para o futuro das nossas crianças.",
         itens=["Inglês e espanhol", "Informática", "Sustentabilidade"]),
    dict(href="cultura.html", nome="Cultura", icone="fa-masks-theater",
         img="https://loremflickr.com/800/500/community,culture,people?lock=104",
         texto="Valorização das origens, convivência comunitária e ações solidárias.",
         itens=["Ações solidárias", "Cultura e comunidade"]),
    dict(href="preservacao-ambiental.html", nome="Preservação", icone="fa-leaf",
         img="https://loremflickr.com/800/500/beach,nature,turtle?lock=105",
         texto="Proteção do território e educação socioambiental com as crianças do Sagi.",
         itens=["Proteção de tartarugas", "Educação ambiental"]),
]

GRID_NOVO = ('<div class="grid gap-6 md:grid-cols-2 xl:grid-cols-3">'
             + "".join(CARD.format(itens="".join(f"<li>{i}</li>" for i in c["itens"]),
                                   **{k: v for k, v in c.items() if k != "itens"})
                       for c in CATEGORIAS)
             + '</div>')

# ============================================================
# ETAPA 1 — acoes.html
# ============================================================
p = os.path.join(BASE, "acoes.html")
txt = open(p, encoding="utf-8", newline="").read()

padrao = re.compile(r'<div class="grid gap-6 md:grid-cols-2 xl:grid-cols-3">.*?</section>', re.DOTALL)
txt, qtd = padrao.subn(GRID_NOVO + '</section>', txt, count=1)
assert qtd == 1, "acoes.html: grade de cards nao encontrada"

# ajusta o texto do banner (agora sao categorias)
txt = txt.replace(
    "Projetos e serviços que geram impacto concreto na comunidade",
    "Categorias de atuação do Instituto")
txt = txt.replace(
    "Da saúde ao esporte, da educação à preservação ambiental: conheça cada frente de atuação do Instituto na comunidade do Sagi.",
    "Escolha uma categoria para conhecer as áreas e as ações que o Instituto desenvolve na comunidade do Sagi.")
open(p, "w", encoding="utf-8", newline="").write(txt)
print("  ✅ acoes.html: 6 acoes -> 5 CATEGORIAS")

# ============================================================
# ETAPA 2a — consultorio-odontologico.html (conteudo atual)
# ============================================================
orig = open(os.path.join(BASE, "saude.html"), encoding="utf-8", newline="").read()

doc = orig

# breadcrumb: 3 -> 4 niveis
DE = '''      <ol>
        <li><a href="./">Início</a></li>
        <li><a href="acoes.html">Nossas Ações</a></li>
        <li><span aria-current="page">Saúde</span></li>
      </ol>'''
PARA = '''      <ol>
        <li><a href="./">Início</a></li>
        <li><a href="acoes.html">Nossas Ações</a></li>
        <li><a href="saude.html">Saúde</a></li>
        <li><span aria-current="page">Consultório Odontológico</span></li>
      </ol>'''
assert DE in doc, "saude.html: breadcrumb de 3 niveis nao encontrado"
doc = doc.replace(DE, PARA, 1)

# JSON-LD: 3 -> 4 niveis
DE = '''      { "@type": "ListItem", "position": 3, "name": "Saúde", "item": "https://bimbord.github.io/projeto_ser_sagi/saude.html" }'''
PARA = '''      { "@type": "ListItem", "position": 3, "name": "Saúde", "item": "https://bimbord.github.io/projeto_ser_sagi/saude.html" },
      { "@type": "ListItem", "position": 4, "name": "Consultório Odontológico", "item": "https://bimbord.github.io/projeto_ser_sagi/consultorio-odontologico.html" }'''
assert DE in doc, "saude.html: JSON-LD nao encontrado"
doc = doc.replace(DE, PARA, 1)

# "voltar" passa a apontar para a categoria Saude
doc = doc.replace("<p class=\"font-bold text-oceanDeep\">Voltar para Nossas Ações</p>",
                  "<p class=\"font-bold text-oceanDeep\">Voltar para Saúde</p>", 1)
doc = doc.replace("Veja o conjunto completo de frentes de atuação do Instituto na comunidade do Sagi.",
                  "Veja as demais áreas de saúde do Instituto.", 1)
doc = doc.replace('href="acoes.html" class="cta-lift mt-4 inline-flex items-center gap-2 rounded-full bg-ocean px-5 py-2.5 text-sm font-semibold text-white transition hover:brightness-95"><i class="fa-solid fa-arrow-left text-xs"></i>Ver todas as ações',
                  'href="saude.html" class="cta-lift mt-4 inline-flex items-center gap-2 rounded-full bg-ocean px-5 py-2.5 text-sm font-semibold text-white transition hover:brightness-95"><i class="fa-solid fa-arrow-left text-xs"></i>Voltar para Saúde', 1)

open(os.path.join(BASE, "consultorio-odontologico.html"), "w", encoding="utf-8", newline="").write(doc)
print("  ✅ consultorio-odontologico.html criado (conteudo da pagina antiga)")

# ============================================================
# ETAPA 2b — saude.html vira HUB
# ============================================================
cabeca = orig.split("<main", 1)[0].replace(
    "<title>Consultório Odontológico | Instituto S.E.R. Sagi</title>",
    "<title>Saúde | Instituto S.E.R. Sagi</title>", 1)
rodape = "<footer" + orig.split("<footer", 1)[1]

CARD_AREA = ('<a href="consultorio-odontologico.html" class="block h-full rounded-3xl bg-white p-6 shadow-soft transition hover:-translate-y-1 hover:ring-2 hover:ring-ocean/30">'
             '<div class="relative -mx-1 overflow-hidden rounded-2xl"><img src="https://loremflickr.com/800/500/dentist,clinic,tooth?lock=101" alt="Imagem ilustrativa — Consultório Odontológico" class="h-40 w-full object-cover" loading="lazy" /></div>'
             + BADGE +
             '<i class="fa-solid fa-tooth mt-3 block text-2xl text-ocean"></i>'
             '<h3 class="mt-4 text-xl font-bold text-oceanDeep">Consultório Odontológico</h3>'
             '<p class="mt-3 text-sm leading-7 text-slate-600">Atendimento odontológico para crianças, jovens e adultos da comunidade — prevenção, tratamento e acolhimento.</p>'
             '<span class="mt-4 inline-flex items-center gap-1 text-sm font-semibold text-ocean">Saiba mais <i class="fa-solid fa-arrow-right text-xs"></i></span>'
             '</a>')

HUB = '''<main id="conteudo-principal">
    <section class="page-banner text-white relative overflow-hidden banner-alto">
      <img src="https://loremflickr.com/1600/600/dentist,health,care?lock=201" alt="" aria-hidden="true" class="absolute inset-0 h-full w-full object-cover">
      <div class="banner-scrim absolute inset-0"></div>
      <div class="relative z-10 mx-auto max-w-7xl px-4 py-16 lg:px-8 lg:py-20">
        <p class="text-sm font-semibold uppercase tracking-[0.25em] text-sun">Nossas Ações • Categoria</p>
        <h2 class="mt-4 max-w-4xl text-4xl font-extrabold leading-tight sm:text-5xl">Saúde</h2>
        <p class="mt-6 max-w-3xl text-lg text-white/85">Cuidado com a saúde da comunidade do Sagi — do consultório odontológico às ações de bem-estar.</p>
      </div>
    </section>

    <!-- 🧭 Caminho de navegacao (fora do hero) -->
    <nav class="breadcrumb breadcrumb--claro mx-auto max-w-7xl px-4 lg:px-8" aria-label="Você está aqui">
      <ol>
        <li><a href="./">Início</a></li>
        <li><a href="acoes.html">Nossas Ações</a></li>
        <li><span aria-current="page">Saúde</span></li>
      </ol>
    </nav>

    <section class="mx-auto max-w-7xl px-4 py-16 lg:px-8">
      <div class="max-w-3xl">
        <p class="text-sm font-semibold uppercase tracking-[0.25em] text-ocean">Áreas</p>
        <h3 class="section-title text-3xl font-extrabold text-oceanDeep">O que oferecemos em saúde</h3>
        <p class="mt-4 text-slate-600">Cada área tem sua própria página com mais detalhes. Toque em uma para saber mais.</p>
      </div>
      <div class="mt-10 grid gap-6 md:grid-cols-2 xl:grid-cols-3">
        ''' + CARD_AREA + '''
      </div>
    </section>

    <section class="bg-mist/70 py-16">
      <div class="mx-auto max-w-7xl px-4 lg:px-8">
        <div class="rounded-[2rem] bg-oceanDeep p-8 text-center text-white shadow-soft">
          <h2 class="text-3xl font-extrabold">Quer apoiar esta frente?</h2>
          <p class="mx-auto mt-4 max-w-2xl text-white/85">Empresas, voluntários e doadores podem contribuir para a saúde da comunidade do Sagi.</p>
          <div class="mt-8 flex flex-wrap justify-center gap-4">
            <a href="como-ajudar.html" class="cta-lift rounded-full bg-sun px-6 py-3 font-semibold text-oceanDeep">Como ajudar</a>
            <a href="lei-incentivo.html" class="cta-lift rounded-full border border-white/40 px-6 py-3 font-semibold text-white">Lei de Incentivo</a>
            <a href="acoes.html" class="cta-lift rounded-full border border-white/40 px-6 py-3 font-semibold text-white">Voltar às categorias</a>
          </div>
        </div>
      </div>
    </section>
  </main>
  '''

open(os.path.join(BASE, "saude.html"), "w", encoding="utf-8", newline="").write(cabeca + HUB + rodape)
print("  ✅ saude.html virou HUB da categoria Saúde")

# ============================================================
# ETAPA 3 — ajustes de link
# ============================================================
# main.js: destaque do menu
p = os.path.join(BASE, "js", "main.js")
txt = open(p, encoding="utf-8", newline="").read()
DE = "const acoesSub = ['saude.html',"
PARA = "const acoesSub = ['saude.html', 'consultorio-odontologico.html',"
assert DE in txt, "main.js: acoesSub nao encontrado"
txt = txt.replace(DE, PARA, 1)
open(p, "w", encoding="utf-8", newline="").write(txt)
print("  ✅ js/main.js: consultorio-odontologico.html destacado em Nossas Ações")

# instalacoes.html e quem-somos.html: quem fala do CONSULTORIO aponta pra ele
for nome in ("instalacoes.html", "quem-somos.html"):
    p = os.path.join(BASE, nome)
    txt = open(p, encoding="utf-8", newline="").read()
    DE = ('<a href="saude.html" class="flex items-start gap-4 rounded-2xl bg-white p-5 shadow-soft '
          'transition hover:-translate-y-1 hover:ring-2 hover:ring-ocean/30">')
    if DE in txt:
        txt = txt.replace(DE, DE.replace('href="saude.html"', 'href="consultorio-odontologico.html"'), 1)
        print(f"  ✅ {nome}: card do consultorio aponta pra consultorio-odontologico.html")
    DE2 = '<a href="saude.html" class="block h-full rounded-3xl bg-white p-6 shadow-soft transition hover:-translate-y-1 hover:shadow-[0_24px_80px_rgba(8,59,76,0.18)] hover:ring-2 hover:ring-ocean/30">'
    if DE2 in txt:
        txt = txt.replace(DE2, DE2.replace('href="saude.html"', 'href="consultorio-odontologico.html"'), 1)
        print(f"  ✅ {nome}: card do consultorio aponta pra consultorio-odontologico.html")
    open(p, "w", encoding="utf-8", newline="").write(txt)
