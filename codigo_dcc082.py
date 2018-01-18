# -*- coding: utf-8 -*-
import cv2
import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile as wav
import pyaudio  
import wave  
import time
import sys

"""
UNIVERSIDADE FEDERAL DE JUIZ DE FORA 
DEPARTAMENTO DE CIENCIA DA COMPUTACAO
DCC082 - Sistemas Multimidia - Dezembro 2017

Codigo elaborado como proposta de trabalho para a disciplina Sistemas Multimidia
no segundo semestre de 2017

Bernard Rodrigues - bernard_clintwood@hotmail.com
Gisele Goulart    - gisele.goulart@engenharia.ufjf.br
Guilherme Felix   - guilherme.felix@engenharia.ufjf.br

RESUMO:

A ideia desse script e, dada uma imagem como entrada, calcular a transformada
de fourier sobre ela e, usar o valor medio dos coeficientes como frequencia de 
uma onda sonora a ser produzida e executada.

As imagens utilizadas em escala de cinza, tem tamanho 512px x 512px e a 
transformada foi aplicada sobre blocos de tamanho 64px x 64px.
Para os valores obtidos foram calculados a magnitude, tomada a raiz quadrada
(a fim de reduzir a amplitude dos valores encontrados) e, por fim o valor medio.

Essa media foi usada diretamente como a frequencia de uma onda sonora senoide 
exportada em formato wav com taxa de amostragem de 44100 Hz. Assim, para cada 
bloco havera uma onda sonora correspondente.

Ao ser executado o script apresenta a imagem escolhida em escala de cinza (com 
o bloco superior esquerdo destacado em vermelho) e executa o audio produzido. 
Dentro do destaque vermelho aparecera o valor da frequencia da onda emitida 
(recomenta-se o uso de um aparelho que reproduza bem sons graves).

Cada tecla apertada exibe o próximo bloco e seu áudio, até o fim da imagem, 
quando a execucao e finalizada. A tecla ESC encerra a execucao

Para executar digite:
'python codigo_dcc082.py [indice]'
onde [indice] corresponde a cada uma das imagens a seguir:

0 - 'lena.bmp'
1 - 'chess.jpg'
2 - 'squareBW.png'
3 - 'pkmn.png',
4 - 'psycho.jpg',
5 - 'chess1.jpg'
"""


def player(freq):
    '''
    Funcao que abre e executa o arquivo de audio via PyAudio
    Argumentos:
    freq -- frequencia da onda a ser lida. 
    '''
	
    nomeArquivo = 'bloco.wav'
    data = geraSenoide(freq,1)
    sinal = np.array(data, dtype=np.int16)
    wav.write(nomeArquivo, 44100, sinal)
	
	#define stream chunk   
    chunk = 1024  

	#open a wav format music  
    f = wave.open(nomeArquivo,'rb')  
	#instantiate PyAudio  
    p = pyaudio.PyAudio()  
	#open stream  
    stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
					channels = f.getnchannels(),  
					rate = f.getframerate(),  
					output = True)  
	#read data  
    data = f.readframes(chunk)  

	#play stream  
    while data:  
        stream.write(data)  
        data = f.readframes(chunk)  

	#stop stream  
    stream.stop_stream()  
    stream.close()  

	#close PyAudio  
    p.terminate()  

def realTimePlayer(freq):
    '''
    Funcao que abre e executa o arquivo de audio via PyAudio
    Argumentos:
    freq -- frequencia da onda a ser lida. 
    feito olhando em: https://people.csail.mit.edu/hubert/pyaudio/docs/
    '''
    
    nomeArquivo = 'bloco.wav'
    data = geraSenoide(freq,1)
    sinal = np.array(data, dtype=np.int16)
    wav.write(nomeArquivo, 44100, sinal)
    #open a wav format music  
    f = wave.open(nomeArquivo,'rb')  
    #instantiate PyAudio  
    p = pyaudio.PyAudio()  
    # define callback (2)
    def callback(in_data, frame_count, time_info, status):
        data = f.readframes(frame_count)
        return (data, pyaudio.paContinue)

    # open stream using callback (3)
    stream = p.open(format=p.get_format_from_width(f.getsampwidth()),
                    channels=f.getnchannels(),
                    rate=f.getframerate(),
                    output=True,
                    stream_callback=callback)

    # start the stream (4)
    stream.start_stream()

    # wait for stream to finish (5)
    while stream.is_active():
        time.sleep(0.1)

    # stop stream (6)
    stream.stop_stream()
    stream.close()
    f.close()
    # close PyAudio (7)
    p.terminate()

