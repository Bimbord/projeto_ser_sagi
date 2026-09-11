# -*- coding: utf-8 -*-
"""
Reconstrói a parte das AÇÕES (perdida com o drive D:):
1) torna os 6 cards de acoes.html clicáveis (link + "Saiba mais")
2) gera as 6 páginas individuais de cada ação
"""
import os

BASE = r"C:/Projetos Code/Projeto SER Sagi/projeto_SER_Sagi - Hermes"

ACOES = [
    {
        "slug": "consultorio-odontologico", "titulo": "Consultório Odontológico",
        "icone": "fa-tooth", "img": "dentist,clinic,tooth?lock=101",
        "kicker": "Saúde", "curto": "Saúde bucal",
        "intro": "Cuidado com a saúde bucal da comunidade: prevenção, tratamento e autoestima.",
        "desc": "O consultório odontológico atende crianças, jovens e adultos da comunidade do Sagi. Com foco em prevenção e acolhimento, devolve o sorriso e o bem-estar de quem antes não tinha acesso a atendimento.",
        "stats": [("194", "pacientes atendidos"), ("1.149", "procedimentos realizados")],
        "oferece": ["Limpeza e prevenção", "Tratamento de canal", "Próteses", "Orientações de higiene bucal"],
        "frase": "Cuidar do sorriso é cuidar das pessoas!",
    },
    {
        "slug": "estudio-musculacao", "titulo": "Estúdio de Musculação",
        "icone": "fa-dumbbell", "img": "gym,fitness,weights?lock=202",
        "kicker": "Saúde e bem-estar", "curto": "Atividade física",
        "intro": "Saúde, bem-estar e qualidade de vida por meio da prática regular de atividades físicas.",
        "desc": "O estúdio de musculação oferece um espaço adequado para moradores e residentes do Sagi praticarem atividade física com segurança, promovendo saúde e qualidade de vida para todas as idades.",
        "stats": [("118", "inscritos"), ("89", "moradores"), ("29", "residentes")],
        "oferece": ["Equipamentos para treino", "Acompanhamento e orientação", "Espaço acessível à comunidade", "Promoção de hábitos saudáveis"],
        "frase": "",
    },
    {
        "slug": "escola-jiu-jitsu", "titulo": "Escola de Jiu-Jitsu",
        "icone": "fa-medal", "img": "judo,martial,arts?lock=303",
        "kicker": "Esporte e disciplina", "curto": "Arte suave",
        "intro": "A arte suave: espírito de equipe, disciplina, respeito, saúde e inclusão social.",
        "desc": "O jiu-jitsu é uma ferramenta de transformação. As aulas trabalham corpo e mente, ensinando disciplina, respeito e autocontrole — valores que acompanham as crianças dentro e fora do tatame.",
        "stats": [("49", "alunos")],
        "oferece": ["Disciplina e respeito", "Autocontrole e autoestima", "Convivência em grupo", "Hábitos saudáveis"],
        "frase": "",
    },
    {
        "slug": "arena-futevolei-volei", "titulo": "Arena de Futevôlei e Vôlei",
        "icone": "fa-volleyball", "img": "beach,volleyball?lock=404",
        "kicker": "Esporte e lazer", "curto": "Arena viva",
        "intro": "Espaço vivo o ano todo para esporte, cultura e encontro comunitário.",
        "desc": "A arena é o coração pulsante da comunidade: recebe práticas esportivas, comemorações, confraternizações e eventos musicais. Um ponto de encontro para lazer, integração e cultura.",
        "stats": [],
        "oferece": ["Futevôlei e vôlei", "Eventos musicais e culturais", "Comemorações e confraternizações", "Ponto de encontro da comunidade"],
        "frase": "",
    },
    {
        "slug": "acoes-solidarias", "titulo": "Ações Solidárias",
        "icone": "fa-hand-holding-heart", "img": "children,kids,party?lock=505",
        "kicker": "Acolhimento", "curto": "Cuidado e carinho",
        "intro": "Cuidado e acolhimento de crianças e adolescentes em momentos especiais.",
        "desc": "As ações solidárias promovem cuidado e acolhimento: comemorações de aniversário, momentos de convivência e atividades comunitárias que fortalecem os vínculos entre as famílias e o Instituto.",
        "stats": [],
        "oferece": ["Comemorações de aniversário", "Momentos de convivência", "Atividades comunitárias", "Acolhimento de crianças e adolescentes"],
        "frase": "",
    },
    {
        "slug": "preservacao-ambiental", "titulo": "Preservação Ambiental",
        "icone": "fa-turtle", "img": "sea,turtle?lock=606",
        "kicker": "Meio ambiente", "curto": "Origens e natureza",
        "intro": "Valorização das origens indígenas e proteção das tartarugas marinhas.",
        "desc": "O Instituto valoriza as origens indígenas da comunidade e protege as tartarugas marinhas que desovam na praia do Sagi, com educação ambiental e cuidado com os ecossistemas.",
        "stats": [],
        "oferece": ["Proteção das tartarugas marinhas", "Educação ambiental", "Valorização das origens indígenas", "Cuidado com os ecossistemas"],
        "frase": "",
    },
]

