# -*- coding: utf-8 -*-
"""Otimiza os logos que estão na pasta home/parceiros (no lugar, com backup)."""
import os
import shutil
import hashlib
from PIL import Image

BASE = r"G:\Meu Drive\Instituto SER Sagi - PARA O SITE\home\parceiros"
BACKUP = os.path.join(BASE, "_originais", "_antigos")
LARGURA = 1000          # dobro do exibido (463 px) para tela retina
os.makedirs(BACKUP, exist_ok=True)

ANTIGO = "28eeb2070ca77f98da344195d49af8d6"   # md5 do placeholder antigo

for f in sorted(os.listdir(BASE)):
    caminho = os.path.join(BASE, f)
    if not os.path.isfile(caminho) or not f.lower().endswith((".jpg", ".jpeg", ".png")):
        continue
    md5 = hashlib.md5(open(caminho, "rb").read()).hexdigest()
    novo = "ARQUIVO NOVO ✅" if md5 != ANTIGO else "era o placeholder antigo"
    im = Image.open(caminho)
    larg, alt = im.size
    peso_antes = os.path.getsize(caminho)

    if larg <= LARGURA and peso_antes < 400 * 1024:
        print(f"  ✔️  {f:22} {larg}x{alt}  {peso_antes/1024:.0f} KB — já está leve, não mexi")
        continue

    shutil.copy2(caminho, os.path.join(BACKUP, f))      # backup do original
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGB")
    if larg > LARGURA:
        im = im.resize((LARGURA, round(alt * LARGURA / larg)), Image.LANCZOS)
    im.save(caminho, "JPEG", quality=84, optimize=True, progressive=True)
    print(f"  ✅ {f:22} {larg}x{alt} {peso_antes/1024:5.0f} KB -> "
          f"{im.size[0]}x{im.size[1]} {os.path.getsize(caminho)/1024:4.0f} KB   [{novo}]")

print()
print("prontas para publicar:")
for f in sorted(os.listdir(BASE)):
    c = os.path.join(BASE, f)
    if os.path.isfile(c) and f.lower().endswith((".jpg", ".jpeg", ".png")):
        print(f"   {f:24} {os.path.getsize(c)/1024:6.0f} KB")
