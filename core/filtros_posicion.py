import math
import numpy as np
from collections import deque
from typing import Optional, Tuple

class FiltrosPosicion:
    def __init__(self, config):
        self.config = config
        
        # Historiales para suavizado y deteccion
        self.historial_pos_izq = deque(maxlen=config.HISTORIAL_POS_MAXLEN)
        self.historial_vel_izq = deque(maxlen=config.HISTORIAL_VEL_MAXLEN)
        self.pos_estable_izq = None

        self.historial_pos_der = deque(maxlen=config.HISTORIAL_POS_MAXLEN)
        self.historial_vel_der = deque(maxlen=config.HISTORIAL_VEL_MAXLEN)
        self.pos_estable_der = None

        # hover y confianza
        self.historial_hover_izq = deque(maxlen=config.HISTORIAL_HOVER_MAXLEN)
        self.historial_hover_der = deque(maxlen=config.HISTORIAL_HOVER_MAXLEN)
        self.hover_estable_izq = None
        self.hover_estable_der = None
        self.confianza_hover_izq = 0
        self.confianza_hover_der = 0
    
    def aplicar_filtro_kalman(self, medicion: Tuple[int, int],
                              estimado_previo: Optional[Tuple[int, int]]) -> Tuple[int, int]:
        if estimado_previo is None:
            return medicion
        prediccion = estimado_previo
        innov_x = medicion[0] - prediccion[0]
        innov_y = medicion[1] - prediccion[1]
        est_x = prediccion[0] + self.config.GANANCIA_KALMAN * innov_x
        est_y = prediccion[1] + self.config.GANANCIA_KALMAN * innov_y
        return (int(est_x), int(est_y))
    
    def estabilizar_posicion(self, pos_bruta: Tuple[int, int], mano: str) -> Tuple[int, int]:
        historial_pos = getattr(self, f"historial_pos_{mano}")
        historial_vel = getattr(self, f"historial_vel_{mano}")
        attr_estable = f"pos_estable_{mano}"
        previo = getattr(self, attr_estable)

        filtrada = self.aplicar_filtro_kalman(pos_bruta, previo)
        historial_pos.append(filtrada)

        if len(historial_pos) < 3:
            setattr(self, attr_estable, filtrada)
            return filtrada

        recientes = list(historial_pos)[-3:]
        velocidades = []
        for i in range(1, len(recientes)):
            dx = recientes[i][0] - recientes[i-1][0]
            dy = recientes[i][1] - recientes[i-1][1]
            vel = math.sqrt(dx*dx + dy*dy)
            velocidades.append(vel)

        vel_media = np.mean(velocidades) if velocidades else 0
        historial_vel.append(vel_media)

        if vel_media < self.config.UMBRAL_MOVIMIENTO:
            pesos = np.exp(np.linspace(-0.8, 0, len(recientes)))
            pesos /= np.sum(pesos)
            x_est = sum(p[0] * w for p, w in zip(recientes, pesos))
            y_est = sum(p[1] * w for p, w in zip(recientes, pesos))
            pos_estable = (int(x_est), int(y_est))
        else:
            pos_estable = filtrada

        setattr(self, attr_estable, pos_estable)
        return pos_estable
    
    def detectar_hover_estable(self, tecla_actual: Optional[str], mano: str) -> Optional[str]:
        historial_hover = getattr(self, f"historial_hover_{mano}")
        attr_hover = f"hover_estable_{mano}"
        attr_conf = f"confianza_hover_{mano}"

        historial_hover.append(tecla_actual)

        if not tecla_actual:
            confianza = getattr(self, attr_conf)
            setattr(self, attr_conf, max(0, confianza - 1))
            if getattr(self, attr_conf) == 0:
                setattr(self, attr_hover, None)
            return getattr(self, attr_hover)

        recientes = list(historial_hover)[-self.config.MIN_CONFIANZA_HOVER:]
        cuenta = recientes.count(tecla_actual)
        consistencia = cuenta / len(recientes) if recientes else 0
        confianza = getattr(self, attr_conf)
        hover_estable = getattr(self, attr_hover)

        if consistencia > 0.75:
            if tecla_actual == hover_estable:
                nueva_conf = min(8, confianza + 1)
            else:
                nueva_conf = 2
                setattr(self, attr_hover, tecla_actual)
            setattr(self, attr_conf, nueva_conf)
        else:
            setattr(self, attr_conf, max(0, confianza - 0.5))

        return getattr(self, attr_hover) if getattr(self, attr_conf) >= self.config.MIN_CONFIANZA_HOVER else None