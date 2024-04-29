import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import video_quantizer
import cv2

def process_video():
    input_file = input_entry.get()
    export_folder = export_entry.get()

    if not input_file or not export_folder:
        result_label.config(text="please provide both input file and export folder paths.")
        return

    try:
        video_quantizer.extract_and_quantize_frames(input_file, export_folder)
        result_label.config(text="video processing completed successfully")

        open_video_file(export_folder)

    except Exception as e:
        result_label.config(text=f"error: {str(e)}")

def open_video_file(folder_path):
    video_file_path = f"{folder_path}\output.mp4"

    # Creating video player window
    video_window = tk.Toplevel(window)
    video_window.title("video player")
    video_window.iconbitmap("E:\Coding\Python\Video Glitcher\Video-Quantizer\icon.ico")

    # Open the video file with OpenCV
    cap = cv2.VideoCapture(video_file_path)
    if not cap.isOpened():
        raise FileNotFoundError(f"error opening video file: {video_file_path}")

    # Function to update the video frame
    def update_frame():
        ret, frame = cap.read()
        if ret:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            pil_img = Image.fromarray(rgb_frame)

            img = ImageTk.PhotoImage(image=pil_img)

            video_label.config(image=img)
            video_label.image = img

            video_label.after(30, update_frame)
        else:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Loop
            update_frame()

    # Create a label for displaying the video frame
    video_label = tk.Label(video_window)
    video_label.pack()

    update_frame()

def browse_input_file():
    file_path = filedialog.askopenfilename()
    input_entry.delete(0, tk.END)
    input_entry.insert(0, file_path)

def browse_export_folder():
    folder_path = filedialog.askdirectory()
    export_entry.delete(0, tk.END)
    export_entry.insert(0, folder_path)

def show_instructions():
    messagebox.showinfo("Instructions", "1. Select an input file and export folder.\n2. Click 'Quantize Video' to process.\n3. Watch the processed video in the player.\n(It is normal for the window to stop responding while quantizing the video. Quantizing large video files will likely crash the program. However, the effect looks best with low quality videos anyways)")

# Create the main window
window = tk.Tk()
window.title("quantizer")
window.configure(bg="white")

# Window icon
window.iconbitmap("E:\Coding\Python\Video Glitcher\Video-Quantizer\icon.ico")

# Logo
logo = tk.PhotoImage(file="E:\Coding\Python\Video Glitcher\Video-Quantizer\logo.png")
logo_label = tk.Label(window, image=logo, bg="white")
logo_label.pack()

# Input file selection
input_frame = tk.Frame(window, bg="white")
input_frame.pack(pady=10)
input_label = tk.Label(input_frame, text="input file:", bg="white")
input_label.pack(side=tk.LEFT)
input_entry = tk.Entry(input_frame, width=40)
input_entry.pack(side=tk.LEFT)
browse_input_button = tk.Button(input_frame, text="Browse", command=browse_input_file)
browse_input_button.pack(side=tk.LEFT)

# Export folder selection
export_frame = tk.Frame(window, bg="white")
export_frame.pack(pady=10)
export_label = tk.Label(export_frame, text="export folder:", bg="white")
export_label.pack(side=tk.LEFT)
export_entry = tk.Entry(export_frame, width=40)
export_entry.pack(side=tk.LEFT)
browse_export_button = tk.Button(export_frame, text="Browse", command=browse_export_folder)
browse_export_button.pack(side=tk.LEFT)

# Process button
process_button = tk.Button(window, text="Quantize Video", command=process_video)
process_button.pack(pady=20)

# Instructions button
instructions_button = tk.Button(window, text=" ? ", command=show_instructions)
instructions_button.pack(padx=10, pady=10)

# Result label
result_label = tk.Label(window, fg="black", bg="white")
result_label.pack(side=tk.BOTTOM)

window.mainloop()