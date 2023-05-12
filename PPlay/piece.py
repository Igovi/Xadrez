from paths import get_asset_path


class Piece():
    Branca = "W"
    Preta = "B"

    def __init__(self, linha, coluna, color, piece_type, value):
        self.linha = linha
        self.coluna = coluna
        self.color = color
        self.piece_type = piece_type
        self.value = value
        self.first_move = True
    
    def movimento(self, board):
        tabuleiro = board.tabuleiro
        
        match self.piece_type:
            case "K":
                return tabuleiro[self.linha][self.coluna].get_possible_moves(board)
            case "Q":
                return tabuleiro[self.linha][self.coluna].get_possible_moves(tabuleiro)
            case "B":
                return tabuleiro[self.linha][self.coluna].get_possible_moves(tabuleiro)
            case "N":
                return tabuleiro[self.linha][self.coluna].get_possible_moves(tabuleiro)
            case "R":
                return tabuleiro[self.linha][self.coluna].get_possible_moves(tabuleiro)
            case "P":
                return tabuleiro[self.linha][self.coluna].get_possible_moves(tabuleiro)
    
    def promocao_peao(self):
        if self.color == self.Branca and self.linha == 0:
            return True
        elif self.color == self.Preta and self.linha == 7:
            return True
        return False

    def update_position(self, linha, coluna):
        self.linha = linha
        self.coluna = coluna
        self.first_move = False

# OK
class Rook(Piece):
    PIECE_TYPE = "R"
    VALUE = 500
    LADO = None
    
    def __init__(self, linha, coluna, color, lado):
        self.LADO = lado
        self.PATH = get_asset_path('whiteRook.png' if color == 'W' else 'blackRook.png')
        super(Rook, self).__init__(linha, coluna, color, Rook.PIECE_TYPE, Rook.VALUE)
    
    def get_possible_moves(self, tabuleiro):
        posicoes_possiveis = []

        # Verifica as posições possíveis na horizontal (mesma linha)
        for coluna in range(self.coluna - 1, -1, -1):
            if tabuleiro[self.linha][coluna] is None:
                posicoes_possiveis.append((self.linha, coluna))
            elif tabuleiro[self.linha][coluna].color != self.color:
                posicoes_possiveis.append((self.linha, coluna))
                break
            else:
                break

        for coluna in range(self.coluna + 1, len(tabuleiro[0])):
            if tabuleiro[self.linha][coluna] is None:
                posicoes_possiveis.append((self.linha, coluna))
            elif tabuleiro[self.linha][coluna].color != self.color:
                posicoes_possiveis.append((self.linha, coluna))
                break
            else:
                break

        # Verifica as posições possíveis na vertical (mesma coluna)
        for linha in range(self.linha - 1, -1, -1):
            if tabuleiro[linha][self.coluna] is None:
                posicoes_possiveis.append((linha, self.coluna))
            elif tabuleiro[linha][self.coluna].color != self.color:
                posicoes_possiveis.append((linha, self.coluna))
                break
            else:
                break

        for linha in range(self.linha + 1, len(tabuleiro)):
            if tabuleiro[linha][self.coluna] is None:
                posicoes_possiveis.append((linha, self.coluna))
            elif tabuleiro[linha][self.coluna].color != self.color:
                posicoes_possiveis.append((linha, self.coluna))
                break
            else:
                break

        return posicoes_possiveis

# OK
class Knight(Piece):
    PIECE_TYPE = "N"
    VALUE = 320
    
    def __init__(self, linha, coluna, color):
        self.PATH = get_asset_path('whiteKnight.png' if color == 'W' else 'blackKnight.png')
        super(Knight, self).__init__(linha, coluna, color, Knight.PIECE_TYPE, Knight.VALUE)
        
    def get_possible_moves(self, tabuleiro):
        posicoes_possiveis = []

        # Movimentos possíveis para o cavalo (em relação à sua posição)
        movimentos = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]

        # Verifica as posições possíveis para cada um dos movimentos
        for movimento in movimentos:
            nova_coluna = self.coluna + movimento[0]
            nova_linha = self.linha + movimento[1]

            # Verifica se a posição é válida e se não há uma peça da mesma cor na posição
            if (0 <= nova_linha < 8 and 0 <= nova_coluna < 8 and
                    (tabuleiro[nova_linha][nova_coluna] is None or
                     tabuleiro[nova_linha][nova_coluna].color != self.color)):
                posicoes_possiveis.append((nova_linha, nova_coluna))
        return posicoes_possiveis

