# Teclado Virtual

# Funcionalidades Principales

Detección de manos en tiempo real con MediaPipe
Escritura por gestos de pellizco (pulgar + índice)
Teclado visual interactivo con feedback en pantalla
Suavizado de movimientos con filtros Kalman
Soporte multiplataforma (Windows, Mac, Linux)
Teclas especiales (SHIFT, CTRL, ENTER, TAB, DEL, SPACE)
Estados visuales (hover, presionado, modificadores activos)

# Arquitectura del Proyecto


**config/**

**ajustes.py:** Aquí se gestionan todas las configuraciones del sistema (umbrales, colores, dimensiones, parámetros de MediaPipe)
disposiciones_teclado.py: Aquí se controlan los layouts de teclas (teclado normal, shift, teclas especiales)


**core/**

**motor_teclado.py:** Aquí se orquesta todo el sistema principal y coordina todos los módulos
**seguimiento_manos.py:** Aquí se maneja la detección de manos con MediaPipe y reconocimiento de gestos de pellizco
**filtros_posicion.py:** Aquí se controla el suavizado de posiciones y filtros Kalman para estabilizar movimientos


**interfaz/**

**interfaz_teclado.py:** Aquí se gestiona el dibujado del teclado virtual y detección de posiciones de teclas
**elementos_visuales.py:** Aquí se manejan los indicadores visuales de dedos y panel de estado


**system/**

**controlador_entrada.py:** Aquí se controla el envío de teclas al sistema operativo usando pynput
**adaptadores_so.py:** Aquí se gestionan las configuraciones específicas por sistema operativo


# Como Usar

1. Ejecuta el programa - Se abrirá una ventana con la cámara y el teclado virtual
2. Posiciona tus manos frente a la cámara
3. Apunta con el dedo índice a la tecla que quieres presionar
4. Haz pellizco (junta pulgar e índice) para "hacer click"
5. Usa ambas manos - mano izquierda (L) y derecha (R) funcionan independientemente
