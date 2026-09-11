# -*- coding: utf-8 -*-
"""
Cria a hierarquia de páginas pedida:
  Home -> pilar -> página própria (hub) -> sub-página

Novas páginas:
  esporte.html   (hub com 6 modalidades)
  volei.html / futevolei.html / natacao.html / danca.html
  educacao.html
  cultura.html
"""
import os

BASE = r"C:/Projetos Code/Projeto SER Sagi/projeto_SER_Sagi - Hermes"

HEAD = '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="theme-color" content="#0f5c73" />
  <title>{titulo} | Instituto S.E.R. Sagi</title>
  <meta name="description" content="{descricao}" />
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.4.0/css/all.min.css">
  <script src="https://cdn.tailwindcss.com"></script>
  <script>tailwind.config={{theme:{{extend:{{colors:{{ocean:'#0f5c73',oceanDeep:'#083b4c',sand:'#f5efe3',sun:'#f4b400',coral:'#e77b5f',leaf:'#2e7d4f',mist:'#e7f4f7'}},fontFamily:{{sans:['Inter','sans-serif']}},boxShadow:{{soft:'0 20px 60px rgba(8, 59, 76, 0.12)'}}}}}}}};</script>
  <link rel="stylesheet" href="css/style.css" />
</head>
<body class="font-sans text-slate-800">
  <a href="#conteudo-principal" class="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:bg-white focus:text-ocean focus:px-4 focus:py-2 focus:rounded-md focus:shadow">Pular para o conteúdo</a>
  <header class="sticky top-0 z-50 border-b border-slate-200/70 bg-white/90 backdrop-blur">
    <div class="mx-auto flex max-w-7xl items-center justify-between px-4 py-4 lg:px-8">
      <a href="index.html" class="flex items-center" aria-label="Instituto S.E.R. Sagi — página inicial">
        <img src="img/logo.png" alt="Instituto S.E.R. Sagi" class="h-16 w-auto object-contain">
      </a>
      <button id="menu-toggle" class="inline-flex items-center rounded-lg border border-slate-300 px-3 py-2 text-ocean lg:hidden" aria-expanded="false" aria-controls="mobile-menu" aria-label="Abrir menu"><i class="fa-solid fa-bars"></i></button>
      <nav class="hidden items-center gap-6 lg:flex" aria-label="Menu principal"><a href="index.html" data-page-link class="text-sm font-medium hover:text-ocean">Início</a><a href="quem-somos.html" data-page-link class="text-sm font-medium hover:text-ocean">Quem Somos</a><a href="acoes.html" data-page-link class="text-sm font-medium hover:text-ocean">Nossas Ações</a><a href="acervo.html" data-page-link class="text-sm font-medium hover:text-ocean">Acervo</a><a href="como-ajudar.html" data-page-link class="text-sm font-medium hover:text-ocean">Como Ajudar</a><a href="lei-incentivo.html" data-page-link class="text-sm font-medium hover:text-ocean">Lei de Incentivo</a><a href="transparencia.html" data-page-link class="text-sm font-medium hover:text-ocean">Transparência</a><a href="contato.html" data-page-link class="text-sm font-medium hover:text-ocean">Contato</a></nav>
      <div class="hidden items-center gap-3 lg:flex"><a href="lei-incentivo.html" class="cta-lift rounded-full border border-ocean px-4 py-2 text-sm font-semibold text-ocean transition hover:bg-ocean hover:text-white">Seja Parceiro</a><a href="como-ajudar.html#doacao" class="cta-lift rounded-full bg-sun px-4 py-2 text-sm font-semibold text-oceanDeep transition hover:brightness-95">Doe Agora</a></div>
    </div>
    <div id="mobile-menu" class="hidden border-t border-slate-200 bg-white lg:hidden"><nav class="mx-auto flex max-w-7xl flex-col px-4 py-4" aria-label="Menu mobile"><a href="index.html" data-page-link class="py-2 text-sm font-medium">Início</a><a href="quem-somos.html" data-page-link class="py-2 text-sm font-medium">Quem Somos</a><a href="acoes.html" data-page-link class="py-2 text-sm font-medium">Nossas Ações</a><a href="acervo.html" data-page-link class="py-2 text-sm font-medium">Acervo</a><a href="como-ajudar.html" data-page-link class="py-2 text-sm font-medium">Como Ajudar</a><a href="lei-incentivo.html" data-page-link class="py-2 text-sm font-medium">Lei de Incentivo</a><a href="transparencia.html" data-page-link class="py-2 text-sm font-medium">Transparência</a><a href="contato.html" data-page-link class="py-2 text-sm font-medium">Contato</a></nav></div>
  </header>'''

FOOT = '''  <footer class="bg-slate-950 text-white"><div class="mx-auto max-w-7xl px-4 py-10 lg:px-8"><div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between"><p class="text-sm text-white/75">Instituto S.E.R. Sagi &bull; Praia do Sagi, Baía Formosa/RN</p><a href="contato.html" class="text-sm font-semibold text-sun">Fale com a equipe</a></div></div></footer>
  <script src="js/main.js"></script>
