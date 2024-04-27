from PIL import Image
from moviepy.editor import VideoFileClip, ImageSequenceClip
import os

def main():
    input_file = "E:\\Art\\Editing\\EDITS\\Mar24\\data_bending\\input1.mp4" #input("Please enter the folder path and file: (ex: \"C:\\Users\\Shawn\\Videos\\00018549.mp4\")\n ")
    output_folder = "E:\\Art\Editing\\EDITS\\Apr24\\stop_motion" #input("Please enter the desired output folder: (ex: \"C:\\Users\\Shawn\\Videos\\\")\n")

    extract_and_quantize_frames(input_file, output_folder)

def extract_and_quantize_frames(input_file, output_folder):
    
    print("Quantizing frames...")
    
    # Make tiny palette Image, one black pixel
    palIm = Image.new('P', (1,1))

    # Make your desired B&W palette containing only 1 pure white and 255 pure black entries
    palette = [255, 255, 255 ] + [0, 0 ,0] * 255 

    # Push in our lovely B&W palette and save just for debug purposes
    palIm.putpalette(palette)
    palIm.save(f"{output_folder}\\palette.png")

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Load the video clip
    clip = VideoFileClip(input_file)
    
    # Iterate over each frame in the video clip
    for i, frame in enumerate(clip.iter_frames(fps=clip.fps)):
        # Convert the NumPy array to a PIL Image
        pil_frame = Image.fromarray(frame)

        # Quantize the frame to the specified palette
        quantized_frame = pil_frame.quantize(palette=palIm, method=0)
        
        # Save the quantized frame as a PNG image
        frame_path = os.path.join(output_folder, f"frame_{i:04d}.png")
        quantized_frame.save(frame_path)
    
    print("Frames Quantized.")
    
    # Close the video clip
    clip.close()

    images_to_mp4(output_folder, f"{output_folder}\\output.mp4", fps=30)

def images_to_mp4(input_folder, output_file, fps=30):
    # Get the list of image files in the input folder
    image_files = [file for file in os.listdir(input_folder) if file.endswith((".png", ".jpg", ".jpeg")) and file != "palette.png"]
    image_files.sort()  # Sort the files to maintain order
    
    # Initialize a list to hold the frames
    frames = []
    
    # Load each image file and append it to the frames list
    for image_file in image_files:
        image_path = os.path.join(input_folder, image_file)
        frames.append(image_path)

    
    # Create an ImageSequenceClip from the frames list
    video_clip = ImageSequenceClip(frames, fps=fps)
    
    # Write the video clip to an MP4 file
    video_clip.write_videofile(output_file, codec="libx264", fps=fps)

    for image_file in image_files:
        os.remove(os.path.join(input_folder, image_file))
    
    print("Converted back to mp4.")

if __name__ == "__main__":
    main()