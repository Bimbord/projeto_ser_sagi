# -*- coding: utf-8 -*-
"""
Publicador — Projeto SER Sagi
==============================
Sobe mídias pro Cloudflare R2 E registra na tabela `arquivo` do Supabase.
É a porta de entrada pra alimentar o site.

MODO ÚNICO (1 arquivo):
    python publicar.py "C:\pasta\foto.jpg" "Título da foto" --categoria esporte --descricao "Texto" --destaque

MODO LOTE (pasta inteira):
    python publicar.py --pasta "C:\fotos-evento" --categoria eventos --titulo "Festa Junina" --destaque
    → importa todos os jpg/png/webp/mp4 da pasta, com títulos "Festa Junina — 01", "Festa Junina — 02"...

MODO INTERATIVO:
    python publicar.py   (pergunta tudo)

Flags:
    --categoria esporte|saude|educacao|cultura|preservacao|eventos
    --descricao "texto"
    --destaque          → marca como "Destaque do mês" (home)
    --data 2026-08-31   → data do registro (padrão: hoje)
    --titulo "Nome"     → (modo lote) base dos títulos

Credenciais R2: C:/Users/PRE-IMPRESSOR/R2/.r2-sagi.env
Anon key do Supabase é pública por design (fica no JS do site); RLS protege os dados.
"""
import os, sys, json, datetime, urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from upload_r2 import (s3_request, listar_objetos, proximo_nome, slugificar,
                       load_env, ENV_PATH, FOLDER_BY_EXT)

# ---------- Supabase (banco do site) ----------
SUPABASE_URL = "https://icrasqxbxmqbnelmkrei.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImljcmFzcXhieG1xYm5lbG1rcmVpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODgyMDYzOTUsImV4cCI6MjEwMzc4MjM5NX0.u7cWsqTRWIvJJ-jsU7BbcOw1cVI-Su8eJBL_pBaQb_g"

CATEGORIAS = {
    "esporte": "Esporte",
    "saude": "Saúde",
    "educacao": "Educação",
    "cultura": "Cultura",
    "preservacao": "Preservação",
    "eventos": "Eventos",
}
EXT_VIDEO = (".mp4", ".mov", ".webm", ".m4v")
EXT_SUPORTADAS = set(FOLDER_BY_EXT.keys())


def registrar_supabase(payload):
    """Insere uma linha na tabela arquivo. Retorna o id criado."""
    url = f"{SUPABASE_URL}/rest/v1/arquivo"
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, method="POST", data=data)
    req.add_header("Content-Type", "application/json")
    req.add_header("Prefer", "return=representation")  # pede a linha criada na resposta
    req.add_header("apikey", SUPABASE_ANON_KEY)
    req.add_header("Authorization", f"Bearer {SUPABASE_ANON_KEY}")
    with urllib.request.urlopen(req, timeout=30) as r:
        corpo = r.read().decode("utf-8")
    if not corpo.strip():
        return None
    criado = json.loads(corpo)
    return criado[0].get("id") if criado else None


def content_type_por_ext(ext):
    return {
        ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png",
        ".webp": "image/webp", ".gif": "image/gif",
        ".mp4": "video/mp4", ".mov": "video/quicktime",
        ".webm": "video/webm", ".m4v": "video/mp4",
        ".pdf": "application/pdf",
    }.get(ext, "application/octet-stream")


def publicar_um(creds, caminho, titulo, categoria_slug, descricao, destaque,
                data_registro, base=None):
    """Sobe 1 arquivo pro R2 e registra no Supabase. Retorna (chave, url, id)."""
    ext = os.path.splitext(caminho)[1].lower()
    folder = FOLDER_BY_EXT.get(ext)
    if not folder:
        raise ValueError(f"extensão {ext} não suportada")

    tipo = "video" if ext in EXT_VIDEO else "foto"
    categoria = CATEGORIAS[categoria_slug]
    if base is None:
        base = f"{categoria_slug}-{slugificar(titulo)[:40]}"

    existentes = listar_objetos(creds)
    chave = proximo_nome(existentes, folder, base, ext)

    with open(caminho, "rb") as f:
        body = f.read()
    s3_request(creds, "PUT", chave, body=body, content_type=content_type_por_ext(ext))

    public_url = creds.get("R2_PUBLIC_URL", "").rstrip("/")
    url_midia = f"{public_url}/{chave}"

    payload = {
        "titulo": titulo,
        "tipo": tipo,
        "categoria": categoria,
        "descricao": descricao,
        "data_registro": data_registro,
        "destaque": destaque,
        "deleted": False,
    }
    if tipo == "foto":
        payload["imagem_url"] = url_midia
    else:
        payload["video_url"] = url_midia

    novo_id = registrar_supabase(payload)
    return chave, url_midia, novo_id


