import platform

class ConfiguracionTeclado:
    def __init__(self):
        # MediaPipe Hands configuracion
        self.MP_MODEL_COMPLEXITY = 1
        self.MP_MAX_NUM_HANDS = 2
        self.MP_MIN_DETECTION_CONFIDENCE = 0.7
        self.MP_MIN_TRACKING_CONFIDENCE = 0.8
        self.MP_STATIC_IMAGE_MODE = False
        
        # Camara configuracion
        self.FRAME_WIDTH = 1280
        self.FRAME_HEIGHT = 720
        self.FRAME_FPS = 30
        self.BUFFER_SIZE = 1
        
        # Sistema operativo
        self.sistema_operativo = platform.system()
        self.configurar_por_os()
        
        # Historiales para suavizado
        self.HISTORIAL_POS_MAXLEN = 8
        self.HISTORIAL_VEL_MAXLEN = 5
        self.UMBRAL_MOVIMIENTO = 12
        
        # Hover y confianza
        self.HISTORIAL_HOVER_MAXLEN = 6
        self.MIN_CONFIANZA_HOVER = 4
        
        # Estados de click (pellizco)
        self.ESTADOS_CLICK_MAXLEN = 5
        self.UMBRAL_PELLIZCO = 35
        self.DEBOUNCE_SEGUNDOS = 0.35
        
        # Parametros filtro tipo Kalman simple
        self.GANANCIA_KALMAN = 0.6
        self.RUIDO_PROCESO = 0.01
        self.RUIDO_MEDICION = 0.1
        
        # Dibujo teclado
        self.ANCHO_TECLA = 75
        self.ALTO_TECLA = 60
        self.ESPACIO_TECLA = 8
        self.POS_TECLADO = (0, 80)
        self.DURACION_PRESION = 0.25
        
        # Colores
        self.COLOR_NARANJA = (220, 170, 100)
        self.COLOR_MORADO = (140, 100, 180)
        self.COLOR_TEXTO = (255, 255, 255)
        self.COLOR_HOVER_IZQ = (0, 191, 255)
        self.COLOR_HOVER_DER = (100, 100, 255)
        self.COLOR_PRESIONADO = (0, 255, 100)
        self.COLOR_SHIFT_ACTIVO = (255, 140, 0)
        self.COLOR_CTRL_ACTIVO = (140, 0, 255)
        self.COLOR_TEXTO_PRESIONADO = (0, 0, 0)
        self.COLOR_ESTADO = (0, 255, 200)
        self.COLOR_INDICE_IZQ = (0, 150, 255)
        self.COLOR_INDICE_DER = (100, 100, 255)
        self.COLOR_PULGAR = (0, 255, 100)
        self.COLOR_LANDMARKS_PUNTO = (0, 255, 150)
        self.COLOR_LANDMARKS_LINEA = (255, 100, 100)
        
        # Ventana
        self.NOMBRE_VENTANA = 'Teclado Virtual'
        
        # opciones de escritura
        self.MODO_ESCRITURA = True
        self.AUTO_ESPACIO = True
        self.SUGERENCIAS_PALABRA = True
        
        # mediaPipe puntos importantes
        self.PUNTOS_IMPORTANTES = {
            'pulgar_tip': 4, 'pulgar_ip': 3,
            'indice_tip': 8, 'indice_pip': 6,
            'medio_tip': 12, 'anular_tip': 16, 'meñique_tip': 20,
            'muneca': 0
        }
    
    def configurar_por_os(self):
        if self.sistema_operativo == "Windows":
            self.RETRASO_TECLA = 0.01
        elif self.sistema_operativo == "Darwin":
            self.RETRASO_TECLA = 0.02
        else:
            self.RETRASO_TECLA = 0.015