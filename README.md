# Junin Bird

Um jogo no estilo Flappy Bird que fiz em Python com Pygame para treinar lógica, orientação a objetos e o básico de como um jogo funciona por dentro.

## Como jogar

Aperte **espaço** para o passarinho bater as asas e passe entre os canos sem encostar em nada. Cada cano que você passa vale um ponto.

O jogo tem tela inicial com os botões Start e Quit, placar durante a partida e uma tela de Game Over que mostra a pontuação e deixa recomeçar.

## Como rodar

Precisa de Python 3.

```bash
pip install pygame
```

```bash
python Game_flappybird.py
```

Rode o comando de dentro da pasta do projeto, porque o jogo carrega as imagens da pasta `imgs`.

## Como o código está organizado

Fica tudo em `Game_flappybird.py`:

- `Passaro` cuida do pulo, da queda, da rotação e da animação das asas
- `Cano` sorteia a altura de cada cano e verifica a colisão com o passarinho
- `Chao` faz o chão correr sem parar
- `tela_inicial`, `main` e `tela_game_over` controlam as três telas do jogo

## O que aprendi

Foi meu primeiro contato com um loop de jogo: ler os eventos do teclado, atualizar a posição de cada objeto e redesenhar a tela a cada quadro. Também foi onde entendi melhor classes, já que cada elemento do jogo virou uma.
