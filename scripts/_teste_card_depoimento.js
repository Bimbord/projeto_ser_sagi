// Teste da FASE 5 Parte C: roda o markupDepoimento REAL do main.js no Node.
// Extrai as funções do arquivo (não reescreve nada) e imprime o HTML gerado.
const fs = require('fs');
const path = require('path');

const main = fs.readFileSync(path.join('js', 'main.js'), 'utf8');

const ini = main.indexOf('function escaparHtml(texto) {');
const fim = main.indexOf('function renderTestimonials(');
if (ini < 0 || fim < 0) {
  console.error('❌ não achei escaparHtml/markupDepoimento no main.js');
  process.exit(1);
}
const codigo = main.slice(ini, fim) + '\nmodule.exports = { escaper: escaparHtml, markup: markupDepoimento };';
const tmp = path.join(__dirname, '.tmp_teste_card.js');
fs.writeFileSync(tmp, codigo);

const { markup } = require(tmp);

const CASOS = [
  { nome: 'Só mensagem (sem mídia)', item: { nome: 'Carlos Henrique', perfil: 'Pai', texto: 'O Instituto trouxe oportunidade de verdade.', local: 'Baía Formosa/RN' } },
  { nome: 'Com FOTO (vinda do Drive)', item: { nome: 'Ana Paula', perfil: 'Mãe', texto: 'Meu filho está mais motivado.', local: 'Praia do Sagi', legenda: 'Ana Paula e o filho na entrega dos uniformes' }, midia: { imagem: 'https://x.r2.dev/home-ana-paula.jpg' } },
  { nome: 'Com VÍDEO mp4 (Drive)', item: { nome: 'João Miguel', perfil: 'Criança', texto: 'Gosto muito do jiu-jitsu.' }, midia: { video: 'https://x.r2.dev/home-joao-miguel.mp4' } },
  { nome: 'Com foto + vídeo YouTube (URL no banco)', item: { nome: 'Maria', perfil: 'Voluntária', texto: 'Ver a comunidade crescendo não tem preço.', legenda: 'Primeiro treino do ano', video_url: 'https://youtu.be/abc123' }, midia: { imagem: 'https://x.r2.dev/home-maria.jpg' } },
  { nome: 'Texto com HTML (teste de segurança)', item: { nome: 'Teste <script>', perfil: 'X', texto: 'Se <b>aparecer</b> "tag" solta, não escapou.' } },
];

let ok = 0;
for (const c of CASOS) {
  const html = markup(c.item, c.midia);
  const temMidia = html.includes('home-quote__midia');
  const selo = (html.match(/home-quote__selo">([^<]*)</) || [])[1] || '—';
  const temPlay = html.includes('home-quote__play');
  const temLegenda = html.includes('home-quote__legenda');
  const escapou = !html.includes('<script>') && !html.includes('<b>aparecer</b>');
  console.log(`\n  ✅ ${c.nome}`);
  console.log(`     mídia: ${temMidia ? 'sim' : 'não'} | selo: ${selo} | play: ${temPlay ? 'sim' : 'não'} | legenda: ${temLegenda ? 'sim' : 'não'} | escapou HTML: ${escapou ? 'sim' : 'NÃO ⚠️'}`);
  ok++;
}
console.log(`\n  ${ok}/${CASOS.length} casos renderizados sem erro.`);
fs.unlinkSync(path.join('.tmp_teste_card.js'));
