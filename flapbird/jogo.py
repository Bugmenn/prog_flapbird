#importações
import random
import sys
import pygame
from pygame.locals import *
from backend.geral.config import *
from backend.modelo.jogador import Jogador

#carregar jogador do banco de dados
app.app_context().push()
jogador = db.session.query(Jogador).first()
    
#altura e largura da tela
largura = 600
altura = 499
  
#setar a altura e largura da tela
janela = pygame.display.set_mode((largura, altura))
elevacao = altura * 0.8
imagens = {}
framesporsegundo = 32
imagem_cano = 'backend/imagens/cano.png'
background_image = 'backend/imagens/background.jpg'
imagem_jogador = 'backend/imagens/passaro.png'
imagem_mar = 'backend/imagens/base.jfif'
  
#função principal
def flappygame():
    global pontuacao
    pontuacao = 0
    record = jogador.pontos
    horizontal = int(largura/5)
    vertical = int(largura/2)
    chao = 0
    altura_temporaria = 100
  
    # gerar dois canos na janela
    primeiro_cano = criar_cano()
    segundo_cano = criar_cano()
  
    #lista contendo os canos em baixo
    canos_baixo = [
        {'x': largura + 300 - altura_temporaria,
         'y': primeiro_cano[1]['y']},
        {'x': largura + 300 - altura_temporaria + (largura/2),
         'y': segundo_cano[1]['y']},
    ]
  
    #lista contendo os canos de cima
    canos_cima = [
        {'x': largura+300-altura_temporaria,
         'y': primeiro_cano[0]['y']},
        {'x': largura+200-altura_temporaria+(largura/2),
         'y': segundo_cano[0]['y']},
    ]
  
    #velocidade do cano pelo eixo X
    valocidade_x = -4
  
    #velocidade do passaro
    valocidade_passaro_y = -9
    valocidade_max_passaro_y = 10
    velocidade_min_passaro_y = -8
    passaroAccY = 1
  
    velocidade_voo_passaro = -8
    passaro_voo = False
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if vertical > 0:
                    valocidade_passaro_y = velocidade_voo_passaro
                    passaro_voo = True
  
        #essa função vai retornar verdadeiro se o passaro bater
        game_over = GameOver(horizontal, vertical, canos_cima, canos_baixo)
        if game_over:
            return
  
        #verificar pontuação
        posicao_jogador = horizontal + imagens['flappybird'].get_width()/2
        for cano in canos_cima:
            posicao_cano = cano['x'] + imagens['imagem_cano'][0].get_width()/2
            if posicao_cano <= posicao_jogador < posicao_cano + 4:
                pontuacao += 1
                if pontuacao > record:
                    jogador.pontos = pontuacao
                    db.session.commit()
                print(f"Sua pontuação é: {pontuacao}")
  
        if valocidade_passaro_y < valocidade_max_passaro_y and not passaro_voo:
            valocidade_passaro_y += passaroAccY
  
        if passaro_voo:
            passaro_voo = False
        altura_jogador = imagens['flappybird'].get_height()
        vertical = vertical + \
            min(valocidade_passaro_y, elevacao - vertical - altura_jogador)
  
        # mover canos para a esquerda
        for cano_de_cima, cano_de_baixo in zip(canos_cima, canos_baixo):
            cano_de_cima['x'] += valocidade_x
            cano_de_baixo['x'] += valocidade_x
  
        # Add a new cano when the first is
        # about to cross the leftmost part of the screen
        if 0 < canos_cima[0]['x'] < 5:
            novo_cano = criar_cano()
            canos_cima.append(novo_cano[0])
            canos_baixo.append(novo_cano[1])
  
        #se o cano está fora da tela ele sera removido
        if canos_cima[0]['x'] <- imagens['imagem_cano'][0].get_width():
            canos_cima.pop(0)
            canos_baixo.pop(0)
  
        #carregar imagens no programa
        janela.blit(imagens['background'], (0, 0))
        for cano_de_cima, cano_de_baixo in zip(canos_cima, canos_baixo):
            janela.blit(imagens['imagem_cano'][0],
                        (cano_de_cima['x'], cano_de_cima['y']))
            janela.blit(imagens['imagem_cano'][1],
                        (cano_de_baixo['x'], cano_de_baixo['y']))
  
        janela.blit(imagens['sea_level'], (chao, elevacao))
        janela.blit(imagens['flappybird'], (horizontal, vertical))
  
        #arrumando os numeros
        numeros = [int(x) for x in list(str(pontuacao))]
        largura_numeros = 0
  
        #achando a largura dos numeros da pontuação imagens from numeros.
        for num in numeros:
            largura_numeros += imagens['scoreimages'][num].get_width()
        colar_numeros = (largura - largura_numeros)/1.1
  
        #carregando imagens na janela.
        for num in numeros:
            janela.blit(imagens['scoreimages'][num],
                        (colar_numeros, largura*0.02))
            colar_numeros += imagens['scoreimages'][num].get_width()
  
        #recarregar a tela e mostrar a pontuação
        pygame.display.update()
        framesporsegundo_clock.tick(framesporsegundo)
  
  