</body>
</html>
'''

BADGE = ('<span class="mt-3 inline-flex items-center gap-1.5 rounded-full bg-sand px-2.5 py-1 text-[10px] '
         'font-semibold uppercase tracking-[0.15em] text-slate-500" title="Conteúdo ilustrativo — será substituído por imagem real">'
         '<i class="fa-solid fa-wand-magic-sparkles text-[9px]"></i>Imagem ilustrativa</span>')

CTA = '''    <section class="bg-mist/70 py-16">
      <div class="mx-auto max-w-7xl px-4 lg:px-8">
        <div class="rounded-[2rem] bg-oceanDeep p-8 text-center text-white shadow-soft">
          <h2 class="text-3xl font-extrabold">Quer apoiar esta frente?</h2>
          <p class="mx-auto mt-4 max-w-2xl text-white/85">{texto}</p>
          <div class="mt-8 flex flex-wrap justify-center gap-4">
            <a href="como-ajudar.html" class="cta-lift rounded-full bg-sun px-6 py-3 font-semibold text-oceanDeep">Como ajudar</a>
            <a href="lei-incentivo.html" class="cta-lift rounded-full border border-white/40 px-6 py-3 font-semibold text-white">Lei de Incentivo</a>
            <a href="{voltar}" class="cta-lift rounded-full border border-white/40 px-6 py-3 font-semibold text-white">Voltar</a>
          </div>
        </div>
      </div>
    </section>
  </main>'''

MODALIDADES = [
    {"slug": "escola-jiu-jitsu", "titulo": "Jiu-Jitsu", "icone": "fa-medal",
     "img": "judo,martial,arts?lock=1101", "texto": "Disciplina, respeito e autocontrole dentro e fora do tatame."},
    {"slug": "volei", "titulo": "Vôlei", "icone": "fa-volleyball",
     "img": "volleyball,sport,beach?lock=1102", "texto": "Esporte coletivo que trabalha equipe, foco e coordenação."},
    {"slug": "futevolei", "titulo": "Futevôlei", "icone": "fa-futbol",
     "img": "football,beach,sand?lock=1103", "texto": "A modalidade da areia que une futebol e vôlei na praia do Sagi."},
    {"slug": "estudio-musculacao", "titulo": "Musculação", "icone": "fa-dumbbell",
     "img": "gym,fitness,weights?lock=1104", "texto": "Treino orientado para saúde, força e qualidade de vida."},
    {"slug": "natacao", "titulo": "Natação", "icone": "fa-person-swimming",
     "img": "swimming,pool,kids?lock=1105", "texto": "Segurança na água, resistência e desenvolvimento motor."},
    {"slug": "danca", "titulo": "Dança", "icone": "fa-music",
     "img": "dance,kids,music?lock=1106", "texto": "Expressão corporal, cultura e autoestima através do movimento."},
]

CONTEUDO = [
    {
        "slug": "volei", "titulo": "Vôlei", "icone": "fa-volleyball", "kicker": "Esporte",
        "img": "volleyball,sport,beach?lock=1102",
        "intro": "Esporte coletivo que trabalha equipe, foco e coordenação.",
        "desc": "As atividades de vôlei acontecem na arena e na praia do Sagi, reunindo crianças, jovens e adultos em torno do esporte coletivo. Além da parte física, a modalidade desenvolve cooperação, respeito às regras e espírito de equipe.",
        "oferece": ["Fundamentos e táticas", "Jogos e amistosos", "Integração entre as turmas", "Prática esportiva regular"],
        "voltar": "esporte.html", "voltar_txt": "Voltar para Esporte",
    },
    {
        "slug": "futevolei", "titulo": "Futevôlei", "icone": "fa-futbol", "kicker": "Esporte",
        "img": "football,beach,sand?lock=1103",
        "intro": "A modalidade da areia que une futebol e vôlei na praia do Sagi.",
        "desc": "Nascido nas areias, o futevôlei é uma das atividades mais queridas da comunidade. Trabalha controle de bola, reflexo e condicionamento, aproveitando a praia que é a nossa maior riqueza.",
        "oferece": ["Fundamentos do futevôlei", "Treinos na areia", "Jogos e integração", "Uso esportivo da praia"],
        "voltar": "esporte.html", "voltar_txt": "Voltar para Esporte",
    },
    {
        "slug": "natacao", "titulo": "Natação", "icone": "fa-person-swimming", "kicker": "Esporte",
        "img": "swimming,pool,kids?lock=1105",
        "intro": "Segurança na água, resistência e desenvolvimento motor.",
        "desc": "A natação é uma ferramenta de desenvolvimento completo: trabalha resistência, coordenação e, principalmente, a segurança das crianças em ambiente aquático — algo essencial numa comunidade de praia.",
        "oferece": ["Iniciação e aperfeiçoamento", "Segurança aquática", "Condicionamento físico", "Desenvolvimento motor"],
        "voltar": "esporte.html", "voltar_txt": "Voltar para Esporte",
    },
    {
        "slug": "danca", "titulo": "Dança", "icone": "fa-music", "kicker": "Esporte",
        "img": "dance,kids,music?lock=1106",
        "intro": "Expressão corporal, cultura e autoestima através do movimento.",
        "desc": "A dança une esporte, arte e cultura. Nas aulas, as crianças e jovens trabalham coordenação, ritmo e expressão corporal — ganhando confiança e descobrindo novas formas de se expressar.",
        "oferece": ["Ritmo e coordenação", "Expressão corporal", "Trabalho em grupo", "Apresentações e eventos"],
        "voltar": "esporte.html", "voltar_txt": "Voltar para Esporte",
    },
    {
        "slug": "educacao", "titulo": "Educação", "icone": "fa-book-open", "kicker": "Educação",
        "img": "education,kids,school?lock=1201",
        "intro": "Idiomas, informática e sustentabilidade para crianças e adolescentes.",
        "desc": "A educação é a porta de entrada para o futuro. O Instituto oferece aulas de idiomas, informática e sustentabilidade, ampliando as oportunidades de quem cresce no Sagi e preparando as crianças e jovens para novos caminhos.",
        "oferece": ["Aulas de idiomas", "Informática e tecnologia", "Educação para sustentabilidade", "Apoio ao desenvolvimento escolar"],
        "voltar": "index.html", "voltar_txt": "Voltar para o Início",
    },
    {
        "slug": "cultura", "titulo": "Cultura", "icone": "fa-masks-theater", "kicker": "Cultura",
        "img": "culture,music,community?lock=1301",
        "intro": "Origens indígenas, convivência comunitária e ações solidárias.",
        "desc": "A cultura do Sagi é viva e coletiva. O Instituto valoriza as origens indígenas da comunidade, promove encontros, música e ações solidárias que fortalecem os vínculos entre as famílias e mantêm a identidade do território.",
        "oferece": ["Valorização das origens indígenas", "Encontros comunitários", "Música e atividades culturais", "Ações solidárias"],
        "voltar": "index.html", "voltar_txt": "Voltar para o Início",
    },
]


def pagina_conteudo(p):
    oferece = "\n".join(
        f'                <li class="flex items-start gap-3"><i class="fa-solid fa-circle-check mt-1 text-ocean"></i><span>{i}</span></li>'
        for i in p["oferece"]
    )
    return f'''{HEAD.format(titulo=p["titulo"], descricao=p["intro"])}
  <main id="conteudo-principal">
    <section class="page-banner text-white">
      <div class="mx-auto max-w-7xl px-4 py-16 lg:px-8 lg:py-20">
        <p class="text-sm font-semibold uppercase tracking-[0.25em] text-sun">{p["kicker"]} &bull; Nossas Ações</p>
        <h2 class="mt-4 max-w-4xl text-4xl font-extrabold leading-tight sm:text-5xl">{p["titulo"]}</h2>
        <p class="mt-6 max-w-3xl text-lg text-white/85">{p["intro"]}</p>
      </div>
    </section>
    <section class="mx-auto max-w-7xl px-4 py-16 lg:px-8">
      <div class="grid gap-10 lg:grid-cols-[1.05fr_0.95fr] lg:items-start">
        <div class="premium-card rounded-[2rem] bg-white p-6 shadow-soft">
          <div class="relative -mx-1 overflow-hidden rounded-2xl">
            <img src="https://loremflickr.com/800/500/{p["img"]}" alt="Imagem ilustrativa — {p["titulo"]}" class="h-64 w-full object-cover" loading="lazy" />
          </div>
          {BADGE}
          <div class="mt-5 flex items-center gap-3">
            <div class="flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl bg-ocean/10 text-ocean"><i class="fa-solid {p["icone"]} text-2xl"></i></div>
            <h3 class="text-2xl font-bold text-oceanDeep">{p["titulo"]}</h3>
          </div>
          <p class="mt-5 text-base leading-8 text-slate-600">{p["desc"]}</p>
        </div>
        <div>
          <div class="rounded-2xl bg-white p-6 shadow-soft"><h3 class="font-bold text-oceanDeep">O que oferecemos</h3><ul class="mt-4 space-y-3 text-sm text-slate-700">
{oferece}
          </ul></div>
          <div class="mt-6 rounded-2xl bg-sand p-6 text-sm leading-7 text-slate-700">
            <p class="font-bold text-oceanDeep">{p["voltar_txt"]}</p>
            <p class="mt-2">Veja o conjunto completo de frentes de atuação do Instituto.</p>
            <a href="{p["voltar"]}" class="cta-lift mt-4 inline-flex items-center gap-2 rounded-full bg-ocean px-5 py-2.5 text-sm font-semibold text-white transition hover:brightness-95"><i class="fa-solid fa-arrow-left text-xs"></i>{p["voltar_txt"]}</a>
          </div>
        </div>
      </div>
    </section>
{CTA.format(texto="Empresas, voluntários e doadores podem contribuir para o fortalecimento desta atividade na comunidade do Sagi.", voltar="acoes.html")}
{FOOT}'''


def pagina_esporte():
    cards = []
    for m in MODALIDADES:
        cards.append(
            f'          <a href="{m["slug"]}.html" class="block h-full rounded-3xl bg-white p-6 shadow-soft transition hover:-translate-y-1 hover:shadow-[0_24px_80px_rgba(8,59,76,0.18)] hover:ring-2 hover:ring-ocean/30">\n'
            f'            <div class="relative -mx-1 overflow-hidden rounded-2xl"><img src="https://loremflickr.com/800/500/{m["img"]}" alt="Imagem ilustrativa — {m["titulo"]}" class="h-40 w-full object-cover" loading="lazy" /></div>\n'
            f'            {BADGE}\n'
            f'            <i class="fa-solid {m["icone"]} mt-3 block text-2xl text-ocean"></i>\n'
            f'            <h3 class="mt-4 text-xl font-bold text-oceanDeep">{m["titulo"]}</h3>\n'
            f'            <p class="mt-3 text-sm leading-7 text-slate-600">{m["texto"]}</p>\n'
            f'            <span class="mt-4 inline-flex items-center gap-1 text-sm font-semibold text-ocean">Saiba mais <i class="fa-solid fa-arrow-right text-xs"></i></span>\n'
            f'          </a>'
        )
    return f'''{HEAD.format(titulo="Esporte", descricao="Jiu-jitsu, vôlei, futevôlei, musculação, natação e dança para crianças, jovens e adultos da comunidade do Sagi.")}
  <main id="conteudo-principal">
    <section class="page-banner text-white">
      <div class="mx-auto max-w-7xl px-4 py-16 lg:px-8 lg:py-20">
        <p class="text-sm font-semibold uppercase tracking-[0.25em] text-sun">Esporte &bull; Nossas Ações</p>
        <h2 class="mt-4 max-w-4xl text-4xl font-extrabold leading-tight sm:text-5xl">Esporte</h2>
        <p class="mt-6 max-w-3xl text-lg text-white/85">O esporte é uma das principais portas de entrada do Instituto: disciplina, saúde, convivência e oportunidades para crianças, jovens e adultos da comunidade do Sagi.</p>
      </div>
    </section>
    <section class="mx-auto max-w-7xl px-4 py-16 lg:px-8">
      <div class="max-w-3xl">
        <p class="text-sm font-semibold uppercase tracking-[0.25em] text-ocean">Modalidades</p>
        <h3 class="section-title text-3xl font-extrabold text-oceanDeep">O que praticamos no Instituto</h3>
        <p class="mt-4 text-slate-600">Cada modalidade tem sua própria página com mais detalhes. Toque em uma para saber mais.</p>
      </div>
      <div class="mt-10 grid gap-6 md:grid-cols-2 xl:grid-cols-3">
{chr(10).join(cards)}
      </div>
    </section>
{CTA.format(texto="Empresas, voluntários e doadores podem contribuir para o fortalecimento do esporte na comunidade do Sagi.", voltar="acoes.html")}
{FOOT}'''


def main():
    feitos = []
    p = os.path.join(BASE, "esporte.html")
    open(p, "w", encoding="utf-8", newline="\n").write(pagina_esporte())
    feitos.append("esporte.html (hub com 6 modalidades)")

    for item in CONTEUDO:
        p = os.path.join(BASE, f'{item["slug"]}.html')
        open(p, "w", encoding="utf-8", newline="\n").write(pagina_conteudo(item))
        feitos.append(f'{item["slug"]}.html')

    for f in feitos:
        print("  criado:", f)


if __name__ == "__main__":
    main()
