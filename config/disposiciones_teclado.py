class DisposicionesTeclado:
    def __init__(self):
        self.teclas_normal = [
            ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
            ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
            ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
            ['Z', 'X', 'C', 'V', 'B', 'N', 'M', 'DEL'],
            ['CTRL', 'SHIFT', 'SPACE', 'ENTER', 'TAB']
        ]
        
        self.teclas_shift = [
            ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')'],
            ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
            ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
            ['+', '=', '{', '}', '[', ']', '|', '\\', 'DEL'],
            ['CTRL', 'SHIFT', 'SPACE', 'ENTER', 'TAB']
        ]
        
        self.teclas_especiales = ['CTRL', 'SHIFT', 'SPACE', 'ENTER', 'TAB', 'DEL']
    
    def obtener_ancho_tecla(self, tecla: str, ancho_base: int) -> int:
        if tecla == 'SPACE':
            return ancho_base * 6
        elif tecla in ['SHIFT', 'CTRL', 'ENTER', 'TAB']:
            return int(ancho_base * 2.25)
        elif tecla == 'DEL':
            return ancho_base * 2
        else:
            return ancho_base