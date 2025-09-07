import cv2
from typing import Optional, Tuple

class ElementosVisuales:
    def __init__(self, config):
        self.config = config
    
    def dibujar_indicadores_dedos(self, frame, pos_indice_izq, pos_pulgar_izq, pos_indice_der, pos_pulgar_der):
        # Dibujar indicadores de dedos
        if pos_indice_izq:
            cv2.circle(frame, pos_indice_izq, 15, self.config.COLOR_INDICE_IZQ, -1)
            cv2.circle(frame, pos_indice_izq, 18, (255, 255, 255), 3)
            cv2.putText(frame, "L", (pos_indice_izq[0]-8, pos_indice_izq[1]+5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        if pos_pulgar_izq:
            cv2.circle(frame, pos_pulgar_izq, 12, self.config.COLOR_PULGAR, -1)
            cv2.circle(frame, pos_pulgar_izq, 15, (255, 255, 255), 2)

        if pos_indice_der:
            cv2.circle(frame, pos_indice_der, 15, self.config.COLOR_INDICE_DER, -1)
            cv2.circle(frame, pos_indice_der, 18, (255, 255, 255), 3)
            cv2.putText(frame, "R", (pos_indice_der[0]-8, pos_indice_der[1]+5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        if pos_pulgar_der:
            cv2.circle(frame, pos_pulgar_der, 12, self.config.COLOR_PULGAR, -1)
            cv2.circle(frame, pos_pulgar_der, 15, (255, 255, 255), 2)
    
    def dibujar_panel_estado(self, frame, texto_escrito):
        # Panel estado
        textos_estado = [
            f"Texto: {texto_escrito[-40:]}{'...' if len(texto_escrito) > 40 else ''}"
        ]
        for i, t in enumerate(textos_estado):
            y_pos = 20 + i * 25
            cv2.putText(frame, t, (15, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.6, self.config.COLOR_ESTADO, 2)