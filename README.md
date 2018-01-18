# Sistemas-Multimidia

### UNIVERSIDADE FEDERAL DE JUIZ DE FORA 
### DEPARTAMENTO DE CIÊNCIA DA COMPUTAÇÃO
#### DCC082 - Sistemas Multimídia - Dezembro 2017

Codigo elaborado como proposta de trabalho para a disciplina Sistemas Multimidia
no segundo semestre de 2017 <br>

Bernard Rodrigues - bernard_clintwood@hotmail.com       <br>
Gisele Goulart    - gisele.goulart@engenharia.ufjf.br   <br>
Guilherme Felix   - guilherme.felix@engenharia.ufjf.br  <br>

#### RESUMO: 

A ideia desse script é, dada uma imagem como entrada, calcular a transformada
de fourier sobre ela e, usar o valor médio dos coeficientes como frequencia de 
uma onda sonora a ser produzida e executada.

As imagens utilizadas em escala de cinza, tem tamanho 512px x 512px e a 
transformada foi aplicada sobre blocos de tamanho 64px x 64px.
Para os valores obtidos foram calculados a magnitude, tomada a raiz quadrada
(a fim de reduzir a amplitude dos valores encontrados) e, por fim, o valor médio.

Essa media foi usada diretamente como a frequência de uma onda sonora senóide 
exportada em formato <i> .wav </i> com taxa de amostragem de 44100 Hz. Assim, para cada 
bloco haverá uma onda sonora correspondente.

Ao ser executado, o script apresenta a imagem escolhida em escala de cinza (com 
o bloco superior esquerdo destacado em vermelho) e executa o áudio produzido. 
Dentro do destaque vermelho aparecera o valor da frequẽncia da onda emitida 
(recomenta-se o uso de um aparelho que reproduza bem sons graves).

Regiões de imagens com muita variação preto-branco tendem a produzir sons muito agudos
(da ordem de 1000 Hz), portanto <b> cuidado </b> com a calibração do volume.

Cada tecla apertada exibe o próximo bloco e seu áudio, até o fim da imagem, 
quando a execução e finalizada. A tecla ESC encerra a execução

Para executar digite no terminal:
'python codigo_dcc082 [indice]'
onde [indice] corresponde a cada uma das imagens a seguir:

0 - 'lena.bmp'       <br>
1 - 'squareBW.png'   <br>
2 - 'pkmn.png',      <br>
3 - 'psycho.jpg',    <br>
4 - 'chess1.jpg'    

