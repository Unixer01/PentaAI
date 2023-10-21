from fer import FER
import cv2

vid = cv2.VideoCapture(0)

while True:
    ret, frame = vid.read()
    emotion_detector = FER(mtcnn=True)
    analysis = emotion_detector.detect_emotions(frame)
    dominant_emotion, emotion_score = emotion_detector.top_emotion(frame)
    print(dominant_emotion, emotion_score)
    print(analysis)
    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()
