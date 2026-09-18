# -*- coding: utf-8 -*-
"""
FASE 5 · Parte A — as fotos da HOME passam a vir das pastas do Drive.

  home/hero          -> slideshow do topo (js/hero.js)
  home/joia-da-coroa -> imagem do card "A Jóia da Coroa" (index.html)

Regras:
  - 0 fotos publicadas -> mantem o que ja existe (slides locais / ilustrativa)
  - 1 foto             -> modo imagem
  - 2+ fotos           -> slideshow

A chave anon e lida do js/main.js e gravada direto no hero.js
(nunca passa por aqui, para nao ser exposta).
"""
import os
import re

BASE = r"G:/.shortcut-targets-by-id/18wGiptBKUmAmmkKHgdfu05TU4y_roWC1/BBDPRINT - BACKUP/BBDPRINT/App BBDPRiNT/PROJETOS/Projeto SER Sagi/projeto_SER_Sagi - Hermes"

# ---------- 1. descobre a chave anon no main.js ----------
main_js = open(os.path.join(BASE, "js", "main.js"), encoding="utf-8").read()
m = re.search(r"SUPABASE_URL\s*=\s*['\"]([^'\"]+)['\"]", main_js)
url = m.group(1) if m else "https://icrasqxbxmqbnelmkrei.supabase.co"
m = re.search(r"SUPABASE_ANON_KEY\s*=\s*['\"]([^'\"]+)['\"]", main_js)
if not m:
    raise SystemExit("❌ nao achei SUPABASE_ANON_KEY no js/main.js")
key = m.group(1)
print(f"  🔑 chave lida do main.js ({len(key)} chars) — nao exibida")

# ---------- 2. patch no hero.js ----------
p_hero = os.path.join(BASE, "js", "hero.js")
hero = open(p_hero, encoding="utf-8").read()

if "buscarSlidesDoDrive" in hero:
    print("  ⚠️  hero.js ja estava alterado — pulando")
else:
    # 2a. funcao que busca as fotos da pasta home/hero
    ancora = "  function init() {\n    const host = document.getElementById('hero-media');\n    if (!host) return;\n\n    resolveHeroMode().then(function (mode) {"
    novo = (
        "  // ============================================================\n"
        "  // FASE 5 — as fotos do hero vem da pasta `home/hero` do Drive\n"
        "  // (publicadas no Supabase). Sem foto publicada, mantem os\n"
        "  // arquivos locais de img/hero-slides/.\n"
        "  // ============================================================\n"
        f"  const SUPABASE_URL = '{url}';\n"
        f"  const SUPABASE_ANON_KEY = '{key}';\n"
        "  const HERO_CATEGORIA = 'Home';\n"
        "  const HERO_SECAO = 'hero';\n"
        "\n"
        "  function buscarSlidesDoDrive() {\n"
        "    const url = SUPABASE_URL + '/rest/v1/arquivo?select=titulo,imagem_url'\n"
        "      + '&categoria=eq.' + encodeURIComponent(HERO_CATEGORIA)\n"
        "      + '&secao=eq.' + encodeURIComponent(HERO_SECAO)\n"
        "      + '&deleted=eq.false&order=id.asc';\n"
        "\n"
        "    return fetch(url, {\n"
        "      headers: { apikey: SUPABASE_ANON_KEY, Authorization: 'Bearer ' + SUPABASE_ANON_KEY }\n"
        "    })\n"
        "      .then(function (r) { return r.ok ? r.json() : []; })\n"
        "      .then(function (itens) {\n"
        "        const urls = (itens || []).map(function (i) { return i.imagem_url; }).filter(Boolean);\n"
        "        if (!urls.length) return;              // nada publicado -> locais\n"
        "        if (urls.length >= 2) {\n"
        "          HERO_CONFIG.slides = urls;           // 2+ -> slideshow\n"
        "        } else {\n"
        "          HERO_CONFIG.poster = urls[0];        // 1 -> imagem unica\n"
        "          HERO_CONFIG.posterCover = true;\n"
        "        }\n"
        "      })\n"
        "      .catch(function () { /* mantem os arquivos locais */ });\n"
        "  }\n"
        "\n"
        "  function init() {\n"
        "    const host = document.getElementById('hero-media');\n"
        "    if (!host) return;\n"
        "\n"
        "    // Busca as fotos do Drive antes de decidir o modo do hero\n"
        "    buscarSlidesDoDrive().then(resolveHeroMode).then(function (mode) {"
    )
    if ancora not in hero:
        raise SystemExit("❌ nao achei o bloco init() no hero.js")
    hero = hero.replace(ancora, novo, 1)

    # 2b. imagem unica usa object-cover quando vem do Drive (foto real)
    velho_img = "    return '<img src=\"' + HERO_CONFIG.poster + '\" alt=\"Instituto S.E.R. Sagi em ação\" class=\"h-full w-full object-contain object-top\">';"
    novo_img = ("    const ajuste = HERO_CONFIG.posterCover ? 'object-cover' : 'object-contain object-top';\n"
                "    return '<img src=\"' + HERO_CONFIG.poster + '\" alt=\"Instituto S.E.R. Sagi em ação\" class=\"h-full w-full ' + ajuste + '\">';")
    if velho_img in hero:
        hero = hero.replace(velho_img, novo_img, 1)
    else:
        print("  ⚠️  renderImage() nao casou — a imagem unica fica object-contain")

    open(p_hero, "w", encoding="utf-8", newline="").write(hero)
    print("  ✅ js/hero.js — slides do Drive ligados")

# ---------- 3. patch no index.html (Jóia da Coroa) ----------
p_idx = os.path.join(BASE, "index.html")
idx = open(p_idx, encoding="utf-8").read()
velho = '<img src="https://loremflickr.com/800/500/children,kids,playing?lock=710" alt="Imagem ilustrativa de crianças em atividades"'
novo = '<img src="https://loremflickr.com/800/500/children,kids,playing?lock=710" data-categoria="Home" data-secao-img="joia-da-coroa" alt="Imagem ilustrativa de crianças em atividades"'
if 'data-secao-img="joia-da-coroa"' in idx:
    print("  ⚠️  index.html ja estava alterado — pulando")
elif velho in idx:
    idx = idx.replace(velho, novo, 1)
    open(p_idx, "w", encoding="utf-8", newline="").write(idx)
    print("  ✅ index.html — imagem da Jóia da Coroa ligada a home/joia-da-coroa")
else:
    print("  ⚠️  imagem da Jóia da Coroa nao casou no index.html")

# ---------- 4. publicar.py aceita a categoria "home" ----------
p_pub = os.path.join(BASE, "scripts", "publicar.py")
pub = open(p_pub, encoding="utf-8").read()
if '"home": "Home"' in pub:
    print("  ⚠️  publicar.py ja tinha a categoria home — pulando")
elif '    "eventos": "Eventos",' in pub:
    pub = pub.replace('    "eventos": "Eventos",',
                      '    "eventos": "Eventos",\n    "home": "Home",', 1)
    open(p_pub, "w", encoding="utf-8", newline="").write(pub)
    print("  ✅ publicar.py — categoria 'home' adicionada")
else:
    print("  ⚠️  categoria eventos nao casou no publicar.py")
