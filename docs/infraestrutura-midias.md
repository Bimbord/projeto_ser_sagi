# Infraestrutura de Mídias — Cloudflare R2 (Projeto SER Sagi)

> Documento vivo: como o armazenamento de fotos/vídeos do site está configurado.
> Última atualização: 31/08/2026

---

## ✅ Configurado (31/08/2026)

### Bucket
- **Nome:** `midias-ser-sagi` (conta Cloudflare do Bimbord — mesma da BBDPRINT)
- **URL pública (base):**
  ```
  https://pub-4eb5a1fd20eb4452b93cedb4c02e30ea.r2.dev
  ```
- Acesso público via **r2.dev** habilitado (status: Allowed)
- **Região:** Automatic (rede global Cloudflare — edge GRU/São Paulo)

### Credenciais de API (token `sersagi-alimentacao`)
- Arquivo local (⚠️ **nunca commitar / nunca colar no chat**):
  ```
  C:/Users/PRE-IMPRESSOR/R2/.r2-sagi.env
  ```
- Campos: `R2_ACCOUNT_ID`, `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`, `R2_ENDPOINT`, `R2_BUCKET`, `R2_PUBLIC_URL`
- Permissão do token: Object Read & Write, escopo só no bucket `midias-ser-sagi`, TTL Forever

### Ferramenta de upload
- Script: `scripts/upload_r2.py` (na pasta do projeto)
- Uso interativo:
  ```
  python scripts/upload_r2.py
  ```
- Uso direto:
  ```
  python scripts/upload_r2.py "C:\pasta\foto.jpg" esporte-jiu-jitsu
  ```
- O que ele faz: detecta tipo (foto/vídeo/pdf), escolhe a pasta certa (`fotos/`, `videos/`, `docs/`), gera nome limpo (`categoria-assunto-001.ext`), garante nome único e mostra a URL pública.
- Script de teste de conexão: `C:/Users/PRE-IMPRESSOR/R2/testar_conexao_r2.py`

### Ferramenta de publicação (upload + registro) — scripts/publicar.py
- **1 comando** sobe pro R2 E grava na tabela `arquivo` do Supabase (devolve id + URL)
- Uso:
  ```bash
  python scripts/publicar.py "C:\pasta\foto.jpg" "Título" --categoria esporte --descricao "..." --destaque
  ```
- Categorias: `esporte`, `saude`, `educacao`, `cultura`, `preservacao`, `eventos`
- Flags: `--descricao "texto"`, `--destaque` (home), `--data YYYY-MM-DD` (padrão: hoje)
- Vídeos (.mp4/.mov) vão pra `videos/` com `video_url`; fotos pra `fotos/` com `imagem_url`

### Servidor de Mídias (entrada automatizada) — scripts/servidor_midias.py
- Ponte **Google Drive → R2 + Supabase**: a ONG sobe material numa pasta compartilhada, o Bimbord aprova movendo para a pasta espelho por categoria, e o script publica.
- Modos: `--status` (o que chegou) · `--dry-run` (simula) · `--publicar` (sobe e registra)
- Deduplicação por **hash SHA-256** num manifesto guardado no Drive (`_publicados\publicados.json`)
- Fluxo completo, estrutura de pastas e limites: **`docs/servidor-midias.md`**

### ⚠️ Apagar ou editar registro na tabela `arquivo`
- A **anon key NÃO tem permissão** de `UPDATE`/`DELETE` — a API responde 200/204 **sem alterar nada** (falha silenciosa, já nos morderam em teste).
- Para apagar/editar: **Table Editor** do Supabase (Table Editor → arquivo) ou a **service_role** em `C:/Users/PRE-IMPRESSOR/R2/supabase.txt` (⚠️ nunca commitar nem colar em mensagem).

### Manutenção do bucket (modos do upload_r2.py)
```bash
python scripts/upload_r2.py --list                  # lista objetos
python scripts/upload_r2.py --delete fotos/x.jpg    # apaga um objeto
python scripts/upload_r2.py --delete-prefix acervo/ # apaga pasta inteira
```

---

## 📁 Estrutura de pastas do bucket

```
midias-ser-sagi/
├── fotos/       → fotos das atividades (esporte-jiu-jitsu-01.jpg...)
├── videos/      → vídeos curtos
├── acervo/      → itens da página Acervo (⚠️ a pasta criada errada "arcevo/" deve ser apagada)
└── docs/        → PDFs (relatórios, prestação de contas)
```

## 📝 Convenção de nomes

- Tudo minúsculo, hífen no lugar de espaço, sem acentos
- Formato: `categoria-assunto-sequencia.ext`
  - ex.: `fotos/esporte-jiu-jitsu-01.jpg`, `videos/evento-aniversario-01.mp4`

---

## 🔗 Como a URL entra no site

1. Arquivo sobe pro bucket → URL pública:
   ```
   https://pub-4eb5a1fd20eb4452b93cedb4c02e30ea.r2.dev/fotos/esporte-jiu-jitsu-01.jpg
   ```
2. A URL vai no campo `imagem_url` (foto) ou `video_url` (vídeo) da tabela `arquivo` no **Supabase** (banco do site — projeto `sersagi-site` na conta Supabase do Bimbord)
3. O site (`js/main.js` → `fetchTableData`/`submitToTable`) lê/grava via **API do Supabase** (URL + anon key) e renderiza — ✅ já conectado (31/08)

> Quando houver domínio próprio, dá pra trocar a URL base pra
> `https://media.institutosersagi.org.br/...` (custom domain no R2 — de graça).

---

## 🔜 Próximos passos

- [x] Projeto no Supabase (`sersagi-site`, plano grátis) + 7 tabelas + RLS (`docs/supabase-schema.sql`)
- [x] `js/main.js` conectado ao Supabase (URL + anon key)
- [x] Primeira foto real registrada e testada
- [x] Registrador manual `scripts/publicar.py` (upload R2 + tabela em 1 comando)
- [ ] Alimentação: fluxo WhatsApp (híbrido) ou painel self-service
- [ ] Domínio próprio + custom domain no R2 (`media.institutosersagi.org.br`)

---

## 🔒 Segurança

- **Secret Access Key** nunca sai do arquivo local `.r2-sagi.env`
- Token com escopo restrito (só esse bucket) — se vazar, revogar no painel e gerar outro
- O bucket `midias-ser-sagi` é público (URLs abertas) — **não subir nada sensível nele** (nada de documentos com dados pessoais de crianças; só fotos autorizadas e PDFs públicos)
