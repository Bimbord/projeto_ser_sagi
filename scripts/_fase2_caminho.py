# -*- coding: utf-8 -*-
"""
FASE 2 — Secoes em CAMINHO, para suportar as Areas.

Antes:   categoria/secao            -> esporte/hero
Agora:   categoria/pagina/secao     -> esporte/volei/hero

Regra: qualquer subpasta (em QUALQUER nivel) que tenha arquivos de midia vira
uma secao; o caminho relativo dela e a coluna `secao` no banco.

  esporte/hero/foto.jpg          -> secao "hero"
  esporte/volei/hero/foto.jpg    -> secao "volei/hero"
  esporte/volei/foto.jpg         -> secao "volei"
  esporte/foto.jpg               -> IGNORADO (solto na raiz)
"""
import os

BASE = r"G:/.shortcut-targets-by-id/18wGiptBKUmAmmkKHgdfu05TU4y_roWC1/BBDPRINT - BACKUP/BBDPRINT/App BBDPRiNT/PROJETOS/Projeto SER Sagi/projeto_SER_Sagi - Hermes"

# ============================================================
# 1) servidor_midias.py — varredura recursiva
# ============================================================
p = os.path.join(BASE, "scripts", "servidor_midias.py")
txt = open(p, encoding="utf-8", newline="").read()

DE_INI = 'def varrer(manifesto, categoria_filtro=None, max_mb=MAX_MB_PADRAO):'
i = txt.index(DE_INI)
j = txt.index('def validar_creds(creds):')

NOVA = '''def varrer(manifesto, categoria_filtro=None, max_mb=MAX_MB_PADRAO):
    """Varre as PASTAS DE SECAO (recursivo) dentro de cada categoria.

    Uma pasta de secao e qualquer subpasta - em QUALQUER nivel - que contenha
    arquivos de midia. O caminho relativo dela vira a coluna `secao`:

        esporte/hero/foto.jpg          -> secao "hero"        (pagina do hub)
        esporte/volei/hero/foto.jpg    -> secao "volei/hero"  (pagina da area)
        esporte/volei/foto.jpg         -> secao "volei"
        esporte/foto.jpg               -> IGNORADO (solto na raiz)

    Retorna (pendentes, ja_publicados, ignorados).
    """
    pendentes, ja_publicados, ignorados = [], [], []
    for cat in CATEGORIAS:
        if categoria_filtro and cat != categoria_filtro:
            continue
        pasta_cat = os.path.join(BASE, cat)
        if not os.path.isdir(pasta_cat):
            continue
        info_cat = ler_info(pasta_cat)

        for raiz, dirs, arqs in os.walk(pasta_cat):
            # nao desce em pastas internas (_rascunho) nem ocultas
            dirs[:] = [d for d in dirs if not d.startswith((".", "_"))]

            na_raiz = os.path.abspath(raiz) == os.path.abspath(pasta_cat)
            if na_raiz:
                # arquivo solto na raiz da categoria: NAO sobe
                for nome in sorted(arqs):
                    if nome != INFO_FILENAME:
                        ignorados.append((cat, nome,
                                          "solta na raiz - so sobe o que esta em pasta de secao"))
                continue

            secao = os.path.relpath(raiz, pasta_cat).replace(os.sep, "/")
            info_secao = ler_info(raiz)
            info = info_secao if info_secao else info_cat
            rotulo = f"{cat}/{secao}"

            for nome in sorted(arqs):
                if nome == INFO_FILENAME:
                    continue
                caminho = os.path.join(raiz, nome)
                ext = os.path.splitext(nome)[1].lower()
                if ext not in EXT_SUPORTADAS:
                    ignorados.append((rotulo, nome, "extensao nao suportada"))
                    continue
                if ext == ".pdf":
                    ignorados.append((rotulo, nome, "PDF nao entra no Acervo (use upload_r2.py)"))
                    continue
                tamanho = os.path.getsize(caminho)
                if max_mb and tamanho > max_mb * MB:
                    ignorados.append((rotulo, nome,
                                      f"{tamanho / MB:.0f} MB (acima do --max-mb {max_mb})"))
                    continue
                h = hash_arquivo(caminho)
                if h in manifesto["arquivos"]:
                    ja_publicados.append((rotulo, nome, manifesto["arquivos"][h]))
                else:
                    pendentes.append({"caminho": caminho, "categoria": cat, "secao": secao,
                                      "nome": nome, "tamanho": tamanho, "hash": h, "ext": ext,
                                      "tipo": "video" if ext in EXT_VIDEO else "foto",
                                      "info": info})
    return pendentes, ja_publicados, ignorados


'''
txt = txt[:i] + NOVA + txt[j:]

# docstring: atualiza a explicacao das pastas
txt = txt.replace(
    "    saude\\\\\n        hero\\\\               -> imagens do banner",
    "    saude\\\\\n        hero\\\\               -> imagens do banner", 1)

open(p, "w", encoding="utf-8", newline="").write(txt)
print("  ✅ servidor_midias.py: varredura recursiva (secao em caminho)")

# ============================================================
# 2) js/main.js — aceita data-pagina
# ============================================================
p = os.path.join(BASE, "js", "main.js")
txt = open(p, encoding="utf-8", newline="").read()

DE = """  const blocos = document.querySelectorAll('[data-secao]');
  for (const el of blocos) {
    const secao = el.getAttribute('data-secao');
    const categoria = el.getAttribute('data-categoria') || '';"""
PARA = """  const blocos = document.querySelectorAll('[data-secao]');
  for (const el of blocos) {
    // data-pagina opcional: secao da PAGINA DA AREA (ex.: volei/carrossel)
    const pagina = el.getAttribute('data-pagina');
    const secao = pagina ? `${pagina}/${el.getAttribute('data-secao')}` : el.getAttribute('data-secao');
    const categoria = el.getAttribute('data-categoria') || '';"""
assert DE in txt, "main.js: bloco [data-secao] nao encontrado"
txt = txt.replace(DE, PARA, 1)

DE = """  const imagens = document.querySelectorAll('[data-secao-img]');
  for (const img of imagens) {
    const secao = img.getAttribute('data-secao-img');
    const categoria = img.getAttribute('data-categoria') || '';"""
PARA = """  const imagens = document.querySelectorAll('[data-secao-img]');
  for (const img of imagens) {
    const pagina = img.getAttribute('data-pagina');
    const secao = pagina ? `${pagina}/${img.getAttribute('data-secao-img')}` : img.getAttribute('data-secao-img');
    const categoria = img.getAttribute('data-categoria') || '';"""
assert DE in txt, "main.js: bloco [data-secao-img] nao encontrado"
txt = txt.replace(DE, PARA, 1)

# comentario do topo do modulo
txt = txt.replace(
    "// `arquivo`. O bloco marcado com [data-secao=\"x\"] e preenchido",
    "// `arquivo`. O bloco marcado com [data-secao=\"x\"] e preenchido\n// (com [data-pagina] opcional, a secao vira \"pagina/secao\")", 1)

open(p, "w", encoding="utf-8", newline="").write(txt)
print("  ✅ js/main.js: loadSecoes aceita data-pagina")
