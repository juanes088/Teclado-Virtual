import threading
from pynput.keyboard import Listener
from core.motor_teclado import MotorTeclado

def main():
    teclado = MotorTeclado()

    def iniciar_listener_fisico():
        with Listener(on_press=teclado.manejar_presion_fisica) as listener:
            listener.join()

    hilo_listener = threading.Thread(target=iniciar_listener_fisico, daemon=True)
    hilo_listener.start()

    try:
        teclado.ejecutar()
    except KeyboardInterrupt:
        pass
    except Exception:
        pass
    finally:
        teclado.limpiar()

if __name__ == "__main__":
    main()