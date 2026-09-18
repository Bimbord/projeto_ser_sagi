# -*- coding: utf-8 -*-
"""FASE 4b — confere as 22 seções novas (11 áreas × carrossel/galeria)."""
import os
import sys
import json
import urllib.error
import urllib.parse
import urllib.request

BASE = r"G:/.shortcut-targets-by-id/18wGiptBKUmAmmkKHgdfu05TU4y_roWC1/BBDPRINT - BACKUP/BBDPRINT/App BBDPRiNT/PROJETOS/Projeto SER Sagi/projeto_SER_Sagi - Hermes"
sys.path.insert(0, os.path.join(BASE, "scripts"))
from publicar import SUPABASE_URL, SUPABASE_ANON_KEY  # noqa: E402

# lê as seções direto do HTML (não inventa nada)
import glob
import re

secoes = []
for arq in sorted(glob.glob(os.path.join(BASE, "*.html"))):
    txt = open(arq, encoding="utf-8").read()
    for m in re.finditer(r'data-secao="([^"]+)" data-categoria="([^"]+)"(?: data-pagina="([^"]+)")?', txt):
        secao, cat, pag = m.group(1), m.group(2), m.group(3)
        secoes.append((os.path.basename(arq), cat, f"{pag}/{secao}" if pag else secao))

print(f"seções encontradas no HTML: {len(secoes)}\n")

ok = erro = 0
for arq, cat, secao in secoes:
    url = (f"{SUPABASE_URL}/rest/v1/arquivo?select=id"
           f"&categoria=eq.{urllib.parse.quote(cat)}"
           f"&secao=eq.{urllib.parse.quote(secao)}&deleted=eq.false")
    r = urllib.request.Request(url)
    r.add_header("apikey", SUPABASE_ANON_KEY)
    r.add_header("Authorization", f"Bearer {SUPABASE_ANON_KEY}")
    try:
        with urllib.request.urlopen(r, timeout=25) as resp:
            n = len(json.loads(resp.read().decode()))
            print(f"  ✅ {arq:30} {cat}/{secao:40} HTTP {resp.status} · {n} imagem(ns)")
            ok += 1
    except urllib.error.HTTPError as e:
        print(f"  ❌ {arq:30} {cat}/{secao:40} HTTP {e.code}")
        erro += 1

print(f"\n  {ok} OK · {erro} com erro")
