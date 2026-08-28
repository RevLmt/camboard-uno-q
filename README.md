# Camera & Display Breakout for Arduino UNO Q
This camera and display module for the Arduino UNO Q. It breaks out the 2 MIPI-CSI cameras and a single MIPI-DSI display interace. All use a 22-pin cable (similar to compute boards for the Raspberry Pi).

You can ***purchase a this camera board [here](https://www.r1build.com/products/camera-and-display-breakout-for-arduino-uno-q)***.



<img src="assets/camboard_isoview.png" alt="Camera breakout board for Arduino UNO Q (isoview)" width="500" height="500">


## Connections
- 2 MIPI-CSI camera breakouts (22-pin flexible cable connector)
- 1 MIPI-DSI display breakout (22-pin flexible cable connector)
- 2 60-pin headers for interfacing with UNO Q
- 2 60-pin passthrough headers for future expansion

## Installation
In order to use the camera or display interfaces on the UNO Q, one must edit the device tree loaded at boot. Luckily, a device tree blob (DTB) for using a Raspberry Pi V2 Camera comes with the UNO Q. However, to use this board, some small edits must be made to that device tree. There is a shell script at `software/device_trees/setup_device.sh`. If you run this it will carry out the necessary steps in enabling the CAM0 connector for an IMX219 (Raspberry Pi V2 Camera Module). Right now, only the RPi V2 Camera is supported. Contributions are welcome!

To enable CAM0 for the IMX219, copy the `setup_device.sh` to somewhere safe on your UNO Q. The easiest way I've found is to SSH into the UNO Q using VS Code. Then just drag and drop the file into the UNO Q. Then, in your terminal, change to the directory where you have this file. Then, run:
```bash
sudo ./setup_device.sh

```
This file creates a final device tree file for you in a folder located in `/boot/efi/dtb/r1b`, where `r1b` stands for my website r1build.com. The final device tree blob is `qrb2210-arduino-imola-camera-rpiv2-r1b.dtb`. You should check to see if that file exists in the folder.

Next, you will need to point Linux to the right place for loading this file. To do so, you will need to find the `.conf` file that controls the boot. This file name seems to change for every update of the UNO Q. So, I have yet to find a way to standardize it yet. But, luckily, there is only one file with `.conf` in that location. That location is `/boot/efi/loader/entries/`. Go ahead and edit that file with the command:
```bash
sudo nano /boot/efi/loader/entries/(NameOfYourFile).conf
```
at the end of the file, add this line:
```bash
devicetree /dtb/r1b/qrb2210-arduino-imola-camera-rpiv2-r1b.dtb
```
This tells the Debian Linux to load our new device tree. Go ahead and reboot. Afterwards, your camera should be available.

THe shell script shows the basics

## Quickstart - Running with qcam and OpenCV

Below is some example code for running the board with OpenCV. For this to work, you should have a monitor attached. Ideally, just setup the board as a Single Board Computer (SBC), having a keyboard, mouse, and display. This isn't a requirement to run OpenCV with the board, but it will get you started quickly.

It is best to use `libcamera` to manage everything. To install, you can use the following commands in the terminal:

```bash
sudo apt update
sudo apt install libcamera-tools gstreamer1.0-libcamera
```

### Qcam very quick check

As a very quick check, you can use qcam to stream and check if the installation went well. The following command will open a window where you can see the camera stream from.
```bash
qcam
```


### Open CV

For this to work, you should still be using the UNO Q as a SBC (display + keyboard + mouse). This will also display a stream, much like the `qcam` example above. However, it is using `cv2`. It only includes the most basic commands to get the camera running. So, you can then use this as a base to start building your applications.

Save this script anywhere (maybe Desktop for easy access). The stream window can be closed by pressing `q` on the keyboard.

```python
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
```
