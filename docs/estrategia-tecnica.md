# Estratégia Técnica — Instituto S.E.R. Sagi

**Data:** 17/08/2026
**Autor:** Bimbord (dev) + Hermes (consultoria)
**Contexto:** Site institucional multipágina (estático, Tailwind + JS vanilla), publicado em `bimbord.github.io`, com dados dinâmicos via Table API (depoimentos, parceiros, galeria) e formulários funcionais (contato, leads, newsletter).

> Documento de apoio para decisões de domínio, hospedagem, manutenção, alimentação de conteúdo e precificação. Será apresentado a órgãos fiscalizadores (Lei de Incentivo ao Esporte), então toda decisão deve priorizar **credibilidade, transparência e baixo custo**.

---

## 1. Domínio — opções gratuitas e pagas

| Opção | Custo | Avaliação |
|---|---|---|
| `bimbord.github.io` (GitHub Pages) | Grátis | Já em uso; subdomínio de terceiros, passa imagem amadora |
| `site.netlify.app` / `site.vercel.app` | Grátis | Mesma limitação do acima |
| `.tk/.ml/.ga` (Freenom) | Grátis | ⛔ Evitar — serviço instável/morto, sem credibilidade |
| **Domínio `.br` próprio** (registro.br) | ~R$ 40/ano | ✅ **Recomendado** — `institutosersagi.org.br` ou `.com.br` |

**Conclusão:** não existe domínio gratuito legítimo e confiável. O custo anual de um `.br` é baixo e muda completamente a credibilidade perante fiscalizadores e parceiros. **Investir no domínio próprio desde já.**

---

## 2. Hospedagem — gratuita vs paga (Hostinger)

- **Site estático (estado atual):** GitHub Pages, Netlify ou Cloudflare Pages — **100% grátis**, HTTPS, CDN global, performance excelente. **Não pagar por isso.**
- **Hostinger (~R$ 10–25/mês):** só compensa quando houver backend dinâmico, banco de dados no mesmo ambiente ou e-mails institucionais (que o Pages não fornece).
- **E-mail institucional grátis:** Zoho Mail (plano free, até 5 caixas com domínio próprio).

**Conclusão:** manter hospedagem gratuita no estágio atual; reavaliar quando o painel/backend evoluir.

---

## 3. Manutenção e alimentação do site (eventos, fotos, vídeos)

Objetivo: **tirar o conteúdo do código** (já iniciado — depoimentos/parceiros/galeria vêm de tabelas) e permitir que uma pessoa comum alimente o site:

1. **Curto prazo (agora):** planilha (Google Sheets/Airtable) ou formulário simples → o site lê via API e renderiza. Zero código para quem alimenta.
2. **Médio prazo:** painel com login (desenvolvimento próprio — padrão Lite Pro) ou CMS headless gratuito (ex.: Decap CMS).

---

## 4. Banco de dados e armazenamento de mídias

Regra de ouro: **separar metadados de arquivos**.

- **Metadados** (título, data, categoria, descrição) → tabela/banco de dados.
- **Arquivos** (fotos/vídeos) → **storage de objetos** (nunca dentro do banco — pesado e caro).

### Opções reais (baixo/zero custo)

| Serviço | Grátis | Uso indicado |
|---|---|---|
| **Cloudflare R2** | 10GB + tráfego de saída grátis | ⭐ Melhor para fotos/vídeos |
| **Supabase Storage** | 1GB | ⭐ Ótimo se usar Supabase como banco |
| **Firebase Storage** | 5GB | Alternativa Google |
| **Backblaze B2** | 10GB | Backup e arquivos |

### Dicas de mercado
- **Vídeos longos → YouTube (não listado) embutido** — grátis e não pesa o site.
- Banco de dados real (Postgres grátis do Supabase, 500MB) vale quando o volume crescer.

---

## 5. Credibilidade perante órgãos fiscalizadores (Lei de Incentivo) ⚠️

**Ponto crítico:** o que aprova na Lei de Incentivo **não é o site** — é o projeto, CNPJ, plano de trabalho, certidões e prestação de contas. O site é a **vitrine de credibilidade**.

O que pesa no site:
- Domínio próprio + HTTPS + dados de contato reais + **CNPJ no rodapé**
- Página de **Transparência real** (relatórios, atas, prestação de contas em PDF)
- **Política de privacidade + LGPD** — atenção redobrada: **fotos de crianças exigem autorização dos responsáveis** (direito de imagem). Sem isso, vira problema, não vitrine.
- Backend robusto = backups automáticos + dados protegidos (GitHub já é o backup do código).

---

## 6. Estrutura futura amigável para pessoa comum

1. **Hoje:** site estático + tabelas/planilha (já existente) — alimentação via formulário simples.
2. **Futuro:** **Supabase** (banco + storage + login, tudo no plano grátis) + **mini-painel próprio** onde a pessoa comum: faz login → cadastra evento → sobe fotos → marca "destaque do mês". O site atualiza sozinho.
3. **Bônus:** vira **case de portfólio** — "site + painel de gestão para ONG" é apresentável para futuros clientes.

---

## 7. Precificação — manutenção mensal

- Mercado: R$ 300–1.000/mês; agências cobram mais.
- **Camarada para ONG comunitária: R$ 150–250/mês** (atualizações de fotos/vídeos/eventos, suporte, backups).
- Alternativa: pacote anual com desconto (ex.: R$ 150/mês ou R$ 1.500/ano).
- **Separar custos fixos do trabalho:** ONG cobre domínio (~R$ 40/ano) e e-mail — transparente e saudável.
- **Documentar tudo:** proposta, escopo e o que está incluso — vira prova de organização perante fiscalizadores.

---

## 8. Ideias extras

- **PIX com QR code** na página "Como Ajudar" + prestação de contas pública.
- **Google Analytics** grátis — números de audiência para mostrar impacto a parceiros.
- **Termo de uso de imagem das crianças** (prioridade máxima) — campanha de autorização com responsáveis.
- **Manual de manutenção** simples para a ONG (evoluir o README.md atual).
- **WhatsApp/Instagram integrados** (@s.e.r_sagi).
- Seção **"Destaques do mês"** na home (já planejada) — vira o "jornalzinho" do instituto.

---

## ✅ Caminho recomendado (resumo)

> **Grátis até onde der:** GitHub Pages/Cloudflare Pages + Supabase (banco) + Cloudflare R2 (mídias) → painel próprio quando crescer → **domínio próprio + e-mails institucionais desde já** (custo baixo, ganho enorme de credibilidade).

---

## Anexo — Perguntas do briefing original

1. Quais domínios gratuitos para projeto social sem fins lucrativos?
2. Vale a pena hospedar em serviço gratuito ou hospedagem paga (Hostinger)?
3. Como realizar manutenção e alimentação do site (eventos, fotos, vídeos mensais)?
4. Vale criar banco de dados para subir arquivos? (opções reais, baixo/zero custo)
5. O projeto precisa ser forte no frontend e backend (apresentação a órgãos fiscalizadores — Lei de Incentivo).
6. Primeiro cliente — presente para a comunidade; manutenção ficará com o dev. Estrutura amigável para pessoa comum alimentar.
7. Preço camarada de manutenção mensal.
8. Ideias extras.
