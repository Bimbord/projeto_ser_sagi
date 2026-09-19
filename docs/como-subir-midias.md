COMO COLOCAR E EDITAR O CONTEÚDO DO SITE
========================================
Instituto S.E.R. Sagi · atualizado em 18/09/2026


A IDEIA (em uma frase)
----------------------
Cada bloco do site tem uma PASTA, e dentro dela ficam DUAS coisas:
as FOTOS e um arquivo ficha.txt com os textos.

    📁 home/depoimentos/
    ├── 🖼️ ana-paula.jpg          <- a foto
    ├── 📄 ficha.txt               <- o nome, o perfil e o texto
    └── 📁 _originais/             <- as fotos originais (não sobem)

Foto e texto sempre juntos. Não tem mais texto escondido no código.


A ROTINA (3 passos)
-------------------
  1. Coloque a foto na pasta  E  edite o ficha.txt
  2. Avise o Hermes: "publiquei os depoimentos"
  3. Aparece no site


COMO É UMA FICHA
----------------
Abra o ficha.txt. É assim (cada bloco = um card):

    foto: ana-paula.jpg
    nome: Ana Paula
    perfil: Mãe
    local: Praia do Sagi
    destaque: sim
    texto: Desde que começou nas atividades, meu filho está mais motivado.

  • separe os blocos com UMA LINHA EM BRANCO
  • "foto:" é o nome do arquivo que está na mesma pasta
  • "destaque: sim" = aparece na home
  • a ORDEM dos blocos é a ordem no site (o primeiro vem primeiro)
  • linhas começando com # são comentários (ignoradas)
  • o "texto" é a frase que aparece entre aspas no card


ONDE FICA CADA COISA
--------------------
  home/hero/              foto grande do topo da home
  home/numeros/           fotos dos cards de números (120, 300, 11...)
  home/pilares/           fotos dos 5 pilares
  home/depoimentos/       depoimentos + ficha   <- TEM FICHA
  home/parceiros/         logos + ficha        <- TEM FICHA
  home/como-ajudar/       fotos da chamada final
  home/joia-da-coroa/     foto do card da Jóia da Coroa
  <categoria>/<pagina>/   hero, imagem principal, galeria, carrossel...


SITUAÇÕES ESPECIAIS (cards onde o nome do arquivo importa)
----------------------------------------------------------
Algumas fotos não são casadas por nome comum, e sim por uma CHAVE.
Nesses casos o arquivo precisa ter o nome exato:

  home/numeros/      projeto-principal.jpg  criancas.jpg  pessoas.jpg
                     aulas.jpg  modalidades.jpg  parceiros.jpg
                     voluntarios.jpg  bairros.jpg  criancas-hj.jpg
  home/pilares/      esporte.jpg  saude.jpg  educacao.jpg
                     cultura.jpg  preservacao.jpg
  home/como-ajudar/  doe.jpg  seja-parceiro.jpg  voluntario.jpg
  home/joia-da-coroa/ joia-da-coroa.jpg

Os demais (depoimentos, parceiros, galerias, heros) usam o nome normal.


TAMANHOS RECOMENDADOS (px)
--------------------------
  Foto do topo (hero) .......... 1920 x 700   (proporção 2,7:1)
  Card / imagem principal ...... 1000 x 500   (2:1)
  Card de depoimento ........... 1200 x 750   (16:10)
  Logo de parceiro ............. 600 x 600    (quadrado)
  Foto de galeria .............. 800 x 600    (4:3)

Peso: até ~500 KB por foto. Se vier mais pesada, o Hermes otimiza
(a última leva caiu de 16,9 MB para 0,5 MB).


ANTES DE PUBLICAR (checklist)
-----------------------------
  [ ] As fotos têm autorização de uso de imagem?
  [ ] Os nomes estão escritos do jeito certo (acentos ok)?
  [ ] A ordem dos blocos na ficha é a ordem que você quer no site?
  [ ] Fotos pesadas? O Hermes otimiza na publicação.


COMANDOS (o Hermes roda; você só me avisa)
------------------------------------------
  python scripts/servidor_midias.py --status      o que chegou de novo
  python scripts/servidor_midias.py --publicar    sobe as fotos
  python scripts/fichas.py --status               confere as fichas
  python scripts/fichas.py --publicar             aplica as fichas no site
