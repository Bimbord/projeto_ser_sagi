# -*- coding: utf-8 -*-
"""
Suporte a PASTAS DE SECAO no servidor de midias.

Regra nova:
  - Só sobem arquivos que estao DENTRO de uma subpasta de secao.
    Ex.: G:/Meu Drive/Instituto SER Sagi - PARA O SITE/saude/carrossel/foto.jpg
  - Arquivos soltos na raiz da categoria NAO sobem (viram "ignorados").
  - O nome da subpasta vira a coluna `secao` na tabela `arquivo`.

Altera: scripts/publicar.py, scripts/servidor_midias.py
Cria:   docs/supabase-add-secao.sql
"""
import os

BASE = r"G:/.shortcut-targets-by-id/18wGiptBKUmAmmkKHgdfu05TU4y_roWC1/BBDPRINT - BACKUP/BBDPRINT/App BBDPRiNT/PROJETOS/Projeto SER Sagi/projeto_SER_Sagi - Hermes"

# ============================================================
# 1) publicar.py — aceita e grava a coluna `secao`
# ============================================================
p = os.path.join(BASE, "scripts", "publicar.py")
txt = open(p, encoding="utf-8", newline="").read()

DE = '''def publicar_um(creds, caminho, titulo, categoria_slug, descricao, destaque,
                data_registro, base=None):
    """Sobe 1 arquivo pro R2 e registra no Supabase. Retorna (chave, url, id)."""'''
PARA = '''def publicar_um(creds, caminho, titulo, categoria_slug, descricao, destaque,
                data_registro, base=None, secao=None):
    """Sobe 1 arquivo pro R2 e registra no Supabase. Retorna (chave, url, id).

    `secao` = subpasta de secao dentro da categoria (ex.: hero, carrossel,
    galeria, "imagem principal"). Vai para a coluna `secao` da tabela `arquivo`.
    """'''
assert DE in txt, "publicar.py: assinatura de publicar_um nao encontrada"
txt = txt.replace(DE, PARA)

DE = '''    payload = {
        "titulo": titulo,
        "tipo": tipo,
        "categoria": categoria,
        "descricao": descricao,'''
PARA = '''    payload = {
        "titulo": titulo,
        "tipo": tipo,
        "categoria": categoria,
        "secao": secao,
        "descricao": descricao,'''
assert DE in txt, "publicar.py: payload nao encontrado"
txt = txt.replace(DE, PARA)
open(p, "w", encoding="utf-8", newline="").write(txt)
print("  ✅ publicar.py atualizado")

# ============================================================
# 2) servidor_midias.py — varre SUBPASTAS de secao
# ============================================================
p = os.path.join(BASE, "scripts", "servidor_midias.py")
txt = open(p, encoding="utf-8", newline="").read()

# --- 2.1 docstring ---
DE = '''Este script le o que esta nas pastas de categoria, sobe pro R2, registra no
Supabase (tabela `arquivo`), move o arquivo para `_publicados\\\\<categoria>\\\\`
e anota tudo no manifesto `_publicados\\\\publicados.json` (guardado NO DRIVE,
nao no C: - sobrevive a qualquer problema no PC).'''
PARA = '''Dentro de cada categoria existem as PASTAS DE SECAO. O nome da subpasta vira a
coluna `secao` da tabela `arquivo` (o site usa isso para saber onde cada imagem
aparece). Exemplo:

    saude\\\\
        hero\\\\               -> imagens do banner
        carrossel\\\\          -> imagens do carrossel horizontal
        galeria\\\\            -> imagens da galeria
        imagem principal\\\\   -> imagem de destaque da pagina

    >>> SO SOBE o que esta dentro de uma pasta de secao.
    >>> Arquivo solto na raiz da categoria e IGNORADO.

Este script le as secoes, sobe pro R2, registra no Supabase (tabela `arquivo`),
move o arquivo para `_publicados\\\\<categoria>\\\\` e anota tudo no manifesto
`_publicados\\\\publicados.json` (guardado NO DRIVE, nao no C: - sobrevive a
qualquer problema no PC).'''
assert DE in txt, "servidor_midias.py: docstring nao encontrada"
txt = txt.replace(DE, PARA)

