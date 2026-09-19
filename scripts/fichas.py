# -*- coding: utf-8 -*-
"""
FICHAS — o texto E a foto moram na MESMA pasta.

O QUE MUDOU (e por que)
-----------------------
Antes: a foto ficava na pasta, mas o nome/descrição/texto ficavam escondidos
no código (js/main.js). Trocar a foto não trocava o nome, e o site ligava
a imagem ao card "adivinhando" pelo nome do arquivo. Confuso.

Agora: cada pasta tem um arquivo ficha.txt com TUDO. A ficha aponta
explicitamente qual foto pertence a qual card ("foto: ana-paula.jpg"),
e o site guarda essa ligação — não adivinha mais nada.

FORMATO (um bloco por card, separados por linha em branco):

    foto: ana-paula.jpg
    nome: Ana Paula
    perfil: Mãe
    local: Praia do Sagi
    destaque: sim
    texto: Desde que começou nas atividades, meu filho está mais motivado.

  - linhas começando com # são ignoradas (use como comentário)
  - "foto" é o arquivo de imagem que está NESTA mesma pasta
  - campos ausentes simplesmente não aparecem no card

USO:
    python scripts/fichas.py --status      # mostra o que está nas fichas
    python scripts/fichas.py --publicar     # envia para o site (banco)
"""
import os
import sys
import json
import unicodedata
import urllib.parse
import urllib.request
import urllib.error

# ----------------------------------------------------------------------------
# Configuração
# ----------------------------------------------------------------------------
PASTA_MIDIAS = r"G:/Meu Drive/Instituto SER Sagi - PARA O SITE"
ARQ_CREDENCIAL = r"C:/Users/PRE-IMPRESSOR/R2/.supabase-sagi.env"

# pasta da ficha -> (tabela do banco, categoria, seção das fotos)
DESTINOS = {
    "home/depoimentos": ("depoimentos", "Home", "depoimentos"),
    "home/parceiros":   ("parceiros",   "Home", "parceiros"),
}

CAMPOS_VALIDOS = {
    "depoimentos": ["nome", "perfil", "titulo", "texto", "local", "legenda",
                    "destaque", "ordem", "foto", "video"],
    "parceiros": ["nome", "categoria", "descricao", "logo", "foto", "texto"],
}


def normalizar_chave(txt):
    """Mesma regra do site: sem acento, minúsculo, espaços viram hífen."""
    if not txt:
        return ""
    sem_acento = unicodedata.normalize("NFKD", str(txt))
    sem_acento = "".join(c for c in sem_acento if not unicodedata.combining(c))
    limpo = "".join(c if c.isalnum() else "-" for c in sem_acento.lower())
    return "-".join(p for p in limpo.split("-") if p)


def carregar_credencial():
    """Lê a service_role do arquivo local (fica fora do git)."""
    if not os.path.isfile(ARQ_CREDENCIAL):
        raise SystemExit("❌ Arquivo de credencial não encontrado:\n   " + ARQ_CREDENCIAL)
    valores = {}
    with open(ARQ_CREDENCIAL, encoding="utf-8") as fh:
        for linha in fh:
            linha = linha.strip()
            if not linha or linha.startswith("#") or "=" not in linha:
                continue
            chave, _, valor = linha.partition("=")
            valores[chave.strip()] = valor.strip().strip('"').strip("'")
    url = valores.get("SUPABASE_URL") or valores.get("URL")
    chave = (valores.get("SUPABASE_SERVICE_ROLE_KEY")
             or valores.get("SUPABASE_SERVICE_KEY")
             or valores.get("SERVICE_ROLE_KEY")
             or valores.get("SERVICE_ROLE")
             or valores.get("SERVICE_KEY"))
    if not url or not chave:
        raise SystemExit("❌ A credencial não tem SUPABASE_URL e a chave service_role.")
    return url.rstrip("/"), chave


