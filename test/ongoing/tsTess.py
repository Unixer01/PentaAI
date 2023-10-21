import pytesseract
import cv2
import numpy as np
vid = cv2.VideoCapture(0)
while True:
    ret, img = vid.read()


    cv2.imshow('frame', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()