# OK
class Bishop(Piece):
    PIECE_TYPE = "B"
    VALUE = 330

    def __init__(self, linha, coluna, color):
        self.PATH = get_asset_path('whiteBishop.png' if color == 'W' else 'blackBishop.png')
        super(Bishop, self).__init__(linha, coluna, color, Bishop.PIECE_TYPE, Bishop.VALUE)

    def get_possible_moves(self, tabuleiro):
        posicoes_possiveis = []

        # Verifica as posições possíveis na diagonal superior direita
        for i in range(1, 8):
            linha = self.linha - i
            coluna = self.coluna + i
            if linha < 0 or coluna > 7:
                break
            if tabuleiro[linha][coluna] is None:
                posicoes_possiveis.append((linha, coluna))
            elif tabuleiro[linha][coluna].color != self.color:
                posicoes_possiveis.append((linha, coluna))
                break
            else:
                break

        # Verifica as posições possíveis na diagonal inferior direita
        for i in range(1, 8):
            linha = self.linha + i
            coluna = self.coluna + i
            if linha > 7 or coluna > 7:
                break
            if tabuleiro[linha][coluna] is None:
                posicoes_possiveis.append((linha, coluna))
            elif tabuleiro[linha][coluna].color != self.color:
                posicoes_possiveis.append((linha, coluna))
                break
            else:
                break

        # Verifica as posições possíveis na diagonal inferior esquerda
        for i in range(1, 8):
            linha = self.linha + i
            coluna = self.coluna - i
            if linha > 7 or coluna < 0:
                break
            if tabuleiro[linha][coluna] is None:
                posicoes_possiveis.append((linha, coluna))
            elif tabuleiro[linha][coluna].color != self.color:
                posicoes_possiveis.append((linha, coluna))
                break
            else:
                break

        # Verifica as posições possíveis na diagonal superior esquerda
        for i in range(1, 8):
            linha = self.linha - i
            coluna = self.coluna - i
            if linha < 0 or coluna < 0:
                break
            if tabuleiro[linha][coluna] is None:
                posicoes_possiveis.append((linha, coluna))
            elif tabuleiro[linha][coluna].color != self.color:
                posicoes_possiveis.append((linha, coluna))
                break
            else:
                break

        return posicoes_possiveis

# OK
class Queen(Piece):
    PIECE_TYPE = "Q"
    VALUE = 900

    def __init__(self, linha, coluna, color):
        self.PATH = get_asset_path('whiteQueen.png' if color == 'W' else 'blackQueen.png')
        super(Queen, self).__init__(linha, coluna, color, Queen.PIECE_TYPE, Queen.VALUE)
        
    def get_possible_moves(self, tabuleiro):
        possible_moves = []
    
        # Movimentos horizontais e verticais
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for dx, dy in directions:
            for i in range(1, 8):
                new_linha = self.linha + dy * i
                new_coluna = self.coluna + dx * i
    
                if 0 <= new_linha < 8 and 0 <= new_coluna < 8:
                    target_piece = tabuleiro[new_linha][new_coluna]
                    if target_piece is None:
                        possible_moves.append((new_linha, new_coluna))
                    elif target_piece.color != self.color:
                        possible_moves.append((new_linha, new_coluna))
                        break
                    else:
                        break
                    
        # Movimentos diagonais
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dx, dy in directions:
            for i in range(1, 8):
                new_linha = self.linha + dy * i
                new_coluna = self.coluna + dx * i
    
                if 0 <= new_linha < 8 and 0 <= new_coluna < 8:
                    target_piece = tabuleiro[new_linha][new_coluna]
                    if target_piece is None:
                        possible_moves.append((new_linha, new_coluna))
                    elif target_piece.color != self.color:
                        possible_moves.append((new_linha, new_coluna))
                        break
                    else:
                        break
                    
        return possible_moves

