# -*- coding: utf-8 -*-
"""
cadastrar.py — cadastra depoimentos e parceiros da home.

Exemplos
--------
# Depoimento em destaque na home (aparece nos 3 cards)
python scripts/cadastrar.py --depoimento "Ana Paula" --perfil "Mãe" \
    --local "Praia do Sagi" --texto "Desde que começou..." \
    --legenda "Ana Paula e o filho na entrega dos uniformes" --destaque

# Depoimento comum (aparece só na página depoimentos.html)
python scripts/cadastrar.py --depoimento "Carlos Henrique" --perfil "Pai" \
    --texto "O Instituto trouxe oportunidade de verdade..."

# Vídeo do YouTube (opcional — tem prioridade sobre a mídia do Drive)
python scripts/cadastrar.py --depoimento "João Miguel" --perfil "Criança" \
    --texto "Eu gosto muito do jiu-jitsu" --video "https://youtu.be/XXXX"

# Parceiro
python scripts/cadastrar.py --parceiro "Grupo Atlântico" \
    --categoria "Empresa apoiadora" --descricao "Apoio institucional..."

# Listar
python scripts/cadastrar.py --listar depoimentos
python scripts/cadastrar.py --listar parceiros

A MÍDIA (foto/vídeo) normalmente NÃO vai por aqui: coloque o arquivo na
pasta home/depoimentos do Drive com o nome igual ao da pessoa
("ana-paula.jpg") e o site casa sozinho. Use --imagem/--video apenas
para apontar uma URL externa.
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from publicar import SUPABASE_URL, SUPABASE_ANON_KEY  # noqa: E402

HEADERS = {
    "apikey": SUPABASE_ANON_KEY,
    "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
    "Content-Type": "application/json",
}


def inserir(tabela, dados):
    req = urllib.request.Request(f"{SUPABASE_URL}/rest/v1/{tabela}", method="POST",
                                 data=json.dumps(dados, ensure_ascii=False).encode("utf-8"))
    for k, v in HEADERS.items():
        req.add_header(k, v)
    req.add_header("Prefer", "return=representation")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())


def listar(tabela):
    url = f"{SUPABASE_URL}/rest/v1/{tabela}?select=*&deleted=eq.false&order=id.asc"
    req = urllib.request.Request(url)
    for k, v in HEADERS.items():
        if k != "Content-Type":
            req.add_header(k, v)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())


def main():
    ap = argparse.ArgumentParser(description="Cadastra depoimentos e parceiros do site.")
    ap.add_argument("--depoimento", metavar="NOME", help="cadastra um depoimento com este nome")
    ap.add_argument("--parceiro", metavar="NOME", help="cadastra um parceiro com este nome")
    ap.add_argument("--listar", choices=["depoimentos", "parceiros"], help="lista os registros ativos")

    for campo in ("perfil", "local", "texto", "legenda", "imagem", "video",
                  "categoria", "descricao", "logo-texto", "logo"):
        ap.add_argument(f"--{campo}", default=None)
    ap.add_argument("--ordem", type=int, default=0)
    ap.add_argument("--destaque", action="store_true", help="aparece nos cards da home")

    a = ap.parse_args()

    try:
        if a.listar:
            itens = listar(a.listar)
            if not itens:
                print(f"  (nenhum {a.listar} cadastrado ainda)")
            for i in itens:
                extra = "⭐" if i.get("destaque") else "  "
                print(f"  {extra} id {i['id']:>3} | {i.get('nome','')}"
                      f"{' · ' + i.get('perfil','') if i.get('perfil') else ''}")
                if i.get("texto"):
                    print(f"        “{i['texto'][:90]}{'…' if len(i.get('texto','')) > 90 else ''}”")
            return

        if a.depoimento:
            if not a.texto:
                sys.exit("❌ informe --texto \"a mensagem do depoimento\"")
            dados = {
                "nome": a.depoimento,
                "perfil": a.perfil,
                "local": a.local,
                "texto": a.texto,
                "legenda": a.legenda,
                "imagem_url": a.imagem,
                "video_url": a.video,
                "destaque": bool(a.destaque),
                "ordem": a.ordem,
            }
            dados = {k: v for k, v in dados.items() if v is not None}
            r = inserir("depoimentos", dados)[0]
            print(f"  ✅ depoimento cadastrado — id {r['id']}: {r['nome']}"
                  f"{' (destaque na home)' if r.get('destaque') else ''}")
            print(f"     💡 a mídia entra sozinha se houver arquivo em home/depoimentos/"
                  f"{'-'.join(r['nome'].lower().split())}.jpg")
            return

        if a.parceiro:
            dados = {
                "nome": a.parceiro,
                "categoria": a.categoria,
                "logo_texto": a.logo_texto,
                "descricao": a.descricao,
                "logo_url": a.logo,
            }
            dados = {k: v for k, v in dados.items() if v is not None}
            r = inserir("parceiros", dados)[0]
            print(f"  ✅ parceiro cadastrado — id {r['id']}: {r['nome']}")
            return

        ap.print_help()

    except urllib.error.HTTPError as e:
        corpo = e.read().decode()[:300]
        sys.exit(f"❌ Supabase respondeu {e.code}: {corpo}\n"
                 f"   (se falar de coluna inexistente, rode docs/supabase-add-depoimentos.sql)")


if __name__ == "__main__":
    main()
