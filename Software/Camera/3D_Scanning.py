import os
import PySpin
import numpy as np
import matplotlib.pyplot as plt
import math
import cv2
import time
import queue
import keyboard
import sys
from threading import Thread, Event
from matplotlib.animation import FuncAnimation
from matplotlib import cm  # For colormap usage
from matplotlib.colors import Normalize  # For normalizing z-axis values

# Initialize global variables
x_coordinates = []
frame_queue = queue.Queue()  # Create a queue.Queue object
stop_event = Event()

# Initialize global variables
ThreeD_data = np.empty((0, 375, 375), dtype=np.float16)  # Define data type as float16
pixel_distance = 37.53333333 / 375  # Real distance per pixel: 0.100088888 mm per pixel
theta = math.radians(90 - 19.5)  # Angle for height calculation
yaxis_zaxis_image = np.zeros((375, 375), dtype=np.float16)
conveyorbelt_speed = 30 / 4  # Conveyor belt speed in mm/s

scatter_plot_buffers = []  # List to store all chunks
current_buffer = []  # Current chunk buffer
MAX_POINTS_PER_BUFFER = 10000  # Maximum points per chunk

# Global variables for visualization
fig = None
ax = None
sustain_flag = 0
restart = 0
frame_count = 0

def update_plot(frame):
    """
    Update the 3D plot with current and past buffers.
    """
    global ax, sustain_flag, update_count, current_buffer, restart, stop_event, frame_count, drawing

    if restart == 1:
        user_input = input("Press 'Enter' key to restart")
        if user_input == "":  # 'Enter': restart
            restart = 0
            drawing = 0
            sustain_flag = 0
            update_count = 0
            current_buffer = []

    ax.cla()

    # Configure colormap and normalization
    colormap = cm.viridis  # Choose colormap ('viridis', 'plasma', etc.)
    norm = Normalize(vmin=0, vmax=375)  # Normalize z-axis range (0~375)

    for x, y, z in current_buffer:
        # Separate points where z != 0
        valid_indices = z > 20
        valid_z = z  # Use entire z array
        valid_x = np.full(valid_z.shape, x)
        valid_y = np.full(valid_z.shape, y)

        # Determine colors based on height (z-axis)
        colors = colormap(norm(valid_z))  # Compute colors for entire z array
        alphas = np.where(valid_indices, 1.0, 0)  # Set transparency based on z values
        rgba_colors = np.zeros((valid_z.size, 4))  # Create RGBA color array
        rgba_colors[:, :3] = colors[:, :3]  # Copy R, G, B values
        rgba_colors[:, 3] = alphas  # Apply alpha values

        # Scatter plot
        ax.scatter(valid_x, valid_y, valid_z, c=rgba_colors, marker='.', s=1)

    # Get axis ranges
    x_min, x_max = ax.get_xlim()
    y_min, y_max = ax.get_ylim()
    z_min, z_max = ax.get_zlim()

    # Adjust aspect ratios
    x_range = abs(x_max - x_min)
    y_range = abs(y_max - y_min)
    z_range = abs(z_max - z_min)
    max_range = max(x_range, y_range, z_range)
    ax.set_box_aspect([x_range / max_range, y_range / max_range, z_range / max_range])

    # Configure tick labels based on data ranges
    x_ticks = np.linspace(x_min, x_max, 5)
    y_ticks = np.linspace(y_min, y_max, 5)
    z_ticks = np.linspace(z_min, z_max, 5)

    ax.set_xticks(x_ticks)
    ax.set_yticks(y_ticks)
    ax.set_zticks(z_ticks)

    ax.set_xticklabels([f"{tick:.1f}" for tick in x_ticks])
    ax.set_yticklabels([f"{tick:.1f}" for tick in y_ticks])
    ax.set_zticklabels([f"{tick:.1f}" for tick in z_ticks])

    plt.title("Real-Time 3D Visualization")
    frame_count += 1

