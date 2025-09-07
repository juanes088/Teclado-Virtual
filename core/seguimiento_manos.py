import cv2
import mediapipe as mp
import math
import time
from collections import deque
from typing import Optional, Tuple

class SeguimientoManos:
    def __init__(self, config):
        self.config = config
        
        # MediaPipe Hands
        self.mp_manos = mp.solutions.hands
        self.manos = self.mp_manos.Hands(
            model_complexity=config.MP_MODEL_COMPLEXITY,
            max_num_hands=config.MP_MAX_NUM_HANDS,
            min_detection_confidence=config.MP_MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence=config.MP_MIN_TRACKING_CONFIDENCE,
            static_image_mode=config.MP_STATIC_IMAGE_MODE
        )
        self.mp_dibujar = mp.solutions.drawing_utils
        
        # Estados de click (pellizco)
        self.estados_click_izq = deque(maxlen=config.ESTADOS_CLICK_MAXLEN)
        self.estados_click_der = deque(maxlen=config.ESTADOS_CLICK_MAXLEN)
        self.click_confirmado_izq = False
        self.click_confirmado_der = False
        self.ultimo_tiempo_tecla = 0
    
    def obtener_landmarks_mano(self, imagen):
        rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
        rgb.flags.writeable = False
        resultados = self.manos.process(rgb)
        return resultados
    
    def obtener_posiciones_dedos(self, landmarks) -> dict:
        if not landmarks:
            return {}
        h, w = self.config.FRAME_HEIGHT, self.config.FRAME_WIDTH
        posiciones = {}
        for nombre, idx in self.config.PUNTOS_IMPORTANTES.items():
            lm = landmarks.landmark[idx]
            posiciones[nombre] = (int(lm.x * w), int(lm.y * h))
        return posiciones
    
    def calcular_distancia_pellizco(self, posiciones: dict) -> float:
        if 'pulgar_tip' not in posiciones or 'indice_tip' not in posiciones:
            return 100
        return math.hypot(
            posiciones['pulgar_tip'][0] - posiciones['indice_tip'][0],
            posiciones['pulgar_tip'][1] - posiciones['indice_tip'][1]
        )
    
    def detectar_click_estable(self, distancia_pellizco: float, mano: str) -> bool:
        estados = getattr(self, f"estados_click_{mano}")
        attr_confirm = f"click_confirmado_{mano}"

        es_pellizco = distancia_pellizco < self.config.UMBRAL_PELLIZCO
        estados.append(es_pellizco)

        if len(estados) < 3:
            return False

        recientes = list(estados)[-3:]
        if not recientes[0] and all(recientes[1:]):
            if not getattr(self, attr_confirm):
                ahora = time.time()
                if ahora - self.ultimo_tiempo_tecla > self.config.DEBOUNCE_SEGUNDOS:
                    setattr(self, attr_confirm, True)
                    return True

        if not any(recientes[-2:]):
            setattr(self, attr_confirm, False)

        return False
    
    def actualizar_tiempo_tecla(self):
        self.ultimo_tiempo_tecla = time.time()
    
    def dibujar_landmarks(self, frame, landmarks):
        self.mp_dibujar.draw_landmarks(
            frame, landmarks, self.mp_manos.HAND_CONNECTIONS,
            self.mp_dibujar.DrawingSpec(color=self.config.COLOR_LANDMARKS_PUNTO, thickness=2, circle_radius=3),
            self.mp_dibujar.DrawingSpec(color=self.config.COLOR_LANDMARKS_LINEA, thickness=2)
        )