
from random import choice
from turtle import *
from freegames import floor, vector

state = {'score': 0} # Dicionário para armazenar a pontuação do jogo
path = Turtle(visible=False) # Objeto Turtle para desenhar caminhos
writer = Turtle(visible=False) # Objeto Turtle para escrever informações
aim = vector(0, 0) # Vetor que representa a direção inicial do Patriota
pacman = vector(-20, 0) # Vetor que representa a posição inicial do Patriota
ghosts = [ # Lista de Comunistas com os vetores de posições, direções e velocidades
    [vector(-50, 120), vector(-10, 0), 0.5],
    [vector(120, -50), vector(-10, 0), 1.0], 
    
]
# fmt: off
# Configuração do Mapa
tiles = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0,
    0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0,
    0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0,
    0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
]
# fmt: on


def square(x, y):
    """controla na posição (x, y)."""
    path.up()
    path.goto(x, y)
    path.down()
    path.begin_fill()

    for count in range(4):
        path.forward(20)
        path.left(90)

    path.end_fill()


def offset(point):
    """Retorna o deslocamento do ponto na lista."""
    x = (floor(point.x, 20) + 200) / 20
    y = (180 - floor(point.y, 20)) / 20
    index = int(x + y * 20)
    return index


def valid(point):
    """Retorna True se o ponto for válido."""
    index = offset(point)

    if tiles[index] == 0:
        return False

    index = offset(point + 19)

    if tiles[index] == 0:
        return False

    return point.x % 20 == 0 or point.y % 20 == 0


def world():
    """Desenha o mapa."""
    bgcolor('green') # Cor do mapa
    path.color('yellow') # Cor do mapa

    for index in range(len(tiles)):
        tile = tiles[index]

        if tile > 0:
            x = (index % 20) * 20 - 200
            y = 180 - (index // 20) * 20
            square(x, y)

            if tile == 1:
                path.up()
                path.goto(x + 10, y + 10)
                path.dot(3, 'blue') # Tamanho e cor dos pontos


def move():
    """Move o Pacman e todos os fantasmas."""
    writer.undo()
    writer.write("Verbas:", align="right", font=("Arial", 16, "normal")) # print para pontuação
    writer.write(state['score'],font=("Arial", 16, "normal")) # Recebe a pontuação atual do jogo usando o objeto "writer".

    clear() 

    if valid(pacman + aim): 
        pacman.move(aim)

    index = offset(pacman) 

    if tiles[index] == 1: 
        tiles[index] = 2
        state['score'] += 1
        x = (index % 20) * 20 - 200
        y = 180 - (index // 20) * 20
        square(x, y)

    up() 
    goto(pacman.x + 10, pacman.y + 10)
    dot(35, 'blue') # Tamanho e cor do Patriota
    
    for point, course, speed in ghosts: # Posição, Direção e Velocidade
        if valid(point + course * speed):
            point.move(course * speed)
        else: # Senão um novo vetor de direção é escolhido aleatoriamente
            options = [
                
                vector(0, -10),
                vector(10, 0),
                vector(0, 10),
                vector(-10, 0),
            ]
            
            plan = choice(options)
            course.x = plan.x
            course.y = plan.y

        up()
        goto(point.x + 10, point.y + 10)
    
        dot(20, 'red') # Tamanho e cor dos Comunistas
      

    update()

    for point, course, speed in ghosts: # Verifica a colisão
        if abs(pacman - point) < 20:
           writer.goto(vector(-20, 0)) #posição
           writer.color('red') # cor
           writer.write("INELEGÍVEL:", align="center", font=("Arial", 16, "normal")) #fim de jogo
           return 
        


    ontimer(move, 40) # Velocidade do jogo


def change(x, y):
    """Altera a direção do Pacman se for válida."""
    if valid(pacman + vector(x, y)):
        aim.x = x
        aim.y = y


setup(600, 400, 370, 0)  # Configura a tela
hideturtle()  # Esconde a tartaruga padrão
tracer(False)  # Desativa a animação
writer.goto(160, 160)  # Posiciona o objeto `writer`
writer.color('white')  # Define a cor do texto do `writer`
writer.write(state['score'])  # Escreve a pontuação inicial
listen()  # Habilita a escuta de eventos do teclado
onkey(lambda: change(5, 0), 'Right')  # Associa a tecla 'Right' à função `change()` com os parâmetros corretos
onkey(lambda: change(-5, 0), 'Left')  # Associa a tecla 'Left' à função `change()` com os parâmetros corretos
onkey(lambda: change(0, 5), 'Up')  # Associa a tecla 'Up' à função `change()` com os parâmetros corretos
onkey(lambda: change(0, -5), 'Down')  # Associa a tecla 'Down' à função `change()` com os parâmetros corretos
world()  # Desenha o mundo inicial do labirinto
move()  # Inicia o movimento
done()  # Finaliza o jogo