# --- 2.2 funcao varrer() ---
DE = '''def varrer(manifesto, categoria_filtro=None, max_mb=MAX_MB_PADRAO):
    """Varre as pastas de categoria. Retorna (pendentes, ja_publicados, ignorados)."""
    pendentes, ja_publicados, ignorados = [], [], []
    for cat in CATEGORIAS:
        if categoria_filtro and cat != categoria_filtro:
            continue
        pasta = os.path.join(BASE, cat)
        if not os.path.isdir(pasta):
            continue
        info = ler_info(pasta)
        for nome in sorted(os.listdir(pasta)):
            caminho = os.path.join(pasta, nome)
            if not os.path.isfile(caminho) or nome == INFO_FILENAME:
                continue
            ext = os.path.splitext(nome)[1].lower()
            if ext not in EXT_SUPORTADAS:
                ignorados.append((cat, nome, "extensao nao suportada"))
                continue
            if ext == ".pdf":
                ignorados.append((cat, nome, "PDF nao entra no Acervo (use upload_r2.py)"))
                continue
            tamanho = os.path.getsize(caminho)
            if max_mb and tamanho > max_mb * MB:
                ignorados.append((cat, nome, f"{tamanho / MB:.0f} MB (acima do --max-mb {max_mb})"))
                continue
            h = hash_arquivo(caminho)
            if h in manifesto["arquivos"]:
                ja_publicados.append((cat, nome, manifesto["arquivos"][h]))
            else:
                pendentes.append({"caminho": caminho, "categoria": cat, "nome": nome,
                                  "tamanho": tamanho, "hash": h, "ext": ext,
                                  "tipo": "video" if ext in EXT_VIDEO else "foto",
                                  "info": info})
    return pendentes, ja_publicados, ignorados'''

PARA = '''def varrer(manifesto, categoria_filtro=None, max_mb=MAX_MB_PADRAO):
    """Varre as SUBPASTAS DE SECAO dentro de cada categoria.

    Retorna (pendentes, ja_publicados, ignorados).
    Regra: so entram arquivos DENTRO de uma pasta de secao. Arquivo solto na
    raiz da categoria vai para `ignorados` (nao sobe).
    """
    pendentes, ja_publicados, ignorados = [], [], []
    for cat in CATEGORIAS:
        if categoria_filtro and cat != categoria_filtro:
            continue
        pasta_cat = os.path.join(BASE, cat)
        if not os.path.isdir(pasta_cat):
            continue
        info_cat = ler_info(pasta_cat)

        for entrada in sorted(os.listdir(pasta_cat)):
            caminho_entrada = os.path.join(pasta_cat, entrada)

            # ---- arquivo solto na raiz da categoria: NAO sobe ----
            if os.path.isfile(caminho_entrada):
                if entrada != INFO_FILENAME:
                    ignorados.append((cat, entrada,
                                      "solta na raiz - so sobe o que esta em pasta de secao"))
                continue

            # ---- subpasta = SECAO ----
            secao = entrada
            info_secao = ler_info(caminho_entrada)
            info = info_secao if info_secao else info_cat
            rotulo = f"{cat}/{secao}"

            for nome in sorted(os.listdir(caminho_entrada)):
                caminho = os.path.join(caminho_entrada, nome)
                if not os.path.isfile(caminho) or nome == INFO_FILENAME:
                    continue
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
    return pendentes, ja_publicados, ignorados'''
assert DE in txt, "servidor_midias.py: funcao varrer() nao encontrada"
txt = txt.replace(DE, PARA)

# --- 2.3 status: mostra cat/secao ---
DE = """        for p in pendentes:
            print(f"   [{p['categoria']:11}] {p['nome']}  ({p['tamanho'] / MB:.1f} MB)")"""
PARA = """        for p in pendentes:
            print(f"   [{p['categoria'] + '/' + p['secao']:26}] {p['nome']}  ({p['tamanho'] / MB:.1f} MB)")"""
assert DE in txt, "servidor_midias.py: print do status nao encontrado"
txt = txt.replace(DE, PARA)

