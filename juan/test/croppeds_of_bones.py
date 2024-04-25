import cv2
import mediapipe as mp
import numpy as np


def crop_rotated_rectangle(image, point_A, point_B, thickness):
    # Calcular el ángulo entre los puntos A y B
    angle = np.arctan2(point_B[1] - point_A[1], point_B[0] - point_A[0]) * 180 / np.pi

    # Obtener la longitud y la anchura del rectángulo
    length = np.sqrt((point_B[0] - point_A[0]) ** 2 + (point_B[1] - point_A[1]) ** 2)
    width = thickness

    # Calcular los puntos del rectángulo
    center = ((point_A[0] + point_B[0]) / 2, (point_A[1] + point_B[1]) / 2)
    rect_pts = cv2.boxPoints(((center[0], center[1]), (length, width), angle))
    rect_pts = np.int0(rect_pts)

    # Crear una máscara para recortar el rectángulo
    mask = np.zeros_like(image)

    cv2.drawContours(mask, [rect_pts], -1, (255, 255, 255), -1)

    # Recortar el rectángulo en la imagen
    cropped = cv2.bitwise_and(image, mask)

    return cropped


mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic

# Camptura de video y sprite
cap = cv2.VideoCapture("media/edmundo.mp4")
# cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
sprite = cv2.imread("media/standing.jpeg")

# Dimensiones del video
columnas = 600
filas = 600

# rescalar la imagen
sprite = cv2.resize(sprite, (columnas, filas))

# Crear video de salida
fps = cap.get(cv2.CAP_PROP_FPS)
out_video = cv2.VideoWriter('media/esqueleto_ed.mp4', cv2.VideoWriter_fourcc(*'XVID'), fps, (columnas, filas))

# Puntos a descartar
descarte = [1, 2, 3, 4, 5, 6, 10, 9, 22, 20, 18, 21, 19, 17, 32, 30, 29, 31]
# Conexiones de los huesos
connexions = [(12,14), (14,16), (11,13), (13,15), (24,26), (26,28), (23,25), (25,27)]

with mp_holistic.Holistic(
    static_image_mode=False,
    model_complexity=0) as holistic:
    
    results = holistic.process(sprite)
    
    for i in descarte:
        results.pose_landmarks.landmark[i].visibility = 0

    # Postura
    # mp_drawing.draw_landmarks(
    #     sprite, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
    #     mp_drawing.DrawingSpec(color=(128, 0, 255), thickness=2, circle_radius=1),
    #     mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2))
    # Postura
    mp_drawing.draw_landmarks(
        sprite, results.pose_landmarks,)

    # recortar huesos
    for i, conexion in enumerate(connexions):
        point_A = (int(results.pose_landmarks.landmark[conexion[0]].x * columnas), int(results.pose_landmarks.landmark[conexion[0]].y * filas))
        point_B = (int(results.pose_landmarks.landmark[conexion[1]].x * columnas), int(results.pose_landmarks.landmark[conexion[1]].y * filas))
        cropped = crop_rotated_rectangle(sprite, point_A, point_B, 50)
        cv2.imshow(f"Hueso{i}", cropped)

    sprite = cv2.flip(sprite, 1)
    cv2.imshow("Image", sprite)

cv2.waitKey(0)
cap.release()
out_video.release()
cv2.destroyAllWindows()
