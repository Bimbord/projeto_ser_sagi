# -*- coding: utf-8 -*-
"""Gera as 6 páginas individuais das ações + torna os cards de acoes.html clicáveis."""
import os

BASE = r"D:/BBDPRINT - BACKUP/BBDPRINT/App BBDPRiNT/PROJETOS/Projetos Code/Projeto SER Sagi/projeto_SER_Sagi - Hermes"

# ---------------------------------------------------------------------------
# Cabeçalho e rodapé padrão (mesmo padrão visual das páginas existentes)
# ---------------------------------------------------------------------------
HEADER = '''  <header class="sticky top-0 z-50 border-b border-slate-200/70 bg-white/90 backdrop-blur">
    <div class="mx-auto flex max-w-7xl items-center justify-between px-4 py-4 lg:px-8">
      <a href="index.html" class="flex items-center" aria-label="Instituto S.E.R. Sagi - página inicial">
        <img src="img/logo.png" alt="Instituto S.E.R. Sagi" class="h-16 w-auto object-contain">
      </a>
      <button id="menu-toggle" class="inline-flex items-center rounded-lg border border-slate-300 px-3 py-2 text-ocean lg:hidden" aria-expanded="false" aria-controls="mobile-menu" aria-label="Abrir menu"><i class="fa-solid fa-bars"></i></button>
      <nav class="hidden items-center gap-6 lg:flex" aria-label="Menu principal"><a href="index.html" data-page-link class="text-sm font-medium hover:text-ocean">Início</a><a href="quem-somos.html" data-page-link class="text-sm font-medium hover:text-ocean">Quem Somos</a><a href="acoes.html" data-page-link class="text-sm font-medium hover:text-ocean">Nossas Ações</a><a href="acervo.html" data-page-link class="text-sm font-medium hover:text-ocean">Acervo</a><a href="como-ajudar.html" data-page-link class="text-sm font-medium hover:text-ocean">Como Ajudar</a><a href="lei-incentivo.html" data-page-link class="text-sm font-medium hover:text-ocean">Lei de Incentivo</a><a href="transparencia.html" data-page-link class="text-sm font-medium hover:text-ocean">Transparência</a><a href="contato.html" data-page-link class="text-sm font-medium hover:text-ocean">Contato</a></nav>
      <div class="hidden items-center gap-3 lg:flex"><a href="lei-incentivo.html" class="cta-lift rounded-full border border-ocean px-4 py-2 text-sm font-semibold text-ocean transition hover:bg-ocean hover:text-white">Seja Parceiro</a><a href="como-ajudar.html#doacao" class="cta-lift rounded-full bg-sun px-4 py-2 text-sm font-semibold text-oceanDeep transition hover:brightness-95">Doe Agora</a></div>
    </div>
    <div id="mobile-menu" class="hidden border-t border-slate-200 bg-white lg:hidden"><nav class="mx-auto flex max-w-7xl flex-col px-4 py-4" aria-label="Menu mobile"><a href="index.html" data-page-link class="py-2 text-sm font-medium">Início</a><a href="quem-somos.html" data-page-link class="py-2 text-sm font-medium">Quem Somos</a><a href="acoes.html" data-page-link class="py-2 text-sm font-medium">Nossas Ações</a><a href="acervo.html" data-page-link class="py-2 text-sm font-medium">Acervo</a><a href="como-ajudar.html" data-page-link class="py-2 text-sm font-medium">Como Ajudar</a><a href="lei-incentivo.html" data-page-link class="py-2 text-sm font-medium">Lei de Incentivo</a><a href="transparencia.html" data-page-link class="py-2 text-sm font-medium">Transparência</a><a href="contato.html" data-page-link class="py-2 text-sm font-medium">Contato</a></nav></div>
  </header>'''

FOOTER = '''  <footer class="bg-slate-950 text-white"><div class="mx-auto max-w-7xl px-4 py-10 lg:px-8"><div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between"><p class="text-sm text-white/75">Instituto S.E.R. Sagi • Praia do Sagi, Baía Formosa/RN</p><a href="contato.html" class="text-sm font-semibold text-sun">Fale com a equipe</a></div></div></footer>'''

