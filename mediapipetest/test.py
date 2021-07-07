import cv2
import mediapipe as mp
#from typing import NamedTuple

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

# For static images:
with mp_face_detection.FaceDetection(min_detection_confidence=0.5) as face_detection:
    # for idx, file in enumerate(file_list):
    image = cv2.imread("test.png")
    # cv2.imshow("img", image)
    # waitkey(0)
    # Convert the BGR image to RGB and process it with MediaPipe Face Detection.
    results = face_detection.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    #print(results.detections[1])

    # Draw face detections of each face.
    if not results.detections:
        pass
    annotated_image = image.copy()
    for detection in results.detections:
        #print("Nose tip:")
        print(
            detection.location_data.relative_bounding_box
            )
        
    
        mp_drawing.draw_detection(annotated_image, detection)
    cv2.imwrite("me" + ".png", annotated_image)
