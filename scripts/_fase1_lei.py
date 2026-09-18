# -*- coding: utf-8 -*-
"""FASE 1 (complemento) — breadcrumb na lei-incentivo.html (banner hero-pattern)."""
import os
import re

BASE = r"G:/.shortcut-targets-by-id/18wGiptBKUmAmmkKHgdfu05TU4y_roWC1/BBDPRINT - BACKUP/BBDPRINT/App BBDPRiNT/PROJETOS/Projeto SER Sagi/projeto_SER_Sagi - Hermes"
SITE = "https://bimbord.github.io/projeto_ser_sagi/"
ITENS = [("Início", "./"), ("Lei de Incentivo", None)]

NAV = '''    <!-- 🧭 Caminho de navegacao (fora do hero) -->
    <nav class="breadcrumb breadcrumb--claro mx-auto max-w-7xl px-4 lg:px-8" aria-label="Você está aqui">
      <ol>
        <li><a href="./">Início</a></li>
        <li><span aria-current="page">Lei de Incentivo</span></li>
      </ol>
    </nav>
'''

JSONLD = '''  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      { "@type": "ListItem", "position": 1, "name": "Início", "item": "''' + SITE + '''" },
      { "@type": "ListItem", "position": 2, "name": "Lei de Incentivo", "item": "''' + SITE + '''lei-incentivo.html" }
    ]
  }
  </script>
'''

p = os.path.join(BASE, "lei-incentivo.html")
txt = open(p, encoding="utf-8", newline="").read()

if "breadcrumb--claro" in txt:
    print("  ℹ️  já tinha breadcrumb")
else:
    padrao = re.compile(r'(<section class="hero-pattern[^"]*">.*?</section>)', re.DOTALL)
    m = padrao.search(txt)
    assert m, "banner hero-pattern nao encontrado"
    txt = txt[:m.end()] + "\n\n" + NAV.rstrip("\n") + txt[m.end():]
    if "BreadcrumbList" not in txt:
        txt = txt.replace("</head>", JSONLD + "</head>", 1)
    open(p, "w", encoding="utf-8", newline="").write(txt)
    print("  ✅ lei-incentivo.html: breadcrumb inserido")