# ---------------------------------------------------------------------------
# Dados das 6 ações
# ---------------------------------------------------------------------------
ACOES = [
    {
        "slug": "consultorio-odontologico",
        "titulo": "Consultório Odontológico",
        "kicker": "Saúde",
        "icone": "fa-tooth",
        "img": "dentist,clinic,tooth?lock=101",
        "intro": "Cuidado com a saúde bucal da comunidade: prevenção, tratamento e autoestima.",
        "descricao": "O consultório odontológico atende crianças, jovens e adultos da comunidade do Sagi. Com foco em prevenção e acolhimento, devolve o sorriso e o bem-estar de quem antes não tinha acesso a atendimento odontológico.",
        "stats": [("194", "pacientes atendidos"), ("1.149", "procedimentos realizados")],
        "oferece": ["Limpeza e prevenção", "Tratamento de canal", "Próteses dentárias", "Orientações de higiene bucal"],
        "frase": "Cuidar do sorriso é cuidar das pessoas!",
    },
    {
        "slug": "estudio-musculacao",
        "titulo": "Estúdio de Musculação",
        "kicker": "Saúde e bem-estar",
        "icone": "fa-dumbbell",
        "img": "gym,fitness,weights?lock=202",
        "intro": "Saúde, bem-estar e qualidade de vida por meio da prática regular de atividades físicas.",
        "descricao": "O estúdio de musculação oferece um espaço adequado para moradores e residentes do Sagi praticarem atividade física com segurança, promovendo saúde e qualidade de vida para todas as idades.",
        "stats": [("118", "inscritos"), ("89", "moradores"), ("29", "residentes")],
        "oferece": ["Equipamentos para treino", "Acompanhamento e orientação", "Espaço acessível à comunidade", "Promoção de hábitos saudáveis"],
        "frase": "",
    },
    {
        "slug": "escola-jiu-jitsu",
        "titulo": "Escola de Jiu-Jitsu",
        "kicker": "Esporte e disciplina",
        "icone": "fa-medal",
        "img": "judo,martial,arts?lock=303",
        "intro": "A arte suave: espírito de equipe, disciplina, respeito, saúde e inclusão social.",
        "descricao": "O jiu-jitsu é uma ferramenta de transformação. As aulas trabalham corpo e mente, ensinando disciplina, respeito e autocontrole — valores que acompanham as crianças dentro e fora do tatame.",
        "stats": [("49", "alunos atendidos")],
        "oferece": ["Disciplina e respeito", "Autocontrole e autoestima", "Convivência em grupo", "Hábitos saudáveis"],
        "frase": "",
    },
    {
        "slug": "arena-futevolei-volei",
        "titulo": "Arena de Futevôlei e Vôlei",
        "kicker": "Esporte e lazer",
        "icone": "fa-volleyball",
        "img": "beach,volleyball?lock=404",
        "intro": "Espaço vivo o ano todo para esporte, cultura e encontro comunitário.",
        "descricao": "A arena é o coração pulsante da comunidade: recebe práticas esportivas, comemorações, confraternizações e eventos musicais. Um ponto de encontro para lazer, integração e cultura.",
        "stats": [],
        "oferece": ["Futevôlei e vôlei", "Eventos musicais e culturais", "Comemorações e confraternizações", "Ponto de encontro da comunidade"],
        "frase": "",
    },
    {
        "slug": "acoes-solidarias",
        "titulo": "Ações Solidárias",
        "kicker": "Acolhimento",
        "icone": "fa-hand-holding-heart",
        "img": "children,kids,party?lock=505",
        "intro": "Cuidado e acolhimento de crianças e adolescentes em momentos especiais.",
        "descricao": "As ações solidárias promovem cuidado e acolhimento: comemorações de aniversário, momentos de convivência e atividades comunitárias que fortalecem os vínculos entre as famílias e o Instituto.",
        "stats": [],
        "oferece": ["Comemorações de aniversário", "Momentos de convivência", "Atividades comunitárias", "Acolhimento de crianças e adolescentes"],
        "frase": "",
    },
    {
        "slug": "preservacao-ambiental",
        "titulo": "Preservação Ambiental",
        "kicker": "Meio ambiente",
        "icone": "fa-turtle",
        "img": "sea,turtle?lock=606",
        "intro": "Valorização das origens indígenas e proteção das tartarugas marinhas.",
        "descricao": "O Instituto valoriza as origens indígenas da comunidade e protege as tartarugas marinhas que desovam na praia do Sagi, com educação ambiental e cuidado com os ecossistemas.",
        "stats": [],
        "oferece": ["Proteção das tartarugas marinhas", "Educação ambiental", "Valorização das origens indígenas", "Cuidado com os ecossistemas"],
        "frase": "",
    },
]


def build_stats(stats):
    if not stats:
        return ""
    cards = "".join(
        f'<div class="rounded-2xl bg-white p-5 shadow-soft"><p class="stat-number text-3xl font-extrabold text-oceanDeep">{n}</p><p class="mt-1 text-sm text-slate-600">{l}</p></div>'
        for n, l in stats
    )
    cols = "sm:grid-cols-2" if len(stats) > 1 else "sm:grid-cols-1"
    return f'<div class="grid gap-4 {cols}">{cards}</div>'


def build_oferece(oferece):
    if not oferece:
        return ""
    items = "".join(
        f'<li class="flex items-start gap-3"><i class="fa-solid fa-circle-check mt-1 text-ocean"></i><span>{i}</span></li>'
        for i in oferece
    )
    return (
        '<div class="mt-6 rounded-2xl bg-white p-6 shadow-soft">'
        '<h3 class="font-bold text-oceanDeep">O que esta ação oferece</h3>'
        f'<ul class="mt-4 space-y-3 text-sm text-slate-700">{items}</ul>'
        "</div>"
    )