def add_3D_frame(yaxis_zaxis_image, current_x):
    """
    Add a new y-z plane data to 3D data along the x-axis.
    """
    global ThreeD_data, x_coordinates

    # Apply minimal data type (float16)
    yaxis_zaxis_image = yaxis_zaxis_image.astype(np.float16)
    yaxis_zaxis_image[yaxis_zaxis_image <= 50] = 0  # Set values below threshold to 0

    if len(ThreeD_data) == 0:
        # Initialize ThreeD_data
        ThreeD_data = yaxis_zaxis_image[np.newaxis, ...]
        x_coordinates = [current_x]

    ThreeD_data = np.concatenate([ThreeD_data, yaxis_zaxis_image[np.newaxis, ...]], axis=0)
    x_coordinates.append(current_x)

def set_camera_fps(cam, desired_fps=None):
    """
    Set the FPS (Frames Per Second) for the camera.
    """
    try:
        nodemap = cam.GetNodeMap()
        node_acquisition_frame_rate_enable = PySpin.CBooleanPtr(nodemap.GetNode("AcquisitionFrameRateEnable"))
        if PySpin.IsAvailable(node_acquisition_frame_rate_enable) and PySpin.IsWritable(node_acquisition_frame_rate_enable):
            node_acquisition_frame_rate_enable.SetValue(True)
            print("Acquisition Frame Rate Enabled")

        node_acquisition_frame_rate = PySpin.CFloatPtr(nodemap.GetNode("AcquisitionFrameRate"))
        if PySpin.IsAvailable(node_acquisition_frame_rate) and PySpin.IsWritable(node_acquisition_frame_rate):
            max_fps = node_acquisition_frame_rate.GetMax()
            if desired_fps is None or desired_fps > max_fps:
                print(f"Requested FPS ({desired_fps}) exceeds max FPS ({max_fps}). Setting to max FPS.")
                desired_fps = max_fps
            node_acquisition_frame_rate.SetValue(desired_fps)
            print(f"Acquisition Frame Rate set to: {desired_fps} FPS")
    except PySpin.SpinnakerException as ex:
        print(f"Error setting FPS: {ex}")

def capture_images(cam, fps):
    """
    Capture images and put them into the queue.
    """
    try:
        nodemap = cam.GetNodeMap()
        node_acquisition_mode = PySpin.CEnumerationPtr(nodemap.GetNode('AcquisitionMode'))
        node_acquisition_mode_continuous = node_acquisition_mode.GetEntryByName('Continuous')
        node_acquisition_mode.SetIntValue(node_acquisition_mode_continuous.GetValue())

        cam.BeginAcquisition()
        print('Capturing images...')

        frame_time = 1 / fps
        while not stop_event.is_set():
            start_time = time.time()
            image_result = cam.GetNextImage(1000)

            if image_result.IsIncomplete():
                print(f"Image incomplete with status {image_result.GetImageStatus()}")
                continue

            frame_queue.put(image_result.GetNDArray())
            image_result.Release()

            elapsed_time = time.time() - start_time
            if elapsed_time < frame_time:
                time.sleep(frame_time - elapsed_time)

        cam.EndAcquisition()
    except PySpin.SpinnakerException as ex:
        print(f"Error during image capture: {ex}")

scatter_plot_data = []  # List to store data for plotting

