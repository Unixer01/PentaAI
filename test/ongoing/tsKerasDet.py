from keras.models import load_model  # TensorFlow is required for Keras to work
import cv2  # Install opencv-python
import numpy as np

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model = load_model("../../resources/keras_model.h5", compile=False)

# Load the labels
class_names = open("../../resources/labels.txt", "r").readlines()

# CAMERA can be 0 or 1 based on default camera of your computer
camera = cv2.VideoCapture(0)
class_name = '   '
confidence_score = '   '
while True:
    # Grab the webcamera's image.
    ret, image = camera.read()

    try:
        cv2.putText(image,
                    (str(class_name[1:]) + ' ' + str(confidence_score)[:-2]),
                    (50, 50),
                    cv2.FONT_HERSHEY_DUPLEX, 1,
                    (255, 255, 255),
                    2,
                    cv2.LINE_4)

    except:
        pass

    class_name = ''
    confidence_score = ''
    keyboard_input = cv2.waitKey(1)

    cv2.imshow("Webcam Image", image)
    # Resize the raw image into (224-height,224-width) pixels
    image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)

    # Show the image in a window

    # Make the image a numpy array and reshape it to the models input shape.
    image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)

    # Normalize the image array
    image = (image / 127.5) - 1

    # Predicts the model
    prediction = model.predict(image)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]
    keyboard_input = cv2.waitKey(1)

    # 27 is the ASCII for the esc key on your keyboard.
    if keyboard_input == 27:
        break

camera.release()
cv2.destroyAllWindows()
