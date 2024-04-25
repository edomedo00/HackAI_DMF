import cv2
import mediapipe as mp
import numpy as np


mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic

cap = cv2.VideoCapture("media/edmundo.mp4")
# cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
sprite = cv2.imread("media/silueta.png")

witdth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# rescalar la imagen
sprite = cv2.resize(sprite, (height, witdth))

fps = cap.get(cv2.CAP_PROP_FPS)
out_video = cv2.VideoWriter('media/esqueleto_ed.mp4', cv2.VideoWriter_fourcc(*'XVID'), fps, (height, witdth))

descarte = [1, 2, 3, 4, 5, 6, 10, 9, 22, 20, 18, 21, 19, 17, 32, 30, 29, 31]

with mp_holistic.Holistic(
    static_image_mode=False,
    model_complexity=0) as holistic:

    while True:
        ret, frame = cap.read()
        if ret == False:
            break

        
        canva = np.zeros((height, witdth, 3), dtype=np.uint8)
        results = holistic.process(frame)
        if results.pose_landmarks is None:
            out_video.write(canva)
            continue
        
        for i in descarte:
            results.pose_landmarks.landmark[i].visibility = 0

        # Postura
        mp_drawing.draw_landmarks(
            canva, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(128, 0, 255), thickness=2, circle_radius=1),
            mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2))

        
        canva = cv2.flip(canva, 1)
        # cv2.imshow("Frame", canva)

        out_video.write(canva)

        if cv2.waitKey(1) & 0xFF == 27:
            break

cap.release()
out_video.release()
cv2.destroyAllWindows()
