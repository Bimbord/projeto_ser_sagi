# -*- coding: utf-8 -*-
"""
Servidor de Midias - Projeto SER Sagi
=====================================
Ponte Google Drive -> Cloudflare R2 + Supabase (fase 2 da alimentacao do site).

COMO FUNCIONA
-------------
A ONG sobe o material "cru" na pasta compartilhada (caixa de entrada).
O responsavel aprova e move o que serve para a PASTA ESPELHO, uma subpasta
por categoria do site:

    G:\\Meu Drive\\Instituto SER Sagi - PARA O SITE\\
        esporte\\  saude\\  educacao\\  cultura\\  preservacao\\  eventos\\
        _publicados\\            (arquivo do que ja subiu)

Este script le o que esta nas pastas de categoria, sobe pro R2, registra no
Supabase (tabela `arquivo`), move o arquivo para `_publicados\\<categoria>\\`
e anota tudo no manifesto `_publicados\\publicados.json` (guardado NO DRIVE,
nao no C: - sobrevive a qualquer problema no PC).

USO
---
    python scripts/servidor_midias.py --status      # o que chegou / o que ja foi
    python scripts/servidor_midias.py --dry-run     # simula (nao sobe nada)
    python scripts/servidor_midias.py --publicar    # publica de verdade

FLAGS
-----
    --limite-gb N    para depois de acumular N GB na rodada (padrao 1.0)
    --max-mb N       pula arquivo maior que N MB (padrao 800) - protege a RAM
    --categoria X    processa so a categoria X
    --autorizado     registra no manifesto que a conferencia de autorizacao
                     de uso de imagem foi feita (ECA + LGPD). Nao bloqueia.

COMO NOMEAR OS ARQUIVOS
-----------------------
Comece com a data (AAAA-MM-DD) e descreva o evento - o script usa isso:

    2026-09-14-festa-das-criancas-01.jpg
        -> titulo "Festa Das Criancas 01"  |  data "2026-09-14"

ARQUIVO OPCIONAL `_info.txt` (por pasta de categoria)
----------------------------------------------------
    titulo_base=Festa Junina 2026      -> titulos viram "Festa Junina 2026 - 01", "- 02"...
    descricao=Comemoração na comunidade
    destaque=1                         -> aparece nos Destaques da home (max 3!)
    autorizado=sim

LIMITES CONHECIDOS
------------------
- O arquivo e lido para a memoria antes de subir (igual ao publicar.py).
  Com 1 GB por rodada e trava de 800 MB/arquivo isso fica seguro.
- Nada e copiado para o C: - os bytes vao do Drive direto pro R2.
- PDFs nao entram no Acervo (nao ha area de documentos no site): use
  `python scripts/upload_r2.py` para subir documentos avulsos.

Credenciais R2: C:/Users/PRE-IMPRESSOR/R2/.r2-sagi.env (nunca commitar).
"""
import os
import re
import sys
import json
import shutil
import hashlib
import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from publicar import (publicar_um, CATEGORIAS, EXT_SUPORTADAS, EXT_VIDEO,
                      load_env, ENV_PATH)

# ---------- Configuracao ----------
BASE = r"G:/Meu Drive/Instituto SER Sagi - PARA O SITE"
MANIFEST_PATH = os.path.join(BASE, "_publicados", "publicados.json")
INFO_FILENAME = "_info.txt"
LIMITE_GB_PADRAO = 1.0
MAX_MB_PADRAO = 800
MB = 1024 * 1024


# ---------- Utilidades ----------
def cor(txt, codigo):
    return f"\033[{codigo}m{txt}\033[0m" if sys.stdout.isatty() else txt


def espaco_livre_c_gb():
    try:
        return shutil.disk_usage("C:/").free / (1024 ** 3)
    except Exception:
        return -1.0


def titulo_e_data(nome_arquivo):
    """Deriva titulo e data do nome do arquivo. Ex.: 2026-09-14-festa-01.jpg"""
    base = os.path.splitext(nome_arquivo)[0]
    data = None
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})[-_ ]*(.*)", base)
    if m:
        data = f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
        resto = m.group(4)
    else:
        resto = base
    resto = re.sub(r"[-_]+", " ", resto).strip()
    resto = re.sub(r"\s+", " ", resto)
    if not resto:
        resto = base
    return resto.title(), data


