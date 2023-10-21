import cv2
from deepface import DeepFace


video = cv2.VideoCapture(0)  # requisting the input from the webcam or camera

while video.isOpened():  # checking if are getting video feed and using it
    _, frame = video.read()

    # this is the part where we display the output to the user
    try:
        processed = DeepFace.analyze(frame, enforce_detection=0)[0]
        print(processed['dominant_emotion'],(processed['emotion'][processed['dominant_emotion']])[0:3])

    except:
        pass
    cv2.imshow('video', frame)
    key = cv2.waitKey(1)
    if key == 0xFF & ord('q'):  # here we are specifying the key which will stop the loop and stop all the processes going
        break

video.release()
cv2.destroyAllWindows()