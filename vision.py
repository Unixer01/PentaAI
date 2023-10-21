import argparse as ap
import cv2
import mediapipe as mp
import supervision as sv
from ultralytics import YOLO
from fer import FER
import os
import numpy as np
def parse_arguments() -> ap.Namespace:
    parser = ap.ArgumentParser(description="YOLOv8 live")
    parser.add_argument("--webcam-resolution",
                        default=[720, 720],
                        nargs=2,
                        type=int)
    args = parser.parse_args()
    return args




box_annotator = sv.BoxAnnotator(
    thickness=2,
    text_thickness=2,
    text_scale=1
)


def run(model_version):
    if model_version in ["yolov8m", "yolov8n", "yolov8s", "yolov8l", "yolov8x"]:
        model = YOLO('resources/' + model_version)

    else:
        print("Invalid model version, auto-changing model version to yolov8n")
        model = YOLO('resources/yolov8s.pt')

    webcam = cv2.VideoCapture(0)
    args = parse_arguments()

    frame_width, frame_height = args.webcam_resolution

    webcam.set(cv2.CAP_PROP_FRAME_WIDTH, frame_height)
    webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_width)

    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_face_mesh = mp.solutions.face_mesh
    mp_holistic = mp.solutions.holistic
    holistic_model = mp_holistic.Holistic(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )

    while webcam.isOpened():
        success, img = webcam.read()
        img = cv2.flip(img, 1)
        result = model(img)[0]
        emotion_detector = FER(mtcnn=True)
        analysis = emotion_detector.detect_emotions(img)
        dominant_emotion, emotion_score = emotion_detector.top_emotion(img)
        detections = sv.Detections.from_yolov8(result)
        labels = [
            f"{model.model.names[class_id]} {confidence:0.2f}"
            for _, confidence, class_id, _
            in detections
        ]
        img = box_annotator.annotate(scene=img,
                                     detections=detections,
                                     labels=labels

                                     )
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        results = mp_face_mesh.FaceMesh(
            max_num_faces=100
        ).process(img)
        resultsHAND = holistic_model.process(img)

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        mp_drawing.draw_landmarks(
            img,
            resultsHAND.right_hand_landmarks,
            mp_holistic.HAND_CONNECTIONS
        )

        mp_drawing.draw_landmarks(
            img,
            resultsHAND.left_hand_landmarks,
            mp_holistic.HAND_CONNECTIONS
        )
        if results.multi_face_landmarks:
            for face_landmark in results.multi_face_landmarks:
                mp_drawing.draw_landmarks(image=img,
                                          landmark_list=face_landmark,
                                          connections=mp_face_mesh.FACEMESH_CONTOURS,
                                          landmark_drawing_spec=None,
                                          connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_contours_style())
                mp_drawing.draw_landmarks(image=img,
                                          landmark_list=face_landmark,
                                          connections=mp_face_mesh.FACEMESH_TESSELATION,
                                          landmark_drawing_spec=None,
                                          connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style())



        font = cv2.FONT_HERSHEY_DUPLEX
        try:

            cv2.putText(img,
                        dominant_emotion + " " + str(emotion_score),
                        (50, 50),
                        font, 1,
                        (255, 255, 255),
                        2,
                        cv2.LINE_4)

        except TypeError:
            pass

        cv2.imshow("VISION", img)
        os.system('clear')
        if cv2.waitKey(20) == 0xFF & ord('q'):
            break

    webcam.release()
    cv2.destroyAllWindows()
