# -*- coding: utf-8 -*-
"""
Ajustes na Home (pedidos pelo Bimbord):

1. Card de número: "Projeto principal" -> "JÓIA DA COROA"
   e a descrição -> "crianças tendo suas vidas transformadas"
2. Depoimentos: remove o selo "Conteúdo ilustrativo" + troca a legenda
3. Parceiros:   remove o selo "Conteúdo ilustrativo" + troca a legenda
4. Chamada para ação: remove o rótulo "CHAMADA PARA AÇÃO" + troca a legenda

A chave da foto (data-secao-chave="projeto-principal") NÃO muda — só o rótulo.
"""
import os
import re

BASE = r"G:/.shortcut-targets-by-id/18wGiptBKUmAmmkKHgdfu05TU4y_roWC1/BBDPRINT - BACKUP/BBDPRINT/App BBDPRiNT/PROJETOS/Projeto SER Sagi/projeto_SER_Sagi - Hermes"
L = lambda p: os.path.join(BASE, p)  # noqa: E731

p_idx = L("index.html")
h = open(p_idx, encoding="utf-8", newline="").read()
antes = h

TEXTOS = {
    "depoimentos": 'Depoimentos reais de mães, pais, crianças e parceiros. "Esse é o nosso estímulo, é a força continuar doando: esperança e dignidade para as crianças da comunidade".',
    "parceiros": "Seja investindo recursos, tempo ou parcerias, quem apoia nossa instituição ajuda a quebrar ciclos de vulnerabilidade e plantar um futuro melhor.",
    "cta": "Apoiar financeiramente nossa causa não é apenas manter uma estrutura aberta, é garantir que crianças tenham o suporte necessário para sonhar e construir uma trajetória digna.",
}

# ---------- 1. card de número ----------
h, n1 = re.subn(r'<span class="home-stat__label">Projeto principal</span>',
                '<span class="home-stat__label">Jóia da Coroa</span>', h, count=1)
h, n1b = re.subn(r'<p class="home-stat__desc">crianças na Jóia da Coroa</p>',
                 '<p class="home-stat__desc">crianças tendo suas vidas transformadas</p>', h, count=1)
print(f"  1) card de número: rótulo {'✅' if n1 else '❌'} | descrição {'✅' if n1b else '❌'}")

# ---------- 2. selos "Conteúdo ilustrativo" (depoimentos e parceiros) ----------
padrao_selo = r'<div class="mt-4 flex items-center gap-2"[^>]*>.*?Conteúdo ilustrativo</span></div>'
h, n_selos = re.subn(padrao_selo, '', h)
print(f"  2) selos 'Conteúdo ilustrativo' removidos: {n_selos} (esperado 2)")

# ---------- 3. legendas ----------
trocas = [
    (r'<p class="mt-4 leading-8 text-slate-600">Depoimentos reais.*?</p>',
     f'<p class="mt-4 leading-8 text-slate-600">{TEXTOS["depoimentos"]}</p>', "depoimentos"),
    (r'<p class="mt-4 leading-8 text-slate-600">Os nomes abaixo.*?</p>',
     f'<p class="mt-4 leading-8 text-slate-600">{TEXTOS["parceiros"]}</p>', "parceiros"),
    (r'<p class="mt-6 max-w-2xl leading-8 text-slate-600">Empresas, voluntários.*?</p>',
     f'<p class="mt-6 max-w-2xl leading-8 text-slate-600">{TEXTOS["cta"]}</p>', "chamada p/ ação (texto)"),
    (r'<p class="text-sm font-semibold uppercase tracking-\[0\.25em\] text-ocean">Chamada para ação</p>',
     '', "chamada p/ ação (rótulo)"),
]
for pat, novo, nome in trocas:
    h, n = re.subn(pat, novo, h, count=1, flags=re.DOTALL)
    print(f"  3) legenda '{nome}': {'✅' if n else '❌ NÃO ACHOU'}")

if h != antes:
    open(p_idx, "w", encoding="utf-8", newline="").write(h)

# ---------- conferência ----------
print("\n  --- conferência ---")
print(f"     'Jóia da Coroa' no card de número ....... {'Jóia da Coroa</span>' in h}")
print(f"     'vidas transformadas' ................... {'vidas transformadas' in h}")
print(f"     'Conteúdo ilustrativo' restantes ........ {h.count('Conteúdo ilustrativo')} (o da imagem no card da Jóia deve ficar)")
print(f"     'Chamada para ação' restantes .......... {h.count('Chamada para ação')}")
print("     chave da foto preservada ................ " + str('data-secao-chave="projeto-principal"' in h))
