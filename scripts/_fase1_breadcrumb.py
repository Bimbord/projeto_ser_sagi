# -*- coding: utf-8 -*-
"""
FASE 1 — Breadcrumb em todas as páginas (fora do hero, faixa clara).

Cada página recebe:
  - a faixa de breadcrumb logo ABAIXO do banner
  - os dados estruturados BreadcrumbList (schema.org) no <head>

Não mexe na home (é a raiz) nem na saude.html (já tem).
"""
import os
import re

BASE = r"G:/.shortcut-targets-by-id/18wGiptBKUmAmmkKHgdfu05TU4y_roWC1/BBDPRINT - BACKUP/BBDPRINT/App BBDPRiNT/PROJETOS/Projeto SER Sagi/projeto_SER_Sagi - Hermes"
SITE = "https://bimbord.github.io/projeto_ser_sagi/"

# ---------------------------------------------------------------
# Mapa: pagina -> caminho. O ULTIMO item é a página atual.
# ---------------------------------------------------------------
MAPA = {
    # Nossas Ações
    "acoes.html": [("Início", "./"), ("Nossas Ações", None)],
    "esporte.html": [("Início", "./"), ("Nossas Ações", "acoes.html"), ("Esporte", None)],
    "educacao.html": [("Início", "./"), ("Nossas Ações", "acoes.html"), ("Educação", None)],
    "cultura.html": [("Início", "./"), ("Nossas Ações", "acoes.html"), ("Cultura", None)],
    "preservacao-ambiental.html": [("Início", "./"), ("Nossas Ações", "acoes.html"), ("Preservação", None)],
    "acoes-solidarias.html": [("Início", "./"), ("Nossas Ações", "acoes.html"), ("Cultura", "cultura.html"), ("Ações Solidárias", None)],

    # Áreas de Esporte
    "escola-jiu-jitsu.html": [("Início", "./"), ("Nossas Ações", "acoes.html"), ("Esporte", "esporte.html"), ("Jiu-Jitsu", None)],
    "volei.html": [("Início", "./"), ("Nossas Ações", "acoes.html"), ("Esporte", "esporte.html"), ("Vôlei", None)],
    "futevolei.html": [("Início", "./"), ("Nossas Ações", "acoes.html"), ("Esporte", "esporte.html"), ("Futevôlei", None)],
    "estudio-musculacao.html": [("Início", "./"), ("Nossas Ações", "acoes.html"), ("Esporte", "esporte.html"), ("Musculação", None)],
    "natacao.html": [("Início", "./"), ("Nossas Ações", "acoes.html"), ("Esporte", "esporte.html"), ("Natação", None)],
    "danca.html": [("Início", "./"), ("Nossas Ações", "acoes.html"), ("Esporte", "esporte.html"), ("Dança", None)],
    "arena-futevolei-volei.html": [("Início", "./"), ("Nossas Ações", "acoes.html"), ("Esporte", "esporte.html"), ("Arena de Futevôlei e Vôlei", None)],

    # Áreas de Educação
    "ingles.html": [("Início", "./"), ("Nossas Ações", "acoes.html"), ("Educação", "educacao.html"), ("Inglês", None)],
    "espanhol.html": [("Início", "./"), ("Nossas Ações", "acoes.html"), ("Educação", "educacao.html"), ("Espanhol", None)],
    "informatica.html": [("Início", "./"), ("Nossas Ações", "acoes.html"), ("Educação", "educacao.html"), ("Informática", None)],
    "sustentabilidade.html": [("Início", "./"), ("Nossas Ações", "acoes.html"), ("Educação", "educacao.html"), ("Sustentabilidade e Meio Ambiente", None)],

    # Institucional
    "quem-somos.html": [("Início", "./"), ("Quem Somos", None)],
    "instalacoes.html": [("Início", "./"), ("Quem Somos", "quem-somos.html"), ("Instalações", None)],
    "lei-incentivo.html": [("Início", "./"), ("Lei de Incentivo", None)],
    "transparencia.html": [("Início", "./"), ("Transparência", None)],
    "contato.html": [("Início", "./"), ("Contato", None)],
    "como-ajudar.html": [("Início", "./"), ("Como Ajudar", None)],

    # Acervo
    "acervo.html": [("Início", "./"), ("Acervo", None)],
    "acervo-esporte.html": [("Início", "./"), ("Acervo", "acervo.html"), ("Esporte", None)],
    "acervo-saude.html": [("Início", "./"), ("Acervo", "acervo.html"), ("Saúde", None)],
    "acervo-educacao.html": [("Início", "./"), ("Acervo", "acervo.html"), ("Educação", None)],
    "acervo-cultura.html": [("Início", "./"), ("Acervo", "acervo.html"), ("Cultura", None)],
    "acervo-preservacao.html": [("Início", "./"), ("Acervo", "acervo.html"), ("Preservação", None)],
    "acervo-eventos.html": [("Início", "./"), ("Acervo", "acervo.html"), ("Eventos", None)],
}

NAV = '''    <!-- 🧭 Caminho de navegacao (fora do hero) -->
    <nav class="breadcrumb breadcrumb--claro mx-auto max-w-7xl px-4 lg:px-8" aria-label="Você está aqui">
      <ol>
{itens}
      </ol>
    </nav>

'''


def bloco_nav(itens):
    lis = []
    for i, (nome, href) in enumerate(itens):
        if i == len(itens) - 1:
            lis.append('        <li><span aria-current="page">%s</span></li>' % nome)
        else:
            lis.append('        <li><a href="%s">%s</a></li>' % (href, nome))
    return NAV.format(itens="\n".join(lis))


def bloco_jsonld(itens):
    itens_js = []
    for i, (nome, href) in enumerate(itens, 1):
        url = SITE if href == "./" else SITE + (href or "")
        itens_js.append('      { "@type": "ListItem", "position": %d, "name": "%s", "item": "%s" }'
                        % (i, nome, url))
    return ('  <script type="application/ld+json">\n'
            '  {\n'
            '    "@context": "https://schema.org",\n'
            '    "@type": "BreadcrumbList",\n'
            '    "itemListElement": [\n' + ",\n".join(itens_js) + '\n'
            '    ]\n'
            '  }\n'
            '  </script>\n')


feitos, pulados, erros = [], [], []

for nome, itens in MAPA.items():
    p = os.path.join(BASE, nome)
    if not os.path.isfile(p):
        erros.append((nome, "nao existe"))
        continue
    txt = open(p, encoding="utf-8", newline="").read()

    if "breadcrumb--claro" in txt:
        pulados.append(nome)
        continue

    # 1) insere a faixa DEPOIS do banner
    padrao = re.compile(r'(<section class="page-banner[^"]*">.*?</section>)', re.DOTALL)
    m = padrao.search(txt)
    if not m:
        erros.append((nome, "banner page-banner nao encontrado"))
        continue
    nav = bloco_nav(itens)
    txt = txt[:m.end()] + "\n\n" + nav.rstrip("\n") + txt[m.end():]

    # 2) JSON-LD antes do </head>
    if "BreadcrumbList" not in txt:
        txt = txt.replace("</head>", bloco_jsonld(itens) + "</head>", 1)

    open(p, "w", encoding="utf-8", newline="").write(txt)
    feitos.append(nome)

print(f"✅ FASE 1 — breadcrumb aplicado em {len(feitos)} páginas")
print(f"   já tinham (puladas): {len(pulados)} {pulados if pulados else ''}")
if erros:
    print(f"\n⚠️  PROBLEMAS ({len(erros)}):")
    for n, motivo in erros:
        print(f"   [{n}] {motivo}")
