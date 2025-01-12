# muon-data-visualiser

<h2>  Código por: <br></h2>
<uL> 
  <li><a href="https://github.com/kauaQuintella">Kauã Quintella</a></li>
</ul>

<div align="justify"> 

## Descrição

Projeto encarregado de fazer a visualização dos dados obtidos no programa DAC. Diferente dele, a única preocupação é fazer a exibição dos dados de uma forma simples, compreensível e eficaz.

## Fluxograma

O programa faz a leitura do arquivo do tipo LABENSOL (.lbsl) resultado do <a href="https://github.com/compnuclearuefs/oscilloscope-automation">programa de aquisição</a>, fazendo a:

- Conversão de data juliana **ALTERADA** para gregoriana;
- Salvando os dados no objeto do tipo _Data_;

Após, acontece o um set de dados no objeto do tipo *Dashboard* e, logo após, a configuração desse dashboard.

<div align="justify">

## Fontes importantes

Dash lib Phyton: https://plotly.com/