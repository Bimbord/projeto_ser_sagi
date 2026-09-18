# -*- coding: utf-8 -*-
"""
Limpa a demo dos cards de "Resultados" (home/numeros) e do teste em home/pilares.

Remove, em ordem:
  1. os registros no Supabase (deleted = true)
  2. os objetos no R2
  3. os arquivos arquivados em _publicados/home/
  4. confere que não sobrou nada ativo
"""
import os
import re
import subprocess
import sys

BASE = r"G:/.shortcut-targets-by-id/18wGiptBKUmAmmkKHgdfu05TU4y_roWC1/BBDPRINT - BACKUP/BBDPRINT/App BBDPRiNT/PROJETOS/Projeto SER Sagi/projeto_SER_Sagi - Hermes"
S = r"G:/Meu Drive/Instituto SER Sagi - PARA O SITE"

CHAVES_R2 = [
    "fotos/home-projeto-principal.png", "fotos/home-saude.png", "fotos/home-consultorio.png",
    "fotos/home-esporte.png", "fotos/home-esporte-001.png", "fotos/home-jiu-jitsu.png",
    "fotos/home-musculacao.png",
]

print("=== 1) registros no banco ===")
# descobre os ids ativos das seções usadas na demo
sys.path.insert(0, os.path.join(BASE, "scripts"))
from supabase_admin import SUPABASE_URL, admin_headers  # noqa: E402
import json  # noqa: E402
import urllib.request  # noqa: E402

ids = []
for sec in ("numeros", "pilares"):
    url = f"{SUPABASE_URL}/rest/v1/arquivo?select=id&categoria=eq.Home&secao=eq.{sec}&deleted=eq.false"
    r = urllib.request.Request(url)
    for k, v in admin_headers().items():
        r.add_header(k, v)
    with urllib.request.urlopen(r, timeout=30) as resp:
        ids += [i["id"] for i in json.loads(resp.read().decode())]

print(f"  ids ativos em Home/numeros e Home/pilares: {ids}")
if ids:
    subprocess.run([sys.executable, os.path.join(BASE, "scripts", "excluir.py"),
                    "--tabela", "arquivo", "--ids", ",".join(map(str, ids))],
                   cwd=BASE, check=False)

print("\n=== 2) objetos no R2 ===")
for chave in CHAVES_R2:
    subprocess.run([sys.executable, os.path.join(BASE, "scripts", "upload_r2.py"), "--delete", chave],
                   cwd=BASE, check=False, stdout=subprocess.DEVNULL)
    print(f"  🗑️  {chave}")

print("\n=== 3) _publicados/home ===")
p = os.path.join(S, "_publicados", "home")
if os.path.isdir(p):
    for f in sorted(os.listdir(p)):
        os.remove(os.path.join(p, f))
        print(f"  🗑️  {f}")
    try:
        os.rmdir(p)
        print("  🗑️  pasta _publicados/home removida")
    except OSError:
        pass
else:
    print("  (não existia)")

print("\n=== 4) conferência final ===")
for sec in ("numeros", "pilares", "como-ajudar", "joia-da-coroa"):
    url = f"{SUPABASE_URL}/rest/v1/arquivo?select=id&categoria=eq.Home&secao=eq.{sec}&deleted=eq.false"
    r = urllib.request.Request(url)
    for k, v in admin_headers().items():
        r.add_header(k, v)
    with urllib.request.urlopen(r, timeout=30) as resp:
        n = len(json.loads(resp.read().decode()))
    print(f"  Home/{sec:14} -> {n} registro(s) ativo(s)  {'✅' if n == 0 else '⚠️ '}")
