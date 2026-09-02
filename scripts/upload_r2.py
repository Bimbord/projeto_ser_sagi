# -*- coding: utf-8 -*-
"""
Upload para o Cloudflare R2 — Projeto SER Sagi
================================================
Ferramenta para subir fotos/vídeos/documentos do computador para o bucket,
com nome organizado e URL pública na saída.

Uso interativo:
    python upload_r2.py
    → informa o caminho do arquivo (pode arrastar pra dentro do terminal)
    → dá um nome curto (ex.: esporte-jiu-jitsu)
    → sobe pro bucket e mostra a URL pública

Uso direto:
    python upload_r2.py "C:\pasta\foto.jpg" esporte-jiu-jitsu

Manutenção:
    python upload_r2.py --list                          → lista todos os objetos
    python upload_r2.py --delete fotos/arquivo.jpg      → apaga um objeto
    python upload_r2.py --delete-prefix arcevo/         → apaga tudo que começa com o prefixo (pasta)

As credenciais ficam em C:/Users/PRE-IMPRESSOR/R2/.r2-sagi.env
"""
import os, sys, re, datetime, hashlib, hmac, urllib.request, mimetypes

ENV_PATH = r"C:/Users/PRE-IMPRESSOR/R2/.r2-sagi.env"

# Extensões -> pasta de destino
FOLDER_BY_EXT = {
    ".jpg": "fotos/", ".jpeg": "fotos/", ".png": "fotos/", ".webp": "fotos/", ".gif": "fotos/", ".heic": "fotos/",
    ".mp4": "videos/", ".mov": "videos/", ".webm": "videos/", ".m4v": "videos/",
    ".pdf": "docs/",
}


def load_env(path):
    creds = {}
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        creds[k.strip()] = v.strip()
    return creds


# ---------- AWS SigV4 ----------
def _sign(key, msg):
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()


def _sig_key(secret, date_stamp, region, service):
    k_date = _sign(("AWS4" + secret).encode("utf-8"), date_stamp)
    k_region = _sign(k_date, region)
    k_service = _sign(k_region, service)
    return _sign(k_service, "aws4_request")


def s3_request(creds, method, key, body=b"", content_type=None):
    account = creds["R2_ACCOUNT_ID"]
    ak = creds["R2_ACCESS_KEY_ID"]
    sk = creds["R2_SECRET_ACCESS_KEY"]
    bucket = creds["R2_BUCKET"]
    region, service = "auto", "s3"
    host = f"{account}.r2.cloudflarestorage.com"

    now = datetime.datetime.now(datetime.timezone.utc)
    amz_date = now.strftime("%Y%m%dT%H%M%SZ")
    date_stamp = now.strftime("%Y%m%d")

    payload_hash = hashlib.sha256(body).hexdigest()
    canonical_uri = f"/{bucket}/{key}"
    canonical_headers = f"host:{host}\nx-amz-content-sha256:{payload_hash}\nx-amz-date:{amz_date}\n"
    signed_headers = "host;x-amz-content-sha256;x-amz-date"
    canonical_request = "\n".join([method, canonical_uri, "", canonical_headers, signed_headers, payload_hash])

    scope = f"{date_stamp}/{region}/{service}/aws4_request"
    string_to_sign = "\n".join(["AWS4-HMAC-SHA256", amz_date, scope,
                                hashlib.sha256(canonical_request.encode()).hexdigest()])
    signing_key = _sig_key(sk, date_stamp, region, service)
    signature = hmac.new(signing_key, string_to_sign.encode(), hashlib.sha256).hexdigest()
    auth = f"AWS4-HMAC-SHA256 Credential={ak}/{scope}, SignedHeaders={signed_headers}, Signature={signature}"

    url = f"https://{host}/{bucket}/{key}"
    req = urllib.request.Request(url, method=method, data=body)
    req.add_header("Authorization", auth)
    req.add_header("x-amz-date", amz_date)
    req.add_header("x-amz-content-sha256", payload_hash)
    req.add_header("Host", host)
    if content_type:
        req.add_header("Content-Type", content_type)
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.status


def listar_objetos(creds):
    """Lista as chaves (caminhos) de todos os objetos do bucket."""
    account = creds["R2_ACCOUNT_ID"]
    ak = creds["R2_ACCESS_KEY_ID"]
    sk = creds["R2_SECRET_ACCESS_KEY"]
    bucket = creds["R2_BUCKET"]
    region, service = "auto", "s3"
    host = f"{account}.r2.cloudflarestorage.com"
    now = datetime.datetime.now(datetime.timezone.utc)
    amz_date = now.strftime("%Y%m%dT%H%M%SZ")
    date_stamp = now.strftime("%Y%m%d")
    payload_hash = hashlib.sha256(b"").hexdigest()
    query = "list-type=2&max-keys=1000"
    canonical_uri = f"/{bucket}"
    canonical_headers = f"host:{host}\nx-amz-content-sha256:{payload_hash}\nx-amz-date:{amz_date}\n"
    signed_headers = "host;x-amz-content-sha256;x-amz-date"
    canonical_request = "\n".join(["GET", canonical_uri, query, canonical_headers, signed_headers, payload_hash])
    scope = f"{date_stamp}/{region}/{service}/aws4_request"
    string_to_sign = "\n".join(["AWS4-HMAC-SHA256", amz_date, scope,
                                hashlib.sha256(canonical_request.encode()).hexdigest()])
    signing_key = _sig_key(sk, date_stamp, region, service)
    signature = hmac.new(signing_key, string_to_sign.encode(), hashlib.sha256).hexdigest()
    auth = f"AWS4-HMAC-SHA256 Credential={ak}/{scope}, SignedHeaders={signed_headers}, Signature={signature}"
    url = f"https://{host}/{bucket}?{query}"
    req = urllib.request.Request(url, method="GET")
    req.add_header("Authorization", auth)
    req.add_header("x-amz-date", amz_date)
    req.add_header("x-amz-content-sha256", payload_hash)
    req.add_header("Host", host)
    with urllib.request.urlopen(req, timeout=25) as r:
        body = r.read().decode("utf-8", "replace")
    return re.findall(r"<Key>([^<]+)</Key>", body)