def processar_lote(creds, pasta, categoria_slug, titulo_base, descricao,
                   destaque, data_registro):
    """Importa todos os arquivos de mídia de uma pasta."""
    arquivos = sorted(
        f for f in os.listdir(pasta)
        if os.path.splitext(f)[1].lower() in EXT_SUPORTADAS
    )
    if not arquivos:
        print("❌ Nenhum arquivo suportado (jpg/png/webp/gif/mp4/mov) na pasta.")
        return 0

    print(f"📦 Encontrados {len(arquivos)} arquivo(s) em: {pasta}\n")
    base = f"{categoria_slug}-{slugificar(titulo_base)[:40]}"
    ok, falhas = 0, []

    for i, arquivo in enumerate(arquivos, 1):
        caminho = os.path.join(pasta, arquivo)
        titulo = f"{titulo_base} — {i:02d}"
        try:
            chave, url, novo_id = publicar_um(creds, caminho, titulo, categoria_slug,
                                              descricao, destaque, data_registro, base=base)
            print(f"  ✅ {arquivo} → id {novo_id} ({chave})")
            ok += 1
        except Exception as e:
            print(f"  ⚠️  {arquivo}: {e}")
            falhas.append(arquivo)

    print(f"\n✅ Importados: {ok}/{len(arquivos)}")
    if falhas:
        print("⚠️  Falharam:", ", ".join(falhas))
    return ok


def main():
    creds = load_env(ENV_PATH)
    for k in ("R2_ACCOUNT_ID", "R2_ACCESS_KEY_ID", "R2_SECRET_ACCESS_KEY"):
        v = creds.get(k, "")
        if not v or "COLOQUE_AQUI" in v:
            print(f"❌ Credencial {k} não preenchida no arquivo .env")
            sys.exit(1)

    args = sys.argv[1:]

    # ---- parse ----
    caminho, pasta = None, None
    titulo, titulo_base, categoria_slug, descricao = None, None, None, ""
    destaque, data_registro = False, datetime.date.today().isoformat()

    for i, a in enumerate(args):
        if a == "--categoria" and i + 1 < len(args):
            categoria_slug = args[i + 1]
        elif a == "--descricao" and i + 1 < len(args):
            descricao = args[i + 1]
        elif a == "--destaque":
            destaque = True
        elif a == "--data" and i + 1 < len(args):
            data_registro = args[i + 1]
        elif a == "--pasta" and i + 1 < len(args):
            pasta = args[i + 1].strip('"')
        elif a == "--titulo" and i + 1 < len(args):
            titulo = titulo_base = args[i + 1]
        elif a.startswith("-"):
            continue
        elif caminho is None:
            caminho = a.strip('"')

    # ---- modo lote ----
    if pasta:
        if not os.path.isdir(pasta):
            print("❌ Pasta não encontrada:", pasta)
            sys.exit(1)
        if not titulo_base:
            titulo_base = input("🏷️  Título base (ex.: Festa Junina): ").strip()
        if not categoria_slug:
            print("📂 Categorias:", ", ".join(CATEGORIAS.keys()))
            categoria_slug = input("📂 Categoria: ").strip().lower()
        if categoria_slug not in CATEGORIAS:
            print(f"❌ Categoria inválida. Use: {', '.join(CATEGORIAS.keys())}")
            sys.exit(1)
        processar_lote(creds, pasta, categoria_slug, titulo_base, descricao,
                       destaque, data_registro)
        return

    # ---- modo único ----
    if not caminho:
        caminho = input("📁 Caminho do arquivo (ou arraste pra cá): ").strip('"').strip()
    if not titulo:
        titulo = input("🏷️  Título (ex.: Aula de jiu-jitsu): ").strip()
    if not categoria_slug:
        print("📂 Categorias:", ", ".join(CATEGORIAS.keys()))
        categoria_slug = input("📂 Categoria: ").strip().lower()

    if not os.path.isfile(caminho):
        print("❌ Arquivo não encontrado:", caminho)
        sys.exit(1)
    if not titulo:
        print("❌ Título é obrigatório.")
        sys.exit(1)
    if categoria_slug not in CATEGORIAS:
        print(f"❌ Categoria inválida. Use: {', '.join(CATEGORIAS.keys())}")
        sys.exit(1)

    print("\n⏳ Publicando...")
    try:
        chave, url, novo_id = publicar_um(creds, caminho, titulo, categoria_slug,
                                          descricao, destaque, data_registro)
    except Exception as e:
        print(f"⚠️  Falhou: {e}")
        sys.exit(1)

    print("\n✅ Publicado com sucesso!")
    print(f"   🆔 id: {novo_id}")
    print(f"   🏷️  {titulo} | {CATEGORIAS[categoria_slug]} | {'⭐ destaque' if destaque else 'sem destaque'}")
    print(f"   📎 URL: {url}")
    print("\n💡 O site já vai exibir este item no Acervo" + (" e nos Destaques da home." if destaque else "."))


if __name__ == "__main__":
    main()
