# -*- coding: utf-8 -*-
"""
Reconstrói a parte do ACERVO (perdida com o drive D:):
1) arquivo.html -> acervo.html (título, menu, banner, cards estáticos clicáveis)
2) atualiza referências 'arquivo.html' -> 'acervo.html' em todos os arquivos
3) gera as 6 páginas de categoria (acervo-esporte.html etc.)
"""
import os, re

BASE = r"C:/Projetos Code/Projeto SER Sagi/projeto_SER_Sagi - Hermes"

CATS = [
    {
        "slug": "acervo-esporte", "nome": "Esporte", "icone": "fa-futbol",
        "img": "sport,soccer,training?lock=741", "kicker": "Esporte",
        "intro": "Registros das atividades esportivas: jiu-jitsu, futevôlei, vôlei, musculação e natação.",
        "desc": "Momentos de disciplina, saúde e convivência nas atividades esportivas do Instituto. Cada imagem é um registro da transformação que o esporte traz para as crianças e adolescentes do Sagi.",
        "galeria": ["sport,soccer,training?lock=801", "judo,martial,arts?lock=802", "beach,volleyball?lock=803", "gym,fitness,weights?lock=804", "swimming,pool,kids?lock=805", "running,athletics,track?lock=806"],
    },
    {
        "slug": "acervo-saude", "nome": "Saúde", "icone": "fa-heart-pulse",
        "img": "dentist,health,clinic?lock=742", "kicker": "Saúde",
        "intro": "Atendimentos no consultório odontológico e ações de bem-estar na comunidade.",
        "desc": "O cuidado com a saúde começa pelo sorriso. Registros dos atendimentos odontológicos e das ações de bem-estar que atendem crianças, jovens e adultos da comunidade.",
        "galeria": ["dentist,clinic,tooth?lock=811", "doctor,health,checkup?lock=812", "healthcare,nurse,care?lock=813", "smile,teeth,dental?lock=814", "wellness,healthy,lifestyle?lock=815", "hospital,medicine,clinic?lock=816"],
    },
    {
        "slug": "acervo-educacao", "nome": "Educação", "icone": "fa-book-open",
        "img": "education,kids,school?lock=743", "kicker": "Educação",
        "intro": "Aulas de idiomas, informática e sustentabilidade para crianças e adolescentes.",
        "desc": "Educação como porta de entrada para o futuro. Registros das aulas de idiomas, informática e sustentabilidade que ampliam as oportunidades dos nossos alunos.",
        "galeria": ["education,kids,school?lock=821", "classroom,teacher,learning?lock=822", "computer,technology,kids?lock=823", "books,reading,library?lock=824", "language,english,spanish?lock=825", "sustainability,recycling,kids?lock=826"],
    },
    {
        "slug": "acervo-cultura", "nome": "Cultura", "icone": "fa-masks-theater",
        "img": "culture,music,community?lock=744", "kicker": "Cultura",
        "intro": "Origens indígenas, convivência comunitária e ações solidárias.",
        "desc": "A cultura do Sagi é viva: valorização das origens indígenas, encontros comunitários, música e ações solidárias que fortalecem os laços entre as famílias.",
        "galeria": ["culture,music,community?lock=831", "indigenous,tradition,brazil?lock=832", "festival,celebration,dance?lock=833", "art,craft,creative?lock=834", "music,concert,band?lock=835", "community,gathering,people?lock=836"],
    },
    {
        "slug": "acervo-preservacao", "nome": "Preservação", "icone": "fa-leaf",
        "img": "turtle,nature,sea?lock=745", "kicker": "Preservação",
        "intro": "Proteção das tartarugas marinhas e educação socioambiental.",
        "desc": "O Instituto protege as tartarugas marinhas que desovam na praia do Sagi e promove educação ambiental, cuidando do ecossistema que sustenta a comunidade.",
        "galeria": ["turtle,nature,sea?lock=841", "beach,ocean,coast?lock=842", "environment,recycling,green?lock=843", "turtle,hatchling,baby?lock=844", "ocean,waves,nature?lock=845", "mangrove,coast,ecosystem?lock=846"],
    },
    {
        "slug": "acervo-eventos", "nome": "Eventos", "icone": "fa-calendar-days",
        "img": "party,event,celebration?lock=746", "kicker": "Eventos",
        "intro": "Comemorações, confraternizações e eventos musicais da comunidade.",
        "desc": "Os eventos são o momento em que a comunidade se encontra: comemorações de aniversário, confraternizações, festas e apresentações musicais na arena.",
        "galeria": ["party,event,celebration?lock=851", "birthday,kids,party?lock=852", "concert,music,event?lock=853", "community,event,gathering?lock=854", "festival,food,fun?lock=855", "celebration,confetti,party?lock=856"],
    },
]

