import copy
from PPlay.piece import Bishop, King, Knight, Pawn, Piece, Queen, Rook

class Board:
    window_size = 800
    # Define o tamanho de cada quadrado do tabuleiro
    TAMANHO_QUADRADO = window_size / 8
    
    def __init__(self):
        self.tabuleiro = [[None for j in range(8)] for i in range(8)]
        self.jogador_da_vez = "W"
        self.origem = None
        self.destino = None
        self.movimentos = None
        self.posicionar_peças()
    
    def set_origem(self, linha, coluna):
        self.origem = (linha, coluna)
        self.movimentos = self.rotas_movimento()

    
    # PREPARAR XADREZ PARA INICIO DO JOGO, GRAFICO + POSICOES DAS PEÇAS    
    def desenhar_tabuleiro(self, pygame, janela):
        COR1 = (255, 244, 139) # Player 1
        COR2 = (117, 59, 39) # Player 2
        COR3 = (255, 0, 0) # Selecionado
        
        # Calcula a posição do quadrado na tela
        for linha in range(8):
            for coluna in range(8):
                x = coluna * self.TAMANHO_QUADRADO
                y = linha * self.TAMANHO_QUADRADO
                
                if self.movimentos is not None and (linha, coluna) in self.movimentos:
                    cor = COR3
                else:
                    cor = COR1 if (linha + coluna) % 2 == 0 else COR2
                # Desenha o quadrado na tela
                pygame.draw.rect(janela, cor, (x, y, self.TAMANHO_QUADRADO, self.TAMANHO_QUADRADO))
                
    def posicionar_peças(self):
        pieces = [
            [Pawn(1, i, Piece.Preta) for i in range(8)],
            [Pawn(6, i, Piece.Branca) for i in range(8)],
            Rook(0, 0, Piece.Preta, "ESQ"),
            Rook(0, 7, Piece.Preta, "DIR"),
            Rook(7, 0, Piece.Branca, "ESQ"),
            Rook(7, 7, Piece.Branca, "DIR"),
            Knight(0, 1, Piece.Preta),
            Knight(0, 6, Piece.Preta),
            Knight(7, 1, Piece.Branca),
            Knight(7, 6, Piece.Branca),
            Bishop(0, 2, Piece.Preta),
            Bishop(0, 5, Piece.Preta),
            Bishop(7, 2, Piece.Branca),
            Bishop(7, 5, Piece.Branca),
            King(7, 4, Piece.Branca),
            King(0, 4, Piece.Preta),
            Queen(7, 3, Piece.Branca),
            Queen(0, 3, Piece.Preta)
        ]

        for piece in pieces:
            if isinstance(piece, list):
                for pawn in piece:
                    if pawn is not None:
                        self.tabuleiro[pawn.linha][pawn.coluna] = pawn
            else:
                self.tabuleiro[piece.linha][piece.coluna] = piece
        self.tabuleiro

    def desenhar_pecas(self, pygame, janela):
        for linha in range(8):
            for coluna in range(8):
                x = coluna * self.TAMANHO_QUADRADO
                y = linha * self.TAMANHO_QUADRADO
                # Desenha a peça na posição inicial correspondente na matriz
                if self.tabuleiro[linha] is not None and self.tabuleiro[linha][coluna] is not None:
                    peca_imagem = pygame.image.load(self.tabuleiro[linha][coluna].PATH)
                    # Obtém um objeto Rect que representa a imagem da peça e define sua posição central como o centro do quadrado
                    peca_rect = peca_imagem.get_rect()
                    peca_rect.center = (x + self.TAMANHO_QUADRADO // 2, y + self.TAMANHO_QUADRADO // 2)
                    # Desenha a imagem da peça na tela
                    janela.blit(peca_imagem, peca_rect)
    # FIM DA INICIALIZAÇÃO
    
    
    # MOVIMENTACAO
    # Temos que pegar o board atualizado, se usarmos o do self, estaremos apontando para uma versao diferente
    def rotas_movimento(self):
        movimentos = []
        if self.origem is not None:
            linha = self.origem[0]
            coluna = self.origem[1]
            movimentos = self.tabuleiro[linha][coluna].movimento(self)
        return movimentos
    
    def mover_elemento(self, atualizar_pecas=True):
        torres = [(0,0), (0,7), (7,0), (7,7)]
        
        # Obter o valor do elemento na posição antiga
        peca = self.tabuleiro[self.origem[0]][self.origem[1]]
    
        # Definir o valor do elemento na posição antiga como None
        self.tabuleiro[self.origem[0]][self.origem[1]] = None
        
        # Tratamento para o caso de Rook (Roque)
        if isinstance(peca, King):
            try:
                offsets = [1, -2]  # Possíveis deslocamentos para encontrar a torre
                torre = None
                for offset in offsets:
                    try:
                        torre_index = torres.index((self.destino[0], self.destino[1] + offset))
                        linha, coluna = torres[torre_index]
                        torre = self.tabuleiro[linha][coluna]
                        if isinstance(torre, Rook):
                            break  # Encontramos a torre, então podemos sair do loop
                    except ValueError:
                        continue  # Se não encontrarmos a torre, tentamos o próximo deslocamento
                    
                if torre and torre.LADO == "DIR":  # Para a torre à direita
                    new_torre_coluna = self.destino[1] - 1
                else:  # Para a torre à esquerda
                    new_torre_coluna = self.destino[1] + 1
    
                # Move a Torre
                self.tabuleiro[linha][coluna] = None
                self.tabuleiro[self.destino[0]][new_torre_coluna] = torre
                torre.update_position(self.destino[0], new_torre_coluna)
            except:
                pass  # Ignoramos qualquer exceção no processo de roque e prosseguimos com o movimento normal
        
        # Definir o valor do elemento na nova posição como o valor da posição antiga
        self.tabuleiro[self.destino[0]][self.destino[1]] = peca
        
        if atualizar_pecas:
            # Atualiza na peça sua localizacao
            self.tabuleiro[self.destino[0]][self.destino[1]].update_position(self.destino[0], self.destino[1])
            
        if isinstance(peca, Pawn):
            if peca.promocao_peao():
                self.tabuleiro[self.destino[0]][self.destino[1]] = Queen(self.destino[0], self.destino[1], peca.color)

    def is_checkmate(self):
        player = self.jogador_da_vez
        # Verifica se o rei está em xeque
        if self.is_check():
            # Verifica se há alguma jogada possível para o jogador
            for row in range(8):
                for col in range(8):
                    if self.tabuleiro[row][col] is not None and self.tabuleiro[row][col].color == player:
                        piece = self.tabuleiro[row][col]
                        if isinstance(piece, King):
                            possible_moves = piece.get_possible_moves(self)
                        else:
                            possible_moves = piece.get_possible_moves(self.tabuleiro)
                        for move in possible_moves:
                            # Simula a jogada
                            temp_board = copy.deepcopy(self.tabuleiro)
                            temp_board[move[0]][move[1]] = temp_board[row][col]
                            temp_board[row][col] = None
                            # Verifica se o rei ainda está em xeque
                            if not self.is_check():
                                return False
            # Se não há jogadas possíveis, é checkmate
            return True
        else:
            return False


    def is_check(self):
        player = self.jogador_da_vez
        king_position = self.achar_posicao_rei()
        # Verifica se alguma peça do outro jogador pode atacar o rei
        for row in range(8):
            for col in range(8):
                piece = self.tabuleiro[row][col]
                if piece is not None and piece.color != player:
                    if isinstance(piece, King):
                        possible_moves = piece.get_possible_moves(self)
                    else:
                        possible_moves = piece.get_possible_moves(self.tabuleiro)
                    if king_position in possible_moves:
                        return True
        return False

    def achar_posicao_rei(self):
        player = self.jogador_da_vez
        for pecas in self.tabuleiro:
            for peca in pecas:
                if isinstance(peca, King) and peca.color == player:
                    return (peca.linha, peca.coluna)
        return None

    def inverter_jogador(self):
        self.jogador_da_vez = "B" if self.jogador_da_vez == "W" else "W"
    
    def limpar_jogada(self):
        self.origem = None
        self.destino = None
        self.movimentos = None
        
    def __deepcopy__(self, memo):
        # Cria uma nova instância da classe Board
        new_board = Board()
        new_board.jogador_da_vez = self.jogador_da_vez
        new_board.origem = copy.deepcopy(self.origem, memo)
        new_board.destino = copy.deepcopy(self.destino, memo)
        new_board.movimentos = copy.deepcopy(self.movimentos, memo)
        new_board.tabuleiro = [[copy.deepcopy(peca, memo) for peca in linha] for linha in self.tabuleiro]
        return new_board