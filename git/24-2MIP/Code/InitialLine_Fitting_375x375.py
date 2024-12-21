"""
Course: 24-2 MIP
Purpose: This code is for the preparation to set the line laser to the initial line.
Revised date: 24.12.20
Name: YunKi Noh
"""

import os
import PySpin
import matplotlib.pyplot as plt
import sys
import keyboard
import time
import cv2
import numpy as np
import math

global continue_recording
continue_recording = True 

def handle_close(evt):
    """
    This function will close the GUI when the close event happens.

    :param evt: Event that occurs when the figure closes.
    :type evt: Event
    """
    global continue_recording
    continue_recording = False

def set_camera_fps(cam, fps):
    """
    Set the FPS (Frames Per Second) for the camera.

    :param cam: Camera object.
    :type cam: CameraPtr
    :param fps: Desired frames per second.
    :type fps: float
    """
    try:
        nodemap = cam.GetNodeMap()

        # Enable the frame rate control
        node_acquisition_frame_rate_enable = PySpin.CBooleanPtr(nodemap.GetNode("AcquisitionFrameRateEnable"))
        if PySpin.IsAvailable(node_acquisition_frame_rate_enable) and PySpin.IsWritable(node_acquisition_frame_rate_enable):
            node_acquisition_frame_rate_enable.SetValue(True)
            print("Acquisition Frame Rate Enabled")
        else:
            print("Acquisition Frame Rate Enable not available or writable")

        # Set the desired frame rate
        node_acquisition_frame_rate = PySpin.CFloatPtr(nodemap.GetNode("AcquisitionFrameRate"))
        if PySpin.IsAvailable(node_acquisition_frame_rate) and PySpin.IsWritable(node_acquisition_frame_rate):
            max_fps = node_acquisition_frame_rate.GetMax()
            if fps > max_fps:
                print(f"Requested FPS ({fps}) exceeds max FPS ({max_fps}). Setting to max FPS.")
                fps = max_fps
            node_acquisition_frame_rate.SetValue(fps)
            print(f"Acquisition Frame Rate set to: {fps}")
        else:
            print("Acquisition Frame Rate not available or writable")

    except PySpin.SpinnakerException as ex:
        print("Error setting FPS: %s" % ex)

def detect_bright_spots(image_data):

    # Convert to grayscale if not already
    if len(image_data.shape) == 3:  # Check if it's RGB
        gray_image = cv2.cvtColor(image_data, cv2.COLOR_BGR2GRAY)
    else:
        gray_image = image_data

    # Threshold to find bright spots
    _, binary_image = cv2.threshold(gray_image, 250, 255, cv2.THRESH_BINARY)

    return binary_image