def GameOver(horizontal, vertical, canos_cima, canos_baixo):
    if vertical > elevacao - 25 or vertical < 0:
        return True
  
    for cano in canos_cima:
        canoHeight = imagens['imagem_cano'][0].get_height()
        if(vertical < canoHeight + cano['y'] and\
           abs(horizontal - cano['x']) < imagens['imagem_cano'][0].get_width()):
            return True
  
    for cano in canos_baixo:
        if (vertical + imagens['flappybird'].get_height() > cano['y']) and\
        abs(horizontal - cano['x']) < imagens['imagem_cano'][0].get_width():
            return True
    return False
  
  
def criar_cano():
    offset = altura/3
    canoHeight = imagens['imagem_cano'][0].get_height()
    y2 = offset + \
        random.randrange(
            0, int(altura - imagens['sea_level'].get_height() - 1.2 * offset))  
    canoX = largura + 10
    y1 = canoHeight - y2 + offset
    cano = [
        # upper cano
        {'x': canoX, 'y': -y1},
  
        # lower cano
        {'x': canoX, 'y': y2}
    ]
    return cano
  
  
#programa que começa o jogo
if __name__ == "__main__":
  
    #para inicializar os modulos da biblioteca do pygame
    pygame.init()
    framesporsegundo_clock = pygame.time.Clock()
  
    #coloca o nome da janela
    pygame.display.set_caption('Flappy bird Game')
  
    #carrega todas as imagens que vão ser utilizadas
    #imagens da pontuação
    imagens['scoreimages'] = (
        pygame.image.load('backend/imagens/0.png').convert_alpha(),
        pygame.image.load('backend/imagens/1.png').convert_alpha(),
        pygame.image.load('backend/imagens/2.png').convert_alpha(),
        pygame.image.load('backend/imagens/3.png').convert_alpha(),
        pygame.image.load('backend/imagens/4.png').convert_alpha(),
        pygame.image.load('backend/imagens/5.png').convert_alpha(),
        pygame.image.load('backend/imagens/6.png').convert_alpha(),
        pygame.image.load('backend/imagens/7.png').convert_alpha(),
        pygame.image.load('backend/imagens/8.png').convert_alpha(),
        pygame.image.load('backend/imagens/9.png').convert_alpha()
    )
    imagens['flappybird'] = pygame.image.load(
        imagem_jogador).convert_alpha()
    imagens['sea_level'] = pygame.image.load(
        imagem_mar).convert_alpha()
    imagens['background'] = pygame.image.load(
        background_image).convert_alpha()
    imagens['imagem_cano'] = (pygame.transform.rotate(pygame.image.load(
        imagem_cano).convert_alpha(), 180), pygame.image.load(
      imagem_cano).convert_alpha())
    
    #laço de repetição principal  
    while True:
  
        #coordenadas do jogador
        horizontal = int(largura/5)
        vertical = int(
            (altura - imagens['flappybird'].get_height())/2)
        chao = 0
        while True:
            for event in pygame.event.get():
  
                #se pressionar o botão ESC fechara o jogo
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
  
                #se o usuario apertar a barra de espaço ou a setinha de cima
                #o jogo vai começar
                elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                    flappygame()
  
                #se o usuario não apertar nada, nada acontece
                else:
                    janela.blit(imagens['background'], (0, 0))
                    janela.blit(imagens['flappybird'],
                                (horizontal, vertical))
                    janela.blit(imagens['sea_level'], (chao, elevacao))
                    pygame.display.update()
                    framesporsegundo_clock.tick(framesporsegundo) 