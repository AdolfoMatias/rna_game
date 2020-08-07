#Instalar o pygame e o numpy atráves do comando pip install

#importação das bibliotecas necessárias
import numpy as np
import pygame
import random
from pygame.locals import *
from random import uniform
import asyncio

#gameOver é valor booleano de perder o jogo, inciando em False, irei usar o while true só pra montar o jogo com o gameOver
gameOver = False

#Tamanho da tela e incializador
TAMANHO = (800, 600)
pygame.init()
tela = pygame.display.set_mode(TAMANHO)
tela_retangulo = tela.get_rect()
pygame.display.set_caption('unifacisa_adolfo')

posicaoYraquete = 0


#basicamente as cores de cada componente do jogo: raquete, tela, bola
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
AZUL = (0, 0, 156)
#criando nosso objeto raquete

class Raquete:
    def __init__(self, tamanho):
        self.imagem = pygame.Surface(tamanho)
        self.imagem.fill(AZUL)
        self.imagem_retangulo = self.imagem.get_rect()
        self.imagem_retangulo[0] = 0

# a função move promove a velocidade em que a raquete se move com base nos valores de saída da rede neural, isso ficou ao meu critério.
    def move(self, y):
        self.imagem_retangulo[1] += y * 10

        global posicaoYraquete
        posicaoYraquete = self.imagem_retangulo.centery

#aqui temos a função de atualizar a tecla mediante aos valores de saída, fazendo a raquete se mover
    def atualiza(self, tecla):
        if tecla > 0.5:
            self.move(-1)
        elif tecla < 0.5:
            self.move(1)
        self.imagem_retangulo.clamp_ip(tela_retangulo)

    def realiza(self):
        tela.blit(self.imagem, self.imagem_retangulo)


posicaoYbola = 0
posicaoXbola = 0

#criando o valor do erro que começa 0
erro = 0

# criando nosso objeto bola
class Bola:
    def __init__(self, tamanho):
        self.altura, self.largura = tamanho
        self.imagem = pygame.Surface(tamanho)
        self.imagem.fill(BRANCO)
        self.imagem_retangulo = self.imagem.get_rect()
        self.setBola()
        global erro
        self.erro = 0

    def aleatorio(self):
        while True:
            num = random.uniform(-1, 1)
            if num > -0.5 and num < 0.5:
                continue
            else:
                return num

    def setBola(self):
        x = self.aleatorio()
        y = self.aleatorio()
        self.imagem_retangulo.x = tela_retangulo.centerx
        self.imagem_retangulo.y = tela_retangulo.centery
        self.velo = [x, y]
        self.pos = list(tela_retangulo.center)

    def colideParede(self):
        if self.imagem_retangulo.y <= 0 or self.imagem_retangulo.y > tela_retangulo.bottom - self.altura:
            self.velo[1] *= -1

        if self.imagem_retangulo.x <= 0 or self.imagem_retangulo.x > tela_retangulo.right - self.largura:
            self.velo[0] *= -1
            if self.imagem_retangulo.x <= 0:
                placar1.pontos -= 1
                print('Deixou bater :(')


    #O calculo do erro da rede neural quando a bola bate na parede
                self.erro = (posicaoYraquete - posicaoYbola)/10
                rede.atualizaPesos(self.erro)

    def move(self):
        self.pos[0] += self.velo[0] * 4

        self.pos[1] += self.velo[1] * 4
        self.imagem_retangulo.center = self.pos

    def colideRaquete(self, raqueteRect):
        if self.imagem_retangulo.colliderect(raqueteRect):
            self.velo[0] *= -1
            placar1.pontos += 1
            print('Adolfo defendeu!')
            #self.erro = 0

            global erro
            erro = 0


    def atualiza(self, raqueteRect):
        self.colideParede()
        global posicaoYbola, posicaoXbola
        posicaoYbola = self.imagem_retangulo.y
        posicaoXbola = self.imagem_retangulo.x
        self.colideRaquete(raqueteRect=raqueteRect)
        self.move()

    def realiza(self):
        tela.blit(self.imagem, self.imagem_retangulo)

#o placar que é mostrado na tela
class Placar:
    def __init__(self):
        pygame.font.init()
        self.fonte = pygame.font.Font(None, 36)
        self.pontos = 0

    def contagem(self):
        self.text = self.fonte.render(
            'Pontuação: ' + str(self.pontos), 1, (255, 255, 255))
        self.textpos = self.text.get_rect()
        self.textpos.centerx = tela.get_width() / 2
        tela.blit(self.text, self.textpos)
        tela.blit(tela, (0, 0))


raquete = Raquete((10, 100))
bola = Bola((15, 15))
placar1 = Placar()

tecla = 0


#Aqui criei os pesos entre a camada de entrada e as camadas ocultas, são inseridas em vetores como se pode ver:
# o uso de vetores irá facilitar o calculo...
pesosPrimeiroNeuronioCamadaEntrada = np.array(
    [uniform(-1, 1) for i in range(4)])
    #estou utilizando o list comprehension como fizemos em aula
pesosSegundoNeuronioCamadaEntrada = np.array(
    [uniform(-1, 1) for i in range(4)])

pesosPrimeiroNeuronioCamadaOculta = np.array(
    [uniform(-1, 1) for i in range(2)])
pesosSegundoNeuronioCamadaOculta = np.array([uniform(-1, 1) for i in range(2)])

pesosNeuronioDeSaida = np.array([uniform(-1, 1) for i in range(2)])

