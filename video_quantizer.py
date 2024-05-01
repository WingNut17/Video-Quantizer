import sys
from PIL import Image
from moviepy.editor import VideoFileClip, ImageSequenceClip
import os

def extract_and_quantize_frames(input_file, output_folder):
    print("Quantizing frames...")

    # Make tiny palette Image, one black pixel
    paletteImage = Image.new('P', (1, 1))

    # Make B&W palette containing only 1 pure white and 255 pure black entries
    palette = [255, 255, 255] + [0, 0, 0] * 255

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Push in B&W palette and save for debug purposes
    paletteImage.putpalette(palette)
    paletteImage.save(os.path.join(output_folder, "palette.png"))

    # Load the video
    clip = VideoFileClip(input_file)

    # Iterate over each frame in the video
    for i, frame in enumerate(clip.iter_frames(fps=clip.fps)):
        # Convert the NumPy array to a PIL Image
        pil_frame = Image.fromarray(frame)

        # Quantize the frame to the specified palette
        quantized_frame = pil_frame.quantize(palette=paletteImage, method=3)

        # Save the quantized frames as PNG's image
        frame_path = os.path.join(output_folder, f"frame_{i:04d}.png")
        quantized_frame.save(frame_path)

    print("Frames Quantized.")

    # Close the video
    clip.close()

    images_to_mp4(output_folder, f"{output_folder}\output_1.mp4")

def images_to_mp4(input_folder, output_file):
    # Get the list of image files in the input folder
    image_files = [file for file in os.listdir(input_folder) if file.endswith((".png", ".jpg", ".jpeg")) and file.startswith(("frame_"))]
    image_files.sort()  # Sort the files to maintain order

    frames = []

    # Load each image file and append it to the frames list
    for image_file in image_files:
        image_path = os.path.join(input_folder, image_file)
        frames.append(image_path)

    # Create a video from the frames
    video_clip = ImageSequenceClip(frames, fps=30)
    video_clip.write_videofile(output_file, codec="libx264", fps=30)

    # Deletes the frames, keeps the video and palette
    for image_file in image_files:
        os.remove(os.path.join(input_folder, image_file))

    print("Converted back to mp4.")

if __name__ == "__main__":
    if len(sys.argv) == 3:
        input_file = sys.argv[1]
        output_folder = sys.argv[2]
        try:
            extract_and_quantize_frames(input_file, output_folder)
        except FileNotFoundError:
            print("Error: Input file not found.")
        except Exception as e:
            print(f"Error: {e}")
            print("Usage: python video_quantizer.py input_file output_folder")
            print("(ex: \"C:\\Users\\Shawn\\Videos\\00018549.mp4\" \"C:\\Users\\Shawn\\Videos\\\")")
            
    else:
        print("Usage: python video_quantizer.py input_file output_folder")
        print("(ex: \"C:\\Users\\Shawn\\Videos\\00018549.mp4\" \"C:\\Users\\Shawn\\Videos\\\")")
        input_file = input("Enter the file you'd like to quantize: ")
        output_folder = input("Enter the folder you'd like to output to: ")
        extract_and_quantize_frames(input_file, output_folder)