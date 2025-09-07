import cv2
import time
from typing import Optional, Tuple

class InterfazTeclado:
    def __init__(self, config, disposiciones):
        self.config = config
        self.disposiciones = disposiciones
        self.teclas = self.disposiciones.teclas_normal
        self.teclas_pulsadas = {}
        
        # calcular offsets por fila para centrar
        self.offset_fila = []
        for fila in self.teclas:
            fila_ancho = 0
            for tecla in fila:
                fila_ancho += self.disposiciones.obtener_ancho_tecla(tecla, config.ANCHO_TECLA) + config.ESPACIO_TECLA
            fila_ancho -= config.ESPACIO_TECLA
            offset = (config.FRAME_WIDTH - fila_ancho) // 2
            self.offset_fila.append(offset)
    
    def obtener_tecla_en_pos(self, pos: Tuple[int, int]) -> Optional[str]:
        kx, ky = self.config.POS_TECLADO
        px, py = pos
        rel_y = py - ky
        if rel_y < 0:
            return None
        fila = int(rel_y / (self.config.ALTO_TECLA + self.config.ESPACIO_TECLA))
        if fila < 0 or fila >= len(self.teclas):
            return None
        offset = self.offset_fila[fila]
        rel_x = px - offset
        if rel_x < 0:
            return None
        acumulado = 0
        for col, tecla in enumerate(self.teclas[fila]):
            ancho = self.disposiciones.obtener_ancho_tecla(tecla, self.config.ANCHO_TECLA)
            if acumulado <= rel_x < acumulado + ancho:
                return tecla
            acumulado += ancho + self.config.ESPACIO_TECLA
        return None
    
    def actualizar_layout(self, shift_activo: bool):
        self.teclas = self.disposiciones.teclas_shift if shift_activo else self.disposiciones.teclas_normal
        # Recalcular offsets para el nuevo layout
        self.offset_fila = []
        for fila in self.teclas:
            fila_ancho = 0
            for tecla in fila:
                fila_ancho += self.disposiciones.obtener_ancho_tecla(tecla, self.config.ANCHO_TECLA) + self.config.ESPACIO_TECLA
            fila_ancho -= self.config.ESPACIO_TECLA
            offset = (self.config.FRAME_WIDTH - fila_ancho) // 2
            self.offset_fila.append(offset)
    
    def marcar_tecla_pulsada(self, tecla: str):
        self.teclas_pulsadas[tecla] = time.time()
    
    def dibujar_teclado(self, frame, hover_estable_izq, hover_estable_der, shift_activo, ctrl_activo):
        ahora = time.time()
        a_eliminar = [k for k, t in self.teclas_pulsadas.items() if ahora - t >= self.config.DURACION_PRESION]
        for k in a_eliminar:
            del self.teclas_pulsadas[k]

        kb_x, kb_y = self.config.POS_TECLADO

        for fila_idx, fila in enumerate(self.teclas):
            x_offset = self.offset_fila[fila_idx]
            for col_idx, tecla in enumerate(fila):
                x = x_offset
                y = kb_y + fila_idx * (self.config.ALTO_TECLA + self.config.ESPACIO_TECLA)
                ancho = self.disposiciones.obtener_ancho_tecla(tecla, self.config.ANCHO_TECLA)
                alto = self.config.ALTO_TECLA

                if tecla in self.disposiciones.teclas_especiales:
                    color = self.config.COLOR_MORADO
                else:
                    color = self.config.COLOR_NARANJA

                color_texto = self.config.COLOR_TEXTO

                if tecla == hover_estable_izq:
                    color = self.config.COLOR_HOVER_IZQ
                elif tecla == hover_estable_der:
                    color = self.config.COLOR_HOVER_DER

                if tecla in self.teclas_pulsadas:
                    color = self.config.COLOR_PRESIONADO
                    alto = int(self.config.ALTO_TECLA * 0.85)
                    color_texto = self.config.COLOR_TEXTO_PRESIONADO

                if tecla == 'SHIFT' and shift_activo:
                    color = self.config.COLOR_SHIFT_ACTIVO
                    color_texto = self.config.COLOR_TEXTO_PRESIONADO
                elif tecla == 'CTRL' and ctrl_activo:
                    color = self.config.COLOR_CTRL_ACTIVO

                cv2.rectangle(frame, (x, y), (x + ancho, y + alto), color, -1)
                texto = tecla
                escala = 0.7 if len(tecla) <= 3 else 0.5
                grosor = 2
                tam_texto = cv2.getTextSize(texto, cv2.FONT_HERSHEY_SIMPLEX, escala, grosor)[0]
                tx = x + (ancho - tam_texto[0]) // 2
                ty = y + (alto + tam_texto[1]) // 2
                cv2.putText(frame, texto, (tx, ty), cv2.FONT_HERSHEY_SIMPLEX, escala, color_texto, grosor)
                x_offset += ancho + self.config.ESPACIO_TECLA
        
        return frame