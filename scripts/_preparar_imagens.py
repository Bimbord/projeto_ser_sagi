# -*- coding: utf-8 -*-
"""
Prepara as imagens fictícias para publicar:

1. PARCEIROS — o nome do arquivo precisa casar com o nome do parceiro no card.
   Os cards (illustrativos) são: Grupo Atlântico, Instituto Horizonte,
   Onda Verde e Rede Potiguar. Renomeia sua-marca01..04 para esses nomes.
2. OTIMIZA tudo (redimensiona + comprime) — as originais vêm com ~2,8 MB,
   o que deixaria o site pesado.
3. Guarda as ORIGINAIS em _originais/ (não sobem — pasta com "_" é ignorada).
"""
import os
import shutil
from PIL import Image

S = r"G:/Meu Drive/Instituto SER Sagi - PARA O SITE"

PARCEIROS = [
    ("sua-marca01.jpg", "grupo-atlantico.jpg"),
    ("sua-marca02.jpg", "instituto-horizonte.jpg"),
    ("sua-marca03.jpg", "onda-verde.jpg"),
    ("sua-marca04.jpg", "rede-potiguar.jpg"),
]
DEPOIMENTOS = [("ana-paula.png", "ana-paula.jpg"),
               ("carlos-henrique.png", "carlos-henrique.jpg"),
               ("joao-miguel.png", "joao-miguel.jpg")]


def otimizar(origem, destino, largura, qualidade=82):
    im = Image.open(origem)
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGB")
    larg, alt = im.size
    if larg > largura:
        im = im.resize((largura, round(alt * largura / larg)), Image.LANCZOS)
    im.save(destino, "JPEG", quality=qualidade, optimize=True, progressive=True)
    return os.path.getsize(origem), os.path.getsize(destino)


print("=== PARCEIROS (logo no card: ~400x400) ===")
pasta = os.path.join(S, "home", "parceiros")
backup = os.path.join(pasta, "_originais")
os.makedirs(backup, exist_ok=True)
for de, para in PARCEIROS:
    o = os.path.join(pasta, de)
    if not os.path.isfile(o):
        print(f"  ⚠️  {de} não existe")
        continue
    shutil.move(o, os.path.join(backup, de))
    antes, depois = otimizar(os.path.join(backup, de), os.path.join(pasta, para), 800)
    print(f"  ✅ {de} → {para}   {antes/1024:.0f} KB → {depois/1024:.0f} KB")

print("\n=== DEPOIMENTOS (mídia do card: 16:10) ===")
pasta = os.path.join(S, "home", "depoimentos")
backup = os.path.join(pasta, "_originais")
os.makedirs(backup, exist_ok=True)
for de, para in DEPOIMENTOS:
    o = os.path.join(pasta, de)
    if not os.path.isfile(o):
        print(f"  ⚠️  {de} não existe")
        continue
    shutil.move(o, os.path.join(backup, de))
    antes, depois = otimizar(os.path.join(backup, de), os.path.join(pasta, para), 1200)
    print(f"  ✅ {de} → {para}   {antes/1024:.0f} KB → {depois/1024:.0f} KB")

print("\n--- o que sobrou pronto para publicar ---")
for sub in ("home/parceiros", "home/depoimentos"):
    p = os.path.join(S, sub.replace("/", os.sep))
    for f in sorted(os.listdir(p)):
        if os.path.isfile(os.path.join(p, f)):
            print(f"  {sub}/{f}  ({os.path.getsize(os.path.join(p, f))/1024:.0f} KB)")