# --- 2.4 contador por (categoria, secao) ---
DE = '''        cat, nome = p["categoria"], p["nome"]
        contador_por_categoria[cat] = contador_por_categoria.get(cat, 0) + 1
        info = p["info"]
        titulo, data = titulo_e_data(nome)

        if info.get("titulo_base"):
            titulo = f"{info['titulo_base']} — {contador_por_categoria[cat]:02d}"'''
PARA = '''        cat, secao, nome = p["categoria"], p["secao"], p["nome"]
        chave_cont = f"{cat}/{secao}"
        contador_por_categoria[chave_cont] = contador_por_categoria.get(chave_cont, 0) + 1
        info = p["info"]
        titulo, data = titulo_e_data(nome)

        if info.get("titulo_base"):
            titulo = f"{info['titulo_base']} — {contador_por_categoria[chave_cont]:02d}"'''
assert DE in txt, "servidor_midias.py: contador nao encontrado"
txt = txt.replace(DE, PARA)

# --- 2.5 prints do publicar + passar secao ---
DE = '''            print(f"  [simula] [{cat}] {nome} → titulo \\"{titulo}\\" ({p['tamanho'] / MB:.1f} MB)")'''
PARA = '''            print(f"  [simula] [{cat}/{secao}] {nome} → titulo \\"{titulo}\\" ({p['tamanho'] / MB:.1f} MB)")'''
assert DE in txt, "servidor_midias.py: print dry-run nao encontrado"
txt = txt.replace(DE, PARA)

DE = '''            chave, url, novo_id = publicar_um(creds, p["caminho"], titulo, cat,
                                              descricao, destaque,
                                              data or datetime.date.today().isoformat())
            manifesto["arquivos"][p["hash"]] = {
                "arquivo": nome, "categoria": cat, "titulo": titulo,'''
PARA = '''            chave, url, novo_id = publicar_um(creds, p["caminho"], titulo, cat,
                                              descricao, destaque,
                                              data or datetime.date.today().isoformat(),
                                              secao=secao)
            manifesto["arquivos"][p["hash"]] = {
                "arquivo": nome, "categoria": cat, "secao": secao, "titulo": titulo,'''
assert DE in txt, "servidor_midias.py: chamada publicar_um nao encontrada"
txt = txt.replace(DE, PARA)

DE = '''            print(f"  ✅ [{cat}] {nome} → id {novo_id} | {url}")'''
PARA = '''            print(f"  ✅ [{cat}/{secao}] {nome} → id {novo_id} | {url}")'''
assert DE in txt, "servidor_midias.py: print de sucesso nao encontrado"
txt = txt.replace(DE, PARA)

DE = '''            print(f"  ⚠️  [{cat}] {nome}: {e}")'''
PARA = '''            print(f"  ⚠️  [{cat}/{secao}] {nome}: {e}")'''
assert DE in txt, "servidor_midias.py: print de erro nao encontrado"
txt = txt.replace(DE, PARA)

open(p, "w", encoding="utf-8", newline="").write(txt)
print("  ✅ servidor_midias.py atualizado")

# ============================================================
# 3) SQL da coluna secao
# ============================================================
sql_path = os.path.join(BASE, "docs", "supabase-add-secao.sql")
open(sql_path, "w", encoding="utf-8", newline="").write('''-- ============================================================
-- Adiciona a coluna `secao` na tabela `arquivo`
-- Motivo: cada imagem agora pertence a uma PASTA DE SECAO dentro da
-- categoria (ex.: saude/hero, saude/carrossel, saude/galeria).
-- Rodar no SQL Editor do Supabase (projeto sersagi-site).
-- ============================================================

alter table public.arquivo
  add column if not exists secao text;

comment on column public.arquivo.secao is
  'Subpasta de secao dentro da categoria (ex.: hero, carrossel, galeria, imagem principal)';

-- Índice para o site filtrar por categoria + secao
create index if not exists arquivo_categoria_secao_idx
  on public.arquivo (categoria, secao);

-- Conferir:
-- select categoria, secao, count(*) from public.arquivo
--   where deleted = false group by 1,2 order by 1,2;
''')
print("  ✅ docs/supabase-add-secao.sql criado")
