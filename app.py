import tkinter as tk
import cv2

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

        # Create a frame for the camera view (right)
        self.camera_frame = tk.Frame(self.root)
        self.camera_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        # Create labels and buttons
        self.camera_label = tk.Label(self.camera_frame)
        self.camera_label.pack()

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

    def create_settings(self):
        default_settings = {
            'dir': 'path',
            'last_capt': '21 Desember 2002',
            'frame': 'path'
        }

        with open('setting.log', 'w') as settings_file:
            for key, value in default_settings.items():
                settings_file.write(f'{key}: {value}\n')

    def show_directory(self):
        try:
            settings = {}
            with open('setting.log', 'r') as log:
                lines = log.readlines()

            for line in lines:
                key, value = line.strip().split(':')
                settings[key.strip()] = value.strip()

            print(settings)

            self.directory_label.config(text=settings.get('dir'))

        except FileNotFoundError:
            self.create_settings()
        except Exception as e:
            print(f"An error occurred: {e}")

    def open_directory(self):
        # Implementasi logika untuk membuka direktori
        pass

    def change_directory(self):
        global dir  # Declare dir as a global variable
        try:
            new_directory = filedialog.askdirectory()  # Open a directory dialog
            if new_directory:
                dir = new_directory
                self.directory_label.config(text=f"Directory: {dir}")

                # Update the 'dir' setting in the setting.log file
                # self.update_setting('dir', dir)

        except Exception as e:
            print(f"An error occurred: {e}")

    def upload_to_gdrive(self):
        # Implementasi logika untuk mengunggah gambar ke Google Drive
        pass

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

            # Crop the image to maintain a 1:1 aspect ratio
            frame = frame[0:display_width, 0:display_width]

            photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.camera_label.config(image=photo)
            self.camera_label.photo = photo
        self.camera_label.after(10, self.update_camera_frame)

    def run(self):
        self.root.mainloop()
        self.cap.release()


# Create an instance of the CameraApp class and run the application
app = CameraApp()
app.run()