def requisitar(url, chave, metodo="GET", corpo=None):
    req = urllib.request.Request(url, data=corpo, method=metodo)
    req.add_header("apikey", chave)
    req.add_header("Authorization", "Bearer " + chave)
    if corpo:
        req.add_header("Content-Type", "application/json")
        req.add_header("Prefer", "resolution=merge-duplicates,return=representation")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            texto = resp.read().decode("utf-8")
            return json.loads(texto) if texto.strip() else []
    except urllib.error.HTTPError as erro:
        detalhe = erro.read().decode("utf-8", "replace")[:400]
        raise SystemExit(f"❌ Erro HTTP {erro.code} em {url.split('/rest/')[-1][:60]}\n   {detalhe}")


def ler_ficha(caminho):
    """Lê o ficha.txt: devolve uma lista de blocos (um dict por card)."""
    with open(caminho, encoding="utf-8-sig") as fh:
        linhas = fh.read().splitlines()
    blocos, atual = [], {}
    for linha in linhas:
        limpa = linha.strip()
        if not limpa or limpa.startswith("#"):
            if atual:
                blocos.append(atual)
                atual = {}
            continue
        if ":" not in limpa:
            continue
        chave, _, valor = limpa.partition(":")
        atual[chave.strip().lower()] = valor.strip()
    if atual:
        blocos.append(atual)
    return blocos


def mapa_de_fotos(url_base, chave, categoria, secao):
    """titulo normalizado -> URL pública da foto (vem da tabela 'arquivo')."""
    url = (f"{url_base}/rest/v1/arquivo?select=titulo,imagem_url,video_url,descricao"
           f"&categoria=eq.{urllib.parse.quote(categoria)}"
           f"&secao=eq.{urllib.parse.quote(secao)}&deleted=eq.false")
    itens = requisitar(url, chave)
    mapa = {}
    for i in itens:
        k = normalizar_chave(i.get("titulo"))
        if k and k not in mapa:
            mapa[k] = {"foto": i.get("imagem_url") or i.get("video_url") or "",
                       "video": i.get("video_url") or "",
                       "legenda": i.get("descricao") or ""}
    return mapa


def montar_registro(tabela, bloco, origem, fotos, indice=0):
    """Converte um bloco da ficha no formato da tabela do banco."""
    reg, foto_nome, problemas = {}, bloco.get("foto") or bloco.get("logo") or "", []

    for campo, valor in bloco.items():
        if not valor or campo in ("foto", "logo"):
            continue
        if campo not in CAMPOS_VALIDOS[tabela]:
            problemas.append(f"campo desconhecido '{campo}' (ignorado)")
            continue
        reg[campo] = valor
    if tabela == "parceiros" and "texto" in reg and "descricao" not in reg:
        reg["descricao"] = reg.pop("texto")

    reg.setdefault("nome", "Sem nome")
    if tabela == "depoimentos":
        # a ordem na ficha é a ordem no site (1, 2, 3...)
        if "ordem" not in reg:
            reg["ordem"] = indice + 1
        if "destaque" in reg:
            reg["destaque"] = reg["destaque"].lower() in ("sim", "s", "true", "1", "x")

    # ---- liga a foto de forma EXPLÍCITA (nada de adivinhar pelo nome) ----
    if foto_nome:
        achado = fotos.get(normalizar_chave(os.path.splitext(foto_nome)[0]))
        if not achado:
            problemas.append(f"a foto '{foto_nome}' ainda não foi publicada "
                             f"(rode: python scripts/servidor_midias.py --publicar)")
        else:
            if tabela == "depoimentos":
                if achado.get("video") and not achado.get("foto"):
                    reg["video_url"] = achado["video"]
                else:
                    reg["imagem_url"] = achado["foto"]
                if not reg.get("legenda") and achado.get("legenda"):
                    reg["legenda"] = achado["legenda"]
            else:
                reg["logo_url"] = achado["foto"]
    reg["deleted"] = False
    return reg, foto_nome, problemas


def listar_fichas():
    achados = []
    for pasta, (tabela, categoria, secao) in DESTINOS.items():
        caminho = os.path.join(PASTA_MIDIAS, pasta.replace("/", os.sep), "ficha.txt")
        if os.path.isfile(caminho):
            achados.append((pasta, caminho, tabela, categoria, secao))
    return achados