BADGE = ('<span class="mt-3 inline-flex items-center gap-1.5 rounded-full bg-sand px-2.5 py-1 '
         'text-[10px] font-semibold uppercase tracking-[0.15em] text-slate-500" '
         'title="Conteúdo ilustrativo — será substituído por imagem real">'
         '<i class="fa-solid fa-wand-magic-sparkles text-[9px]"></i>Imagem ilustrativa</span>')

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


def card_categoria(c):
    return (
        f'<a href="{c["slug"]}.html" class="block h-full rounded-3xl bg-white p-6 shadow-soft transition hover:-translate-y-1 hover:shadow-[0_24px_80px_rgba(8,59,76,0.18)] hover:ring-2 hover:ring-ocean/30">\n'
        f'            <div class="relative -mx-1 overflow-hidden rounded-2xl"><img src="https://loremflickr.com/800/500/{c["img"]}" alt="Imagem ilustrativa de {c["nome"]}" class="h-40 w-full object-cover" loading="lazy" /></div>\n'
        f'            {BADGE}\n'
        f'            <i class="fa-solid {c["icone"]} mt-3 block text-2xl text-ocean"></i>\n'
        f'            <h3 class="mt-4 text-xl font-bold text-oceanDeep">{c["kicker"]}</h3>\n'
        f'            <p class="mt-3 text-sm leading-7 text-slate-600">{c["intro"]}</p>\n'
        f'            <span class="mt-4 inline-flex items-center gap-1 text-sm font-semibold text-ocean">Ver galeria <i class="fa-solid fa-arrow-right text-xs"></i></span>\n'
        f'          </a>'
    )


