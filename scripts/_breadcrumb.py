# -*- coding: utf-8 -*-
"""
Breadcrumb no topo do hero (banner) da pagina Saude.

  Início > Nossas Ações > Saúde > Consultório Odontológico

Inclui tambem os dados estruturados (schema.org BreadcrumbList) para o Google.
"""
import os

BASE = r"G:/.shortcut-targets-by-id/18wGiptBKUmAmmkKHgdfu05TU4y_roWC1/BBDPRINT - BACKUP/BBDPRINT/App BBDPRiNT/PROJETOS/Projeto SER Sagi/projeto_SER_Sagi - Hermes"

# ============================================================
# 1) CSS
# ============================================================
CSS = """
/* ============================================================
   BREADCRUMB (caminho de navegacao no topo do hero)
   ============================================================ */
.breadcrumb { margin-bottom: 1.25rem; }
.breadcrumb ol {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: .45rem;
  margin: 0;
  padding: 0;
  list-style: none;
  font-size: .8125rem;
  line-height: 1.4;
}
.breadcrumb li { display: inline-flex; align-items: center; gap: .45rem; }
.breadcrumb li + li::before {
  content: '›';
  color: rgba(255, 255, 255, 0.5);
  font-size: 1rem;
  line-height: 1;
}
.breadcrumb a {
  color: rgba(255, 255, 255, 0.78);
  text-decoration: none;
  transition: color .2s ease;
}
.breadcrumb a:hover { color: #fff; text-decoration: underline; }
.breadcrumb [aria-current="page"] { color: #fff; font-weight: 600; }

/* Sobre fundo claro (uso opcional fora do hero) */
.breadcrumb--claro a { color: var(--ocean); }
.breadcrumb--claro li + li::before { color: rgba(15, 92, 115, 0.5); }
.breadcrumb--claro [aria-current="page"] { color: var(--ocean-deep); }
"""

p = os.path.join(BASE, "css", "style.css")
txt = open(p, encoding="utf-8", newline="").read()
if ".breadcrumb {" not in txt:
    open(p, "w", encoding="utf-8", newline="").write(txt.rstrip() + "\n" + CSS)
    print("  ✅ css: estilos do breadcrumb (claro e escuro)")
else:
    print("  ℹ️  css: breadcrumb ja existia")

# ============================================================
# 2) saude.html — breadcrumb no topo do hero + JSON-LD
# ============================================================
BREADCRUMB = '''        <nav class="breadcrumb" aria-label="Você está aqui">
          <ol>
            <li><a href="./">Início</a></li>
            <li><a href="acoes.html">Nossas Ações</a></li>
            <li><a href="saude.html">Saúde</a></li>
            <li><span aria-current="page">Consultório Odontológico</span></li>
          </ol>
        </nav>
'''

JSONLD = '''  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      { "@type": "ListItem", "position": 1, "name": "Início", "item": "https://bimbord.github.io/projeto_ser_sagi/" },
      { "@type": "ListItem", "position": 2, "name": "Nossas Ações", "item": "https://bimbord.github.io/projeto_ser_sagi/acoes.html" },
      { "@type": "ListItem", "position": 3, "name": "Saúde", "item": "https://bimbord.github.io/projeto_ser_sagi/saude.html" },
      { "@type": "ListItem", "position": 4, "name": "Consultório Odontológico", "item": "https://bimbord.github.io/projeto_ser_sagi/saude.html" }
    ]
  }
  </script>
'''

p = os.path.join(BASE, "saude.html")
txt = open(p, encoding="utf-8", newline="").read()

# 2.1 insere o breadcrumb antes do kicker do banner
ANCORA = '''      <div class="relative z-10 mx-auto max-w-7xl px-4 py-16 lg:px-8 lg:py-20">
        <p class="text-sm font-semibold uppercase tracking-[0.25em] text-sun">Saúde • Nossas Ações</p>'''
NOVO = '''      <div class="relative z-10 mx-auto max-w-7xl px-4 py-16 lg:px-8 lg:py-20">
''' + BREADCRUMB + '''        <p class="text-sm font-semibold uppercase tracking-[0.25em] text-sun">Saúde • Nossas Ações</p>'''
assert ANCORA in txt, "saude.html: ancora do kicker do banner nao encontrada"
txt = txt.replace(ANCORA, NOVO, 1)
print("  ✅ saude.html: breadcrumb inserido no topo do hero")

# 2.2 JSON-LD antes do </head>
if "BreadcrumbList" not in txt:
    DE = '<link rel="stylesheet" href="css/style.css" />\n</head>'
    PARA = '<link rel="stylesheet" href="css/style.css" />\n' + JSONLD + '</head>'
    assert DE in txt, "saude.html: </head> nao encontrado"
    txt = txt.replace(DE, PARA, 1)
    print("  ✅ saude.html: dados estruturados (BreadcrumbList) adicionados")

open(p, "w", encoding="utf-8", newline="").write(txt)
print("  ✅ saude.html salvo")
