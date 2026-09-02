# 📥 Fluxo de Importação de Mídias — Instituto S.E.R. Sagi

> Como levar fotos/vídeos do "mundo real" pro site, do início ao fim.
> Ferramentas: `scripts/upload_r2.py` e `scripts/publicar.py` (na pasta do projeto).

---

## 🗺️ Visão geral do fluxo

```
📱 FOTO/VIDEO (WhatsApp, celular, câmera)
        ↓ 1. Salvar no computador (pasta local)
💻 PASTA LOCAL (ex.: C:\fotos-evento)
        ↓ 2. Rodar o publicador
⚙️  publicar.py
        ├─ ⬆️ arquivo → Cloudflare R2 (bucket midias-ser-sagi)
        └─ 🗄️ registro → Supabase (tabela arquivo)
        ↓ 3. Abrir o site
🌐 SITE → Acervo (e Destaques na home, se marcado)
```

**Regra de ouro:** o site nunca guarda o arquivo — só a URL. Quem guarda o arquivo é o R2; quem guarda os metadados (título, categoria, URL) é o Supabase.

---

## ✅ Pré-requisitos (já configurados)

- Python instalado (o script usa só a biblioteca padrão — zero instalação)
- Credenciais do R2 em `C:/Users/PRE-IMPRESSOR/R2/.r2-sagi.env` (⚠️ nunca commitar)
- Supabase já conectado no `js/main.js` (URL + anon key)

---

## 🖼️ MODO ÚNICO — publicar 1 foto/vídeo

### 1. Salve a mídia no computador
- **WhatsApp:** abra a conversa → botão direito na mídia → **Salvar como** (ou "Salvar imagem")
- **Celular → PC:** cabo USB, Google Fotos, ou envie pra si mesmo no WhatsApp Web

### 2. Rode o publicador

**Jeito interativo (mais fácil):**
```bash
cd "D:/BBDPRINT - BACKUP/BBDPRINT/App BBDPRiNT/PROJETOS/Projetos Code/Projeto SER Sagi/projeto_SER_Sagi - Hermes"
python scripts/publicar.py
```
Ele pergunta: caminho do arquivo (dá pra **arrastar o arquivo** pra dentro do terminal), título, categoria.

**Jeito direto (1 comando):**
```bash
python scripts/publicar.py "C:\fotos\jiu-jitsu.jpg" "Aula de jiu-jitsu" --categoria esporte --descricao "Turma da tarde" --destaque
```

### 3. Confira a saída
```
✅ Publicado com sucesso!
   🆔 id: 12
   🏷️  Aula de jiu-jitsu | Esporte | ⭐ destaque
   📎 URL: https://pub-....r2.dev/fotos/esporte-aula-de-jiu-jitsu.png
```

### 4. Abra o site e veja no ar 🎉

---

## 📦 MODO LOTE — importar uma pasta inteira

Quando a ONG manda **30 fotos de um evento**, não publique uma a uma:

```bash
python scripts/publicar.py --pasta "C:\fotos-festa-junina" --categoria eventos --titulo "Festa Junina" --destaque
```

- Importa **todos** os `.jpg/.png/.webp/.gif/.mp4/.mov` da pasta
- Títulos viram `Festa Junina — 01`, `Festa Junina — 02`...
- Arquivos viram `fotos/eventos-festa-junina.png`, `-001.png`, `-002.png`...
- Mostra resumo: `✅ Importados: 30/30`

> ⚠️ Antes de importar, **renomeie os arquivos** se quiser ordem específica
> (ex.: `01-abertura.jpg`, `02-apresentacao.jpg`) — a pasta é processada em ordem alfabética.

---

## 📂 Categorias disponíveis

| Slug (usar no comando) | Nome que aparece no site |
|---|---|
| `esporte` | Esporte |
| `saude` | Saúde |
| `educacao` | Educação |
| `cultura` | Cultura |
| `preservacao` | Preservação |
| `eventos` | Eventos |

---

## ⚠️ Regras importantes (não pular)

1. **Autorização de imagem (OBRIGATÓRIO)** — crianças/adolescentes precisam de autorização dos responsáveis (ECA + LGPD). Só publique fotos autorizadas.
2. **Nada de dados sensíveis** — o bucket é público: **não subir** documentos com CPF, RG, prontuários etc. Só fotos autorizadas e PDFs públicos (relatórios, prestação de contas).
3. **Qualidade** — fotos escuras/tremidas/prints de baixa resolução não valorizam o site. Prefira as melhores do lote.
4. **`--destaque` com moderação** — só os 3 melhores registros do mês merecem destaque na home (a seção mostra até 3).

---

## 🧹 Manutenção

```bash
# Listar tudo que está no bucket
python scripts/upload_r2.py --list

# Apagar um arquivo do R2 (ex.: foto errada)
python scripts/upload_r2.py --delete fotos/esporte-jiu-jitsu-01.jpg

# Apagar uma pasta inteira do R2
python scripts/upload_r2.py --delete-prefix acervo/
```

**Corrigir título/categoria/descrição** de um registro: edite a linha direto no **Supabase → Table Editor → arquivo** (o site atualiza na hora).

**Apagar um registro** (foto que não deve ficar): Table Editor → checkbox da linha → **Delete**. (O arquivo no R2 pode ser apagado com `--delete`.)

---

## 🚨 Se algo der errado

| Sintoma | Causa provável | Solução |
|---|---|---|
| `Credencial X não preenchida` | `.env` incompleto | Abrir `C:/Users/PRE-IMPRESSOR/R2/.r2-sagi.env` e conferir os 3 campos |
| `Mídia subiu, mas registro falhou` | Rede/Supabase indisponível | Rodar de novo (o arquivo duplicado no R2 ganha `-001`; apague o que sobrou) |
| Foto aparece quebrada no site | Linha no Supabase aponta pra arquivo apagado do R2 | Apagar a linha no Table Editor |
| Site não atualiza | Cache do navegador | **Ctrl+Shift+R** (hard refresh) |

---

*Documento vivo — atualizar conforme o fluxo evoluir (ex.: fluxo WhatsApp, painel self-service).*
