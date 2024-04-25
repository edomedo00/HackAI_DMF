import cv2
import mediapipe as mp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic

with mp_holistic.Holistic(
    static_image_mode=True,
    model_complexity=1) as holistic:

    image = cv2.imread("media/silueta.png")
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    results = holistic.process(image_rgb)

    
    for i, landmark in enumerate(results.pose_landmarks.landmark):
        if i in [1, 2, 3, 4, 5, 6, 10, 9, 22, 20, 18, 21, 19, 17, 32, 30, 29, 31]:
            results.pose_landmarks.landmark[i].visibility = 0

    # Postura
    mp_drawing.draw_landmarks(
        image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
        mp_drawing.DrawingSpec(color=(128, 0, 255), thickness=2, circle_radius=1),
        mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2))

    print(mp_holistic.POSE_CONNECTIONS)

    cv2.imshow("Image", image)



    # Plot: puntos de referencia y conexiones en matplotlib 3D
    mp_drawing.plot_landmarks(
        results.pose_world_landmarks, mp_holistic.POSE_CONNECTIONS)


    cv2.waitKey(0)
cv2.destroyAllWindows()