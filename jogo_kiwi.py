import random
import pygame

# Inicializa o Pygame
pygame.init()

# Definir as dimensões da tela
largura_tela = 800
altura_tela = 600
screen = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption('Jogo do Kiwi')

# Carregar imagens
cenario = pygame.image.load("cenario_grama.png")
cenario = pygame.transform.scale(cenario, (largura_tela, altura_tela))  # Ajusta ao tamanho da tela

personagem_img = pygame.image.load("fantasminha_camarada.png")
personagem_img = pygame.transform.scale(personagem_img, (64, 64))  # Fantasma maior

kiwi_img = pygame.image.load("kiwi_fruit.png")
kiwi_img = pygame.transform.scale(kiwi_img, (40, 40))  # Kiwi um pouco maior

# Fonte para o texto
fonte = pygame.font.Font(None, 36)

# Relógio para controlar o FPS
clock = pygame.time.Clock()

# Botão "Voltar" (coordenadas e tamanho)
botao_voltar = pygame.Rect(650, 10, 140, 40)


# Classe do Personagem
class Personagem(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = personagem_img
        self.rect = self.image.get_rect()
        self.rect.x = largura_tela // 2
        self.rect.y = altura_tela // 2

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT] and self.rect.right < largura_tela:
            self.rect.x += 5
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= 5
        if keys[pygame.K_DOWN] and self.rect.bottom < altura_tela:
            self.rect.y += 5


# Classe do Kiwi
class Kiwi(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = kiwi_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, largura_tela - 40)
        self.rect.y = random.randint(0, altura_tela - 40)


# Função para exibir a tela inicial
def tela_inicial():
    esperando = True
    while esperando:
        screen.fill((50, 168, 82))  # Fundo verde para a tela inicial
        titulo = fonte.render("Jogo do Kiwi", True, (255, 255, 255))
        instrucao = fonte.render("Pressione ENTER para jogar", True, (255, 255, 255))

        screen.blit(titulo, (largura_tela // 2 - titulo.get_width() // 2, 200))
        screen.blit(instrucao, (largura_tela // 2 - instrucao.get_width() // 2, 300))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    esperando = False


# Função para rodar o jogo
def jogo():
    player = Personagem()
    kiwis = pygame.sprite.Group()

    # Criar 5 kiwis na tela inicialmente
    for _ in range(5):
        kiwis.add(Kiwi())

    # Variável de pontuação
    pontuacao = 0

    rodando = True
    while rodando:
        screen.blit(cenario, (0, 0))  # Aplica o novo fundo de grama

        keys = pygame.key.get_pressed()
        player.update(keys)

        # Checa colisão do personagem com os kiwis
        colisoes = pygame.sprite.spritecollide(player, kiwis, True)
        pontuacao += len(colisoes)  # Aumenta a pontuação conforme pega os kiwis

        # Adiciona novos kiwis quando algum for coletado
        for _ in range(len(colisoes)):
            kiwis.add(Kiwi())

        # Desenha os sprites na tela
        screen.blit(player.image, player.rect)
        kiwis.draw(screen)

        # Exibir pontuação
        texto_pontos = fonte.render(f"Pontos: {pontuacao}", True, (0, 0, 0))
        screen.blit(texto_pontos, (10, 10))

        # Desenhar o botão "Voltar"
        pygame.draw.rect(screen, (200, 0, 0), botao_voltar)
        texto_voltar = fonte.render("Voltar", True, (255, 255, 255))
        screen.blit(texto_voltar, (botao_voltar.x + 30, botao_voltar.y + 5))

        pygame.display.flip()

        # Controlar FPS
        clock.tick(30)

        # Capturar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if botao_voltar.collidepoint(event.pos):
                    return  # Sai do jogo e volta para a tela inicial


# **Rodando o jogo**
while True:
    tela_inicial()
    jogo()
