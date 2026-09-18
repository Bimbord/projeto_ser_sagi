# -*- coding: utf-8 -*-
"""
FASE 6 — hero com imagem nas 15 páginas restantes.

  Institucional (6): quem-somos, instalacoes, lei-incentivo, transparencia,
                     contato, como-ajudar
  Ações (2):         acoes, acoes-solidarias
  Acervo (7):        acervo, acervo-esporte, acervo-saude, acervo-educacao,
                     acervo-cultura, acervo-preservacao, acervo-eventos

Pastas novas no Drive:
  institucional/<pagina>/hero/
  acoes/hero/            acoes/acoes-solidarias/hero/
  acervo/hero/           acervo/<pagina>/hero/

Sem foto publicada, a imagem ilustrativa continua (nada quebra).
"""
import os
import re

BASE = r"G:/.shortcut-targets-by-id/18wGiptBKUmAmmkKHgdfu05TU4y_roWC1/BBDPRINT - BACKUP/BBDPRINT/App BBDPRiNT/PROJETOS/Projeto SER Sagi/projeto_SER_Sagi - Hermes"
L = lambda p: os.path.join(BASE, p)  # noqa: E731

# pagina -> (categoria no banco, data-pagina ou None, tema da imagem de reserva)
CONFIG = {
    # ---- INSTITUCIONAL ----
    "quem-somos.html":      ("Institucional", "quem-somos",      "community,volunteers,people"),
    "instalacoes.html":     ("Institucional", "instalacoes",     "building,community,center"),
    "lei-incentivo.html":   ("Institucional", "lei-incentivo",   "business,meeting,handshake"),
    "transparencia.html":   ("Institucional", "transparencia",   "documents,office,report"),
    "contato.html":         ("Institucional", "contato",         "phone,contact,communication"),
    "como-ajudar.html":     ("Institucional", "como-ajudar",     "volunteer,helping,hands"),
    # ---- AÇÕES ----
    "acoes.html":           ("Ações",         None,              "volunteers,community,action"),
    "acoes-solidarias.html": ("Ações",        "acoes-solidarias", "donation,helping,food"),
    # ---- ACERVO ----
    "acervo.html":          ("Acervo",        None,              "photos,gallery,camera"),
    "acervo-esporte.html":  ("Acervo",        "acervo-esporte",  "sports,team,kids"),
    "acervo-saude.html":    ("Acervo",        "acervo-saude",    "health,care,clinic"),
    "acervo-educacao.html": ("Acervo",        "acervo-educacao", "classroom,learning,kids"),
    "acervo-cultura.html":  ("Acervo",        "acervo-cultura",  "culture,community,music"),
    "acervo-preservacao.html": ("Acervo",     "acervo-preservacao", "nature,beach,sea"),
    "acervo-eventos.html":  ("Acervo",        "acervo-eventos",  "event,party,community"),
}

ABRE_ANTIGO = '<section class="page-banner text-white">'
ABRE_NOVO = '<section class="page-banner text-white relative overflow-hidden banner-alto">'


def camadas(cat, pasta, tema, lock, dica_pasta):
    pag = f' data-pagina="{pasta}"' if pasta else ""
    return (f'{ABRE_NOVO}\n'
            f'      <!-- CAMADA 1 · IMAGEM de fundo (ilustrativa — trocar por foto real em {dica_pasta}/hero/) -->\n'
            f'      <img src="https://loremflickr.com/1600/600/{tema}?lock={lock}" alt="" aria-hidden="true"'
            f' data-secao-img="hero" data-categoria="{cat}"{pag} class="absolute inset-0 h-full w-full object-cover">\n'
            f'      <!-- CAMADA 2 · SCRIM (véu diagonal, mesmo efeito do hero da home) -->\n'
            f'      <div class="banner-scrim absolute inset-0"></div>')


feitos, problemas = [], []
SLUGS = {"Institucional": "institucional", "Ações": "acoes", "Acervo": "acervo"}

for i, (nome, (cat, pasta, tema)) in enumerate(CONFIG.items(), 1):
    p = L(nome)
    if not os.path.isfile(p):
        problemas.append((nome, "não existe"))
        continue
    txt = open(p, encoding="utf-8", newline="").read()

    if "banner-scrim" in txt:
        problemas.append((nome, "já tinha hero com imagem"))
        continue

    dica = SLUGS[cat] + (f"/{pasta}" if pasta else "")

    # --- casos com banner simples (14 páginas) ---
    if ABRE_ANTIGO in txt:
        i0 = txt.index(ABRE_ANTIGO)
        k = txt.index('<div class="', i0)
        txt = txt[:k] + '<div class="relative z-10 ' + txt[k + len('<div class="'):]
        i0 = txt.index(ABRE_ANTIGO)
        txt = txt[:i0] + camadas(cat, pasta, tema, 500 + i, dica) + txt[i0 + len(ABRE_ANTIGO):]

    # --- lei-incentivo: hero-pattern (2 colunas) ---
    elif 'class="hero-pattern' in txt:
        marca = '<section class="hero-pattern'
        i0 = txt.index(marca)
        fim_abre = txt.index(">", i0) + 1
        pag = f' data-pagina="{pasta}"' if pasta else ""
        img = (f'\n      <!-- CAMADA 1 · IMAGEM de fundo (ilustrativa — trocar por foto real em {dica}/hero/) -->\n'
               f'      <img src="https://loremflickr.com/1600/600/{tema}?lock={500 + i}" alt="" aria-hidden="true"'
               f' data-secao-img="hero" data-categoria="{cat}"{pag} class="absolute inset-0 h-full w-full object-cover">\n'
               f'      <!-- CAMADA 2 · SCRIM -->\n'
               f'      <div class="banner-scrim absolute inset-0"></div>')
        # conteúdo do hero precisa ficar acima das camadas
        txt = txt[:fim_abre] + img + txt[fim_abre:]
        txt = txt.replace('<div class="mx-auto grid max-w-7xl gap-10 px-4 py-16',
                          '<div class="relative z-10 mx-auto grid max-w-7xl gap-10 px-4 py-16', 1)
    else:
        problemas.append((nome, "não achei banner reconhecido"))
        continue

    open(p, "w", encoding="utf-8", newline="").write(txt)
    feitos.append((nome, cat, pasta))

print(f"✅ FASE 6 — hero com imagem em {len(feitos)} páginas:")
for nome, cat, pasta in feitos:
    print(f"   • {nome:26} {cat}" + (f" · pasta {SLUGS[cat]}/{pasta}/hero/" if pasta else f" · pasta {SLUGS[cat]}/hero/"))
if problemas:
    print(f"\n⚠️  {len(problemas)} sem alteração:")
    for n, m in problemas:
        print(f"   [{n}] {m}")

# ---------- categorias novas no publicar.py ----------
p_pub = L("scripts/publicar.py")
pub = open(p_pub, encoding="utf-8", newline="").read()
novas = [('    "depoimentos": "Depoimentos",',
          '    "depoimentos": "Depoimentos",\n'
          '    "institucional": "Institucional",\n'
          '    "acervo": "Acervo",\n'
          '    "acoes": "Ações",')]
if '"institucional"' in pub:
    print("\n  ⚠️  publicar.py já tinha as categorias novas")
else:
    velho, novo = novas[0]
    if velho in pub:
        open(p_pub, "w", encoding="utf-8", newline="").write(pub.replace(velho, novo, 1))
        print("\n  ✅ publicar.py — categorias institucional, acervo e acoes")
    else:
        print("\n  ⚠️  não achei o ponto de inserção no publicar.py")