def build_page(a):
    frase = (
        f'<blockquote class="mt-6 rounded-2xl bg-mist p-5 font-semibold text-oceanDeep"><i class="fa-solid fa-quote-left mr-2 text-ocean"></i>{a["frase"]}</blockquote>'
        if a.get("frase")
        else ""
    )
    stats = build_stats(a["stats"])
    oferece = build_oferece(a["oferece"])
    return f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="theme-color" content="#0f5c73" />
  <title>{a["titulo"]} | Instituto S.E.R. Sagi</title>
  <meta name="description" content="{a["intro"]}" />
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
{HEADER}
  <main id="conteudo-principal">
    <section class="page-banner text-white">
      <div class="mx-auto max-w-7xl px-4 py-16 lg:px-8 lg:py-20">
        <p class="text-sm font-semibold uppercase tracking-[0.25em] text-sun">{a["kicker"]} • Nossas Ações</p>
        <h2 class="mt-4 max-w-4xl text-4xl font-extrabold leading-tight sm:text-5xl">{a["titulo"]}</h2>
        <p class="mt-6 max-w-3xl text-lg text-white/85">{a["intro"]}</p>
      </div>
    </section>
    <section class="mx-auto max-w-7xl px-4 py-16 lg:px-8">
      <div class="grid gap-10 lg:grid-cols-[1.05fr_0.95fr] lg:items-start">
        <div class="premium-card rounded-[2rem] bg-white p-6 shadow-soft">
          <div class="relative -mx-1 overflow-hidden rounded-2xl">
            <img src="https://loremflickr.com/800/500/{a["img"]}" alt="Imagem ilustrativa — {a["titulo"]}" class="h-64 w-full object-cover" loading="lazy" />
          </div>
          <span class="mt-3 inline-flex items-center gap-1.5 rounded-full bg-sand px-2.5 py-1 text-[10px] font-semibold uppercase tracking-[0.15em] text-slate-500" title="Conteúdo ilustrativo — será substituído por imagem real"><i class="fa-solid fa-wand-magic-sparkles text-[9px]"></i>Imagem ilustrativa</span>
          <div class="mt-5 flex items-center gap-3">
            <div class="flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl bg-ocean/10 text-ocean"><i class="fa-solid {a["icone"]} text-2xl"></i></div>
            <h3 class="text-2xl font-bold text-oceanDeep">{a["titulo"]}</h3>
          </div>
          <p class="mt-5 text-base leading-8 text-slate-600">{a["descricao"]}</p>
          {frase}
        </div>
        <div>
          {stats}
          {oferece}
          <div class="mt-6 rounded-2xl bg-sand p-6 text-sm leading-7 text-slate-700">
            <p class="font-bold text-oceanDeep">Voltar para Nossas Ações</p>
            <p class="mt-2">Veja o conjunto completo de frentes de atuação do Instituto na comunidade do Sagi.</p>
            <a href="acoes.html" class="cta-lift mt-4 inline-flex items-center gap-2 rounded-full bg-ocean px-5 py-2.5 text-sm font-semibold text-white transition hover:brightness-95"><i class="fa-solid fa-arrow-left text-xs"></i>Ver todas as ações</a>
          </div>
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
            <a href="contato.html" class="cta-lift rounded-full border border-white/40 px-6 py-3 font-semibold text-white">Falar com a equipe</a>
          </div>
        </div>
      </div>
    </section>
  </main>
{FOOTER}
  <script src="js/main.js"></script>
</body>
</html>
'''


def main():
    # 1) Gera as 6 páginas
    for a in ACOES:
        path = os.path.join(BASE, a["slug"] + ".html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(build_page(a))
        print(f"  ✅ Criado: {a['slug']}.html")

    # 2) Torna os cards de acoes.html clicáveis (em ordem)
    fp = os.path.join(BASE, "acoes.html")
    html = open(fp, encoding="utf-8").read()
    open_tag = '<article class="rounded-3xl bg-white p-6 shadow-soft">'
    close_tag = "</article>"
    out = []
    pos = 0
    for a in ACOES:
        oi = html.find(open_tag, pos)
        if oi == -1:
            print("  ⚠️ card não encontrado:", a["slug"]); break
        ci = html.find(close_tag, oi)
        out.append(html[pos:oi])
        out.append(f'<a href="{a["slug"]}.html" class="block rounded-3xl bg-white p-6 shadow-soft transition hover:-translate-y-1 hover:ring-2 hover:ring-ocean/30">')
        out.append(html[oi + len(open_tag):ci])
        out.append('<span class="mt-4 inline-flex items-center gap-2 text-sm font-semibold text-ocean">Saiba mais <i class="fa-solid fa-arrow-right text-xs"></i></span>')
        out.append("</a>")
        pos = ci + len(close_tag)
    out.append(html[pos:])
    with open(fp, "w", encoding="utf-8") as f:
        f.write("".join(out))
    print("  ✅ acoes.html: cards tornados clicáveis (com 'Saiba mais')")


if __name__ == "__main__":
    main()
