# -*- coding: utf-8 -*-
"""
FASE 2 — valida a CONSULTA com secao em caminho (ex.: "volei/hero").

Simula exatamente a URL que o js/main.js monta quando a pagina tem
data-pagina="volei" data-secao="hero".

Espera: HTTP 200 e lista vazia (ainda nao ha imagem publicada nessa secao).
O importante e nao dar erro — prova que a barra funciona na consulta.
"""
import sys, os, json, urllib.request, urllib.error, urllib.parse

BASE = r"G:/.shortcut-targets-by-id/18wGiptBKUmAmmkKHgdfu05TU4y_roWC1/BBDPRINT - BACKUP/BBDPRINT/App BBDPRiNT/PROJETOS/Projeto SER Sagi/projeto_SER_Sagi - Hermes"
sys.path.insert(0, os.path.join(BASE, "scripts"))
from publicar import SUPABASE_URL, SUPABASE_ANON_KEY

enc = lambda s: urllib.parse.quote(s, safe="!~*'()")


def consultar(categoria, secao):
    url = (f"{SUPABASE_URL}/rest/v1/arquivo?select=id,titulo,secao,imagem_url"
           f"&categoria=eq.{enc(categoria)}&secao=eq.{enc(secao)}"
           f"&deleted=eq.false&order=id.asc")
    req = urllib.request.Request(url)
    req.add_header("apikey", SUPABASE_ANON_KEY)
    req.add_header("Authorization", f"Bearer {SUPABASE_ANON_KEY}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.status, json.loads(r.read().decode())


testes = [
    ("Esporte", "hero"),          # hub Esporte
    ("Esporte", "volei/hero"),    # pagina Volei (secao em caminho)
    ("Esporte", "volei/carrossel"),
    ("Educação", "ingles/galeria"),
    ("Saúde", "carrossel"),       # ja existe (4 imagens)
]

for cat, sec in testes:
    try:
        status, itens = consultar(cat, sec)
        print(f"  ✅ HTTP {status} | [{cat}/{sec}] -> {len(itens)} imagem(ns)")
    except urllib.error.HTTPError as e:
        print(f"  ❌ ERRO {e.code} | [{cat}/{sec}] -> {e.read().decode()[:150]}")

print("\n(200 + lista vazia = a barra funciona; só falta publicar imagem nessas seções)")
