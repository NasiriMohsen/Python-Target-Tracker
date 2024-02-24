# ESP32 Webcam Tracker

## Introduction

This project allows you to create a tracker system to track a target using the webcam.

## Hardware Requirements

- **DevBoard:** NodeMCU ESP32
- **Servos:** Two RC Servos (MG90)
- **Webcam:** Cheap Chinese Cams

## Setup Instructions (Latest Model)

1. Connect the Servos to the Board.
2. Connect the Board to your PC.
3. Upload the Arduino code to the board
4. Connect the Webcam to your PC.
5. Install the necessary software mentioned below!
6. Connect to the Board using Bluetooth.
7. Run the Python code.

## Software Requirements

### For All Models:

- **OpenCV:** Install using the following terminal command:
  ```
  pip install opencv-python
  ```

### Additional Requirements for the Latest Model:

- **Bluetooth Serial Terminal:** Download and install the "Bluetooth Serial Terminal" software from Microsoft Store. [Download Link](https://www.microsoft.com/store/productId/9WZDNCRDFST8?ocid=pdpshare)

## Notes

- The ESP32 officially does not support USB webcams. Consider using ESPCAM for streaming or connect the webcam to your PC for efficient operation.

Feel free to modify and enhance the project. Happy tinkering!