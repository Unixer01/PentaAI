# Python program to open the
# camera in Tkinter
# Import the libraries,
# tkinter, cv2, Image and ImageTk
import cv2
from tkinter import *

from PIL import Image, ImageTk

# Define a video capture object
vid = cv2.VideoCapture(0)

# Declare the width and height in variables


# Create a GUI app
app = Tk()

# Bind the app with Escape keyboard to
# quit app whenever pressed
app.bind('<Escape>', lambda e: app.quit())

# Create a label and display it on app
label_widget = Label(app)
label_widget.pack()


# Create a function to open camera and
# display it in the label_widget on app


def open_camera():
    # Capture the video frame by frame
    _, frame = vid.read()

    opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

    captured_image = Image.fromarray(opencv_image)

    photo_image = ImageTk.PhotoImage(image=captured_image)

    label_widget.photo_image = photo_image

    label_widget.configure(image=photo_image)

    label_widget.after(10, open_camera)


open_camera()

# Create an infinite loop for displaying app on screen
app.mainloop()
