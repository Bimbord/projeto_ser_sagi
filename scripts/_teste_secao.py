# -*- coding: utf-8 -*-
"""Verifica se a coluna `secao` existe na tabela arquivo (somente leitura)."""
import sys, os, json, urllib.request, urllib.error

BASE = r"G:/.shortcut-targets-by-id/18wGiptBKUmAmmkKHgdfu05TU4y_roWC1/BBDPRINT - BACKUP/BBDPRINT/App BBDPRiNT/PROJETOS/Projeto SER Sagi/projeto_SER_Sagi - Hermes"
sys.path.insert(0, os.path.join(BASE, "scripts"))
from publicar import SUPABASE_URL, SUPABASE_ANON_KEY

url = f"{SUPABASE_URL}/rest/v1/arquivo?select=id,titulo,categoria,secao&limit=5"
req = urllib.request.Request(url)
req.add_header("apikey", SUPABASE_ANON_KEY)
req.add_header("Authorization", f"Bearer {SUPABASE_ANON_KEY}")

try:
    with urllib.request.urlopen(req, timeout=30) as r:
        corpo = r.read().decode("utf-8")
    linhas = json.loads(corpo)
    print("HTTP", r.status, "- COLUNA `secao` EXISTE ✅")
    print("linhas retornadas:", len(linhas))
    for L in linhas:
        print(f"  id={L.get('id')} | {L.get('categoria')} | secao={L.get('secao')!r} | {L.get('titulo')}")
except urllib.error.HTTPError as e:
    print("❌ ERRO HTTP", e.code)
    print(e.read().decode("utf-8")[:600])
except Exception as e:
    print("❌ ERRO:", type(e).__name__, e)
