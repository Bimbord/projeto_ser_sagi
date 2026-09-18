# -*- coding: utf-8 -*-
"""FASE 5 — diagnostico: quais tabelas existem no banco e o que a home ja consome."""
import sys, os, json, urllib.request, urllib.error

BASE = r"G:/.shortcut-targets-by-id/18wGiptBKUmAmmkKHgdfu05TU4y_roWC1/BBDPRINT - BACKUP/BBDPRINT/App BBDPRiNT/PROJETOS/Projeto SER Sagi/projeto_SER_Sagi - Hermes"
sys.path.insert(0, os.path.join(BASE, "scripts"))
from publicar import SUPABASE_URL, SUPABASE_ANON_KEY

TABELAS = ["arquivo", "depoimentos", "parceiros", "galeria", "pilares",
           "numeros", "leads", "contatos", "newsletter", "secoes"]

print("=== TABELAS NO BANCO ===")
for t in TABELAS:
    url = f"{SUPABASE_URL}/rest/v1/{t}?select=*&limit=1"
    req = urllib.request.Request(url)
    req.add_header("apikey", SUPABASE_ANON_KEY)
    req.add_header("Authorization", f"Bearer {SUPABASE_ANON_KEY}")
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            itens = json.loads(r.read().decode())
            print(f"  ✅ {t:12} HTTP {r.status}  ({len(itens)} amostra)")
            if itens:
                print(f"       colunas: {', '.join(itens[0].keys())}")
    except urllib.error.HTTPError as e:
        msg = e.read().decode()[:90].replace("\n", " ")
        print(f"  ❌ {t:12} HTTP {e.code}  {msg}")
    except Exception as e:
        print(f"  ⚠️  {t:12} {type(e).__name__}: {e}")

# quantos cards de numero existem na home (HTML fixo)
html = open(os.path.join(BASE, "index.html"), encoding="utf-8").read()
print("\n=== HOME ===")
print("  cards de número (home-stat) .......", html.count('class="home-stat"'))
print("  cards de pilar (home-pillar) ......", html.count('home-pillar"'))
print("  imagens ilustrativas (loremflickr) ", html.count("loremflickr"))
print("  blocos dinâmicos (data-render) ....", html.count("data-render="))