def comando_status():
    fichas = listar_fichas()
    if not fichas:
        print("Nenhuma ficha.txt encontrada nas pastas:")
        for p in DESTINOS:
            print("   " + p)
        return
    url_base, chave = carregar_credencial()
    for pasta, caminho, tabela, categoria, secao in fichas:
        blocos = ler_ficha(caminho)
        try:
            fotos = mapa_de_fotos(url_base, chave, categoria, secao)
        except SystemExit:
            fotos = {}
        print(f"\n📋 {pasta}/ficha.txt  →  tabela '{tabela}'  ({len(blocos)} card(s))")
        print("   " + "-" * 68)
        for b in blocos:
            foto = b.get("foto") or b.get("logo") or ""
            achou = bool(fotos.get(normalizar_chave(os.path.splitext(foto)[0])))
            marca = "🖼️" if achou else "⚠️ "
            print(f"   {marca} {b.get('nome','?'):20} | "
                  f"{(b.get('perfil') or b.get('categoria') or ''):22} | {foto or '(sem foto)'}")
            if foto and not achou:
                print("        ⚠️  esta foto ainda não foi publicada no site")


def sincronizar(url_base, chave, tabela, registros):
    """
    Faz a ficha virar a verdade no banco, SEM depender de campo único:
      - nome que já existe  -> atualiza
      - nome novo           -> insere
      - nome que sumiu      -> marca como removido (soft delete)
    """
    existentes = requisitar(
        f"{url_base}/rest/v1/{tabela}?select=id,nome&deleted=eq.false", chave)
    por_chave = {normalizar_chave(e.get("nome")): e for e in existentes}

    atualizados, inseridos = [], []
    for reg in registros:
        k = normalizar_chave(reg["nome"])
        if k in por_chave:
            alvo = por_chave.pop(k)["id"]
            salvo = requisitar(f"{url_base}/rest/v1/{tabela}?id=eq.{alvo}", chave,
                               metodo="PATCH",
                               corpo=json.dumps([reg], ensure_ascii=False).encode("utf-8"))
            atualizados.append((reg["nome"], alvo))
        else:
            salvo = requisitar(f"{url_base}/rest/v1/{tabela}", chave, metodo="POST",
                               corpo=json.dumps([reg], ensure_ascii=False).encode("utf-8"))
            inseridos.append((reg["nome"], salvo[0].get("id") if salvo else "?"))

    sobrando = [v for v in por_chave.values() if v.get("id")]
    if sobrando:
        ids = ",".join(str(v["id"]) for v in sobrando)
        requisitar(f"{url_base}/rest/v1/{tabela}?id=in.({ids})", chave, metodo="PATCH",
                   corpo=json.dumps({"deleted": True}).encode("utf-8"))

    return atualizados, inseridos, [v.get("nome") for v in sobrando]


def comando_publicar():
    url_base, chave = carregar_credencial()
    fichas = listar_fichas()
    if not fichas:
        print("Nenhuma ficha.txt encontrada — nada a publicar.")
        return
    for pasta, caminho, tabela, categoria, secao in fichas:
        blocos = ler_ficha(caminho)
        if not blocos:
            print(f"⚠️  {pasta}/ficha.txt está vazia, pulando")
            continue
        fotos = mapa_de_fotos(url_base, chave, categoria, secao)
        registros, avisos = [], []
        for idx, b in enumerate(blocos):
            reg, _, probs = montar_registro(tabela, b, f"{pasta}/ficha.txt", fotos, idx)
            registros.append(reg)
            for p in probs:
                avisos.append(f"{reg.get('nome')}: {p}")

        atualizados, inseridos, removidos = sincronizar(url_base, chave, tabela, registros)

        print(f"\n✅ {pasta}/ficha.txt  →  tabela '{tabela}'")
        for nome, i in inseridos:
            print(f"   ➕ novo      {nome}  (id {i})")
        for nome, i in atualizados:
            print(f"   ♻️  atualizado {nome}  (id {i})")
        for nome in removidos:
            print(f"   🗑️  removido   {nome}  (não está mais na ficha)")
        for a in avisos:
            print(f"   ⚠️  {a}")
        print(f"   = {len(registros)} card(s) no site")


if __name__ == "__main__":
    import urllib.parse  # noqa: E402  (usado em mapa_de_fotos)
    if "--publicar" in sys.argv:
        comando_publicar()
    else:
        comando_status()
