import pygame

# inicialização do pygame
pygame.init()

# configurações da tela
tamanho_tela = (650, 650)
tela = pygame.display.set_mode(tamanho_tela)
pygame.display.set_caption("Brick Breaker")

# configurações dos elementos do jogo
tamanho_bola = 12
bola = pygame.Rect(100, 400, tamanho_bola, tamanho_bola)
tamanho_jogador = 100
jogador = pygame.Rect(0, 600, tamanho_jogador, 15)

qtde_blocos_por_linha = 8
qtde_linhas_blocos = 5
qtde_total_blocos = qtde_blocos_por_linha * qtde_linhas_blocos


def criar_blocos(qtde_blocos_por_linha, qtde_linhas_blocos):
    altura_tela = tamanho_tela[1]
    largura_tela = tamanho_tela[0]
    distancia_entre_blocos = 5
    largura_bloco = largura_tela / qtde_blocos_por_linha - distancia_entre_blocos
    altura_bloco = 15
    distancia_entre_linhas = altura_bloco + 10

    blocos = []
    for j in range(qtde_linhas_blocos):
        for i in range(qtde_blocos_por_linha):
            bloco = pygame.Rect(
                i * (largura_bloco + distancia_entre_blocos),
                j * distancia_entre_linhas,
                largura_bloco,
                altura_bloco,
            )
            blocos.append(bloco)
    return blocos


# dicionário de cores (RGB)
cores = {
    "branca": (255, 255, 255),
    "preta": (0, 0, 0),
    "amarela": (255, 255, 0),
    "azul": (0, 0, 255),
    "verde": (0, 255, 0),
}

# variáveis de controle do jogo
fim_jogo = False
pontuacao = 0
movimento_bola = [2, -2]  # [eixo_x, eixo_y] — começa subindo


# funções de desenho e regras
def desenhar_inicio_jogo(jogador, bola, cores):
    tela.fill(cores["preta"])
    pygame.draw.rect(tela, cores["azul"], jogador)
    pygame.draw.rect(tela, cores["branca"], bola)


def desenhar_blocos(blocos, cores):
    for bloco in blocos:
        pygame.draw.rect(tela, cores["verde"], bloco)


def movimentar_jogador(jogador):
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_RIGHT]:
        if (jogador.x + tamanho_jogador) < tamanho_tela[0]:
            jogador.x += 2
    if teclas[pygame.K_LEFT]:
        if jogador.x > 0:
            jogador.x -= 2


def movimentar_bola(bola, movimento_bola, jogador, blocos):
    movimento = movimento_bola[:]
    bola.x += movimento[0]
    bola.y += movimento[1]

    # colisão com as bordas da tela
    if bola.x <= 0:
        movimento[0] = -movimento[0]
    if bola.y <= 0:
        movimento[1] = -movimento[1]
    if (bola.x + tamanho_bola) >= tamanho_tela[0]:
        movimento[0] = -movimento[0]
    if (bola.y + tamanho_bola) >= tamanho_tela[1]:
        # bola passou pelo fundo da tela: encerra o movimento
        return None

    # colisão com a barra do jogador
    if jogador.collidepoint(bola.x, bola.y) or jogador.collidepoint(
        bola.x + tamanho_bola, bola.y + tamanho_bola
    ):
        movimento[1] = -movimento[1]

    # colisão com os blocos
    for bloco in blocos:
        if bloco.collidepoint(bola.x, bola.y) or bloco.collidepoint(
            bola.x + tamanho_bola, bola.y + tamanho_bola
        ):
            blocos.remove(bloco)
            movimento[1] = -movimento[1]
            break

    return movimento


def atualizar_pontuacao(pontuacao):
    fonte = pygame.font.Font(None, 30)
    texto = fonte.render(f"Pontuação: {pontuacao}", 1, cores["amarela"])
    tela.blit(texto, (10, 10)) # local onde fica a pontuação na tela

    if pontuacao >= qtde_total_blocos:
        return True
    else:
        return False


# criação inicial dos blocos
blocos = criar_blocos(qtde_blocos_por_linha, qtde_linhas_blocos)

# loop principal do jogo
while not fim_jogo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            fim_jogo = True

    desenhar_inicio_jogo(jogador, bola, cores)
    desenhar_blocos(blocos, cores)
    fim_jogo = atualizar_pontuacao(qtde_total_blocos - len(blocos))

    movimentar_jogador(jogador)
    movimento_bola = movimentar_bola(bola, movimento_bola, jogador, blocos)

    if not movimento_bola:
        fim_jogo = True

    pygame.time.wait(1)
    pygame.display.flip()

pygame.quit()
