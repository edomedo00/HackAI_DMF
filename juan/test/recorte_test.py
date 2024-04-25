import cv2
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

# Leer la imagen
image = cv2.imread('media/isaac.jpg')

# Definir los puntos A y B
point_A = (100, 100)  # Ejemplo de coordenada A
point_B = (300, 200)  # Ejemplo de coordenada B

# Especificar el grosor del rectángulo
thickness = 20  # Puedes ajustar este valor según sea necesario

# Recortar el rectángulo rotado
cropped_rotated_rectangle = crop_rotated_rectangle(image, point_A, point_B, thickness)

# Mostrar la imagen original y el rectángulo recortado
cv2.imshow('Original Image', image)
cv2.imshow('Cropped Rotated Rectangle', cropped_rotated_rectangle)
cv2.waitKey(0)
cv2.destroyAllWindows()