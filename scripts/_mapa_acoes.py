# -*- coding: utf-8 -*-
"""
OPCAO A — acoes.html vira o MAPA COMPLETO:
  - Home     = vitrine (5 cards visuais, curtos)
  - acoes.html = mapa completo: cada categoria com TODAS as areas, cada area
                 com LINK DIRETO para a sua pagina
  - Categoria = hub da categoria

Detalhe tecnico: o card deixa de ser um <a> unico (nao pode ter <a> dentro de
<a>) e passa a ser um <article>, com links na imagem, no titulo, em cada area
e no "Ver categoria".
"""
import os
import re

BASE = r"G:/.shortcut-targets-by-id/18wGiptBKUmAmmkKHgdfu05TU4y_roWC1/BBDPRINT - BACKUP/BBDPRINT/App BBDPRiNT/PROJETOS/Projeto SER Sagi/projeto_SER_Sagi - Hermes"

BADGE = ('<span class="mt-3 inline-flex items-center gap-1.5 rounded-full bg-sand px-2.5 py-1 text-[10px] '
         'font-semibold uppercase tracking-[0.15em] text-slate-500" title="Conteúdo ilustrativo — será substituído por imagem real">'
         '<i class="fa-solid fa-wand-magic-sparkles text-[9px]"></i>Imagem ilustrativa</span>')

CARD = '''<article class="flex h-full flex-col rounded-3xl bg-white p-6 shadow-soft transition hover:-translate-y-1 hover:ring-2 hover:ring-ocean/30">
            <a href="{href}" class="block" aria-label="{nome} — ver a categoria">
              <div class="relative -mx-1 overflow-hidden rounded-2xl"><img src="{img}" alt="Imagem ilustrativa — {nome}" class="h-40 w-full object-cover" loading="lazy" /></div>
            </a>
            ''' + BADGE + '''
            <i class="fa-solid {icone} mt-3 block text-2xl text-ocean"></i>
            <h3 class="mt-4 text-xl font-bold text-oceanDeep"><a href="{href}" class="hover:underline">{nome}</a></h3>
            <p class="mt-3 text-sm leading-7 text-slate-600">{texto}</p>
            {areas}
            <a href="{href}" class="mt-5 inline-flex items-center gap-2 pt-1 text-sm font-semibold text-ocean hover:underline">Ver categoria <i class="fa-solid fa-arrow-right text-xs"></i></a>
          </article>'''

AREAS_BLOCO = '''
            <p class="mt-5 text-xs font-semibold uppercase tracking-[0.15em] text-slate-500">Áreas nesta categoria</p>
            <ul class="mt-3 space-y-2 text-sm leading-6">
              {itens}
            </ul>'''

AREA_ITEM = '<li><a href="{href}" class="text-ocean underline-offset-2 transition hover:text-oceanDeep hover:underline">{nome}</a></li>'

CATEGORIAS = [
    dict(href="saude.html", nome="Saúde", icone="fa-heart-pulse",
         img="https://loremflickr.com/800/500/dentist,health,clinic?lock=101",
         texto="Cuidado com a saúde da comunidade do Sagi, começando pelo consultório odontológico.",
         areas=[("Consultório Odontológico", "consultorio-odontologico.html")]),

    dict(href="esporte.html", nome="Esporte", icone="fa-futbol",
         img="https://loremflickr.com/800/500/sports,kids,team?lock=102",
         texto="O esporte como ferramenta de disciplina, saúde e convivência para crianças e adolescentes.",
         areas=[("Jiu-Jitsu", "escola-jiu-jitsu.html"),
                ("Vôlei", "volei.html"),
                ("Futevôlei", "futevolei.html"),
                ("Musculação", "estudio-musculacao.html"),
                ("Natação", "natacao.html"),
                ("Dança", "danca.html")]),

    dict(href="educacao.html", nome="Educação", icone="fa-book-open",
         img="https://loremflickr.com/800/500/classroom,education,kids?lock=103",
         texto="Aulas que ampliam horizontes e abrem portas para o futuro das nossas crianças.",
         areas=[("Inglês", "ingles.html"),
                ("Espanhol", "espanhol.html"),
                ("Informática", "informatica.html"),
                ("Sustentabilidade e Meio Ambiente", "sustentabilidade.html")]),

    dict(href="cultura.html", nome="Cultura", icone="fa-masks-theater",
         img="https://loremflickr.com/800/500/community,culture,people?lock=104",
         texto="Valorização das origens, convivência comunitária e ações solidárias.",
         areas=[("Ações Solidárias", "acoes-solidarias.html")]),

    dict(href="preservacao-ambiental.html", nome="Preservação", icone="fa-leaf",
         img="https://loremflickr.com/800/500/beach,nature,turtle?lock=105",
         texto="Proteção do território e educação socioambiental com as crianças do Sagi.",
         areas=[]),
]


def monta(c):
    if c["areas"]:
        areas = AREAS_BLOCO.format(itens="\n              ".join(
            AREA_ITEM.format(nome=n, href=h) for n, h in c["areas"]))
    else:
        areas = ""
    return CARD.format(areas=areas, **{k: v for k, v in c.items() if k != "areas"})


GRID = ('<div class="grid gap-6 md:grid-cols-2 xl:grid-cols-3">\n          '
        + "\n          ".join(monta(c) for c in CATEGORIAS)
        + '\n        </div>')

p = os.path.join(BASE, "acoes.html")
txt = open(p, encoding="utf-8", newline="").read()

padrao = re.compile(r'<div class="grid gap-6 md:grid-cols-2 xl:grid-cols-3">.*?</section>', re.DOTALL)
txt, qtd = padrao.subn(GRID + '</section>', txt, count=1)
assert qtd == 1, "acoes.html: grade nao encontrada"

# banner: reforca o papel de MAPA COMPLETO
txt = txt.replace(
    "Escolha uma categoria para conhecer as áreas e as ações que o Instituto desenvolve na comunidade do Sagi.",
    "Todas as categorias e áreas de atuação do Instituto na comunidade do Sagi — com link direto para cada uma.", 1)

open(p, "w", encoding="utf-8", newline="").write(txt)

total_areas = sum(len(c["areas"]) for c in CATEGORIAS)
print(f"  ✅ acoes.html: mapa completo — {len(CATEGORIAS)} categorias, {total_areas} áreas com link direto")
