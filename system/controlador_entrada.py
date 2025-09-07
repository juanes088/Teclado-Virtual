import time
import threading
from pynput.keyboard import Key, Controller
from pynput import mouse

class ControladorEntrada:
    def __init__(self, config):
        self.config = config
        self.controlador_teclado = Controller()
        self.controlador_mouse = mouse.Controller()
    
    def procesar_tecla(self, tecla: str, texto_escrito: str, shift_activo: bool, ctrl_activo: bool) -> tuple:
        """procesa una tecla y retorna (nuevo_texto, nuevo_shift, nuevo_ctrl)"""
        def hilo_tecla():
            try:
                time.sleep(self.config.RETRASO_TECLA)

                if tecla == 'DEL':
                    self.controlador_teclado.press(Key.backspace)
                    self.controlador_teclado.release(Key.backspace)
                elif tecla == 'SPACE':
                    self.controlador_teclado.press(Key.space)
                    self.controlador_teclado.release(Key.space)
                elif tecla == 'ENTER':
                    self.controlador_teclado.press(Key.enter)
                    self.controlador_teclado.release(Key.enter)
                elif tecla == 'TAB':
                    self.controlador_teclado.press(Key.tab)
                    self.controlador_teclado.release(Key.tab)
                elif tecla not in ['SHIFT', 'CTRL']:
                    if tecla.isalpha():
                        caracter = tecla.upper() if shift_activo else tecla.lower()
                        if self.config.sistema_operativo == "Darwin":
                            self.controlador_teclado.type(caracter)
                        else:
                            self.controlador_teclado.press(caracter)
                            self.controlador_teclado.release(caracter)
                    else:
                        if self.config.sistema_operativo == "Darwin":
                            self.controlador_teclado.type(tecla)
                        else:
                            self.controlador_teclado.press(tecla)
                            self.controlador_teclado.release(tecla)
            except Exception:
                # silenciar errores en el hilo para no bloquear loop principal
                pass

        threading.Thread(target=hilo_tecla, daemon=True).start()
        
        # Actualizar texto local
        nuevo_texto = texto_escrito
        nuevo_shift = shift_activo
        nuevo_ctrl = ctrl_activo
        
        if tecla == 'DEL':
            if nuevo_texto:
                nuevo_texto = nuevo_texto[:-1]
        elif tecla == 'SPACE':
            nuevo_texto += ' '
        elif tecla == 'ENTER':
            nuevo_texto += '\n'
        elif tecla == 'TAB':
            nuevo_texto += '\t'
        elif tecla == 'SHIFT':
            nuevo_shift = not shift_activo
        elif tecla == 'CTRL':
            nuevo_ctrl = not ctrl_activo
        else:
            if tecla.isalpha():
                caracter = tecla.upper() if shift_activo else tecla.lower()
                nuevo_texto += caracter
                if shift_activo:
                    nuevo_shift = False
            else:
                nuevo_texto += tecla
        
        return nuevo_texto, nuevo_shift, nuevo_ctrl