# -*- coding: utf-8 -*-
"""
Detalha as diferenças entre GitHub e local:
- tamanho (GitHub x local)
- se a diferença é só fim de linha (CRLF) ou conteúdo real
"""
import os, json, hashlib, urllib.request

BASE = r"C:/Projetos Code/Projeto SER Sagi/projeto_SER_Sagi - Hermes"
REPO = "Bimbord/projeto_ser_sagi"
RAW = f"https://raw.githubusercontent.com/{REPO}/main/"


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "hermes-check"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def api(url):
    return json.loads(fetch(url).decode())


def blob_hash(data):
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


tree = api(f"https://api.github.com/repos/{REPO}/git/trees/main?recursive=1")
remotos = {i["path"]: i for i in tree["tree"] if i["type"] == "blob"}

IGNORAR = (".git/", "__pycache__", "instagram-scrap", "cloudflare_tokens.txt", ".env")
locais = {}
for raiz, dirs, arqs in os.walk(BASE):
    for a in arqs:
        p = os.path.join(raiz, a)
        rel = os.path.relpath(p, BASE).replace("\\", "/")
        if any(x in rel for x in IGNORAR):
            continue
        locais[rel] = p

print(f"{'arquivo':<42} {'gh':>8} {'local':>8}  diagnóstico")
print("-" * 90)
import urllib.parse
so_crlf = conteudo = 0
for rel, info in sorted(remotos.items()):
    if rel not in locais:
        continue
    local_bytes = open(locais[rel], "rb").read()
    if blob_hash(local_bytes) == info["sha"]:
        continue
    # baixa do GitHub e compara ignorando CR
    try:
        gh_bytes = fetch(RAW + urllib.parse.quote(rel))
    except Exception as e:
        print(f"{rel:<42} {info['size']:>8} {len(local_bytes):>8}  ⚠️ erro ao baixar: {e}")
        continue
    gh_norm = gh_bytes.replace(b"\r\n", b"\n")
    lo_norm = local_bytes.replace(b"\r\n", b"\n")
    if gh_norm == lo_norm:
        diag = "só fim de linha (CRLF)"
        so_crlf += 1
    elif gh_norm == b"" and lo_norm == b"":
        diag = "vazios"
    else:
        diag = ">>> CONTEÚDO DIFERENTE <<<"
        conteudo += 1
    print(f"{rel:<42} {info['size']:>8} {len(local_bytes):>8}  {diag}")

print("-" * 90)
print(f"Resumo: {so_crlf} arquivo(s) diferem só por fim de linha | {conteudo} com conteúdo realmente diferente")
