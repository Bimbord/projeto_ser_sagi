# -*- coding: utf-8 -*-
"""
Adiciona a coluna "Frentes de Atuação" no rodapé (Saúde, Educação, Esporte,
Ações Solidárias, Preservação Ambiental) em todas as páginas.
O link "Esporte" sai da coluna Navegação (migra para a nova coluna).
"""
import os

BASE = r"C:/Projetos Code/Projeto SER Sagi/projeto_SER_Sagi - Hermes"

GRID_OLD = '<div class="grid gap-10 lg:grid-cols-[1.5fr_0.7fr_0.8fr_1fr]">'
GRID_NEW = '<div class="grid gap-10 lg:grid-cols-[1.4fr_0.6fr_0.8fr_0.8fr_1fr]">'

NAV_OLD = '''        <section>
          <h3 class="text-sm font-semibold uppercase tracking-[0.2em] text-sun">Navegação</h3>
          <ul class="mt-4 space-y-3 text-sm">
            <li><a href="./" class="text-white/70 transition hover:text-white">Início</a></li>
            <li><a href="quem-somos.html" class="text-white/70 transition hover:text-white">Quem Somos</a></li>
            <li><a href="acoes.html" class="text-white/70 transition hover:text-white">Nossas Ações</a></li>
            <li><a href="esporte.html" class="text-white/70 transition hover:text-white">Esporte</a></li>
            <li><a href="acervo.html" class="text-white/70 transition hover:text-white">Acervo</a></li>
            <li><a href="como-ajudar.html" class="text-white/70 transition hover:text-white">Como Ajudar</a></li>
          </ul>
        </section>'''

NAV_NEW = '''        <section>
          <h3 class="text-sm font-semibold uppercase tracking-[0.2em] text-sun">Navegação</h3>
          <ul class="mt-4 space-y-3 text-sm">
            <li><a href="./" class="text-white/70 transition hover:text-white">Início</a></li>
            <li><a href="quem-somos.html" class="text-white/70 transition hover:text-white">Quem Somos</a></li>
            <li><a href="acoes.html" class="text-white/70 transition hover:text-white">Nossas Ações</a></li>
            <li><a href="acervo.html" class="text-white/70 transition hover:text-white">Acervo</a></li>
            <li><a href="como-ajudar.html" class="text-white/70 transition hover:text-white">Como Ajudar</a></li>
          </ul>
        </section>
        <section>
          <h3 class="text-sm font-semibold uppercase tracking-[0.2em] text-sun">Frentes de Atuação</h3>
          <ul class="mt-4 space-y-3 text-sm">
            <li><a href="consultorio-odontologico.html" class="text-white/70 transition hover:text-white">Saúde</a></li>
            <li><a href="educacao.html" class="text-white/70 transition hover:text-white">Educação</a></li>
            <li><a href="esporte.html" class="text-white/70 transition hover:text-white">Esporte</a></li>
            <li><a href="acoes-solidarias.html" class="text-white/70 transition hover:text-white">Ações Solidárias</a></li>
            <li><a href="preservacao-ambiental.html" class="text-white/70 transition hover:text-white">Preservação Ambiental</a></li>
          </ul>
        </section>'''

total = 0
falhas = []
for nome in sorted(os.listdir(BASE)):
    if not nome.endswith(".html"):
        continue
    p = os.path.join(BASE, nome)
    txt = open(p, encoding="utf-8").read()
    if GRID_OLD not in txt or NAV_OLD not in txt:
        falhas.append(nome)
        continue
    novo = txt.replace(GRID_OLD, GRID_NEW).replace(NAV_OLD, NAV_NEW)
    open(p, "w", encoding="utf-8", newline="\n").write(novo)
    total += 1

print(f"✅ coluna 'Frentes de Atuação' adicionada em {total} páginas")
if falhas:
    print("⚠️ páginas não alteradas (padrão não encontrado):", falhas)