def acquire_and_display_images(cam, nodemap, nodemap_tldevice):

    global continue_recording

    sNodemap = cam.GetTLStreamNodeMap()

    # Change buffer handling mode to NewestOnly
    node_bufferhandling_mode = PySpin.CEnumerationPtr(sNodemap.GetNode('StreamBufferHandlingMode'))
    if not PySpin.IsAvailable(node_bufferhandling_mode) or not PySpin.IsWritable(node_bufferhandling_mode):
        print('Unable to set stream buffer handling mode.. Aborting...')
        return False

    node_newestonly = node_bufferhandling_mode.GetEntryByName('NewestOnly')
    if not PySpin.IsAvailable(node_newestonly) or not PySpin.IsReadable(node_newestonly):
        print('Unable to set stream buffer handling mode.. Aborting...')
        return False

    node_newestonly_mode = node_newestonly.GetValue()
    node_bufferhandling_mode.SetIntValue(node_newestonly_mode)

    print('*** IMAGE ACQUISITION ***\n')

    try:
        node_acquisition_mode = PySpin.CEnumerationPtr(nodemap.GetNode('AcquisitionMode'))
        if not PySpin.IsAvailable(node_acquisition_mode) or not PySpin.IsWritable(node_acquisition_mode):
            print('Unable to set acquisition mode to continuous. Aborting...')
            return False

        node_acquisition_mode_continuous = node_acquisition_mode.GetEntryByName('Continuous')
        if not PySpin.IsAvailable(node_acquisition_mode_continuous) or not PySpin.IsReadable(
                node_acquisition_mode_continuous):
            print('Unable to set acquisition mode to continuous. Aborting...')
            return False

        acquisition_mode_continuous = node_acquisition_mode_continuous.GetValue()
        node_acquisition_mode.SetIntValue(acquisition_mode_continuous)

        print('Acquisition mode set to continuous...')

        # Begin acquiring images
        cam.BeginAcquisition()

        print('Acquiring images...')

        # Create a single plot figure for Source Image
        fig, ax = plt.subplots(figsize=(10, 10))
        img_display0 = ax.imshow(np.zeros((375, 375)), cmap='gray')
        plt.colorbar(img_display0, ax=ax, label='Pixel Intensity')
        plt.title('Source Image')
        plt.xlabel('X-axis (pixels)')
        plt.ylabel('Y-axis (pixels)')

        # Create a single plot figure to unify the fine line of line laser and the initial line
        fig, ax = plt.subplots(figsize=(10, 10))
        img_display4 = ax.imshow(np.zeros((375, 375)), cmap='gray')
        plt.colorbar(img_display4, ax=ax, label='Pixel Intensity')
        plt.title('Fine Line')
        plt.xlabel('X-axis (pixels)')
        plt.ylabel('Y-axis (pixels)')

        # Set each axis
        x_ticks = np.linspace(0, 374, 4, dtype=int)  
        y_ticks = np.linspace(0, 374, 4, dtype=int)

        if 275 not in y_ticks:
            y_ticks = np.sort(np.append(y_ticks, 275))  # Mark the position of y value of 275
        ax.set_xticks(x_ticks)
        ax.set_yticks(y_ticks)

        # Draw parallel line of 275
        ax.axhline(y=275, color='blue', linestyle='--', linewidth=1, label='Initial Line (275)')

        ax.set_xticklabels(x_ticks, rotation=90)   

        plt.legend()
        plt.ion()
        plt.show()

        while continue_recording:
            try:
                # Retrieve next received image
                image_result = cam.GetNextImage(1000)

                if image_result.IsIncomplete():
                    print('Image incomplete with image status %d ...' % image_result.GetImageStatus())
                else:
                    # Resize the shape of source image
                    image_data = image_result.GetNDArray()
                    image_data = cv2.resize(image_data, (375, 375), interpolation=cv2.INTER_AREA)

                    # GrayScale
                    _, binary_image = cv2.threshold(image_data.astype(np.uint8), 250, 255, cv2.THRESH_BINARY)
                    bright_spots_image = detect_bright_spots(image_data)

                    # Median Filter
                    kernel = np.ones((1, 1), np.uint8)
                    median_filtered_image = cv2.morphologyEx(bright_spots_image, cv2.MORPH_ERODE, kernel)

                    # Calculate average pixel values for each column, fine line
                    avg_pixel_image = np.zeros_like(median_filtered_image)

                    # Initial setting
                    pixelDistance = 37.53333333/374 # 0.01833577593mm # sensor width(or height):37.533333mm / pixel No:2047 # mm
                    theta =  math.radians(90 - 19.5) # radian

                    for col in range(median_filtered_image.shape[1]):
                        # Get rows with bright pixels in the current column
                        bright_rows = np.where(median_filtered_image[:, col] > 0)[0]

                        if bright_rows.size > 0:
                            # Compute the average row position
                            avg_row = int(np.mean(bright_rows))
                            if 0 <= avg_row < median_filtered_image.shape[0]:
                                avg_pixel_image[avg_row, col] = 255  # Mark each average point
                                Height = (275.0 - avg_row)*pixelDistance*np.tan(theta) # calculate height value
                                pixelNo_of_Height = round(Height/pixelDistance) # Convert height value into pixel scale(integer)
                                Height = round(Height, 1) # Set 0.1mm precision
                                print("Height:", Height) # Check each height value in real time
                                
                        else:
                            # Skip columns with no bright pixels
                            continue                    

                    # Update the displayed image
                    img_display0.set_data(image_data) # Display source image
                    img_display0.set_clim(vmin=0, vmax=255)  # Update intensity scale


                    img_display4.set_data(avg_pixel_image) # Display fine line image to set with initial line
                    img_display4.set_clim(vmin=0, vmax=255)  # Update intensity scale


                    plt.draw()
                    plt.pause(0.001)

                    # Break the loop if 'q' is pressed
                    if keyboard.is_pressed('q'):
                        print('Program is closing...')
                        continue_recording = False

                # Release image
                image_result.Release()

            except PySpin.SpinnakerException as ex:
                print('Error: %s' % ex)
                break

        # End acquisition
        cam.EndAcquisition()

    except PySpin.SpinnakerException as ex:
        print('Error: %s' % ex)
        return False

    finally:
        # Close the display window
        plt.ioff()
        plt.close()

    return True


def run_single_camera(cam):
    """
    This function acts as the body of the example; please see NodeMapInfo example
    for more in-depth comments on setting up cameras.

    :param cam: Camera to run on.
    :type cam: CameraPtr
    :return: True if successful, False otherwise.
    :rtype: bool
    """
    try:
        result = True

        nodemap_tldevice = cam.GetTLDeviceNodeMap()

        # Initialize camera
        cam.Init()

        # Set desired FPS (e.g., 30 FPS)
        desired_fps = 67
        set_camera_fps(cam, desired_fps)

        # Retrieve GenICam nodemap
        nodemap = cam.GetNodeMap()

        # Acquire images
        result &= acquire_and_display_images(cam, nodemap, nodemap_tldevice)

        # Deinitialize camera
        cam.DeInit()

    except PySpin.SpinnakerException as ex:
        print('Error: %s' % ex)
        result = False

    return result

def main():
    """
    Example entry point; notice the volume of data that the logging event handler
    prints out on debug despite the fact that very little really happens in this
    example. Because of this, it may be better to have the logger set to lower
    level in order to provide a more concise, focused log.

    :return: True if successful, False otherwise.
    :rtype: bool
    """
    result = True

    # Retrieve singleton reference to system object
    system = PySpin.System.GetInstance()

    # Get current library version
    version = system.GetLibraryVersion()
    print('Library version: %d.%d.%d.%d' % (version.major, version.minor, version.type, version.build))

    # Retrieve list of cameras from the system
    cam_list = system.GetCameras()

    num_cameras = cam_list.GetSize()

    print('Number of cameras detected: %d' % num_cameras)

    # Finish if there are no cameras
    if num_cameras == 0:

        # Clear camera list before releasing system
        cam_list.Clear()

        # Release system instance
        system.ReleaseInstance()

        print('Not enough cameras!')
        input('Done! Press Enter to exit...')
        return False

    # Run example on each camera
    for i, cam in enumerate(cam_list):

        print('Running example for camera %d...' % i)

        result &= run_single_camera(cam)
        print('Camera %d example complete... \n' % i)

    # Release reference to camera
    del cam

    # Clear camera list before releasing system
    cam_list.Clear()

    # Release system instance
    system.ReleaseInstance()

    input('Done! Press Enter to exit...')
    return result

if __name__ == '__main__':
    if main():
        sys.exit(0)