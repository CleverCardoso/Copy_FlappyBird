import pygame
import os
import random

# Constantes
tela_largura = 500
tela_altura = 800

# Imagens
imagem_cano = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png')))
imagem_chao = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png')))
imagem_background = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')))
imagens_passaro = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird3.png')))
]

# Fonte
pygame.font.init()
fonte_pontos = pygame.font.SysFont('arial', 50)

# Classes
class Passaro:
    IMGS = imagens_passaro
    rotaçao_maxima = 25
    velocidade_rotaçao = 20
    tempo_animaçao = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = y
        self.tempo = 0
        self.contagem_imagem = 0
        self.imagem = self.IMGS[0]

    def pular(self):
        self.velocidade = -10.5
        self.tempo = 0
        self.altura = self.y

    def mover(self):
        self.tempo += 1
        deslocamento = 1.5 * (self.tempo ** 2) + self.velocidade * self.tempo

        if deslocamento > 16:
            deslocamento = 16
        elif deslocamento < 0:
            deslocamento -= 2

        self.y += deslocamento

        if deslocamento < 0 or self.y < self.altura + 50:
            if self.angulo < self.rotaçao_maxima:
                self.angulo = self.rotaçao_maxima
        else:
            if self.angulo > -90:
                self.angulo -= self.velocidade_rotaçao

    def desenhar(self, tela):
        self.contagem_imagem += 1

        if self.contagem_imagem < self.tempo_animaçao:
            self.imagem = self.IMGS[0]
        elif self.contagem_imagem < self.tempo_animaçao * 2:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem < self.tempo_animaçao * 3:
            self.imagem = self.IMGS[2]
        elif self.contagem_imagem < self.tempo_animaçao * 4:
            self.imagem = self.IMGS[1]
        else:
            self.imagem = self.IMGS[0]
            self.contagem_imagem = 0

        if self.angulo <= -80:
            self.imagem = self.IMGS[1]
            self.contagem_imagem = self.tempo_animaçao * 2

        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        pos_centro = self.imagem.get_rect(topleft=(self.x, self.y)).center
        retangulo = imagem_rotacionada.get_rect(center=pos_centro)
        tela.blit(imagem_rotacionada, retangulo.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.imagem)


class Cano:
    distancia = 200
    velocidade = 5

    def __init__(self, x):
        self.x = x
        self.altura = 0
        self.pos_topo = 0
        self.pos_base = 0
        self.cano_topo = pygame.transform.flip(imagem_cano, False, True)
        self.cano_base = imagem_cano
        self.passou = False
        self.definir_altura()

    def definir_altura(self):
        self.altura = random.randrange(50, 450)
        self.pos_topo = self.altura - self.cano_topo.get_height()
        self.pos_base = self.altura + self.distancia

    def mover(self):
        self.x -= self.velocidade

    def desenhar(self, tela):
        tela.blit(self.cano_topo, (self.x, self.pos_topo))
        tela.blit(self.cano_base, (self.x, self.pos_base))

    def colidir(self, passaro):
        passaro_mask = passaro.get_mask()
        topo_mask = pygame.mask.from_surface(self.cano_topo)
        base_mask = pygame.mask.from_surface(self.cano_base)

        distancia_topo = (self.x - passaro.x, self.pos_topo - round(passaro.y))
        distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y))

        topo_ponto = passaro_mask.overlap(topo_mask, distancia_topo)
        base_ponto = passaro_mask.overlap(base_mask, distancia_base)

        return topo_ponto or base_ponto


class Chao:
    velocidade = 5
    largura = imagem_chao.get_width()
    imagem = imagem_chao

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.largura

    def mover(self):
        self.x1 -= self.velocidade
        self.x2 -= self.velocidade

        if self.x1 + self.largura < 0:
            self.x1 = self.x2 + self.largura
        if self.x2 + self.largura < 0:
            self.x2 = self.x1 + self.largura

    def desenhar(self, tela):
        tela.blit(self.imagem, (self.x1, self.y))
        tela.blit(self.imagem, (self.x2, self.y))


# Funções principais
def desenhar_tela(tela, passaros, canos, chao, pontos):
    tela.blit(imagem_background, (0, 0))

    for passaro in passaros:
        passaro.desenhar(tela)

    for cano in canos:
        cano.desenhar(tela)

    texto = fonte_pontos.render(f"Pontuação: {pontos}", True, (255, 255, 255))
    tela.blit(texto, (tela_largura - 10 - texto.get_width(), 10))

    chao.desenhar(tela)
    pygame.display.update()


