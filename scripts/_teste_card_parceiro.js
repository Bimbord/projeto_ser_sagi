// Teste: renderPartners REAL do main.js, rodado no Node com um DOM mínimo.
const fs = require('fs');
const path = require('path');

const main = fs.readFileSync(path.join('js', 'main.js'), 'utf8');
const ini = main.indexOf('function escaparHtml(texto) {');
const fim = main.indexOf('function renderPartners(items, midias) {');
const fim2 = main.indexOf('function renderGallery(');
if (ini < 0 || fim < 0 || fim2 < 0) {
  console.error('❌ não achei as funções no main.js');
  process.exit(1);
}

const codigo =
  main.slice(ini, main.indexOf('function renderTestimonials(')) +   // escaparHtml + markupDepoimento
  main.slice(main.indexOf('// Normaliza texto para casar'),
             main.indexOf('async function fetchSecao')) +          // normalizarChave (fica mais abaixo no arquivo)
  main.slice(fim, fim2) +                                          // renderPartners
  '\nmodule.exports = { markup: markupDepoimento, partners: renderPartners };';
const tmp = path.join(__dirname, '.tmp_teste_partners.js');
fs.writeFileSync(tmp, codigo);

// DOM mínimo: guarda o que foi injetado no container
let injetado = '';
global.document = {
  querySelector: () => ({ set innerHTML(v) { injetado = v; }, get innerHTML() { return injetado; } }),
};

const { partners } = require(tmp);

function testar(titulo, itens, midias) {
  injetado = '';
  partners(itens, midias || {});
  const temImg = /<img/.test(injetado);
  const temIniciais = /home-partner__logo"[^>]*>(GA|IH|OV|RP|MK)/.test(injetado);
  const escapou = !injetado.includes('<script>') && !injetado.includes('<b>x</b>');
  const nomes = (injetado.match(/home-partner__name">([^<]*)</g) || []).map((s) => s.replace(/.*>/, ''));
  console.log(`\n  ${titulo}`);
  console.log(`     cards: ${nomes.length} | com <img>: ${temImg ? 'sim' : 'não'} | iniciais: ${temIniciais ? 'sim' : 'não'} | escapou: ${escapou ? 'sim' : 'NÃO ⚠️'}`);
  console.log(`     nomes: ${nomes.join(', ')}`);
}

testar('Sem registros (fallback ilustrativo)', [], {});
testar('Registro sem logo (mostra iniciais)', [{ nome: 'Grupo Atlântico', categoria: 'Empresa apoiadora', logo_texto: 'GA' }], {});
testar('Registro COM logo da pasta home/parceiros', [{ nome: 'Grupo Atlântico', categoria: 'Empresa apoiadora', logo_texto: 'GA' }], { 'grupo-atlantico': { imagem: 'https://x.r2.dev/parceiros/grupo-atlantico.png' } });
testar('Registro com logo_url (URL externa)', [{ nome: 'Onda Verde', categoria: 'Patrocinador', logo_url: 'https://exemplo.com/logo.png' }], {});
testar('Nome com HTML (segurança)', [{ nome: 'Empresa <script>x</script>', categoria: 'Teste', logo_texto: 'EX' }], {});

fs.unlinkSync(tmp);
