# -*- coding: utf-8 -*-
"""FASE 5 · Parte A — valida a consulta exata que o site faz para a home."""
import sys, os, json, urllib.request, urllib.error

BASE = r"G:/.shortcut-targets-by-id/18wGiptBKUmAmmkKHgdfu05TU4y_roWC1/BBDPRINT - BACKUP/BBDPRINT/App BBDPRiNT/PROJETOS/Projeto SER Sagi/projeto_SER_Sagi - Hermes"
sys.path.insert(0, os.path.join(BASE, "scripts"))
from publicar import SUPABASE_URL, SUPABASE_ANON_KEY


def consultar(categoria, secao):
    url = (f"{SUPABASE_URL}/rest/v1/arquivo?select=id,titulo,imagem_url"
           f"&categoria=eq.{urllib.parse.quote(categoria)}"
           f"&secao=eq.{urllib.parse.quote(secao)}"
           f"&deleted=eq.false&order=id.asc")
    req = urllib.request.Request(url)
    req.add_header("apikey", SUPABASE_ANON_KEY)
    req.add_header("Authorization", f"Bearer {SUPABASE_ANON_KEY}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.status, json.loads(r.read().decode())


CASOS = [
    ("Home", "hero",          "slideshow do topo (2+ fotos)"),
    ("Home", "joia-da-coroa", "imagem do card Jóia da Coroa"),
]

for cat, sec, desc in CASOS:
    try:
        status, itens = consultar(cat, sec)
        print(f"  ✅ HTTP {status} | {cat}/{sec} → {len(itens)} foto(s)  ({desc})")
        for i in itens:
            print(f"       id {i['id']}: {i['imagem_url'].split('/')[-1]}")
    except urllib.error.HTTPError as e:
        print(f"  ❌ ERRO {e.code} | {cat}/{sec} → {e.read().decode()[:120]}")

# simula a decisao do hero.js
status, itens = consultar("Home", "hero")
urls = [i["imagem_url"] for i in itens if i.get("imagem_url")]
if len(urls) >= 2:
    print(f"\n  🎬 hero.js escolheria: SLIDESHOW com {len(urls)} slides")
elif len(urls) == 1:
    print(f"\n  🖼️  hero.js escolheria: IMAGEM ÚNICA")
else:
    print(f"\n  ⚪ hero.js manteria: os slides LOCAIS (img/hero-slides/)")