def tela_inicial():
    tela = pygame.display.set_mode((tela_largura, tela_altura))
    relogio = pygame.time.Clock()
    fonte_titulo = pygame.font.SysFont('arial', 70)
    fonte_botao = pygame.font.SysFont('arial', 40)

    while True:
        relogio.tick(30)
        tela.blit(imagem_background, (0, 0))

        texto_titulo = fonte_titulo.render("Junin Bird", True, (255, 255, 255))
        tela.blit(texto_titulo, ((tela_largura - texto_titulo.get_width()) // 2, 100))

        botao_start = pygame.Rect(150, 300, 200, 60)
        botao_quit = pygame.Rect(150, 400, 200, 60)

        pygame.draw.rect(tela, (0, 200, 0), botao_start)
        pygame.draw.rect(tela, (200, 0, 0), botao_quit)

        texto_start = fonte_botao.render("Start", True, (255, 255, 255))
        texto_quit = fonte_botao.render("Quit", True, (255, 255, 255))

        tela.blit(texto_start, (botao_start.x + (botao_start.width - texto_start.get_width()) // 2,
                                botao_start.y + (botao_start.height - texto_start.get_height()) // 2))
        tela.blit(texto_quit, (botao_quit.x + (botao_quit.width - texto_quit.get_width()) // 2,
                               botao_quit.y + (botao_quit.height - texto_quit.get_height()) // 2))
        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if botao_start.collidepoint(mouse_pos):
                    return main()
                elif botao_quit.collidepoint(mouse_pos):
                    pygame.quit()
                    quit()


def tela_game_over(pontuacao):
    tela = pygame.display.set_mode((tela_largura, tela_altura))
    relogio = pygame.time.Clock()
    fonte_titulo = pygame.font.SysFont('arial', 70)
    fonte_botao = pygame.font.SysFont('arial', 40)
    fonte_pontos = pygame.font.SysFont('arial', 50)

    while True:
        relogio.tick(30)
        tela.blit(imagem_background, (0, 0))

        texto_game_over = fonte_titulo.render("Game Over", True, (255, 0, 0))
        tela.blit(texto_game_over, ((tela_largura - texto_game_over.get_width()) // 2, 100))

        texto_pontos = fonte_pontos.render(f"Pontuação: {pontuacao}", True, (255, 255, 255))
        tela.blit(texto_pontos, ((tela_largura - texto_pontos.get_width()) // 2, 200))

        botao_restart = pygame.Rect(150, 350, 200, 60)
        botao_quit = pygame.Rect(150, 450, 200, 60)

        pygame.draw.rect(tela, (0, 200, 0), botao_restart)
        pygame.draw.rect(tela, (200, 0, 0), botao_quit)

        texto_restart = fonte_botao.render("Restart", True, (255, 255, 255))
        texto_quit = fonte_botao.render("Quit", True, (255, 255, 255))

        tela.blit(texto_restart, (botao_restart.x + (botao_restart.width - texto_restart.get_width()) // 2,
                                  botao_restart.y + (botao_restart.height - texto_restart.get_height()) // 2))
        tela.blit(texto_quit, (botao_quit.x + (botao_quit.width - texto_quit.get_width()) // 2,
                               botao_quit.y + (botao_quit.height - texto_quit.get_height()) // 2))
        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if botao_restart.collidepoint(mouse_pos):
                    return main()
                elif botao_quit.collidepoint(mouse_pos):
                    pygame.quit()
                    quit()


def main():
    passaros = [Passaro(230, 350)]
    chao = Chao(730)
    canos = [Cano(700)]
    tela = pygame.display.set_mode((tela_largura, tela_altura))
    pontos = 0
    relogio = pygame.time.Clock()

    while True:
        relogio.tick(30)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                for passaro in passaros:
                    passaro.pular()

        for passaro in passaros:
            passaro.mover()

        chao.mover()

        adicionar_cano = False
        remover_canos = []

        for cano in canos:
            for i, passaro in enumerate(passaros):
                if cano.colidir(passaro):
                    passaros.pop(i)
                if not cano.passou and passaro.x > cano.x:
                    cano.passou = True
                    adicionar_cano = True
            cano.mover()

        if adicionar_cano:
            pontos += 1
            canos.append(Cano(600))

        canos = [cano for cano in canos if cano.x + cano.cano_topo.get_width() > 0]

        for i, passaro in enumerate(passaros):
            if passaro.y + passaro.imagem.get_height() >= chao.y or passaro.y < 0:
                passaros.pop(i)

        if len(passaros) == 0:
            return tela_game_over(pontos)

        desenhar_tela(tela, passaros, canos, chao, pontos)


if __name__ == '__main__':
    tela_inicial()
