# -*- coding: utf-8 -*-
"""Linka os itens de contato do rodapé (Maps, Gmail, tel:) em todas as páginas."""
import os

BASE = r"C:/Projetos Code/Projeto SER Sagi/projeto_SER_Sagi - Hermes"

TRADUCOES = [
    (
        '<li class="flex items-start gap-3"><i class="fa-solid fa-location-dot mt-1 text-sun"></i><span>Praia do Sagi, Baía Formosa/RN</span></li>',
        '<li class="flex items-start gap-3"><i class="fa-solid fa-location-dot mt-1 text-sun"></i><a href="https://www.google.com/maps/search/?api=1&query=Praia+do+Sagi%2C+Ba%C3%ADa+Formosa%2C+RN" target="_blank" rel="noopener" class="hover:text-white">Praia do Sagi, Baía Formosa/RN</a></li>',
    ),
    (
        '<li class="flex items-start gap-3"><i class="fa-solid fa-envelope mt-1 text-sun"></i><a href="mailto:sersagi2025@gmail.com" class="hover:text-white">sersagi2025@gmail.com</a></li>',
        '<li class="flex items-start gap-3"><i class="fa-solid fa-envelope mt-1 text-sun"></i><a href="https://mail.google.com/mail/?view=cm&fs=1&to=sersagi2025@gmail.com" target="_blank" rel="noopener" class="hover:text-white">sersagi2025@gmail.com</a></li>',
    ),
    (
        '<li class="flex items-start gap-3"><i class="fa-solid fa-phone mt-1 text-sun"></i><span>(84) 98655-3747</span></li>',
        '<li class="flex items-start gap-3"><i class="fa-solid fa-phone mt-1 text-sun"></i><a href="tel:+5584986553747" class="hover:text-white">(84) 98655-3747</a></li>',
    ),
]

total = 0
for nome in sorted(os.listdir(BASE)):
    if not nome.endswith(".html"):
        continue
    p = os.path.join(BASE, nome)
    txt = open(p, encoding="utf-8").read()
    novo = txt
    for de, para in TRADUCOES:
        novo = novo.replace(de, para)
    if novo != txt:
        open(p, "w", encoding="utf-8", newline="\n").write(novo)
        total += 1

print(f"✅ contato do rodapé linkado em {total} páginas")
