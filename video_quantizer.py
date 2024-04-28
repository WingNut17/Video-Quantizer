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

    # Push in B&W palette and save for debug purposes
    paletteImage.putpalette(palette)
    paletteImage.save(os.path.join(output_folder, "palette.png"))

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Load the video
    clip = VideoFileClip(input_file)

    # Iterate over each frame in the video
    for i, frame in enumerate(clip.iter_frames(fps=clip.fps)):
        # Convert the NumPy array to a PIL Image
        pil_frame = Image.fromarray(frame)

        # Quantize the frame to the specified palette
        quantized_frame = pil_frame.quantize(palette=paletteImage, method=0)

        # Save the quantized frames as PNG's image
        frame_path = os.path.join(output_folder, f"frame_{i:04d}.png")
        quantized_frame.save(frame_path)

    print("Frames Quantized.")

    # Close the video
    clip.close()

    images_to_mp4(output_folder, os.path.join(output_folder, "output.mp4"), fps=30)

def images_to_mp4(input_folder, output_file, fps=30):
    # Get the list of image files in the input folder
    image_files = [file for file in os.listdir(input_folder) if file.endswith((".png", ".jpg", ".jpeg")) and file != "palette.png"]
    image_files.sort()  # Sort the files to maintain order

    frames = []

    # Load each image file and append it to the frames list
    for image_file in image_files:
        image_path = os.path.join(input_folder, image_file)
        frames.append(image_path)

    # Create a video from the frames
    video_clip = ImageSequenceClip(frames, fps=fps)
    video_clip.write_videofile(output_file, codec="libx264", fps=fps)

    # Deletes the frames, keeps the video and palette
    for image_file in image_files:
        os.remove(os.path.join(input_folder, image_file))

    print("Converted back to mp4.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script_name.py input_file output_folder")
    else:
        input_file = sys.argv[1]
        output_folder = sys.argv[2]
        extract_and_quantize_frames(input_file, output_folder)