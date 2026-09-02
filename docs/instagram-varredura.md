# 📸 Varredura do Instagram — @s.e.r_sagi

> Estado: **parcial** — o Instagram bloqueia extração anônima do feed (HTTP 429 + login).
> Pasta de trabalho: `C:/Projetos Code/Projeto SER Sagi/projeto_SER_Sagi - Hermes/instagram-scrap/`

## ✅ O que já foi coletado

- **Foto de perfil**: `fotos/profile_pic.jpg` (baixada do CDN, 4KB, 150×150)
- **Metadados públicos do perfil**:

| Campo | Valor |
|---|---|
| Usuário | `s.e.r_sagi` |
| Nome | S.E.R. Sagi |
| Seguidores | 909 |
| Seguindo | 78 |
| Bio | "S.E.R. SAGI - TODOS 'SOMOS SAGI'… SABEDORIA, ESFORÇO, RESULTADOS / Consultório Odontológico, Estúdio e Quadra Esportiva para a toda a Comunidade. INSTITUTO" |
| Nº de posts | 8 (pelo HTML) |

## ❌ O que está bloqueado (requer login)

- As **fotos/vídeos reais dos 8 posts** do feed
- **Captions** (legendas) de cada post
- **Datas**, likes, comentários
- **Destaques** (Highlights) reels e conteúdo de vídeo

### Por quê
O Instagram moderno não entrega o feed a scrapers ou IPs de datacenter sem uma **sessão autenticada**.
Tentativas feitas e bloqueadas nesta varredura:
- `web_profile_info` (API interna) → **HTTP 429** (rate limit / block)
- `graphql/query` → **HTTP 400** (invalid request)
- HTML do perfil → veio como shell (sem JSON do feed)
- `instaloader` → exigiria login + instalação de pacote (evitado: preferência zero-install)

## 🎯 Insights da BIO para o site (valor direto, já aproveitável)

A bio do Instagram confirma a **identidade visual e o slogan** do site:
- **"TODOS SOMOS SAGI"** → reforça a seção "Nossa Mensagem — Todos somos Sagi" (já na página `quem-somos.html`)
- **"SABEDORIA, ESFORÇO, RESULTADOS"** → estende o "Sabedoria, Esforço e Resultado" já presente no hero
- **"Consultório Odontológico, Estúdio e Quadra Esportiva para toda a Comunidade"** → ecoa os pilares de Saúde + Esporte
- A frase **"para a toda a Comunidade"** → nota: corrigir para "para **toda a** comunidade" (concordância) se usarmos essa linha em algum lugar.

### Sugestão de uso
- Usar "TODOS SOMOS SAGI" como **hashtag da comunidade** e reforço de marca (ex.: em campanhas, no rodapé, em CTAs de redes sociais).

## 🔓 Como destravar o feed real (próximos passos)

Ver `docs/pendencias.md` e a decisão do usuário sobre uma das rotas abaixo:
1. **Exportação de dados** → Configurações → Baixar suas informações (JSON) → ZIP com tudo
2. **Login no navegador do Hermes** (aba de preview) → navegar e extrair via interface
3. **Sessão autenticada** → disponibilizar cookies/sessão (não recomendado expor senha)

---

*Gerado em 27/08/2026 por Hermes — varredura parcial, pendente de acesso autenticado.*