def hash_arquivo(caminho, bloco=MB):
    h = hashlib.sha256()
    with open(caminho, "rb") as f:
        for pedaco in iter(lambda: f.read(bloco), b""):
            h.update(pedaco)
    return h.hexdigest()


def ler_info(pasta):
    """Le o _info.txt da pasta, se existir. Retorna dict."""
    caminho = os.path.join(pasta, INFO_FILENAME)
    info = {}
    if not os.path.isfile(caminho):
        return info
    with open(caminho, encoding="utf-8", errors="ignore") as f:
        for linha in f:
            linha = linha.strip()
            if not linha or linha.startswith("#") or "=" not in linha:
                continue
            k, v = linha.split("=", 1)
            info[k.strip().lower()] = v.strip()
    return info


def carregar_manifesto():
    if os.path.isfile(MANIFEST_PATH):
        try:
            with open(MANIFEST_PATH, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"arquivos": {}, "atualizado": None}


def salvar_manifesto(manifesto):
    os.makedirs(os.path.dirname(MANIFEST_PATH), exist_ok=True)
    manifesto["atualizado"] = datetime.datetime.now().isoformat(timespec="seconds")
    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifesto, f, ensure_ascii=False, indent=2)


def mover_para_publicados(caminho, categoria, nome):
    destino_dir = os.path.join(BASE, "_publicados", categoria)
    os.makedirs(destino_dir, exist_ok=True)
    destino = os.path.join(destino_dir, nome)
    if os.path.exists(destino):
        raiz, ext = os.path.splitext(nome)
        destino = os.path.join(destino_dir, f"{raiz}-dup{ext}")
    shutil.move(caminho, destino)
    return destino


def varrer(manifesto, categoria_filtro=None, max_mb=MAX_MB_PADRAO):
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
    return pendentes, ja_publicados, ignorados


def validar_creds(creds):
    for k in ("R2_ACCOUNT_ID", "R2_ACCESS_KEY_ID", "R2_SECRET_ACCESS_KEY"):
        v = creds.get(k, "")
        if not v or "COLOQUE_AQUI" in v:
            print(f"❌ Credencial {k} nao preenchida em {ENV_PATH}")
            sys.exit(1)


# ---------- Modos ----------
def modo_status(pendentes, ja_publicados, ignorados):
    print("=" * 62)
    print("SERVIDOR DE MIDIAS - STATUS")
    print("=" * 62)

    if pendentes:
        print(f"\n📥 PARA PUBLICAR ({len(pendentes)} arquivo(s)):")
        for p in pendentes:
            print(f"   [{p['categoria']:11}] {p['nome']}  ({p['tamanho'] / MB:.1f} MB)")
        total = sum(p["tamanho"] for p in pendentes)
        print(f"   → total: {total / MB:.1f} MB")
    else:
        print("\n📥 PARA PUBLICAR: nada novo.")

    if ja_publicados:
        print(f"\n✅ JA PUBLICADOS na pasta ({len(ja_publicados)}) - serao ignorados:")
        for cat, nome, reg in ja_publicados[:10]:
            print(f"   [{cat:11}] {nome} → id {reg.get('id')}")
        if len(ja_publicados) > 10:
            print(f"   ... e mais {len(ja_publicados) - 10}")

    if ignorados:
        print(f"\n⚠️  IGNORADOS ({len(ignorados)}):")
        for cat, nome, motivo in ignorados:
            print(f"   [{cat:11}] {nome} → {motivo}")

    livre = espaco_livre_c_gb()
    print(f"\n💾 Espaco livre no C: {livre:.1f} GB")
    if livre < 5:
        print("   ⚠️  Pouco espaco! O cache do Google Drive usa o C:.")
    print(f"📄 Manifesto: {MANIFEST_PATH} ({len(carregar_manifesto()['arquivos'])} item(ns))")


