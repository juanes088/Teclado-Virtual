import warnings
warnings.filterwarnings("ignore")

import cv2
import time
import threading
from pynput.keyboard import Listener

from config.ajustes import ConfiguracionTeclado
from config.disposiciones_teclado import DisposicionesTeclado
from core.seguimiento_manos import SeguimientoManos
from core.filtros_posicion import FiltrosPosicion
from interfaz.interfaz_teclado import InterfazTeclado
from interfaz.elementos_visuales import ElementosVisuales
from system.controlador_entrada import ControladorEntrada
from system.adaptadores_so import AdaptadoresSO

class MotorTeclado:
    def __init__(self):
        # configuraciones
        self.config = ConfiguracionTeclado()
        self.disposiciones = DisposicionesTeclado()
        
        # modulos principales
        self.seguimiento_manos = SeguimientoManos(self.config)
        self.filtros_posicion = FiltrosPosicion(self.config)
        self.interfaz_teclado = InterfazTeclado(self.config, self.disposiciones)
        self.elementos_visuales = ElementosVisuales(self.config)
        self.controlador_entrada = ControladorEntrada(self.config)
        self.adaptadores_so = AdaptadoresSO(self.config)
        
        # camara
        self.cap = cv2.VideoCapture(0)
        self.cap = self.adaptadores_so.configurar_camara(self.cap)
        
        # estados generales
        self.activo = True
        self.texto_escrito = ""
        self.en_ejecucion = True
        self.ventana_creada = False
        
        self.shift_activo = False
        self.ctrl_activo = False
    
    def ejecutar(self):
        if not self.ventana_creada:
            self.adaptadores_so.configurar_ventana(self.config.NOMBRE_VENTANA)
            self.ventana_creada = True

        while self.en_ejecucion:
            try:
                ret, frame = self.cap.read()
                if not ret:
                    break

                frame = cv2.flip(frame, 1)
                resultados = self.seguimiento_manos.obtener_landmarks_mano(frame)
                landmarks_izq = None
                landmarks_der = None

                if resultados.multi_hand_landmarks:
                    for landmarks, handedness in zip(resultados.multi_hand_landmarks,
                                                     resultados.multi_handedness):
                        etiqueta = handedness.classification[0].label
                        self.seguimiento_manos.dibujar_landmarks(frame, landmarks)
                        if etiqueta == 'Left':
                            landmarks_izq = landmarks
                        else:
                            landmarks_der = landmarks

                # mano izquierda
                pos_indice_izq = None
                pos_pulgar_izq = None
                if landmarks_izq:
                    pos = self.seguimiento_manos.obtener_posiciones_dedos(landmarks_izq)
                    if 'indice_tip' in pos:
                        estable = self.filtros_posicion.estabilizar_posicion(pos['indice_tip'], 'izq')
                        tecla_actual = self.interfaz_teclado.obtener_tecla_en_pos(estable)
                        tecla_estable = self.filtros_posicion.detectar_hover_estable(tecla_actual, 'izq')
                        distancia = self.seguimiento_manos.calcular_distancia_pellizco(pos)
                        if tecla_estable and self.seguimiento_manos.detectar_click_estable(distancia, 'izq'):
                            self.procesar_tecla_pulsada(tecla_estable)
                        pos_indice_izq = estable
                    if 'pulgar_tip' in pos:
                        pos_pulgar_izq = pos['pulgar_tip']

                # mano derecha
                pos_indice_der = None
                pos_pulgar_der = None
                if landmarks_der:
                    pos = self.seguimiento_manos.obtener_posiciones_dedos(landmarks_der)
                    if 'indice_tip' in pos:
                        estable = self.filtros_posicion.estabilizar_posicion(pos['indice_tip'], 'der')
                        tecla_actual = self.interfaz_teclado.obtener_tecla_en_pos(estable)
                        tecla_estable = self.filtros_posicion.detectar_hover_estable(tecla_actual, 'der')
                        distancia = self.seguimiento_manos.calcular_distancia_pellizco(pos)
                        if tecla_estable and self.seguimiento_manos.detectar_click_estable(distancia, 'der'):
                            self.procesar_tecla_pulsada(tecla_estable)
                        pos_indice_der = estable
                    if 'pulgar_tip' in pos:
                        pos_pulgar_der = pos['pulgar_tip']

                # dibujar teclado
                frame = self.interfaz_teclado.dibujar_teclado(
                    frame, 
                    self.filtros_posicion.hover_estable_izq,
                    self.filtros_posicion.hover_estable_der,
                    self.shift_activo,
                    self.ctrl_activo
                )

                # dibujar indicadores de dedos
                self.elementos_visuales.dibujar_indicadores_dedos(
                    frame, pos_indice_izq, pos_pulgar_izq, pos_indice_der, pos_pulgar_der
                )
                
                # dibujar panel de estado
                self.elementos_visuales.dibujar_panel_estado(frame, self.texto_escrito)

                cv2.imshow(self.config.NOMBRE_VENTANA, frame)
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    self.en_ejecucion = False
                    break
            except Exception:
                # Romper en caso de error no controlado
                break
        self.limpiar()
    
    def procesar_tecla_pulsada(self, tecla: str):
        """procesa una tecla pulsada"""
        self.seguimiento_manos.actualizar_tiempo_tecla()
        self.interfaz_teclado.marcar_tecla_pulsada(tecla)
        
        # procesar la tecla
        self.texto_escrito, self.shift_activo, self.ctrl_activo = self.controlador_entrada.procesar_tecla(
            tecla, self.texto_escrito, self.shift_activo, self.ctrl_activo
        )
        
        # actualizar layout si cambio shift
        self.interfaz_teclado.actualizar_layout(self.shift_activo)
    
    def limpiar(self):
        """libera los recursos"""
        self.en_ejecucion = False
        self.adaptadores_so.limpiar_recursos(self.cap)
    
    def manejar_presion_fisica(self, key):
        """maneja la presion de la tecla física para permitir cerrar"""
        try:
            if key.char == 'q':
                self.en_ejecucion = False
                return False
        except AttributeError:
            pass