def slugificar(texto):
    """Converte texto em slug: minúsculo, hífens, sem acentos/espaços."""
    mapa = {
        "á": "a", "à": "a", "ã": "a", "â": "a", "ä": "a",
        "é": "e", "è": "e", "ê": "e", "ë": "e",
        "í": "i", "ì": "i", "î": "i", "ï": "i",
        "ó": "o", "ò": "o", "õ": "o", "ô": "o", "ö": "o",
        "ú": "u", "ù": "u", "û": "u", "ü": "u",
        "ç": "c", "ñ": "n",
    }
    t = texto.lower().strip()
    for a, b in mapa.items():
        t = t.replace(a, b)
    t = re.sub(r"[^a-z0-9]+", "-", t)
    t = re.sub(r"-{2,}", "-", t).strip("-")
    return t


def proximo_nome(existentes, folder, base, ext):
    """Garante nome único: base-001.ext, base-002.ext... (ext já inclui o ponto, ex.: .png)"""
    prefixo = f"{folder}{base}"
    existentes = {k for k in existentes if k.startswith(prefixo)}
    if f"{prefixo}{ext}" not in existentes:
        return f"{prefixo}{ext}"
    n = 1
    while f"{prefixo}-{n:03d}{ext}" in existentes:
        n += 1
    return f"{prefixo}-{n:03d}{ext}"


def main():
    creds = load_env(ENV_PATH)
    for k in ("R2_ACCOUNT_ID", "R2_ACCESS_KEY_ID", "R2_SECRET_ACCESS_KEY"):
        v = creds.get(k, "")
        if not v or "COLOQUE_AQUI" in v:
            print(f"❌ Credencial {k} não preenchida no arquivo .env")
            sys.exit(1)

    args = sys.argv[1:]

    # ---------- Modos de manutenção ----------
    if args and args[0] == "--list":
        print("⏳ Listando objetos...\n")
        for chave in listar_objetos(creds):
            print("  📄", chave)
        return

    if args and args[0] == "--delete":
        if len(args) < 2:
            print("❌ Uso: python upload_r2.py --delete <chave>")
            sys.exit(1)
        chave = args[1].strip('/')
        print(f"🗑️  Apagando {chave} ...")
        s3_request(creds, "DELETE", chave)
        print("✅ Apagado!")
        return

    if args and args[0] == "--delete-prefix":
        if len(args) < 2:
            print("❌ Uso: python upload_r2.py --delete-prefix <prefixo>")
            sys.exit(1)
        prefixo = args[1]
        if not prefixo.endswith("/"):
            prefixo += "/"
        print(f"⏳ Buscando objetos em {prefixo} ...")
        alvos = [k for k in listar_objetos(creds) if k.startswith(prefixo)]
        if not alvos:
            print("ℹ️  Nada encontrado com esse prefixo.")
            return
        print(f"🗑️  Apagando {len(alvos)} objeto(s)...")
        for chave in alvos:
            s3_request(creds, "DELETE", chave)
            print("   ✅", chave)
        print("✅ Limpeza concluída!")
        return

    if len(args) >= 1:
        caminho = args[0].strip('"')
    else:
        caminho = input("📁 Caminho do arquivo (ou arraste pra cá): ").strip('"').strip()

    if not os.path.isfile(caminho):
        print("❌ Arquivo não encontrado:", caminho)
        sys.exit(1)

    ext = os.path.splitext(caminho)[1].lower()
    folder = FOLDER_BY_EXT.get(ext)
    if not folder:
        print(f"❌ Extensão {ext} não suportada. Usar: jpg/png/webp/gif (foto), mp4/mov (vídeo), pdf (doc)")
        sys.exit(1)

    if len(args) >= 2:
        base = slugificar(args[1])
    else:
        base = slugificar(input("📝 Nome curto (ex.: esporte-jiu-jitsu): ").strip())
        if not base:
            base = slugificar(os.path.splitext(os.path.basename(caminho))[0])

    print("\n⏳ Conectando ao bucket...")
    existentes = listar_objetos(creds)
    chave = proximo_nome(existentes, folder, base, ext)

    content_type = mimetypes.guess_type(caminho)[0] or "application/octet-stream"
    with open(caminho, "rb") as f:
        body = f.read()

    print(f"⬆️  Enviando {os.path.basename(caminho)} → {chave} ...")
    s3_request(creds, "PUT", chave, body=body, content_type=content_type)

    public_url = creds.get("R2_PUBLIC_URL", "").rstrip("/")
    url = f"{public_url}/{chave}"
    print("\n✅ Upload concluído!")
    print(f"📎 URL pública:\n   {url}")
    print("\n💡 Use essa URL no site (tabela arquivo.imagem_url) ou compartilhe à vontade.")


if __name__ == "__main__":
    main()