def process_images(fps):
    """
    Process images from the queue and update the buffers for real-time visualization.
    """
    global scatter_plot_buffers, current_buffer, sustain_flag, update_count, restart

    current_x = 0
    update_count = 0
    drawing = 0
    restart = 0
    non_zero_count = 0
    while not stop_event.is_set() or not frame_queue.empty():
        try:
            # Get image from the queue
            image_data = frame_queue.get(timeout=1)
            image_data = cv2.resize(image_data, (375, 375), interpolation=cv2.INTER_AREA)

            # Image processing: Detect bright spots
            _, binary_image = cv2.threshold(image_data.astype(np.uint8), 250, 255, cv2.THRESH_BINARY)

            # Calculate height values and create y-z image
            yaxis_zaxis_image = np.zeros((375, 375), dtype=np.float16)
            zero_count = 0 # counting the case of capturing only ground
            for col in range(binary_image.shape[1]):
                bright_rows = np.where(binary_image[:, col] > 0)[0]
                if bright_rows.size > 0:
                    avg_row = int(np.mean(bright_rows)) # fine line
                    height = (275.0 - avg_row) * pixel_distance * np.tan(theta) # calculate height
                    pixel_no_of_height = round(height / pixel_distance) # convert height value into pixel scale
                    pixel_no_of_height = np.clip(pixel_no_of_height, 0, 374) # fit the size of height to prevent 'out of range' problem
                    if pixel_no_of_height < 5: zero_count += 1 # count the number of ground capturing
                    yaxis_zaxis_image[col, pixel_no_of_height] = 255 # build up 2D image

            # When scanning only ground after scanning the end of object
            if zero_count > 270:
                if drawing == 1:
                    restart = 1
                    drawing = 0 # signal for stopping adding 2D image
            else: # When scanning object
                y, z = np.where(yaxis_zaxis_image > 0) 
                current_buffer.append((np.full_like(y, current_x), y, z)) # add up 2D image to the x axis
                drawing = 1 # signal for keeping adding 2D image

            current_x += 1 # 7.5mm/s of conveyor belt when fps is 75, uinit distance between eac 2D image is 0.1mm

        except queue.Empty:
            continue

def run_camera_with_threads(cam, fps):
    """
    Run the camera and manage threads for capturing and processing images.
    """
    try:
        cam.Init()
        set_camera_fps(cam, fps) # set fps value of camera capture

        # Start threads for image capture and processing
        capture_thread = Thread(target=capture_images, args=(cam, fps)) # deal with image capture at the seperate parallel thread
        process_thread = Thread(target=process_images, args=(fps,)) # deal with image processing at the seperate parallel thread

        capture_thread.start()
        process_thread.start()

        # Finalize threads
        capture_thread.join()
        process_thread.join()

        cam.DeInit()

        # Keep the final 3D plot displayed
        plt.ioff()
        plt.show(block=True)

    except PySpin.SpinnakerException as ex:
        print(f"Error: {ex}")

def main():
    """
    Main function to execute the program.
    """
    global fig, ax, sustain_flag, stop_event
    system = PySpin.System.GetInstance()
    cam_list = system.GetCameras()
    num_cameras = cam_list.GetSize()

    if num_cameras == 0:
        print('No cameras detected.')
        cam_list.Clear()
        system.ReleaseInstance()
        return

    # set fps value before starting this system[set 75 for almost 0.1mm unit distance between each 2D image]
    user_fps = input("Enter desired FPS (leave blank for maximum FPS): ")
    fps = float(user_fps) if user_fps.strip() else None

    try:
        for cam in cam_list:
            try:
                cam.Init()
                set_camera_fps(cam, fps)

                capture_thread = Thread(target=capture_images, args=(cam, fps))
                process_thread = Thread(target=process_images, args=(fps,))
                
                capture_thread.start()
                process_thread.start()

                fig = plt.figure(figsize=(10, 7))
                ax = fig.add_subplot(111, projection='3d')

                interval_current = 1000 / fps
                ani = FuncAnimation(fig, update_plot, interval=interval_current, cache_frame_data=False)

                plt.show(block=True)

                stop_event.set()
                capture_thread.join()
                process_thread.join()

            finally:
                cam.DeInit()
                del cam

    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
        stop_event.set()

    finally:
        try:
            stop_event.set()
            if 'capture_thread' in locals() and capture_thread.is_alive():
                capture_thread.join()
            if 'process_thread' in locals() and process_thread.is_alive():
                process_thread.join()

            for cam in cam_list:
                try:
                    cam.DeInit()
                    del cam
                except Exception as e:
                    print(f"Error while releasing camera: {e}")

        except Exception as e:
            print(f"Error during cleanup: {e}")

        finally:
            try:
                cam_list.Clear()
                system.ReleaseInstance()
                print('Done.')
            except Exception as e:
                print(f"Error releasing system instance: {e}")

if __name__ == '__main__':
    main()