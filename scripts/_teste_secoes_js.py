# -*- coding: utf-8 -*-
"""Simula EXATAMENTE a URL que o js/main.js monta (encodeURIComponent em categoria/secao)."""
import sys, os, json, urllib.request, urllib.parse

BASE = r"G:/.shortcut-targets-by-id/18wGiptBKUmAmmkKHgdfu05TU4y_roWC1/BBDPRINT - BACKUP/BBDPRINT/App BBDPRiNT/PROJETOS/Projeto SER Sagi/projeto_SER_Sagi - Hermes"
sys.path.insert(0, os.path.join(BASE, "scripts"))
from publicar import SUPABASE_URL, SUPABASE_ANON_KEY

# encodeURIComponent equivalente em Python
enc = lambda s: urllib.parse.quote(s, safe="!~*'()")


def consultar(categoria, secao):
    url = (f"{SUPABASE_URL}/rest/v1/arquivo?select=id,titulo,imagem_url"
           f"&categoria=eq.{enc(categoria)}&secao=eq.{enc(secao)}"
           f"&deleted=eq.false&order=id.asc")
    req = urllib.request.Request(url)
    req.add_header("apikey", SUPABASE_ANON_KEY)
    req.add_header("Authorization", f"Bearer {SUPABASE_ANON_KEY}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())


for secao in ("hero", "imagem principal", "carrossel", "galeria"):
    try:
        itens = consultar("Saúde", secao)
        print(f"  [Saúde/{secao}] -> {len(itens)} imagem(ns)")
        for i in itens[:3]:
            print(f"      id={i['id']} | {i['titulo']}")
    except Exception as e:
        print(f"  ❌ [Saúde/{secao}] ERRO: {e}")
