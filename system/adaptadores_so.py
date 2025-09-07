import cv2

class AdaptadoresSO:
    def __init__(self, config):
        self.config = config
    
    def configurar_camara(self, cap):
        """configura la camara según el sistema operativo"""
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.config.FRAME_WIDTH)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.config.FRAME_HEIGHT)
        cap.set(cv2.CAP_PROP_FPS, self.config.FRAME_FPS)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, self.config.BUFFER_SIZE)
        return cap
    
    def configurar_ventana(self, nombre_ventana):
        """Configura la ventana segun el sistema operativo"""
        cv2.namedWindow(nombre_ventana, cv2.WINDOW_AUTOSIZE)
    
    def limpiar_recursos(self, cap):
        """Limpia recursos segun el sistema operativo"""
        try:
            if cap and cap.isOpened():
                cap.release()
            cv2.destroyAllWindows()
            cv2.waitKey(1)
        except Exception:
            pass