SLUGS = [a["slug"] + ".html" for a in ACOES]

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


def pagina_acao(a):
    stats = ""
    if a["stats"]:
        cards = "\n".join(
            f'            <div class="rounded-2xl bg-white p-5 shadow-soft"><p class="text-3xl font-extrabold text-oceanDeep">{n}</p><p class="mt-1 text-sm text-slate-600">{l}</p></div>'
            for n, l in a["stats"]
        )
        stats = f'          <div class="grid gap-4 sm:grid-cols-2">\n{cards}\n          </div>\n'

    oferece = "\n".join(
        f'              <li class="flex items-start gap-2"><i class="fa-solid fa-circle-check mt-1 text-ocean"></i><span>{i}</span></li>'
        for i in a["oferece"]
    )

    frase = ""
    if a["frase"]:
        frase = f'          <blockquote class="mt-6 rounded-2xl bg-mist p-5 font-semibold text-oceanDeep"><i class="fa-solid fa-quote-left mr-2 text-ocean"></i>{a["frase"]}</blockquote>\n'

    return f'''{HEAD.format(titulo=a["titulo"], descricao=a["intro"])}
  <main id="conteudo-principal">
    <section class="page-banner text-white">
      <div class="mx-auto max-w-7xl px-4 py-16 lg:px-8 lg:py-20">
        <p class="text-sm font-semibold uppercase tracking-[0.25em] text-sun">Nossas Ações &bull; {a["kicker"]}</p>
        <h2 class="mt-4 max-w-4xl text-4xl font-extrabold leading-tight sm:text-5xl">{a["titulo"]}</h2>
        <p class="mt-6 max-w-3xl text-lg text-white/85">{a["intro"]}</p>
      </div>
    </section>
    <section class="mx-auto max-w-7xl px-4 py-16 lg:px-8">
      <div class="grid gap-10 lg:grid-cols-[1.05fr_0.95fr] lg:items-start">
        <div class="rounded-[2rem] bg-white p-6 shadow-soft">
          <div class="relative overflow-hidden rounded-2xl"><img src="https://loremflickr.com/800/500/{a["img"]}" alt="Imagem ilustrativa — {a["titulo"]}" class="h-64 w-full object-cover" loading="lazy" /></div>
          <span class="mt-3 inline-flex items-center gap-1.5 rounded-full bg-sand px-2.5 py-1 text-[10px] font-semibold uppercase tracking-[0.15em] text-slate-500" title="Conteúdo ilustrativo — será substituído por imagem real"><i class="fa-solid fa-wand-magic-sparkles text-[9px]"></i>Imagem ilustrativa</span>
          <div class="mt-5 flex items-center gap-3">
            <div class="flex h-12 w-12 items-center justify-center rounded-2xl bg-ocean/10 text-ocean"><i class="fa-solid {a["icone"]} text-2xl"></i></div>
            <h3 class="text-2xl font-bold text-oceanDeep">{a["titulo"]}</h3>
          </div>
          <p class="mt-5 text-base leading-8 text-slate-600">{a["desc"]}</p>
{frase}        </div>
        <div class="space-y-6">
{stats}          <div class="rounded-2xl bg-white p-6 shadow-soft">
            <h3 class="font-bold text-oceanDeep">O que esta ação oferece</h3>
            <ul class="mt-4 space-y-3 text-sm text-slate-700">
{oferece}
            </ul>
          </div>
          <a href="acoes.html" class="flex items-center justify-between rounded-2xl bg-white p-5 shadow-soft transition hover:-translate-y-0.5"><span class="font-semibold text-oceanDeep"><i class="fa-solid fa-arrow-left mr-2 text-ocean"></i>Voltar para Nossas Ações</span><i class="fa-solid fa-list-check text-ocean"></i></a>
        </div>
      </div>
    </section>
    <section class="bg-mist/70 py-16">
      <div class="mx-auto max-w-7xl px-4 lg:px-8">
        <div class="rounded-[2rem] bg-oceanDeep p-8 text-center text-white shadow-soft">
          <h2 class="text-3xl font-extrabold">Quer apoiar esta ação?</h2>
          <p class="mx-auto mt-4 max-w-2xl text-white/85">Empresas, voluntários e doadores podem contribuir para o fortalecimento do {a["titulo"]} na comunidade do Sagi.</p>
          <div class="mt-8 flex flex-wrap justify-center gap-4">
            <a href="como-ajudar.html" class="cta-lift rounded-full bg-sun px-6 py-3 font-semibold text-oceanDeep">Como ajudar</a>
            <a href="lei-incentivo.html" class="cta-lift rounded-full border border-white/40 px-6 py-3 font-semibold text-white">Lei de Incentivo</a>
            <a href="acoes.html" class="cta-lift rounded-full border border-white/40 px-6 py-3 font-semibold text-white">Ver todas as ações</a>
          </div>
        </div>
      </div>
    </section>
  </main>
{FOOT}'''