def geraSenoide(frequencia = 110, duracao = 0.5, valorPico = 16834, taxaAmostragem = 44100):
    """
    Funcao que gera uma onda senoide.
    Argumentos:
    frequencia      -- frequencia da onda a ser gerada, em Hz (frequencia sonora), (float, default 110)
    duracao         -- duracao da onda gerada, em segundos (float, default 0.5)
    valorPico       -- amplitude maxima da onda (float default 16834)
    taxaAmostragem  -- taxa de amostragem do audio a ser gerado, em Hz (int default 44100)
    """
    numeroAmostras = duracao * taxaAmostragem
    if(frequencia != 0):
        periodo = 1.0/frequencia
        omega = 2*np.pi / periodo
    else:
        omega = 0
    deltaT = 1.0/taxaAmostragem

    tempo = np.arange(start = 0, stop= duracao, step = deltaT, dtype = np.float)
    valorSinal = valorPico * np.sin(omega*tempo)

    return valorSinal

def highlight(canvas, medias, tam):
    '''
    Desenha o destaque de cada bloco na tela
    Argumentos:
    canvas -- imagem que sera usada de 'tela' para o desenho
    medias -- vetor com os valores a serem usados
    tam -- tamanho de cada bloco
    '''
    
    # Parametros da visualizacao
    ESC = 27
    BLOCK_COLOR = (0, 0, 255)
    UNIT = "Hz"
    FONT_SIZE = 0.55
    FONT_COLOR = (0, 230, 230)
    BORDER_COLOR = (0, 0, 0)
    red = BLOCK_COLOR

    # Parametros para o laco
    nLin = canvas.shape[0] # N de linhas
    nCol = canvas.shape[1] # N de colunas
    alpha = 1              # transparencia do destaque

    canvas = cv2.cvtColor(canvas, cv2.COLOR_GRAY2RGB) # Converte a imagem de fundo para matriz RGB
    sobreCamada = canvas.copy()

    iterator = 0

    for y in range(0, nCol, tam):
        for x in range(0, nLin, tam):
            FREQ = '{:.1f}'.format(medias[iterator])
            imgSaida = sobreCamada

            # Desenha quadrados vermelhos de destaque
            cv2.rectangle(sobreCamada, (x, y), (x + tam-1, y+ tam-1), red)   
            # Borda
            cv2.putText(sobreCamada, FREQ,(x+1, y+tam/2), cv2.FONT_HERSHEY_DUPLEX, FONT_SIZE, BORDER_COLOR, 3)
            cv2.putText(sobreCamada, UNIT,(x+13, y+tam/2+25), cv2.FONT_HERSHEY_DUPLEX, FONT_SIZE, BORDER_COLOR, 3)
            # Texto em si
            cv2.putText(sobreCamada, FREQ,(x+1, y+tam/2), cv2.FONT_HERSHEY_DUPLEX, FONT_SIZE, FONT_COLOR, 1)
            cv2.putText(sobreCamada, UNIT,(x+13, y+tam/2+25), cv2.FONT_HERSHEY_DUPLEX, FONT_SIZE, FONT_COLOR, 1)
            cv2.addWeighted(sobreCamada, alpha, imgSaida, 1 - alpha, 0, imgSaida)
            cv2.imshow("Saida", imgSaida)
            
            realTimePlayer(medias[iterator])
            # Altere para o tempo de espera (em ms) para a execucao automatica.
            key = cv2.waitKey(0)
            iterator += 1
            print iterator
            if(key == ESC):
                break
        else:
            continue
        break

    cv2.destroyAllWindows()

# Inicio da execucao
# argparser
arg = sys.argv
if len(argv)>1:
	index = int(arg[1])
	if (index >= 0 and index <= 4):
		filename = index
	else:
		print "Indice fora dos limites: Digite um valor na faixa [0 - 4]"
		sys.exit(1)
else:
	print "Insira um parametro: [0 - 4]"
	sys.exit(0)

name = ('lena.bmp','squareBW.png','pkmn.png','psycho.png','chess1.jpg')
img_path = "img_files/"+name[filename]
img = cv2.imread(img_path,0)

nRow = len(img) 
nCol = len(img[0])
tam = 64

blocos_norma = []
blocos_fase = []
blocos_media_n = []
blocos_media_f = []
blocos_max = []

####################
### TRANSFORMADA ###
####################

# para cada bloquinho 
for i in range(0, nCol, tam):
	for j in range(0, nRow, tam):
		fourier = np.fft.fft2(img[i:i+tam,j:j+tam])
		fourier_shft = np.fft.fftshift(fourier)
		
		norma_fourier = np.abs(fourier_shft)
		fase_fourier = np.angle(fourier_shft)
		
		normalize_norma = np.sqrt(norma_fourier)
		max_normalize = normalize_norma.max()
		
		media_norma = norma_fourier.mean()
		media_fase = fase_fourier.mean()
		
		# Append
		blocos_norma.append(norma_fourier)
		blocos_fase.append(fase_fourier)
		blocos_media_n.append(media_norma)
		blocos_media_f.append(media_fase)
		blocos_max.append(max_normalize)

###########
### SOM ###
###########

highlight(img, blocos_media_n, tam)

