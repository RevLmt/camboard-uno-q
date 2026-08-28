'''
Example script for streaming the camera on the UNO Q's desktop. For this to work, 
you must be in single-board-computer (SBC) mode. This means keyboard, mouse, and display.

Tested on Rapberry Pi Camera V2.


Must install libcamera-tools gstreamer1.0-libcamera using apt
'''


import cv2
# The 'libcamerasrc' element handles the UNO Q's ISP and media-ctl automatically
# videoconvert and appsink allow OpenCV to read the frames
pipeline = (
"libcamerasrc ! "
"video/x-raw, width=1280, height=720, framerate=30/1 ! "
"videoconvert ! appsink"
)
cap = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)
if not cap.isOpened():
    print("Error: Could not open camera pipeline.")
    exit()


print("Camera stream started. Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Display the stream on your desktop
    cv2.imshow("UNO Q Camera Feed", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()