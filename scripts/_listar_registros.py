# -*- coding: utf-8 -*-
"""Lista os registros da tabela arquivo (para localizar a imagem renomeada)."""
import sys, os, json, urllib.request

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
print(f"TOTAL: {len(linhas)} registros\n")
print("Imagens ligadas ao pag06_img03 (nome antigo 'Pag06 Img03'):")
for l in linhas:
    if "pag06-img03" in (l.get("imagem_url") or ""):
        print(f"  id={l['id']:3} | secao={str(l.get('secao')):18} | titulo='{l['titulo']}'")
        print(f"        {l['imagem_url']}")

print("\n--- TODOS os registros de Saúde (para referência) ---")
for l in linhas:
    if l["categoria"].startswith("Sa"):
        print(f"  id={l['id']:3} | {str(l.get('secao')):18} | {l['titulo']}")
