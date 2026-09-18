# -*- coding: utf-8 -*-
"""
Auditoria: o que cada pagina ja tem do "padrao Sessao 10" e o que falta.

Checa por pagina:
  - hero com imagem (banner-scrim)
  - banner mais alto (banner-alto)
  - breadcrumb
  - secoes do Drive (data-secao / data-secao-img)
  - carrossel / galeria
"""
import os
import re

BASE = r"G:/.shortcut-targets-by-id/18wGiptBKUmAmmkKHgdfu05TU4y_roWC1/BBDPRINT - BACKUP/BBDPRINT/App BBDPRiNT/PROJETOS/Projeto SER Sagi/projeto_SER_Sagi - Hermes"

# agrupamento por papel na hierarquia
GRUPOS = {
    "HOME": ["index.html"],
    "INSTITUCIONAL": ["quem-somos.html", "instalacoes.html", "lei-incentivo.html",
                      "transparencia.html", "contato.html", "como-ajudar.html"],
    "ACERVO": ["acervo.html", "acervo-esporte.html", "acervo-saude.html", "acervo-educacao.html",
               "acervo-cultura.html", "acervo-preservacao.html", "acervo-eventos.html"],
    "CATEGORIA (hub)": ["esporte.html", "educacao.html"],
    "CATEGORIA (area unica)": ["saude.html", "cultura.html", "preservacao-ambiental.html"],
    "AREA de Esporte": ["escola-jiu-jitsu.html", "volei.html", "futevolei.html",
                        "estudio-musculacao.html", "natacao.html", "danca.html",
                        "arena-futevolei-volei.html"],
    "AREA de Educacao": ["ingles.html", "espanhol.html", "informatica.html", "sustentabilidade.html"],
    "OUTRAS": ["acoes.html", "acoes-solidarias.html"],
}

todos = sorted(f for f in os.listdir(BASE) if f.endswith(".html"))
mapeados = {p for lista in GRUPOS.values() for p in lista}
sem_grupo = [p for p in todos if p not in mapeados]
if sem_grupo:
    GRUPOS["NAO MAPEADAS"] = sem_grupo


def checar(nome):
    txt = open(os.path.join(BASE, nome), encoding="utf-8").read()
    t = re.search(r"<title>([^<]*)</title>", txt)
    return {
        "titulo": (t.group(1).split("|")[0].strip() if t else "?"),
        "hero_img": "banner-scrim" in txt,
        "alto": "banner-alto" in txt,
        "breadcrumb": "breadcrumb" in txt,
        "secao": bool(re.search(r'data-secao(-img)?="', txt)),
        "secoes": sorted(set(re.findall(r'data-secao(?:-img)?="([^"]+)"', txt))),
    }


print("=" * 78)
print("AUDITORIA — PADRAO DA SESSAO 10 (hero com imagem / breadcrumb / secoes)")
print("=" * 78)
print(f"{'pagina':32} {'hero':5} {'alto':5} {'bread':6} {'secoes':7} secoes usadas")
print("-" * 78)

resumo = {}
for grupo, lista in GRUPOS.items():
    print(f"\n### {grupo}")
    for nome in lista:
        if not os.path.isfile(os.path.join(BASE, nome)):
            print(f"  {nome:32} (nao existe)")
            continue
        d = checar(nome)
        resumo[nome] = d
        print(f"  {nome:32} {'✅' if d['hero_img'] else '—':5} "
              f"{'✅' if d['alto'] else '—':5} "
              f"{'✅' if d['breadcrumb'] else '—':6} "
              f"{'✅' if d['secao'] else '—':7} {', '.join(d['secoes']) if d['secoes'] else ''}")

print("\n" + "=" * 78)
total = len(resumo)
print(f"RESUMO ({total} páginas)")
print(f"  com hero + imagem ...... {sum(1 for d in resumo.values() if d['hero_img'])}")
print(f"  com breadcrumb ......... {sum(1 for d in resumo.values() if d['breadcrumb'])}")
print(f"  com seções do Drive .... {sum(1 for d in resumo.values() if d['secao'])}")
print(f"  computador sem nada .... {sum(1 for d in resumo.values() if not d['hero_img'] and not d['breadcrumb'] and not d['secao'])}")
