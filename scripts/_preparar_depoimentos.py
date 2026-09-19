# -*- coding: utf-8 -*-
"""
Prepara as fotos novas dos depoimentos que o Bimbord colocou em _originais/.

- recorta no formato do card (16:10, centro) para nao perder enquadramento
- redimensiona para 1200x750 (o dobro do tamanho exibido)
- salva como .jpg no lugar certo, com o nome que a ficha aponta
"""
import os
import shutil
from PIL import Image

BASE = r"G:\Meu Drive\Instituto SER Sagi - PARA O SITE\home\depoimentos"
ORIG = os.path.join(BASE, "_originais")

# nome na pasta _originais  ->  nome que a ficha espera
PARES = [
    ("ana-paula.png", "ana-paula.jpg"),
    ("carlos-henrique.png", "carlos-henrique.jpg"),
    ("joao-miguel.png", "joao-miguel.jpg"),
]

LARGURA, ALTURA = 1200, 750        # 16:10, exatamente a proporcao do card
os.makedirs(os.path.join(ORIG, "_antigos"), exist_ok=True)

for de, para in PARES:
    origem = os.path.join(ORIG, de)
    if not os.path.isfile(origem):
        print(f"  ⚠️  não achei {de} em _originais — pulando")
        continue

    im = Image.open(origem)
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGB")
    original = im.size

    # recorte central na proporcao do card
    alvo = LARGURA / ALTURA
    largura, altura = im.size
    if largura / altura > alvo:                 # larga demais: corta as laterais
        nova_largura = int(altura * alvo)
        caixa = ((largura - nova_largura) // 2, 0,
                 (largura - nova_largura) // 2 + nova_largura, altura)
    else:                                       # alta demais: corta topo/base
        nova_altura = int(largura / alvo)
        sobra = (altura - nova_altura)
        topo = int(sobra * 0.35)                # puxa um pouco para cima (rosto)
        caixa = (0, topo, largura, topo + nova_altura)

    im = im.crop(caixa).resize((LARGURA, ALTURA), Image.LANCZOS)
    destino = os.path.join(BASE, para)
    im.save(destino, "JPEG", quality=84, optimize=True, progressive=True)

    # guarda a original recebida em _antigos/ (nao sobe: pasta com "_")
    shutil.move(origem, os.path.join(ORIG, "_antigos", de))

    print(f"  ✅ {de:24} {original[0]}x{original[1]}  ->  {para}  "
          f"({os.path.getsize(destino)/1024:.0f} KB)")

print()
print("prontas para publicar:")
for f in sorted(os.listdir(BASE)):
    c = os.path.join(BASE, f)
    if os.path.isfile(c) and f.lower().endswith((".jpg", ".png")) and f != "ficha.txt":
        print(f"   {f:26} {os.path.getsize(c)/1024:6.0f} KB")
im = Image.open(os.path.join(BASE, PARES[0][1]))
print(f"\nformato final: {im.size[0]}x{im.size[1]}")