def modo_publicar(pendentes, manifesto, creds, autorizado, dry_run=False,
                  limite_gb=LIMITE_GB_PADRAO):
    if not pendentes:
        print("Nada novo para publicar. 👍")
        return 0

    limite_bytes = limite_gb * 1024 ** 3
    acumulado, ok, falhas = 0, 0, []
    parou_por_limite = False

    prefixo = "[SIMULACAO] " if dry_run else ""
    print(f"{prefixo}Publicando {len(pendentes)} arquivo(s) (limite {limite_gb} GB nesta rodada)...\n")

    contador_por_categoria = {}
    for p in pendentes:
        if acumulado + p["tamanho"] > limite_bytes and acumulado > 0:
            parou_por_limite = True
            break

        cat, nome = p["categoria"], p["nome"]
        contador_por_categoria[cat] = contador_por_categoria.get(cat, 0) + 1
        info = p["info"]
        titulo, data = titulo_e_data(nome)

        if info.get("titulo_base"):
            titulo = f"{info['titulo_base']} — {contador_por_categoria[cat]:02d}"
        descricao = info.get("descricao", "")
        destaque = str(info.get("destaque", "")).strip().lower() in ("1", "sim", "true", "s")

        if dry_run:
            print(f"  [simula] [{cat}] {nome} → titulo \"{titulo}\" ({p['tamanho'] / MB:.1f} MB)")
            acumulado += p["tamanho"]
            continue

        try:
            chave, url, novo_id = publicar_um(creds, p["caminho"], titulo, cat,
                                              descricao, destaque,
                                              data or datetime.date.today().isoformat())
            manifesto["arquivos"][p["hash"]] = {
                "arquivo": nome, "categoria": cat, "titulo": titulo,
                "id": novo_id, "url": url, "chave": chave,
                "tamanho": p["tamanho"], "publicado_em": datetime.date.today().isoformat(),
                "autorizado": bool(autorizado), "destaque": destaque,
            }
            salvar_manifesto(manifesto)
            mover_para_publicados(p["caminho"], cat, nome)
            print(f"  ✅ [{cat}] {nome} → id {novo_id} | {url}")
            ok += 1
        except Exception as e:
            print(f"  ⚠️  [{cat}] {nome}: {e}")
            falhas.append(nome)
        acumulado += p["tamanho"]

    print(f"\n{prefixo}Resultado: {ok} publicado(s)"
          + (f", {len(falhas)} falha(s)" if falhas else ""))
    if falhas:
        print("   Falharam:", ", ".join(falhas))
    if parou_por_limite:
        print(f"   ⏸️  Parou no limite de {limite_gb} GB - rode de novo para continuar.")
    if ok and not dry_run:
        print("   📦 Os arquivos publicados foram movidos para _publicados\\<categoria>\\.")
    return ok


def main():
    args = sys.argv[1:]
    modo = None
    categoria_filtro = None
    limite_gb = LIMITE_GB_PADRAO
    max_mb = MAX_MB_PADRAO
    autorizado = False

    for i, a in enumerate(args):
        if a == "--status":
            modo = "status"
        elif a == "--dry-run":
            modo = "dry-run"
        elif a == "--publicar":
            modo = "publicar"
        elif a == "--autorizado":
            autorizado = True
        elif a == "--categoria" and i + 1 < len(args):
            categoria_filtro = args[i + 1].strip().lower()
        elif a == "--limite-gb" and i + 1 < len(args):
            limite_gb = float(args[i + 1])
        elif a == "--max-mb" and i + 1 < len(args):
            max_mb = int(args[i + 1])

    if modo is None:
        modo = "status"

    if not os.path.isdir(BASE):
        print(f"❌ Pasta espelho nao encontrada:\n{BASE}")
        print("   Crie as pastas por categoria (esporte, saude, educacao, cultura,")
        print("   preservacao, eventos) e a subpasta _publicados.")
        sys.exit(1)

    if categoria_filtro and categoria_filtro not in CATEGORIAS:
        print(f"❌ Categoria invalida. Use: {', '.join(CATEGORIAS.keys())}")
        sys.exit(1)

    manifesto = carregar_manifesto()
    pendentes, ja_publicados, ignorados = varrer(manifesto, categoria_filtro, max_mb)

    if modo == "status":
        modo_status(pendentes, ja_publicados, ignorados)
        return

    creds = load_env(ENV_PATH)
    validar_creds(creds)
    modo_publicar(pendentes, manifesto, creds, autorizado,
                  dry_run=(modo == "dry-run"), limite_gb=limite_gb)


if __name__ == "__main__":
    main()
