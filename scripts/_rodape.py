# -*- coding: utf-8 -*-
"""
Substitui o rodapé de TODAS as páginas por um rodapé unificado e profissional:
4 colunas (Marca+social+newsletter | Navegação | Institucional | Contato) + barra de copyright.
Usa os dados reais do Instituto e a estrutura de páginas atual.
"""
import os, re, sys

BASE = r"C:/Projetos Code/Projeto SER Sagi/projeto_SER_Sagi - Hermes"

FOOTER = '''  <footer class="bg-slate-950 text-white">
    <div class="mx-auto max-w-7xl px-4 py-14 lg:px-8">
      <div class="grid gap-10 lg:grid-cols-[1.5fr_0.7fr_0.8fr_1fr]">
        <section>
          <a href="./" class="text-2xl font-extrabold text-white">Instituto S.E.R. Sagi</a>
          <p class="mt-1 text-xs font-semibold uppercase tracking-[0.25em] text-sun">Sabedoria &bull; Esforço &bull; Resultado</p>
          <p class="mt-4 max-w-sm text-sm leading-7 text-white/70">Transformação social em Praia do Sagi — saúde, esporte, educação, cultura e preservação ambiental para crianças, adolescentes e famílias.</p>
          <div class="mt-5 flex gap-3">
            <a href="https://instagram.com/s.e.r_sagi" target="_blank" rel="noopener" aria-label="Instagram do Instituto S.E.R. Sagi" class="flex h-10 w-10 items-center justify-center rounded-full border border-white/15 bg-white/5 text-white/80 transition hover:bg-white/10 hover:text-white"><i class="fa-brands fa-instagram text-lg"></i></a>
            <a href="https://wa.me/5584986553747" target="_blank" rel="noopener" aria-label="WhatsApp do Instituto S.E.R. Sagi" class="flex h-10 w-10 items-center justify-center rounded-full border border-white/15 bg-white/5 text-white/80 transition hover:bg-white/10 hover:text-white"><i class="fa-brands fa-whatsapp text-lg"></i></a>
          </div>
          <form class="mt-6 max-w-sm" data-form-type="newsletter" aria-label="Formulário de newsletter do rodapé">
            <p class="text-sm font-semibold text-white/90">Receba novidades do Instituto</p>
            <div class="mt-2 flex gap-2">
              <input type="email" name="email" required placeholder="Seu e-mail" class="min-w-0 flex-1 rounded-full border border-white/20 bg-white/5 px-4 py-2.5 text-sm text-white placeholder:text-white/50">
              <button type="submit" class="rounded-full bg-sun px-4 py-2.5 text-sm font-semibold text-oceanDeep transition hover:brightness-95">Cadastrar</button>
            </div>
            <label class="mt-2 flex items-start gap-2 text-xs text-white/60"><input type="checkbox" name="aceite_comunicacao" class="mt-0.5"><span>Autorizo o recebimento de comunicações do Instituto S.E.R. Sagi.</span></label>
            <div class="form-feedback hidden mt-3 rounded-xl border px-4 py-3 text-sm"></div>
          </form>
        </section>
        <section>
          <h3 class="text-sm font-semibold uppercase tracking-[0.2em] text-sun">Navegação</h3>
          <ul class="mt-4 space-y-3 text-sm">
            <li><a href="./" class="text-white/70 transition hover:text-white">Início</a></li>
            <li><a href="quem-somos.html" class="text-white/70 transition hover:text-white">Quem Somos</a></li>
            <li><a href="acoes.html" class="text-white/70 transition hover:text-white">Nossas Ações</a></li>
            <li><a href="esporte.html" class="text-white/70 transition hover:text-white">Esporte</a></li>
            <li><a href="acervo.html" class="text-white/70 transition hover:text-white">Acervo</a></li>
            <li><a href="como-ajudar.html" class="text-white/70 transition hover:text-white">Como Ajudar</a></li>
          </ul>
        </section>
        <section>
          <h3 class="text-sm font-semibold uppercase tracking-[0.2em] text-sun">Institucional</h3>
          <ul class="mt-4 space-y-3 text-sm">
            <li><a href="lei-incentivo.html" class="text-white/70 transition hover:text-white">Lei de Incentivo</a></li>
            <li><a href="transparencia.html" class="text-white/70 transition hover:text-white">Transparência</a></li>
            <li><a href="instalacoes.html" class="text-white/70 transition hover:text-white">Instalações</a></li>
            <li><a href="contato.html" class="text-white/70 transition hover:text-white">Contato</a></li>
          </ul>
        </section>
        <section>
          <h3 class="text-sm font-semibold uppercase tracking-[0.2em] text-sun">Contato</h3>
          <ul class="mt-4 space-y-3 text-sm text-white/70">
            <li class="flex items-start gap-3"><i class="fa-solid fa-location-dot mt-1 text-sun"></i><span>Praia do Sagi, Baía Formosa/RN</span></li>
            <li class="flex items-start gap-3"><i class="fa-brands fa-instagram mt-1 text-sun"></i><a href="https://instagram.com/s.e.r_sagi" target="_blank" rel="noopener" class="hover:text-white">@s.e.r_sagi</a></li>
            <li class="flex items-start gap-3"><i class="fa-solid fa-envelope mt-1 text-sun"></i><a href="mailto:sersagi2025@gmail.com" class="hover:text-white">sersagi2025@gmail.com</a></li>
            <li class="flex items-start gap-3"><i class="fa-solid fa-phone mt-1 text-sun"></i><span>(84) 98655-3747</span></li>
          </ul>
        </section>
      </div>
      <div class="mt-12 flex flex-col gap-2 border-t border-white/10 pt-6 sm:flex-row sm:items-center sm:justify-between">
        <p class="text-xs text-white/50">&copy; 2026 Instituto S.E.R. Sagi — Todos os direitos reservados.</p>
        <p class="text-xs text-white/50">Uma causa em prol da infância e da comunidade do Sagi.</p>
      </div>
    </div>
  </footer>'''

PADRAO = re.compile(r'<footer\b[^>]*>.*?</footer>', re.S)

total = 0
for nome in sorted(os.listdir(BASE)):
    if not nome.endswith(".html"):
        continue
    p = os.path.join(BASE, nome)
    txt = open(p, encoding="utf-8").read()
    if not PADRAO.search(txt):
        print(f"  ⚠️  {nome}: sem <footer> encontrado")
        continue
    novo, n = PADRAO.subn(FOOTER, txt, count=1)
    if n != 1:
        print(f"  ⚠️  {nome}: substituição inesperada ({n})")
        continue
    open(p, "w", encoding="utf-8", newline="\n").write(novo)
    total += 1

print(f"✅ Rodapé substituído em {total} páginas")
