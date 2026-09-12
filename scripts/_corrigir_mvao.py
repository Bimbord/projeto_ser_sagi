# -*- coding: utf-8 -*-
"""
Corrige a seção Missão/Visão/Valores/Objetivo do quem-somos.html.
Problema: o <article> de "Valores" não foi fechado, então "Objetivo" ficou
aninhado dentro dele — os dois apareciam como um card só.
Solução: reescrever o bloco com 4 <article> irmãos.
"""
import os, re, sys

BASE = r"C:/Projetos Code/Projeto SER Sagi/projeto_SER_Sagi - Hermes"
ARQ = os.path.join(BASE, "quem-somos.html")

html = open(ARQ, encoding="utf-8").read()
original = html

MARCA = '<div class="mt-10 grid gap-6 md:grid-cols-2 xl:grid-cols-4">'
ini = html.find(MARCA)
if ini == -1:
    sys.exit("❌ grade de missão/visão não encontrada")

fim_sec = html.find("</section>", ini)
fim_grade = html.rfind("</div>", ini, fim_sec)
if fim_grade == -1:
    sys.exit("❌ fim da grade não encontrado")

bloco_atual = html[ini:fim_grade + len("</div>")]

# pega os textos de cada card
def texto_de(rotulo):
    m = re.search(r'<' + r'h3[^>]*>' + re.escape(rotulo) + r'</h3>\s*<p[^>]*>(.*?)</p>', bloco_atual, re.S)
    if not m:
        sys.exit(f"❌ texto de '{rotulo}' não encontrado")
    return m.group(1).strip()

textos = {r: texto_de(r) for r in ("Missão", "Visão", "Valores", "Objetivo")}

ART = ('        <article class="rounded-3xl bg-white p-6 shadow-soft">'
       '<h3 class="text-xl font-bold text-oceanDeep">{rot}</h3>'
       '<p class="mt-3 text-sm leading-7 text-slate-600">{txt}</p></article>')

novo = (MARCA + "\n"
        + "\n".join(ART.format(rot=r, txt=textos[r]) for r in ("Missão", "Visão", "Valores", "Objetivo"))
        + "\n      </div>")

html = html[:ini] + novo + html[fim_grade + len("</div>"):]

# ---- validações ----
if html.count("<article") != original.count("<article") or \
   html.count("</article>") != original.count("</article>"):
    sys.exit("❌ ABORTADO: contagem de <article> mudou — nada foi salvo")

sec = html[ini:html.find("</section>", ini)]
abre, fecha = sec.count("<article"), sec.count("</article>")
if abre != 4 or fecha != 4:
    sys.exit(f"❌ ABORTADO: a seção ficou com {abre} abre / {fecha} fecha (esperado 4/4)")

open(ARQ, "w", encoding="utf-8", newline="\n").write(html)
print("✅ Seção corrigida — 4 cards separados:")
for r in ("Missão", "Visão", "Valores", "Objetivo"):
    print(f"   • {r} ({len(textos[r])} caracteres)")
