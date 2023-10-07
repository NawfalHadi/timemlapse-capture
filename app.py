import tkinter as tk
import cv2
from PIL import Image, ImageTk


def open_directory():
    # Implementasi logika untuk membuka direktori
    pass


def change_directory():
    # Implementasi logika untuk mengganti direktori penyimpanan gambar
    pass


def upload_to_gdrive():
    # Implementasi logika untuk mengunggah gambar ke Google Drive
    pass


def set_timer():
    # Implementasi logika untuk mengatur timer foto
    pass


def update_camera_frame():
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
        camera_label.config(image=photo)
        camera_label.photo = photo
    camera_label.after(10, update_camera_frame)


# Inisialisasi kamera
cap = cv2.VideoCapture(0)

# Membuat jendela utama
root = tk.Tk()
root.title("Aplikasi Kamera")

# Membuat frame untuk layout menu (kiri)
menu_frame = tk.Frame(root)
menu_frame.pack(side=tk.LEFT, padx=10, pady=10)

# Frame untuk tombol "Open Directory" dan "Change Directory"
open_change_frame = tk.Frame(menu_frame)
open_change_frame.pack(side=tk.TOP)

# Tombol untuk membuka direktori dan mengganti direktori penyimpanan gambar
open_button = tk.Button(
    open_change_frame, text="Open Directory", command=open_directory)
open_button.pack(side=tk.LEFT, padx=5)

change_dir_button = tk.Button(
    open_change_frame, text="Change Directory", command=change_directory)
change_dir_button.pack(side=tk.LEFT, padx=5)

# Label untuk menampilkan nama direktori
directory_label = tk.Label(menu_frame, text="Directory: /path/to/directory")
directory_label.pack()

# Tombol untuk mengunggah gambar ke Google Drive
upload_button = tk.Button(
    menu_frame, text="Upload to Google Drive", command=upload_to_gdrive)
upload_button.pack()

# Tombol untuk mengatur timer foto
timer_button = tk.Button(menu_frame, text="Set Timer", command=set_timer)
timer_button.pack()

# Membuat frame untuk tampilan kamera (kanan)
camera_frame = tk.Frame(root)
camera_frame.pack(side=tk.RIGHT, padx=10, pady=10)

# Menampilkan kamera di tengah frame
camera_label = tk.Label(camera_frame)
camera_label.pack()
update_camera_frame()

root.mainloop()

# Setelah selesai, pastikan untuk melepaskan kamera
cap.release()