def pagina_categoria(c):
    galeria_html = "\n".join(
        f'          <figure class="overflow-hidden rounded-3xl bg-white p-4 shadow-soft">\n'
        f'            <div class="relative overflow-hidden rounded-2xl"><img src="https://loremflickr.com/800/500/{g}" alt="Imagem ilustrativa — {c["nome"]}" class="h-48 w-full object-cover" loading="lazy" /></div>\n'
        f'            <figcaption class="flex items-center justify-between gap-2 p-2 pt-3"><span class="text-xs font-semibold uppercase tracking-wide text-ocean">{c["nome"]}</span>'
        f'<span class="inline-flex items-center gap-1 rounded-full bg-sand px-2 py-0.5 text-[9px] font-semibold uppercase tracking-wide text-slate-500"><i class="fa-solid fa-wand-magic-sparkles text-[8px]"></i>Ilustrativo</span></figcaption>\n'
        f'          </figure>'
        for g in c["galeria"]
    )
    return f'''{HEAD.format(titulo=c["nome"], descricao=c["intro"])}
  <main id="conteudo-principal">
    <section class="page-banner text-white">
      <div class="mx-auto max-w-7xl px-4 py-16 lg:px-8 lg:py-20">
        <p class="text-sm font-semibold uppercase tracking-[0.25em] text-sun">Acervo &bull; {c["nome"]}</p>
        <h2 class="mt-4 max-w-4xl text-4xl font-extrabold leading-tight sm:text-5xl">{c["kicker"]}</h2>
        <p class="mt-6 max-w-3xl text-lg text-white/85">{c["intro"]}</p>
      </div>
    </section>
    <section class="mx-auto max-w-7xl px-4 py-16 lg:px-8">
      <div class="grid gap-10 lg:grid-cols-[1.05fr_0.95fr] lg:items-start">
        <div>
          <div class="relative overflow-hidden rounded-[2rem]"><img src="https://loremflickr.com/800/500/{c["img"]}" alt="Imagem ilustrativa de {c["nome"]}" class="h-72 w-full object-cover" loading="lazy" /></div>
          {BADGE}
          <div class="mt-5 flex items-center gap-3">
            <div class="flex h-12 w-12 items-center justify-center rounded-2xl bg-ocean/10 text-ocean"><i class="fa-solid {c["icone"]} text-2xl"></i></div>
            <h3 class="text-2xl font-bold text-oceanDeep">{c["kicker"]}</h3>
          </div>
          <p class="mt-5 text-base leading-8 text-slate-600">{c["desc"]}</p>
        </div>
        <div class="space-y-6">
          <div class="rounded-[2rem] border border-dashed border-slate-300 bg-white p-6 shadow-soft">
            <div class="flex h-12 w-12 items-center justify-center rounded-2xl bg-mist text-ocean"><i class="fa-solid fa-camera-retro text-xl"></i></div>
            <h3 class="mt-4 text-lg font-bold text-oceanDeep">Fotos reais em breve</h3>
            <p class="mt-2 text-sm leading-7 text-slate-600">Esta categoria vai receber as fotos e vídeos reais das atividades. Enquanto isso, as imagens acima são ilustrativas e serão substituídas pelos registros oficiais.</p>
            <p class="mt-3 text-sm leading-7 text-slate-600">Acompanhe no Instagram <a href="https://instagram.com/s.e.r_sagi" target="_blank" rel="noopener" class="font-semibold text-ocean underline">@s.e.r_sagi</a>.</p>
          </div>
          <a href="acervo.html" class="flex items-center justify-between rounded-2xl bg-white p-5 shadow-soft transition hover:-translate-y-0.5"><span class="font-semibold text-oceanDeep"><i class="fa-solid fa-arrow-left mr-2 text-ocean"></i>Voltar para o Acervo</span><i class="fa-solid fa-images text-ocean"></i></a>
          <div class="rounded-[2rem] bg-oceanDeep p-6 text-white shadow-soft">
            <h3 class="text-lg font-bold">Tem registros desta categoria?</h3>
            <p class="mt-2 text-sm leading-7 text-white/85">Envie suas fotos e vídeos (com autorização de uso de imagem) para entrarem no acervo oficial.</p>
            <a href="contato.html" class="cta-lift mt-5 inline-flex rounded-full bg-sun px-5 py-2.5 text-sm font-semibold text-oceanDeep">Enviar registros</a>
          </div>
        </div>
      </div>
      <div class="mt-14">
        <h3 class="section-title text-2xl font-extrabold text-oceanDeep">Galeria ilustrativa</h3>
        <p class="mt-2 text-slate-600">Imagens de referência da categoria <strong>{c["kicker"]}</strong>.</p>
        <div class="mt-8 grid gap-6 md:grid-cols-2 xl:grid-cols-3">
{galeria_html}
        </div>
      </div>
    </section>
    <section class="bg-mist/70 py-16">
      <div class="mx-auto max-w-7xl px-4 lg:px-8">
        <div class="rounded-[2rem] bg-white p-8 text-center shadow-soft">
          <h2 class="text-3xl font-extrabold text-oceanDeep">Apoie esta frente do Instituto</h2>
          <p class="mx-auto mt-4 max-w-2xl text-slate-600">O acervo conta a história da transformação. Apoiar o Instituto é garantir que ela continue.</p>
          <div class="mt-8 flex flex-wrap justify-center gap-4">
            <a href="como-ajudar.html" class="cta-lift rounded-full bg-ocean px-6 py-3 font-semibold text-white">Como ajudar</a>
            <a href="lei-incentivo.html" class="cta-lift rounded-full border border-ocean px-6 py-3 font-semibold text-ocean">Lei de Incentivo</a>
            <a href="acervo.html" class="cta-lift rounded-full border border-slate-300 px-6 py-3 font-semibold text-slate-600">Ver todas as categorias</a>
          </div>
        </div>
      </div>
    </section>
  </main>
{FOOT}'''