def main():
    acoes_html = os.path.join(BASE, "acoes.html")
    html = open(acoes_html, encoding="utf-8").read()

    aberto = '<article class="rounded-3xl bg-white p-6 shadow-soft">'
    saida, pos, feitos = [], 0, 0
    for a in ACOES:
        i = html.find(aberto, pos)
        if i == -1:
            print("  ⚠️  card nao encontrado para", a["slug"])
            break
        j = html.find("</article>", i)
        saida.append(html[pos:i])
        saida.append(
            f'<a href="{a["slug"]}.html" class="block h-full rounded-3xl bg-white p-6 shadow-soft transition hover:-translate-y-1 hover:shadow-[0_24px_80px_rgba(8,59,76,0.18)] hover:ring-2 hover:ring-ocean/30">'
        )
        saida.append(html[i + len(aberto):j])
        saida.append(
            f'<span class="mt-4 inline-flex items-center gap-1 text-sm font-semibold text-ocean">Saiba mais <i class="fa-solid fa-arrow-right text-xs"></i></span>\n        </a>'
        )
        pos = j + len("</article>")
        feitos += 1
    saida.append(html[pos:])
    open(acoes_html, "w", encoding="utf-8", newline="\n").write("".join(saida))
    print(f"[1] acoes.html: {feitos} card(s) transformados em link")

    for a in ACOES:
        p = os.path.join(BASE, f'{a["slug"]}.html')
        open(p, "w", encoding="utf-8", newline="\n").write(pagina_acao(a))
        print(f'[2] criado: {a["slug"]}.html')


if __name__ == "__main__":
    main()