# TODO Logica de Check
class King(Piece):
    PIECE_TYPE = "K"
    VALUE = 20000

    def __init__(self, linha, coluna, color):
        self.PATH = get_asset_path('whiteKing.png' if color == 'W' else 'blackKing.png')
        super(King, self).__init__(linha, coluna, color, King.PIECE_TYPE, King.VALUE)
        
    def get_possible_moves(self, board):
        posicoes_possiveis = []

        # Movimentos possíveis para o rei (em relação à sua posição)
        movimentos = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

        for movimento in movimentos:
            nova_coluna = self.coluna + movimento[0]
            nova_linha = self.linha + movimento[1]

            # Verifica se a posição é válida e se não há uma peça da mesma cor na posição
            if 0 <= nova_linha < 8 and 0 <= nova_coluna < 8:
                target_piece = board.tabuleiro[nova_linha][nova_coluna]
                if target_piece is None or target_piece.color != self.color:
                    posicoes_possiveis.append((nova_linha, nova_coluna))

        # Adicionar roque se o rei ainda não se moveu
        if self.first_move:
            for col in (0, 7):  # Colunas das torres (roque longo e curto)
                rook = board.tabuleiro[self.linha][col]
                if rook is not None and rook.piece_type == "R" and rook.first_move:
                    if self.is_roque_possible(board, rook.coluna):
                        posicoes_possiveis.append((self.linha, self.coluna + 2 if col == 7 else self.coluna - 2))

        return posicoes_possiveis

    def is_roque_possible(self, board, rook_col):
        start_col = min(self.coluna, rook_col) + 1
        end_col = max(self.coluna, rook_col) - 1

        # Verificar se as casas entre o rei e a torre estão vazias
        for col in range(start_col, end_col + 1):
            if board.tabuleiro[self.linha][col] is not None:
                return False

        # Verificar se o rei está em xeque ou se passa por casas em xeque durante o roque
        direction = 1 if rook_col > self.coluna else -1
        for col_offset in range(direction, 3 * direction, direction):
            target_col = self.coluna + col_offset
            if 0 <= target_col < 8:
                # Faz a jogada temporária e verifica se o rei fica em xeque
                temp = board.tabuleiro[self.linha][self.coluna]
                board.tabuleiro[self.linha][self.coluna] = None
                board.tabuleiro[self.linha][target_col] = temp
                is_check = False # board.is_check(self.color)
                
                # Desfaz a jogada temporária
                board.tabuleiro[self.linha][self.coluna] = temp
                board.tabuleiro[self.linha][target_col] = None

                if is_check:
                    return False

        return True

# OK
class Pawn(Piece):
    PIECE_TYPE = "P"
    VALUE = 100

    def __init__(self, linha, coluna, color):
        self.PATH = get_asset_path('whitePawn.png' if color == 'W' else 'blackPawn.png')
        super(Pawn, self).__init__(linha, coluna, color, Pawn.PIECE_TYPE, Pawn.VALUE)
        
    def get_possible_moves(self, tabuleiro):
        posicoes_possiveis = []

        # Define o sentido do movimento do peão (de acordo com a sua cor)
        sentido = 1 if self.color != self.Branca else -1

        # Verifica o movimento de avanço
        nova_linha = self.linha + sentido
        if nova_linha >= 0 and nova_linha < 8 and tabuleiro[nova_linha][self.coluna] is None:
            posicoes_possiveis.append((nova_linha, self.coluna))

            # Verifica o movimento de avanço duplo (apenas se o peão ainda não se moveu)
            if (self.color == self.Branca and self.linha == 6) or (self.color == self.Preta and self.linha == 1):
                nova_linha = self.linha + sentido * 2
                if tabuleiro[nova_linha][self.coluna] is None:
                    posicoes_possiveis.append((nova_linha, self.coluna))

        # Verifica os movimentos de captura diagonal
        for coluna in range(self.coluna - 1, self.coluna + 2):
            if coluna < 0 or coluna >= 8 or coluna == self.coluna:
                continue

            nova_linha = self.linha + sentido
            if nova_linha >= 0 and nova_linha < 8:
                peca = tabuleiro[nova_linha][coluna]
                if peca is not None and peca.color != self.color:
                    posicoes_possiveis.append((nova_linha, coluna))

        return posicoes_possiveis