def main():
    src = os.path.join(BASE, "arquivo.html")
    dst = os.path.join(BASE, "acervo.html")
    html = open(src, encoding="utf-8").read()

    html = html.replace("<title>Arquivo | Instituto S.E.R. Sagi</title>", "<title>Acervo | Instituto S.E.R. Sagi</title>")
    html = html.replace('href="arquivo.html"', 'href="acervo.html"')
    html = html.replace(">Arquivo</a>", ">Acervo</a>")
    html = html.replace(">Arquivo<", ">Acervo<")

    novo_container = (
        '<div data-render="archive" class="mt-10">\n'
        '        <div class="mb-8 flex flex-col items-center justify-center rounded-3xl border border-dashed border-slate-300 bg-white px-8 py-8 text-center shadow-soft">\n'
        '          <div class="flex h-14 w-14 items-center justify-center rounded-2xl bg-mist text-ocean"><i class="fa-solid fa-photo-film text-xl"></i></div>\n'
        '          <h3 class="mt-4 text-lg font-bold text-oceanDeep">Nosso acervo está sendo organizado</h3>\n'
        '          <p class="mt-2 max-w-xl text-sm leading-7 text-slate-600">As imagens abaixo são ilustrativas. As fotos e vídeos reais das nossas atividades serão publicados aqui em breve. Acompanhe no Instagram <a href="https://instagram.com/s.e.r_sagi" target="_blank" rel="noopener" class="font-semibold text-ocean underline">@s.e.r_sagi</a>.</p>\n'
        '        </div>\n'
        '        <div class="grid gap-6 md:grid-cols-2 xl:grid-cols-3">\n'
        '          ' + "\n          ".join(card_categoria(c) for c in CATS) + '\n'
        '        </div>\n'
        '      </div>'
    )

    ini = html.find('<div data-render="archive"')
    if ini == -1:
        raise SystemExit("ERRO: container do acervo nao encontrado")
    fim = html.find('</section>', ini)
    html = html[:ini] + novo_container + "\n    " + html[fim:]

    open(dst, "w", encoding="utf-8", newline="\n").write(html)
    os.remove(src)
    print("[1] arquivo.html -> acervo.html  OK")

    alterados = []
    for raiz, _, arquivos in os.walk(BASE):
        if any(x in raiz for x in (".git", "node_modules", "scripts", "docs", "plans")):
            continue
        for nome in arquivos:
            if not nome.endswith((".html", ".js")):
                continue
            p = os.path.join(raiz, nome)
            try:
                t = open(p, encoding="utf-8").read()
            except Exception:
                continue
            o = t
            t = t.replace('href="arquivo.html"', 'href="acervo.html"')
            t = t.replace('"arquivo.html"', '"acervo.html"')
            t = t.replace(">Arquivo</a>", ">Acervo</a>")
            t = t.replace(">Arquivo<", ">Acervo<")
            if t != o:
                open(p, "w", encoding="utf-8", newline="\n").write(t)
                alterados.append(nome)
    print(f"[2] referencias atualizadas: {', '.join(alterados) if alterados else 'nenhum'}")

    for c in CATS:
        p = os.path.join(BASE, f'{c["slug"]}.html')
        open(p, "w", encoding="utf-8", newline="\n").write(pagina_categoria(c))
        print(f'[3] criado: {c["slug"]}.html')


if __name__ == "__main__":
    main()