#aqui tem a class própria da rede neural, na qual são recebidos os valores dos pesos:
class RedeNeural:
    #observe os valores que a class da rede neural recebe, yraquete,ybola,xolinha e o bias.
    def __init__(self, YRaquete, XBolinha, YBola, bias=-1):

        self.entradas = np.array([YRaquete, XBolinha, YBola, bias])
        global pesosPrimeiroNeuronioCamadaEntrada, pesosSegundoNeuronioCamadaEntrada, pesosPrimeiroNeuronioCamadaOculta, pesosSegundoNeuronioCamadaOculta

        self.pesosPrimeiroNeuronioCamadaEntrada = pesosPrimeiroNeuronioCamadaEntrada
        self.pesosSegundoNeuronioCamadaEntrada = pesosSegundoNeuronioCamadaEntrada

        self.pesosPrimeiroNeuronioCamadaOculta = pesosPrimeiroNeuronioCamadaOculta
        self.pesosSegundoNeuronioCamadaOculta = pesosSegundoNeuronioCamadaOculta

        self.pesosNeuronioDeSaida = pesosNeuronioDeSaida


    # função vai pra frente para o calculo dos valores, utilizando a função de ativação
    def feedforward(self):

        self.saidaPrimeiroNeuronioCamadaEntrada = round(self.tangenteHiperbolica(
            np.sum(self.entradas * self.pesosPrimeiroNeuronioCamadaEntrada)), 6)

        self.saidaSegundoNeuronioCamadaEntrada = round(self.tangenteHiperbolica(
            np.sum(self.entradas * self.pesosSegundoNeuronioCamadaEntrada)), 6)

        self.saidaPrimeiroNeuronioCamadaOculta = round(self.tangenteHiperbolica(np.sum(np.array(
            [self.saidaPrimeiroNeuronioCamadaEntrada, self.saidaPrimeiroNeuronioCamadaEntrada]) * self.pesosPrimeiroNeuronioCamadaOculta)), 6)

        self.saidaSegundoNeuronioCamadaOculta = round(self.tangenteHiperbolica(
            np.sum(np.array([self.saidaPrimeiroNeuronioCamadaEntrada, self.saidaSegundoNeuronioCamadaEntrada]) * self.saidaSegundoNeuronioCamadaEntrada)), 6)

        self.resultado = round(self.sigmoid(np.sum(np.array(
            [self.saidaPrimeiroNeuronioCamadaOculta, self.saidaSegundoNeuronioCamadaOculta]) * self.pesosNeuronioDeSaida)), 6)

        return self.resultado


    #ATENÇÃO: aqui são ciradas as duas funções de ativiação, a diferenciação baseia-se apenas em que uma utiliza de -1 a 1 e a outra de 0 a 1
    def tangenteHiperbolica(self, x):

        th = (np.exp(x) - np.exp(-x)) / (np.exp(x) + np.exp(-x))
        return th

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))


#o autaliza pesos recebe o erro e a taxa de aprendizagem em 0.01, a entrada já tenho pois já criei...
    def atualizaPesos(self, erro, alpha=0.01):
        #aqui praticamente é um backpropagation indo para atrás isso depois do feedfoward
        for i in range(len(pesosNeuronioDeSaida)):
            if i == 0:
                entrada = self.saidaPrimeiroNeuronioCamadaOculta
            elif i == 1:
                entrada = self.saidaSegundoNeuronioCamadaOculta

            pesosNeuronioDeSaida[i] = pesosNeuronioDeSaida[i] + \
                (alpha * entrada * erro)

        for i in range(len(pesosPrimeiroNeuronioCamadaOculta)):
            if i == 0:
                entrada1 = self.saidaPrimeiroNeuronioCamadaEntrada
            if i == 1:
                entrada1 = self.saidaSegundoNeuronioCamadaEntrada

            pesosPrimeiroNeuronioCamadaOculta[i] = pesosPrimeiroNeuronioCamadaOculta[i] + (
                alpha * entrada1 * erro)

        for i in range(len(pesosSegundoNeuronioCamadaOculta)):
            if i == 0:
                entrada2 = self.saidaPrimeiroNeuronioCamadaEntrada
            if i == 1:
                entrada2 = self.saidaSegundoNeuronioCamadaEntrada

            pesosSegundoNeuronioCamadaOculta[i] = pesosSegundoNeuronioCamadaOculta[i] + (
                alpha * entrada2 * erro)

        for i in range(len(pesosPrimeiroNeuronioCamadaEntrada)):
            pesosPrimeiroNeuronioCamadaEntrada[i] = pesosPrimeiroNeuronioCamadaEntrada[i] + (
                alpha * self.entradas[i] * erro)

        for i in range(len(pesosSegundoNeuronioCamadaEntrada)):
            pesosSegundoNeuronioCamadaEntrada[i] = pesosSegundoNeuronioCamadaEntrada[i] + (
                alpha * self.entradas[i] * erro)

        print(self.resultado)

# Aqui montei basicamente a estrutura do jogo e a rede neural irá se comportar aqui dentro
while not gameOver:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            gameOver = True

    rede = RedeNeural(posicaoYraquete/600, posicaoXbola/800, posicaoYbola/600)
    tecla = rede.feedforward()

    with open('dadosTreinamento.txt', 'a') as arquivo:
        arquivo.write(str(posicaoYraquete) + " " + str(posicaoXbola) +
                      " " + str(posicaoYbola) + " " + str(tecla) + "\n")

    tela.fill(PRETO)
    raquete.realiza()
    bola.realiza()
    raquete.atualiza(tecla)
    bola.atualiza(raquete.imagem_retangulo)

    #outra atualização do erro
    erro = (posicaoYraquete - posicaoYbola) / 100
    rede.atualizaPesos(erro)

    placar1.contagem()
    pygame.display.update()
