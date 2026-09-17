# -*- coding: utf-8 -*-
"""Confere: registros na tabela arquivo agrupados por categoria+secao, e testa URLs."""
import sys, os, json, urllib.request, urllib.error
from collections import Counter

BASE = r"G:/.shortcut-targets-by-id/18wGiptBKUmAmmkKHgdfu05TU4y_roWC1/BBDPRINT - BACKUP/BBDPRINT/App BBDPRiNT/PROJETOS/Projeto SER Sagi/projeto_SER_Sagi - Hermes"
sys.path.insert(0, os.path.join(BASE, "scripts"))
from publicar import SUPABASE_URL, SUPABASE_ANON_KEY


def api(path):
    req = urllib.request.Request(f"{SUPABASE_URL}/rest/v1/{path}")
    req.add_header("apikey", SUPABASE_ANON_KEY)
    req.add_header("Authorization", f"Bearer {SUPABASE_ANON_KEY}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())


linhas = api("arquivo?select=id,titulo,categoria,secao,imagem_url&deleted=eq.false&order=id.asc")
print(f"TOTAL DE REGISTROS: {len(linhas)}\n")

cont = Counter((l["categoria"], l.get("secao")) for l in linhas)
print("POR CATEGORIA / SECAO:")
for (cat, sec), n in sorted(cont.items(), key=lambda x: (x[0][0], str(x[0][1]))):
    print(f"  {cat:12} | {str(sec):20} | {n} imagem(ns)")

print("\nDETALHE DA SAUDE:")
for l in linhas:
    if l["categoria"].startswith("Sa"):
        print(f"  id={l['id']:3} | {str(l.get('secao')):18} | {l['titulo']}")

hero = [l for l in linhas if l.get("secao") == "hero"]
if hero:
    u = hero[0]["imagem_url"]
    try:
        with urllib.request.urlopen(u, timeout=30) as r:
            dados = r.read()
        print(f"\nTESTE DA URL DO HERO: HTTP {r.status} | {r.headers.get('Content-Type')} | {len(dados)} bytes")
        print(f"  {u}")
    except Exception as e:
        print("\n❌ falha ao baixar a imagem do hero:", e)
