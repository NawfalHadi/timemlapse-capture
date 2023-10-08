import tkinter as tk
import cv2
import os
import datetime

from tkinter import filedialog
from PIL import Image, ImageTk


class CameraApp:
    def __init__(self):
        self.dir = "/path/to/directory"
        self.cap = cv2.VideoCapture(0)

        self.root = tk.Tk()
        self.root.title("Aplikasi Kamera")

        # Create a frame for the menu layout (left)
        self.menu_frame = tk.Frame(self.root)
        self.menu_frame.pack(side=tk.LEFT, padx=10, pady=10)

        # ===== CAMERA ========

        # Create a frame for the camera view (right)
        self.camera_frame = tk.Frame(self.root)
        self.camera_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        # Create labels and buttons
        self.camera_label = tk.Label(self.camera_frame)
        self.camera_label.pack()

        # Create a button for capturing an image
        self.capture_button = tk.Button(
            self.camera_frame, text="Capture", command=self.capture_image)
        self.capture_button.pack()

        # Initialize a variable to store captured images
        self.captured_images = []

        self.open_change_frame = tk.Frame(self.menu_frame)
        self.open_change_frame.pack(side=tk.TOP)

        self.open_button = tk.Button(
            self.open_change_frame, text="Open Directory", command=self.open_directory)
        self.open_button.pack(side=tk.LEFT, padx=5)

        self.change_dir_button = tk.Button(
            self.open_change_frame, text="Change Directory", command=self.change_directory)
        self.change_dir_button.pack(side=tk.LEFT, padx=5)

        self.directory_label = tk.Label(
            self.menu_frame, text=f"Directory: {self.dir}")
        self.directory_label.pack()

        self.upload_button = tk.Button(
            self.menu_frame, text="Upload to Google Drive", command=self.upload_to_gdrive)
        self.upload_button.pack()

        self.timer_button = tk.Button(
            self.menu_frame, text="Set Timer", command=self.set_timer)
        self.timer_button.pack()

        self.show_directory()
        self.update_camera_frame()

    '''
    DIRECTORY FUNCTION
    '''

    def create_settings(self):
        default_settings = {
            'dir': 'path',
            'last_capt': '21 Desember 2002',
            'frame': 'path'
        }

        with open('setting.log', 'w') as settings_file:
            for key, value in default_settings.items():
                settings_file.write(f'{key}= {value}\n')

    def show_directory(self):
        try:
            settings = {}
            with open('setting.log', 'r') as log:
                lines = log.readlines()

            for line in lines:
                key, value = line.strip().split('=')
                settings[key.strip()] = value.strip()

            print(settings)
            self.dir = settings.get('dir')
            self.directory_label.config(text=self.dir)

        except FileNotFoundError:
            self.create_settings()
        except Exception as e:
            print(f"An error occurred: {e}")

    def open_directory(self):
        print(self.dir)
        try:
            os.startfile(self.dir)
        except OSError as e:
            print(f"Error opening folder: {e}")

    def change_directory(self):
        try:
            temp_dir = ""
            new_directory = filedialog.askdirectory()  # Open a directory dialog
            if new_directory:
                temp_dir = new_directory
                self.dir = temp_dir
                self.directory_label.config(text=f"Directory: {self.dir}")

                # Update the 'dir' setting in the setting.log file
                self.update_setting('dir', temp_dir)

        except Exception as e:
            print(f"An error occurred: {e}")

    def update_setting(self, setting_key, setting_value):
        try:
            key = ""
            updated_lines = []  # To store updated lines

            with open('setting.log', 'r') as log:
                lines = log.readlines()

            for line in lines:
                key_value_pair = line.strip().split('=')
                key_in_file = key_value_pair[0].strip()
                value_in_file = key_value_pair[1].strip()

                if key_in_file == setting_key:
                    # Update the key with the new value
                    updated_line = f"{setting_key}= {setting_value}\n"
                    updated_lines.append(updated_line)
                    key = setting_key
                else:
                    # Keep the original line
                    updated_lines.append(line)

            if key:
                # Write the updated content back to the file
                with open('setting.log', 'w') as log:
                    log.writelines(updated_lines)

            print(key)

        except Exception as e:
            print(f"An error occurred while updating the setting: {e}")

    '''
    UPLOAD
    '''

    def upload_to_gdrive(self):
        # Implementasi logika untuk mengunggah gambar ke Google Drive
        pass

    '''
    CAMERA FEATURE
    '''

    def capture_image(self):
        try:
            ret, frame = self.cap.read()
            if ret:
                # Crop the camera frame to make it square
                height, width, _ = frame.shape
                min_dim = min(height, width)

                if height > width:
                    y_start = (height - min_dim) // 2
                    x_start = 0
                else:
                    y_start = 0
                    x_start = (width - min_dim) // 2

                # Crop the image to maintain a 1:1 aspect ratio
                frame = frame[y_start:y_start + min_dim,
                              x_start:x_start + min_dim]

                frame = cv2.flip(frame, 1)

                # Capture the image and save it
                timestamp = datetime.datetime.now().strftime("%Y%m%d")
                image_filename = f"{timestamp}.png"
                image_path = os.path.join(self.dir, image_filename)
                cv2.imwrite(image_path, frame)
                self.captured_images.append(image_path)

                self.update_setting("frame", image_path)

        except Exception as e:
            print(f'error : {e}')

    def set_timer(self):
        # Implementasi logika untuk mengatur timer foto
        pass

    def update_camera_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Get frame dimensions
            height, width, channels = frame.shape

            # Determine the width to be used for the camera display
            display_width = min(height, width)

            if height > width:
                y_start = (height - display_width) // 2
                x_start = 0
            else:
                y_start = 0
                x_start = (width - display_width) // 2

            # Crop the image to maintain a 1:1 aspect ratio
            frame = frame[y_start:y_start + display_width,
                          x_start:x_start + display_width]

            frame = cv2.flip(frame, 1)

            # Load and resize the guideline image to match the camera frame size
            guideline_image = cv2.imread("image.png")
            guideline_image = cv2.resize(
                guideline_image, (display_width, display_width))

            # Blend the camera frame and guideline image with transparency
            alpha = 0.2  # Adjust the alpha value for transparency
            blended_frame = cv2.addWeighted(
                frame, 1 - alpha, guideline_image, alpha, 0)

        photo = ImageTk.PhotoImage(image=Image.fromarray(blended_frame))
        self.camera_label.config(image=photo)
        self.camera_label.photo = photo
        self.camera_label.after(10, self.update_camera_frame)

    def run(self):
        self.root.mainloop()
        self.cap.release()


# Create an instance of the CameraApp class and run the application
app = CameraApp()
app.run()
