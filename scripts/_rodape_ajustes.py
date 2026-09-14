# -*- coding: utf-8 -*-
"""
Aplica os ajustes do rodapé aprovados nas demais páginas (a home já foi feita):
1) encurta a descrição
2) adiciona Facebook e YouTube (links das plataformas)
3) remove "Uma causa em prol..."
4) adiciona "Desenvolvido por: lthomassilver@gmail.com"
"""
import os

BASE = r"C:/Projetos Code/Projeto SER Sagi/projeto_SER_Sagi - Hermes"

WHATSAPP = ('<a href="https://wa.me/5584986553747" target="_blank" rel="noopener" '
            'aria-label="WhatsApp do Instituto S.E.R. Sagi" class="flex h-10 w-10 items-center justify-center '
            'rounded-full border border-white/15 bg-white/5 text-white/80 transition hover:bg-white/10 hover:text-white">'
            '<i class="fa-brands fa-whatsapp text-lg"></i></a>')

FACE = ('<a href="https://www.facebook.com/" target="_blank" rel="noopener" '
        'aria-label="Facebook do Instituto S.E.R. Sagi" class="flex h-10 w-10 items-center justify-center '
        'rounded-full border border-white/15 bg-white/5 text-white/80 transition hover:bg-white/10 hover:text-white">'
        '<i class="fa-brands fa-facebook-f text-lg"></i></a>')

YT = ('<a href="https://www.youtube.com/" target="_blank" rel="noopener" '
      'aria-label="YouTube do Instituto S.E.R. Sagi" class="flex h-10 w-10 items-center justify-center '
      'rounded-full border border-white/15 bg-white/5 text-white/80 transition hover:bg-white/10 hover:text-white">'
      '<i class="fa-brands fa-youtube text-lg"></i></a>')

TRADUCOES = [
    (
        '<p class="mt-4 max-w-sm text-sm leading-7 text-white/70">Transformação social em Praia do Sagi — saúde, esporte, educação, cultura e preservação ambiental para crianças, adolescentes e famílias.</p>',
        '<p class="mt-4 max-w-sm text-sm leading-7 text-white/70">Transformação social em Praia do Sagi</p>',
    ),
    (
        WHATSAPP,
        FACE + "\n            " + YT + "\n            " + WHATSAPP,
    ),
    (
        '<p class="text-xs text-white/50">Uma causa em prol da infância e da comunidade do Sagi.</p>',
        '<p class="text-xs text-white/50">Desenvolvido por: <a href="mailto:lthomassilver@gmail.com" class="hover:text-white">lthomassilver@gmail.com</a></p>',
    ),
]

total = 0
puladas = []
for nome in sorted(os.listdir(BASE)):
    if not nome.endswith(".html"):
        continue
    if nome == "index.html":
        puladas.append(nome)
        continue
    p = os.path.join(BASE, nome)
    txt = open(p, encoding="utf-8").read()
    novo = txt
    for de, para in TRADUCOES:
        novo = novo.replace(de, para)
    if novo != txt:
        open(p, "w", encoding="utf-8", newline="\n").write(novo)
        total += 1

print(f"✅ ajustes aplicados em {total} páginas (index.html pulada: já estava feita)")
